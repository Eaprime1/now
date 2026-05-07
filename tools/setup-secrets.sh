#!/usr/bin/env bash
# Setup script — add API keys as GitHub repository secrets
# Run this on the laptop from /home/sauron/
#
# Usage:
#   chmod +x setup-secrets.sh
#   ./setup-secrets.sh
#
# Reads clavis.txt for keys. clavis.txt format:
#   GEMINI_API_KEY=AIza...
#   PERPLEXITY_API_KEY=pplx-...
#   (one KEY=value per line, # lines are comments)

set -euo pipefail

REPO_OWNER="Eaprime1"
REPO_NAME="now"
CLAVIS="${HOME}/clavis.txt"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

log()  { echo -e "${CYAN}[setup]${RESET} $*"; }
ok()   { echo -e "${GREEN}  ✓${RESET} $*"; }
warn() { echo -e "${YELLOW}  ⚠${RESET} $*"; }
err()  { echo -e "${RED}  ✗${RESET} $*"; }

# ── check prereqs ─────────────────────────────────────────────────────────────
if [[ ! -f "$CLAVIS" ]]; then
    err "clavis.txt not found at $CLAVIS"
    echo "  Create it with one KEY=value per line:"
    echo "  GEMINI_API_KEY=AIza..."
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    err "python3 required"; exit 1
fi

# ── GitHub token ──────────────────────────────────────────────────────────────
if [[ -z "$GITHUB_TOKEN" ]]; then
    echo -e "${BOLD}GitHub Personal Access Token needed${RESET}"
    echo "  (needs repo + secrets:write scope)"
    echo "  Create at: https://github.com/settings/tokens"
    read -r -s -p "  Paste token: " GITHUB_TOKEN
    echo
fi

# ── read clavis.txt ───────────────────────────────────────────────────────────
declare -A KEYS
while IFS='=' read -r key val; do
    [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
    key=$(echo "$key" | tr -d ' ')
    val=$(echo "$val" | tr -d ' ')
    [[ -n "$key" && -n "$val" ]] && KEYS["$key"]="$val"
done < "$CLAVIS"

if [[ ${#KEYS[@]} -eq 0 ]]; then
    err "No keys found in $CLAVIS"; exit 1
fi

log "Found ${#KEYS[@]} key(s) in clavis.txt: ${!KEYS[*]}"

# ── add secrets via GitHub API using python3 ──────────────────────────────────
python3 <<PYEOF
import json, base64, urllib.request, urllib.error, sys
from urllib.request import Request

token = "$GITHUB_TOKEN"
owner = "$REPO_OWNER"
repo  = "$REPO_NAME"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json",
}

# Get repo public key for secret encryption
pub_key_url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key"
req = Request(pub_key_url, headers=headers)
try:
    with urllib.request.urlopen(req) as r:
        pub_key_data = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"  ✗ Failed to get public key: {e.code} {e.reason}")
    sys.exit(1)

key_id    = pub_key_data['key_id']
pub_key_b = pub_key_data['key']

# Encrypt using PyNaCl (libsodium) if available, otherwise fallback instruction
try:
    from nacl import encoding, public as nacl_public

    def encrypt_secret(public_key_b64: str, secret: str) -> str:
        pk = nacl_public.PublicKey(public_key_b64.encode(), encoding.Base64Encoder)
        box = nacl_public.SealedBox(pk)
        enc = box.encrypt(secret.encode())
        return base64.b64encode(enc).decode()

    keys = {$(for k in "${!KEYS[@]}"; do echo "    \"$k\": \"${KEYS[$k]}\","; done)}

    for secret_name, secret_value in keys.items():
        enc_val = encrypt_secret(pub_key_b, secret_value)
        url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/{secret_name}"
        payload = json.dumps({"encrypted_value": enc_val, "key_id": key_id}).encode()
        req = Request(url, payload, headers, method='PUT')
        try:
            with urllib.request.urlopen(req) as r:
                print(f"  \033[32m✓\033[0m {secret_name} → GitHub Secrets")
        except urllib.error.HTTPError as e:
            print(f"  \033[31m✗\033[0m {secret_name}: {e.code} {e.reason}")

except ImportError:
    print("\n  PyNaCl not installed. Install with: pip3 install PyNaCl")
    print("  Then re-run this script.")
    print("\n  OR add secrets manually at:")
    print(f"  https://github.com/{owner}/{repo}/settings/secrets/actions")
    print("\n  Keys to add:")
    keys = {$(for k in "${!KEYS[@]}"; do echo "    \"$k\": \"${KEYS[$k][:4]}...\","; done)}
    for k in keys:
        print(f"    {k}")
PYEOF

echo
log "Done. Verify at: https://github.com/${REPO_OWNER}/${REPO_NAME}/settings/secrets/actions"
