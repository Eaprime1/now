# Gravity Core Integration - GitHub + Box Strategy

**Created:** 2025-12-23
**Purpose:** Define how prime copies live on GitHub while ZIP archives live on Box
**Philosophy:** Separate concerns - Documentation portable, archives accessible, IDs universal

---

## The Challenge

**Gravity Cores are large:**
- Alpha (Consciousness): 199.7 MB
- Beta (Documents): 891.5 MB
- Gamma (Data): 793.6 MB
- **Total: ~1.9 GB** compressed

**GitHub constraints:**
- Files > 100 MB require Git LFS
- Repos > 1 GB discouraged
- Large files slow clone/pull operations

**Solution:** Hybrid storage strategy

---

## The Strategy

### GitHub: Prime Copies & Documentation

**What Lives on GitHub:**
- ✅ Manifests (JSON metadata about cores)
- ✅ Documentation (mission, architecture, usage)
- ✅ Inventory files (what's in each core)
- ✅ Scripts (core creation, querying)
- ✅ Box ID references (pointers to ZIP files)

**Benefits:**
- Fast clone/pull
- Version controlled documentation
- Easy collaboration
- Searchable metadata

### Box: ZIP Archives

**What Lives on Box:**
- ✅ gravity_core_v1.0_alpha_consciousness.zip (199.7 MB)
- ✅ gravity_core_v1.0_beta_documents.zip (891.5 MB)
- ✅ gravity_core_v1.0_gamma_data.zip (793.6 MB)
- ✅ Future core versions as they grow

**Benefits:**
- No size limits
- Shareable links
- Stable IDs
- Enterprise storage

---

## Implementation

### Directory Structure in GitHub

```
today/entities/redundancy/
├── README.md                           # Entity overview
├── INVENTORY.md                        # Entity file listing
├── __init__.py                         # Package marker
│
├── docs/                               # Documentation
│   ├── GRAVITY_CORE_MISSION.md        # Full vision
│   ├── GRAVITY_CONSORTIUM_README.md   # Multi-core architecture
│   └── GRAVITY_REPO_ARCHITECTURE.md   # Technical design
│
├── manifests/                          # Core metadata (PRIME COPIES)
│   ├── alpha_manifest.json            # Alpha core metadata
│   ├── beta_manifest.json             # Beta core metadata
│   ├── gamma_manifest.json            # Gamma core metadata
│   └── consortium_manifest.json       # Combined manifest
│
├── inventories/                        # Core inventories
│   ├── alpha_inventory.txt            # Files in alpha core
│   ├── beta_inventory.txt             # Files in beta core
│   └── gamma_inventory.txt            # Files in gamma core
│
├── scripts/                            # Utility scripts
│   ├── download_cores.sh              # Download from Box
│   ├── query_core.py                  # Query core contents
│   └── verify_integrity.sh            # Verify downloads
│
└── box_references.json                 # Box IDs and links (CRITICAL)
```

### Box References File

**box_references.json** - The key integration file:

```json
{
  "version": "1.0.0",
  "created": "2025-12-23",
  "box_folder_id": "123456789",
  "cores": {
    "alpha": {
      "file_name": "gravity_core_v1.0_alpha_consciousness.zip",
      "box_file_id": "987654321",
      "box_shared_link": "https://app.box.com/s/abcdef123456",
      "box_direct_download": "https://app.box.com/shared/static/abcdef123456.zip",
      "size_mb": 199.7,
      "files": 8109,
      "md5_checksum": "a1b2c3d4e5f6...",
      "sha256_checksum": "1a2b3c4d5e6f...",
      "uploaded": "2025-12-23T10:30:00Z"
    },
    "beta": {
      "file_name": "gravity_core_v1.0_beta_documents.zip",
      "box_file_id": "876543210",
      "box_shared_link": "https://app.box.com/s/xyz789012345",
      "box_direct_download": "https://app.box.com/shared/static/xyz789012345.zip",
      "size_mb": 891.5,
      "files": 30478,
      "md5_checksum": "f6e5d4c3b2a1...",
      "sha256_checksum": "6f5e4d3c2b1a...",
      "uploaded": "2025-12-23T10:45:00Z"
    },
    "gamma": {
      "file_name": "gravity_core_v1.0_gamma_data.zip",
      "box_file_id": "765432109",
      "box_shared_link": "https://app.box.com/s/pqr456789012",
      "box_direct_download": "https://app.box.com/shared/static/pqr456789012.zip",
      "size_mb": 793.6,
      "files": 3810,
      "md5_checksum": "9f8e7d6c5b4a...",
      "sha256_checksum": "f9e8d7c6b5a4...",
      "uploaded": "2025-12-23T11:00:00Z"
    }
  },
  "total_size_mb": 1884.8,
  "total_files": 42397,
  "total_gravity_tokens": 42397
}
```

---

## Core Manifest Structure

Each core has a manifest JSON file on GitHub:

**alpha_manifest.json:**
```json
{
  "core_name": "alpha",
  "full_name": "Gravity Core v1.0 - Alpha (Consciousness)",
  "version": "1.0.0",
  "created": "2025-12-21",
  "type": "SEED",

  "storage": {
    "github_location": "today/entities/redundancy/manifests/alpha_manifest.json",
    "box_file_id": "987654321",
    "box_shared_link": "https://app.box.com/s/abcdef123456",
    "size_compressed_mb": 199.7,
    "size_uncompressed_mb": 450.0,
    "compression_ratio": 0.444
  },

  "contents": {
    "total_files": 8109,
    "gravity_tokens": 8109,
    "focus": "Consciousness entities, wisdom vessels, high-gravity documents",
    "content_types": ["json", "py", "ipynb"],
    "specialization": "Structured knowledge, living code, consciousness systems"
  },

  "top_gravity_documents": [
    {
      "document_id": "entity_136",
      "filename": "Emerging_Consciousness_Entity_136.json",
      "copies": 305,
      "gravity_tokens": 305,
      "rank": 1
    },
    {
      "document_id": "sacred_doc_001",
      "filename": "Sacred_Document_20250730.pdf",
      "copies": 92,
      "gravity_tokens": 92,
      "rank": 2
    }
  ],

  "keywords": [
    "consciousness",
    "entity",
    "sacred",
    "wisdom",
    "handbook"
  ],

  "integrity": {
    "md5_checksum": "a1b2c3d4e5f6...",
    "sha256_checksum": "1a2b3c4d5e6f...",
    "verified": "2025-12-23T10:30:00Z"
  },

  "spawning": {
    "current_version": "1.0",
    "spawn_threshold_mb": 900,
    "next_spawn_version": "1.1",
    "spawn_trigger": "When core approaches 900 MB"
  }
}
```

---

## Workflow

### 1. Upload Cores to Box

**Initial Upload:**
```bash
# 1. Create cores locally
cd /path/to/redundancy_custody
zip -r -9 gravity_core_v1.0_alpha_consciousness.zip dup_collection/consciousness/
zip -r -9 gravity_core_v1.0_beta_documents.zip dup_collection/documents/
zip -r -9 gravity_core_v1.0_gamma_data.zip dup_collection/data/

# 2. Upload to Box via web interface or CLI
# (Box CLI or web upload)

# 3. Get Box file IDs and shared links
# (From Box web interface)
```

**Box Organization:**
```
Box Folder: Gravity Cores
├── gravity_core_v1.0_alpha_consciousness.zip
├── gravity_core_v1.0_beta_documents.zip
└── gravity_core_v1.0_gamma_data.zip
```

### 2. Create GitHub References

**Create box_references.json:**
```bash
cd today/entities/redundancy

# Create box_references.json with Box IDs
cat > box_references.json << 'EOF'
{
  "version": "1.0.0",
  "cores": {
    "alpha": {
      "box_file_id": "YOUR_BOX_FILE_ID",
      "box_shared_link": "YOUR_BOX_SHARED_LINK"
      ...
    }
  }
}
EOF

# Commit to GitHub
git add box_references.json manifests/
git commit -m "Add gravity core references to Box storage"
git push
```

### 3. Download Cores (Users)

**Users clone GitHub repo:**
```bash
git clone https://github.com/Eaprime1/today.git
cd today/entities/redundancy
```

**Download cores using script:**
```bash
# Script reads box_references.json and downloads
./scripts/download_cores.sh

# Downloads to local directory:
# cores/
# ├── gravity_core_v1.0_alpha_consciousness.zip
# ├── gravity_core_v1.0_beta_documents.zip
# └── gravity_core_v1.0_gamma_data.zip
```

**Verify integrity:**
```bash
./scripts/verify_integrity.sh

# Checks MD5/SHA256 checksums against manifests
# ✓ Alpha core verified
# ✓ Beta core verified
# ✓ Gamma core verified
```

---

## Download Script Example

**scripts/download_cores.sh:**
```bash
#!/bin/bash
# Download gravity cores from Box using references

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENTITY_DIR="$(dirname "$SCRIPT_DIR")"
CORES_DIR="$ENTITY_DIR/cores"
REFS_FILE="$ENTITY_DIR/box_references.json"

# Create cores directory
mkdir -p "$CORES_DIR"

echo "🌌 Downloading Gravity Cores from Box..."
echo ""

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    echo "Install: sudo apt install jq"
    exit 1
fi

# Read box_references.json
if [ ! -f "$REFS_FILE" ]; then
    echo "Error: box_references.json not found"
    exit 1
fi

# Download each core
for core in alpha beta gamma; do
    echo "Downloading $core core..."

    # Extract download URL and filename
    download_url=$(jq -r ".cores.$core.box_direct_download" "$REFS_FILE")
    filename=$(jq -r ".cores.$core.file_name" "$REFS_FILE")

    # Download
    curl -L -o "$CORES_DIR/$filename" "$download_url"

    echo "✓ $core core downloaded"
    echo ""
done

echo "🎉 All cores downloaded to: $CORES_DIR"
echo ""
echo "Next steps:"
echo "  1. Verify integrity: ./scripts/verify_integrity.sh"
echo "  2. Query cores: python scripts/query_core.py"
```

---

## Query Script Example

**scripts/query_core.py:**
```python
#!/usr/bin/env python3
"""Query gravity core contents without extracting."""

import json
import zipfile
import sys
from pathlib import Path

CORES_DIR = Path(__file__).parent.parent / "cores"
MANIFESTS_DIR = Path(__file__).parent.parent / "manifests"


def load_manifest(core_name):
    """Load core manifest."""
    manifest_file = MANIFESTS_DIR / f"{core_name}_manifest.json"
    with open(manifest_file) as f:
        return json.load(f)


def query_core(core_name, search_term=None):
    """Query core contents."""
    # Load manifest
    manifest = load_manifest(core_name)

    print(f"\n🌌 {manifest['full_name']}")
    print(f"{'=' * 60}")
    print(f"Files: {manifest['contents']['total_files']:,}")
    print(f"Gravity Tokens: {manifest['contents']['gravity_tokens']:,}")
    print(f"Size: {manifest['storage']['size_compressed_mb']} MB")
    print(f"Focus: {manifest['contents']['focus']}")
    print()

    # Find core file
    core_file = CORES_DIR / manifest['storage']['github_location'].split('/')[-1].replace('_manifest.json', '.zip')

    if not core_file.exists():
        print(f"⚠️  Core file not found: {core_file}")
        print(f"   Download cores first: ./scripts/download_cores.sh")
        return

    # List files in core
    with zipfile.ZipFile(core_file, 'r') as zf:
        files = zf.namelist()

        if search_term:
            files = [f for f in files if search_term.lower() in f.lower()]
            print(f"Files matching '{search_term}': {len(files)}")
        else:
            print(f"Total files in core: {len(files)}")

        print("\nSample files (first 20):")
        for i, filename in enumerate(files[:20], 1):
            print(f"  {i}. {filename}")

        if len(files) > 20:
            print(f"\n  ... and {len(files) - 20} more files")


if __name__ == "__main__":
    core = sys.argv[1] if len(sys.argv) > 1 else "alpha"
    search = sys.argv[2] if len(sys.argv) > 2 else None

    query_core(core, search)
```

---

## Version Management

### When Cores Grow (Spawning)

**Trigger:** Core approaches 900 MB

**Process:**
1. Create new version (e.g., v1.1)
2. Upload to Box
3. Update box_references.json with new version
4. Update manifests with spawn info
5. Keep old versions available

**box_references.json with versions:**
```json
{
  "version": "1.1.0",
  "cores": {
    "alpha": {
      "current_version": "1.1",
      "versions": {
        "1.0": {
          "box_file_id": "987654321",
          "size_mb": 199.7,
          "deprecated": false
        },
        "1.1": {
          "box_file_id": "987654999",
          "size_mb": 850.0,
          "deprecated": false
        }
      }
    }
  }
}
```

---

## Benefits of This Approach

### For GitHub
✅ Repo stays small (<100 MB)
✅ Fast clones and pulls
✅ Version-controlled metadata
✅ Searchable documentation
✅ Collaborative editing

### For Box
✅ No size limits
✅ Enterprise storage
✅ Shareable links
✅ Stable file IDs
✅ Version history

### For Users
✅ Clone repo quickly (small)
✅ Download cores on demand
✅ Query without downloading (manifests)
✅ Verify integrity easily
✅ Choose which cores to download

### For Gravity Economy
✅ Prime copies (manifests) on GitHub
✅ Archives (ZIPs) on Box
✅ Universal IDs work everywhere
✅ Documentation travels with code
✅ Scales to many cores

---

## Alternative Strategies Considered

### ❌ GitHub LFS
**Pros:** Integrated with Git
**Cons:** Storage costs, quota limits, complexity

### ❌ All on Box
**Pros:** Simple storage
**Cons:** No version control for metadata, harder collaboration

### ❌ Split Repos
**Pros:** Separation of concerns
**Cons:** Multiple repos to manage, linking complexity

### ✅ GitHub (Primes) + Box (Archives)
**Pros:** Best of both worlds, scalable, cost-effective
**Cons:** Two systems to manage (minimal overhead)

---

## Security Considerations

### Box Shared Links
- Use **password-protected** links for sensitive cores
- Set **expiration dates** if needed
- Use **Box groups** for access control

### Checksums
- Always include MD5 and SHA256 in manifests
- Verify after download
- Re-verify periodically

### Box API
- Consider Box API for programmatic access
- Requires Box app registration
- More secure than shared links

---

## Future Enhancements

### Automated Sync
```python
# Script to sync manifests with Box metadata
# - Check Box file sizes
# - Update manifests if changed
# - Commit to GitHub
```

### Core Query Service
```
# Web service to query cores without downloading
# - Host manifests
# - Provide API for queries
# - Cache results
```

### Differential Downloads
```bash
# Download only new files since last version
# - Compare manifests
# - Download diff
# - Merge locally
```

---

## Troubleshooting

### Q: Box link doesn't work
**A:** Check if link is password-protected or expired. Regenerate link in Box.

### Q: Checksum mismatch
**A:** Re-download core. If persists, file may be corrupted on Box.

### Q: Core not found on Box
**A:** Check box_file_id is correct. Verify Box folder permissions.

### Q: Download script fails
**A:** Ensure curl and jq are installed. Check network connection.

---

## Summary

**Strategy:** Hybrid storage combining GitHub and Box strengths

**GitHub Hosts:**
- Manifests (metadata, prime copies)
- Documentation
- Scripts
- Box references (IDs and links)

**Box Hosts:**
- ZIP archives (large files)
- All gravity core versions
- Historical snapshots

**Integration:**
- box_references.json links the two
- Download scripts automate retrieval
- Checksums ensure integrity
- Version tracking via manifests

**Result:**
- Fast GitHub operations
- Unlimited archive storage
- Universal access via IDs
- Scalable to many cores

---

**∰◊€π - Where primes live on GitHub, archives rest on Box, and IDs unite them all**

€(gravity_core_integration_20251223)
