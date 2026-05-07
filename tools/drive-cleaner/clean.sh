#!/usr/bin/env bash
# Ubuntu Drive Cleaner
# Usage: ./clean.sh [--dry-run] [--all] [--mode safe|deep|report]
# Chain of custody: now repo → laptop → run as needed

set -euo pipefail

# ── config ────────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.sh"
LOG_FILE="${SCRIPT_DIR}/clean.log"

DRY_RUN=false
MODE="safe"       # safe | deep | report
RUN_ALL=false

# ── load config overrides ─────────────────────────────────────────────────────
[[ -f "$CONFIG_FILE" ]] && source "$CONFIG_FILE"

# ── resolve the real user's home when running under sudo ──────────────────────
# sudo typically sets HOME=/root; we want the invoking user's home instead.
REAL_USER="${SUDO_USER:-${USER:-$(id -un)}}"
REAL_HOME=$(getent passwd "$REAL_USER" 2>/dev/null | cut -d: -f6)
REAL_HOME="${REAL_HOME:-$HOME}"

# ── colours ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

# ── helpers ───────────────────────────────────────────────────────────────────
log()   { echo -e "${CYAN}[$(date '+%H:%M:%S')]${RESET} $*" | tee -a "$LOG_FILE"; }
warn()  { echo -e "${YELLOW}  ⚠  $*${RESET}" | tee -a "$LOG_FILE"; }
ok()    { echo -e "${GREEN}  ✓  $*${RESET}" | tee -a "$LOG_FILE"; }
err()   { echo -e "${RED}  ✗  $*${RESET}" | tee -a "$LOG_FILE"; }
sep()   { echo -e "${BOLD}────────────────────────────────────────${RESET}"; }

run_cmd() {
    local desc="$1"; shift
    if $DRY_RUN; then
        echo -e "  ${YELLOW}[DRY]${RESET} $*"
    else
        log "$desc"
        if "$@" 2>>"$LOG_FILE"; then
            ok "$desc done"
        else
            warn "$desc had warnings (check log)"
        fi
    fi
}

require_root() {
    if [[ $EUID -ne 0 ]]; then
        err "This operation requires sudo. Run with: sudo $0 $*"
        exit 1
    fi
}

bytes_to_human() { numfmt --to=iec --suffix=B "$1" 2>/dev/null || printf "%d B" "$1"; }

# sum available blocks across all local (non-virtual) filesystems
disk_free_bytes() { df -l --output=avail | tail -n +2 | awk '{s+=$1} END {print s * 1024}'; }

# ── argument parsing ──────────────────────────────────────────────────────────
usage() {
    cat <<EOF
${BOLD}Ubuntu Drive Cleaner${RESET}

Usage: $(basename "$0") [options]

Options:
  --dry-run       Show what would be done without doing it
  --mode MODE     safe (default) | deep | report
  --all           Run all safe steps non-interactively
  -h, --help      Show this help

Modes:
  report   Disk usage summary only — no changes
  safe     APT cache, old kernels, snap revisions, journals, thumbnails
  deep     safe + user caches, crash reports, temp files (prompts for each)

Examples:
  sudo ./clean.sh --mode report
  sudo ./clean.sh --dry-run --all
  sudo ./clean.sh --mode deep
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)  DRY_RUN=true ;;
        --all)      RUN_ALL=true ;;
        --mode)     MODE="$2"; shift ;;
        -h|--help)  usage ;;
        *)          err "Unknown option: $1"; usage ;;
    esac
    shift
done

# ── confirm helper ────────────────────────────────────────────────────────────
confirm() {
    local prompt="$1"
    $RUN_ALL && return 0
    read -r -p "  ${BOLD}${prompt} [y/N] ${RESET}" ans
    [[ "${ans,,}" == "y" ]]
}

