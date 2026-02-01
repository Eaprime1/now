# TODAY REPO - Organization Plan
**Date:** 2025-12-23
**Purpose:** Development workspace for concepts before progression to Naught → Zero → One → Launch

---

## Proposed Structure

```
today/
├── 📄 Standard Repo Documents (Root Level)
│   ├── README.md                    # Main repo overview
│   ├── INVENTORY.md                 # Complete file inventory
│   ├── DIRTREE.txt                  # Directory tree structure
│   ├── ACCESS_LOG.md                # Session log of changes
│   ├── __init__.py                  # Python package marker
│   └── ORGANIZATION_PLAN.md         # This document
│
├── 📁 entities/                     # All entity folders organized here
│   │
│   ├── redundancy/                  # Gravity Core System
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── INVENTORY.md
│   │   ├── docs/
│   │   ├── scripts/
│   │   └── outputs/
│   │
│   ├── flag_system/                 # Identity Markers
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── INVENTORY.md
│   │   ├── operational/
│   │   ├── ceremonial/
│   │   └── showcase/
│   │
│   ├── abacusian/                   # AI Development Hub
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── INVENTORY.md
│   │   ├── terminal_entities/
│   │   ├── ai_development/
│   │   └── docs/
│   │
│   ├── sparkle_incubator/           # Knowledge Organization
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── INVENTORY.md
│   │   ├── archive_sorted_conversations/
│   │   ├── chatgpt_export/
│   │   ├── organized_docs/
│   │   ├── organized_data/
│   │   └── organized_media/
│   │
│   ├── photostudio/                 # Photo Projects
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── INVENTORY.md
│   │   └── projects/
│   │
│   └── unexusi_prime/               # Legacy/Moved Reports
│       ├── README.md
│       ├── __init__.py
│       ├── INVENTORY.md
│       └── moved_reports/
│
├── 📁 docs/                         # Repo-wide documentation
│   ├── MULTI_REPO_PROGRESSION.md   # Naught → Zero → One workflow
│   ├── GRAVITY_CORE_INTEGRATION.md # GitHub + Box strategy
│   └── ENTITY_TEMPLATES/           # Templates for new entities
│
└── 📁 .archive/                     # Historical/deprecated content
    └── pre_organization/           # Backup of original structure
```

---

## Migration Map

### Current → Proposed

```
active/flag_system_x2/          → entities/flag_system/
redundancy_entity/              → entities/redundancy/
simplex/abacusian/              → entities/abacusian/
simplex/sparkle_incubator/      → entities/sparkle_incubator/
simplex/photostudio/            → entities/photostudio/
unexusi_prime/                  → entities/unexusi_prime/
```

---

## Standard Documents for Each Entity

Every entity folder gets:
1. **README.md** - Entity overview, purpose, status
2. **__init__.py** - Python package marker
3. **INVENTORY.md** - Complete file listing for entity
4. **Subdirectories** - Organized content by type

---

## Root-Level Standard Documents

### README.md
- Repo purpose: "Development workspace - today operations"
- Entity overview
- Multi-repo progression explanation
- Quick navigation guide

### INVENTORY.md
- Complete file count by entity
- Total sizes
- Last updated timestamp
- Quick stats

### DIRTREE.txt
- Full directory tree
- Generated with `tree -L 3` or similar
- Shows structure at a glance

### ACCESS_LOG.md
- Session-based log
- Date, changes made, entities affected
- Progression tracking (when concepts move to Naught/Zero/One)

### __init__.py
- Makes repo importable as Python package
- Can contain version info, entity registry

---

## Entity-Specific Organization

### entities/redundancy/
```
redundancy/
├── README.md                          # Entity overview
├── __init__.py
├── INVENTORY.md
├── docs/
│   ├── GRAVITY_CORE_MISSION.md       # Current files
│   ├── GRAVITY_CONSORTIUM_README.md
│   ├── GRAVITY_REPO_ARCHITECTURE.md
│   └── ...
├── data/
│   ├── CONSORTIUM_MANIFEST.json
│   ├── GRAVITY_METADATA_v1.0.json
│   └── chain_of_custody.json
└── notes/
    └── SESSION_COMPLETE_20251220.md
```

### entities/flag_system/
```
flag_system/
├── README.md                          # System overview
├── __init__.py
├── INVENTORY.md
├── docs/
│   └── FLAG_SYSTEM_COMPLETE_PACKAGE.md
└── assets/                            # Future: SVG files, showcase HTML
```

