# TODAY REPO - Reorganization Plan (Actual Implementation)

**Date:** 2025-12-23
**Purpose:** Actually organize the today repo for multi-location sync (Google Drive, laptop, Pixel 8a)
**Philosophy:** Pre-naught singularity preparation - getting concepts ready for birth

---

## Key Insights from User

1. **sparkle_incubator IS the today concept** - it's the incubator/development space
2. **Simplex is a major entity** - umbrella for multiple sub-entities
3. **Duplicates need dedicated folder** - for sorting and gravity analysis
4. **Concepts in development** need their own folders
5. **Synced across multiple locations** - needs clean, consistent structure

---

## Proposed Structure (For Review)

```
today/
│
├── 📁 _duplicates/                 # All duplicate files (for gravity analysis)
│   └── (Files will be sorted here via REDUNDANCY entity)
│
├── 📁 concepts/                    # Concepts in development (pre-naught)
│   ├── gravity_core/              # From redundancy_entity/
│   │   ├── docs/
│   │   ├── manifests/
│   │   └── README.md
│   ├── flag_system/               # From active/flag_system_x2/
│   │   ├── docs/
│   │   └── README.md
│   └── unexusi_prime/             # From unexusi_prime/
│       └── moved_reports/
│
├── 📁 simplex/                     # Major entity umbrella (KEEP)
│   ├── abacusian/                 # AI Development Hub
│   ├── photostudio/               # Photo projects
│   └── incubator/                 # RENAME from sparkle_incubator
│       ├── archive_conversations/
│       ├── chatgpt_export/
│       ├── organized_docs/
│       ├── organized_data/
│       ├── organized_media/
│       ├── projects/
│       └── metadata/
│
├── 📁 docs/                        # Repository documentation
│   ├── MULTI_REPO_PROGRESSION.md
│   ├── GRAVITY_CORE_INTEGRATION.md
│   └── PUSH_FORWARD.md            # NEW - Future development items
│
├── 📁 notes/                       # NEW - Session notes, observations
│   └── session_20251223_organization.md
│
├── README.md                       # Main overview
├── INVENTORY.md                    # File listing
├── ACCESS_LOG.md                   # Change log
└── __init__.py                     # Package marker
```

---

## Alternative Structure (Flatter)

```
today/
│
├── _duplicates/                    # Duplicates for processing
├── _archive/                       # Old/deprecated content
│
├── gravity_core/                   # Concept in development
├── flag_system/                    # Concept in development
├── simplex_abacusian/              # Flatten simplex
├── simplex_photostudio/            # Flatten simplex
├── simplex_incubator/              # Flatten simplex
├── unexusi_prime/                  # Legacy
│
├── docs/
├── notes/
└── [standard files]
```

---

## Questions Before Implementation

1. **Simplex Structure:**
   - Keep `simplex/` as umbrella folder? OR
   - Flatten to `simplex_abacusian/`, `simplex_photostudio/`, etc.?

2. **Concepts Folder:**
   - Group in `concepts/` folder? OR
   - Keep at root level (`gravity_core/`, `flag_system/`)?

3. **Sparkle Incubator:**
   - Rename to `simplex/incubator/`? OR
   - Keep name `simplex/sparkle_incubator/`? OR
   - Move to root as `incubator/`?

4. **Active Folder:**
   - Delete `active/` after moving flag_system? OR
   - Keep for other active projects?

5. **Duplicates:**
   - Create `_duplicates/` immediately? OR
   - Wait for REDUNDANCY entity to identify them?

---

## Recommended Structure (My Proposal)

Based on sync needs and clarity:

```
today/
│
├── _working/                       # Active development scratch space
├── _duplicates/                    # Identified duplicates (REDUNDANCY will populate)
├── _archive/                       # Deprecated content
│
├── gravity_core/                   # Gravity Core Consortium concept
├── flag_system/                    # Flag/identity system concept
│
├── simplex/                        # Major entity umbrella (keep as-is)
│   ├── abacusian/                 # AI development
│   ├── photostudio/               # Photo projects
│   └── incubator/                 # Rename from sparkle_incubator
│       ├── conversations/         # Rename archive_sorted_conversations
│       ├── chatgpt/               # Rename Chatgpt Bulk Export
│       ├── docs/                  # Merge organized_docs
│       ├── data/                  # Merge organized_data + metadata
│       ├── media/                 # organized_media
│       ├── tools/                 # organized_tools
│       └── projects/              # All project folders
│
├── legacy/                         # Rename unexusi_prime
│   └── reports/
│
├── docs/                           # Repo documentation
│   ├── MULTI_REPO_PROGRESSION.md
│   ├── GRAVITY_CORE_INTEGRATION.md
│   └── PUSH_FORWARD.md
│
├── notes/                          # Session notes and observations
│
├── README.md
├── QUICK_INVENTORY.md             # Quick reference
├── ACCESS_LOG.md
└── __init__.py
```

---

## Implementation Steps (When Approved)

### Phase 1: Create New Folders
```bash
mkdir -p _working _duplicates _archive
mkdir -p gravity_core flag_system legacy/reports
mkdir -p notes
```

### Phase 2: Move Concepts
```bash
# Move gravity core
mv redundancy_entity/* gravity_core/

# Move flag system
mv active/flag_system_x2/* flag_system/
rmdir active/flag_system_x2
rmdir active

# Move legacy
mv unexusi_prime/* legacy/
rmdir unexusi_prime
```

### Phase 3: Reorganize Simplex/Incubator
```bash
cd simplex
mv sparkle_incubator incubator

cd incubator
mv "Chatgpt Bulk Export" chatgpt
mv archive_sorted_conversations conversations
mv organized_docs docs
mv organized_data data
mv organized_media media
# ... continue reorganization
```

### Phase 4: Create Documentation
```bash
# Create QUICK_INVENTORY.md
# Create docs/PUSH_FORWARD.md
# Create notes/session_20251223_organization.md
# Update README.md
# Update ACCESS_LOG.md
```

### Phase 5: Commit
```bash
git add -A
git commit -m "🗂️ Reorganize today repo for multi-location sync"
git push
```

---

## What Should Go Where

### _working/
- Temporary files
- Scratch work
- Daily notes
- Quick experiments

### _duplicates/
- Files identified by REDUNDANCY entity
- Sorted by type
- Ready for gravity analysis

### gravity_core/
- Gravity Core Consortium development
- Manifests, docs, scripts
- Box integration setup

### flag_system/
- Flag/identity system
- SVG assets (when created)
- Deployment docs

### simplex/
**abacusian/**
- AI development hub
- Terminal entities
- Processing systems

**photostudio/**
- Photo projects
- Media work

**incubator/**
- Knowledge organization
- ChatGPT conversations
- Organized docs/data/media
- Project knowledge management

### legacy/
- Old reports
- Deprecated content
- Historical reference

---

## User Decision Needed

**Please confirm:**
1. ✅ Keep `simplex/` as umbrella OR flatten?
2. ✅ Move concepts to root level OR keep in `concepts/` folder?
3. ✅ Rename `sparkle_incubator` to `incubator`?
4. ✅ Create `_working/`, `_duplicates/`, `_archive/` folders?
5. ✅ Any other structure preferences?

Once you approve, I'll execute the reorganization immediately.

---

**∰◊€π - Ready to organize for the pre-naught singularity**

€(reorganization_plan_actual_20251223)