# ══════════════════════════════════════════════════════════════════════════════
#  REPORT MODE
# ══════════════════════════════════════════════════════════════════════════════
report_mode() {
    sep
    echo -e "${BOLD}  DISK USAGE REPORT  $(date '+%Y-%m-%d %H:%M')${RESET}"
    sep

    echo -e "\n${BOLD}Filesystems:${RESET}"
    df -h --output=source,fstype,size,used,avail,pcent,target \
        | grep -v tmpfs | grep -v udev

    echo -e "\n${BOLD}Top 15 space consumers (known large dirs, depth 3):${RESET}"
    du -ah --max-depth=3 /var /home /usr /opt /snap 2>/dev/null \
        | sort -rh \
        | head -15

    echo -e "\n${BOLD}APT cache size:${RESET}"
    du -sh /var/cache/apt/archives/ 2>/dev/null || echo "  n/a"

    echo -e "\n${BOLD}Journal log size:${RESET}"
    journalctl --disk-usage 2>/dev/null || echo "  n/a"

    echo -e "\n${BOLD}Snap revisions (disabled = removable):${RESET}"
    snap list --all 2>/dev/null | awk 'NR==1 || /disabled/' || echo "  snap not installed"

    echo -e "\n${BOLD}Old kernels installed:${RESET}"
    dpkg --list 'linux-image-*' 2>/dev/null \
        | awk '/^ii/{print $2}' \
        | grep -v "$(uname -r)" \
        || echo "  none found"

    echo -e "\n${BOLD}Thumbnail cache (~/.cache/thumbnails):${RESET}"
    du -sh ~/.cache/thumbnails 2>/dev/null || echo "  empty or missing"

    echo -e "\n${BOLD}Crash reports (/var/crash):${RESET}"
    ls -lh /var/crash/ 2>/dev/null || echo "  empty or missing"

    echo -e "\n${BOLD}User cache dir (${REAL_HOME}/.cache):${RESET}"
    du -sh "${REAL_HOME}/.cache" 2>/dev/null || echo "  n/a"

    if [[ ${#EXTRA_REPORT_DIRS[@]} -gt 0 ]]; then
        echo -e "\n${BOLD}Extra directories:${RESET}"
        for dir in "${EXTRA_REPORT_DIRS[@]}"; do
            [[ -d "$dir" ]] && du -sh "$dir" 2>/dev/null || echo "  $dir: not found"
        done
    fi

    sep
    echo -e "${GREEN}Report complete — no changes made.${RESET}\n"
}

# ══════════════════════════════════════════════════════════════════════════════
#  SAFE CLEANING STEPS
# ══════════════════════════════════════════════════════════════════════════════

clean_apt() {
    sep; log "APT cache & orphan packages"
    run_cmd "apt autoremove"      apt-get -y autoremove
    run_cmd "apt autoclean"       apt-get -y autoclean
    run_cmd "apt clean"           apt-get clean
}

clean_old_kernels() {
    sep; log "Old kernels"
    local current; current=$(uname -r)
    local old_kernels
    # sort -V then head -n -1 preserves the most recent non-running kernel as a fallback
    old_kernels=$(dpkg --list 'linux-image-*' 2>/dev/null \
        | awk '/^ii/{print $2}' \
        | grep -v "$current" \
        | grep -v "linux-image-generic" \
        | sort -V | head -n -1 || true)

    if [[ -z "$old_kernels" ]]; then
        ok "No old kernels to remove"
        return
    fi

    echo "  Old kernels found:"
    echo "$old_kernels" | sed 's/^/    /'
    if confirm "Remove old kernels?"; then
        # shellcheck disable=SC2086
        run_cmd "Removing old kernels" apt-get -y purge $old_kernels
    else
        warn "Skipped old kernel removal"
    fi
}

clean_snap_revisions() {
    sep; log "Snap disabled revisions"
    if ! command -v snap &>/dev/null; then
        warn "snap not installed — skipping"
        return
    fi

    local disabled_snaps
    disabled_snaps=$(snap list --all | awk '/disabled/{print $1, $3}')

    if [[ -z "$disabled_snaps" ]]; then
        ok "No disabled snap revisions found"
        return
    fi

    echo "  Disabled snap revisions:"
    echo "$disabled_snaps" | sed 's/^/    /'

    if confirm "Remove disabled snap revisions?"; then
        while read -r snapname revision; do
            run_cmd "Removing $snapname rev $revision" \
                snap remove "$snapname" --revision="$revision"
        done <<< "$disabled_snaps"
    else
        warn "Skipped snap revision cleanup"
    fi
}

clean_journals() {
    sep; log "systemd journal logs"
    local keep="${JOURNAL_KEEP:-7d}"
    log "Vacuuming logs older than $keep"
    run_cmd "journalctl vacuum (time)" journalctl --vacuum-time="$keep"
    run_cmd "journalctl vacuum (size)" journalctl --vacuum-size=200M
}

clean_thumbnails() {
    sep; log "Thumbnail cache"
    local thumb_dir="${REAL_HOME}/.cache/thumbnails"
    if [[ -d "$thumb_dir" ]]; then
        local size; size=$(du -sh "$thumb_dir" 2>/dev/null | cut -f1)
        log "Thumbnail cache size: $size"
        if confirm "Clear thumbnail cache?"; then
            run_cmd "Clearing thumbnails" rm -rf "${thumb_dir:?}"/*
        fi
    else
        ok "No thumbnail cache found"
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
#  DEEP CLEANING STEPS
# ══════════════════════════════════════════════════════════════════════════════

clean_user_cache() {
    sep; log "User application cache (~/.cache) for ${REAL_USER}"
    local cache_dir="${REAL_HOME}/.cache"
    local size; size=$(du -sh "$cache_dir" 2>/dev/null | cut -f1)
    warn "${cache_dir} is $size — this clears ALL cached app data"
    if confirm "Clear ${cache_dir} (keeps thumbnails dir itself)?"; then
        # exclude thumbnails dir itself since we handle it above
        find "$cache_dir" -mindepth 1 -maxdepth 1 \
            ! -name 'thumbnails' \
            -exec rm -rf {} + 2>/dev/null || true
        ok "User cache cleared (thumbnails folder preserved)"
    else
        warn "Skipped user cache"
    fi
}

clean_crash_reports() {
    sep; log "Crash reports (/var/crash)"
    if [[ -d /var/crash ]] && [[ -n "$(ls -A /var/crash 2>/dev/null)" ]]; then
        ls -lh /var/crash/
        if confirm "Delete crash reports?"; then
            run_cmd "Removing crash reports" rm -f /var/crash/*
        fi
    else
        ok "No crash reports found"
    fi
}

clean_temp_files() {
    sep; log "Old temp files (/tmp, /var/tmp)"
    local tmp_bytes; tmp_bytes=$(du -sb /tmp /var/tmp 2>/dev/null | awk '{sum+=$1} END{print sum+0}')
    log "/tmp + /var/tmp: $(numfmt --to=iec "$tmp_bytes" 2>/dev/null || echo "${tmp_bytes} bytes")"
    if confirm "Remove temp files older than 7 days?"; then
        run_cmd "Cleaning /tmp"     find /tmp     -type f -mtime +7 -delete 2>/dev/null || true
        run_cmd "Cleaning /var/tmp" find /var/tmp -type f -mtime +7 -delete 2>/dev/null || true
    fi
}

clean_locales() {
    sep; log "Unused locale data"
    if command -v localepurge &>/dev/null; then
        run_cmd "localepurge" localepurge
    elif confirm "Install localepurge to remove unused locales?"; then
        run_cmd "Install localepurge" apt-get install -y localepurge
        run_cmd "localepurge" localepurge
    else
        warn "Skipped locale cleanup"
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
main() {
    # report mode may run without root; avoid touching a root-owned log file
    if [[ "$MODE" == "report" ]]; then
        LOG_FILE="/dev/null"
    else
        echo "" > "$LOG_FILE"
    fi
    sep
    echo -e "${BOLD}  Ubuntu Drive Cleaner — mode: ${MODE}${RESET}"
    $DRY_RUN && echo -e "  ${YELLOW}DRY RUN — no changes will be made${RESET}"
    sep

    case "$MODE" in
        report)
            report_mode
            exit 0
            ;;
        safe|deep)
            require_root
            local before; before=$(disk_free_bytes)

            clean_apt
            clean_old_kernels
            clean_snap_revisions
            clean_journals
            clean_thumbnails

            if [[ "$MODE" == "deep" ]]; then
                clean_user_cache
                clean_crash_reports
                clean_temp_files
                clean_locales
            fi

            local after; after=$(disk_free_bytes)
            local gained=$(( after - before ))
            sep
            if (( gained > 0 )); then
                ok "Space freed: $(bytes_to_human $gained)"
            elif (( gained == 0 )); then
                ok "No additional space freed (already clean)"
            else
                warn "Disk free decreased slightly (system activity during run)"
            fi
            log "Log saved to: $LOG_FILE"
            sep
            ;;
        *)
            err "Unknown mode: $MODE"
            usage
            ;;
    esac
}

main "$@"