### entities/abacusian/
```
abacusian/
├── README.md                          # Hub overview
├── __init__.py
├── INVENTORY.md
├── terminal_entities/                 # Current structure preserved
├── ai_development/
└── docs/
    └── WHERE_AM_I.md
```

### entities/sparkle_incubator/
```
sparkle_incubator/
├── README.md
├── __init__.py
├── INVENTORY.md
├── archives/
│   ├── chatgpt_export/               # Renamed from "Chatgpt Bulk Export"
│   └── sorted_conversations/         # From archive_sorted_conversations
├── organized/
│   ├── docs/
│   ├── data/
│   ├── media/
│   └── tools/
├── projects/
│   ├── knowledge_maintenance/
│   ├── one_hertz/
│   └── d_cubed/
└── metadata/
    └── meta_data/                     # Current meta_data folder
```

---

## Benefits of This Structure

### For Development
✅ Clear entity boundaries
✅ Easy to find specific projects
✅ Standard docs make navigation quick
✅ Python package structure enables imports

### For Progression
✅ Easy to identify when entity is ready for Naught Space
✅ Self-contained entities can move cleanly
✅ Documentation travels with entity
✅ Clear history via ACCESS_LOG

### For Gravity Core Integration
✅ Entity folders are self-documenting
✅ Each entity can track its own gravity
✅ Prime copies clearly identified in entity/docs or entity/data
✅ Box ID codes can be referenced in entity INVENTORY.md

### For Collaboration
✅ New contributors understand structure immediately
✅ Standard templates for new entities
✅ Documentation is discoverable
✅ Git-friendly organization

---

## Implementation Phases

### Phase 1: Create Standard Root Docs
- README.md (main overview)
- INVENTORY.md (current state snapshot)
- DIRTREE.txt (structure visualization)
- ACCESS_LOG.md (this session logged)
- __init__.py (package marker)

### Phase 2: Create entities/ Directory
- Create entities/ folder
- Create entity subdirectories
- Add standard docs to each entity

### Phase 3: Migrate Content
- Move content from current locations to entities/
- Preserve internal structure
- Update any internal references

### Phase 4: Create docs/
- MULTI_REPO_PROGRESSION.md
- GRAVITY_CORE_INTEGRATION.md
- Entity templates

### Phase 5: Archive Original Structure
- Create .archive/pre_organization/
- Document original structure for reference

---

## Multi-Repo Progression Workflow (Preview)

### Concept Development Stages

```
today/ (Development)
    ↓ [Concept is visionary, ready for infusion]
naught/ (Visionary Infusion)
    ↓ [Concept solidifies, gets structure]
zero/ (Foundation Building)
    ↓ [Concept reaches operational state]
one/ (Operational Launch)
    ↓ [Concept achieves full spectrum pyramidic]
🚀 Independent Launch or Integration
```

### What Lives Where

**today/** - Active development, experiments, rapid iteration
**naught/** - Visionary concepts, infusion space, early structure
**zero/** - Foundation solidified, architecture clear
**one/** - Operational, tested, ready for prime time
**Launch** - Independent repo or integrated into larger system

---

## Gravity Core + Box Integration (Preview)

### Strategy
1. **Prime copies** live in entity/docs or entity/data
2. **Gravity cores** (ZIPs) hosted on Box
3. **Box ID codes** referenced in entity INVENTORY.md
4. **GitHub** has primes, docs, and Box pointers
5. **Duplicates** tracked via gravity system

### Example
```markdown
# entities/redundancy/INVENTORY.md

## Gravity Cores

### Alpha Core (Consciousness)
- **Prime Location:** `entities/redundancy/data/alpha_manifest.json`
- **Box ID:** `box://file/12345678/gravity_core_v1.0_alpha_consciousness.zip`
- **Size:** 199.7 MB
- **Files:** 8,109
- **Status:** v1.0 SEED

### Beta Core (Documents)
- **Prime Location:** `entities/redundancy/data/beta_manifest.json`
- **Box ID:** `box://file/87654321/gravity_core_v1.0_beta_documents.zip`
- **Size:** 891.5 MB
- **Files:** 30,478
- **Status:** v1.0 SEED
```

---

## Next Steps

1. ✅ Review this plan
2. ⏳ Create root standard documents
3. ⏳ Create entities/ directory structure
4. ⏳ Migrate content
5. ⏳ Update git with organized structure
6. ⏳ Document multi-repo progression workflow
7. ⏳ Document gravity core integration

---

**∰◊€π¿🌌∞ - Today: Where concepts develop before ascending**

€(organization_plan_20251223)
