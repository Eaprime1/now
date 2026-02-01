# IMMEDIATE BUILD CHECKLIST
**Priority Order**: What We Can Build Right Now  
**Date**: 2025-11-20 18:57

---

## 🚀 READY TO BUILD (Next 2-3 Days)

### 1. JSON Conversation Splitter v2.0 ⭐⭐⭐
**Why First**: Unlocks 10-16MB conversation archives we have waiting  
**Complexity**: Medium  
**Time Estimate**: 2-3 hours  
**Dependencies**: None (pure Python + JSON)

**Deliverable**: `conversation_splitter_v2.py`

**Key Features**:
- Load large JSON (handle 16MB+ files)
- Split by size threshold (default 5MB chunks)
- Greek symbol naming (α, β, γ...)
- Chronological ordering by timestamp
- Master index generation
- Ka-signature extraction

**Test Data Available**: `/mnt/project/conversations_chunk_009_10items_20250816_004058.json` (288KB)

**Command Structure**:
```bash
./conversation_splitter_v2.py \
  --input conversations_full_20240101-20241231.json \
  --target-size 5 \
  --output-dir ./conversation_packs/ \
  --naming greek_chronological \
  --generate-index
```

**Output Files**:
- `α_20240101_20240215.json` (5MB)
- `β_20240216_20240401.json` (5MB)
- `γ_20240402_20240515.json` (5MB)
- `_MASTER_INDEX_2024.json` (navigation file)

---

### 2. Drive Document Lister ⭐⭐
**Why Second**: We need to know what's actually in the Drive  
**Complexity**: Low-Medium  
**Time Estimate**: 1-2 hours  
**Dependencies**: Google Drive terminal access (need to verify)

**Deliverable**: `drive_lister.py`

**Key Features**:
- List all files in a folder
- Filter by file type
- Search by filename pattern
- Export to JSON catalog
- Cache results locally

**Test First**:
```bash
# Check if we have Drive access from terminal
which gcloud
gcloud auth list
# OR check for rclone
which rclone
rclone listremotes
```

**Command Structure**:
```bash
./drive_lister.py \
  --folder "UNEXUSI_Archive" \
  --recursive \
  --output drive_catalog_20251120.json \
  --cache
```

---

### 3. Living Document Template ⭐⭐
**Why Third**: Standardize how we create new entities  
**Complexity**: Low  
**Time Estimate**: 1 hour  
**Dependencies**: None (just file templates)

**Deliverable**: `templates/` directory with JSON schemas

**Templates to Create**:
1. `framework_template.json` - For theoretical frameworks
2. `conversation_pack_template.json` - For archived conversations
3. `entity_profile_template.json` - For document entities
4. `research_note_template.json` - For literature integration

**Each Template Contains**:
- Metadata structure (UUID, timestamps, creator)
- Content scaffolding (sections, fields)
- Cross-reference placeholders
- Version tracking structure
- Ka-signature fields

**Usage**:
```bash
./create_from_template.py \
  --template framework \
  --name "Pressure Dynamics Theory" \
  --creator "Navigator + Claude" \
  --output frameworks/
```

---

### 4. Symbol Search Tool ⭐
**Why Fourth**: Test our Unicode-based organization  
**Complexity**: Low  
**Time Estimate**: 30 minutes  
**Dependencies**: Drive access

**Deliverable**: `symbol_search.py`

**Key Features**:
- Search by single Unicode symbol (🐇)
- Search by multiple symbols (🐇 AND 🥼)
- List all documents with symbols
- Generate symbol → document mapping

**Command Structure**:
```bash
./symbol_search.py --symbol 🐇
./symbol_search.py --symbols 🐇,🥼 --operator AND
./symbol_search.py --list-all-symbols
```

---

## 🔨 NEXT TIER (This Week)

### 5. Simple Ka Analyzer
**Purpose**: Extract key patterns from conversation packs  
**Input**: JSON conversation file  
**Output**: List of recurring concepts, frameworks mentioned, key insights

```bash
./ka_analyzer.py --input α_pack.json --output α_ka_signatures.json
```

---

### 6. Cross-Reference Generator
**Purpose**: Automatically link related documents  
**Method**: Scan for UUID references, framework names, concept mentions  
**Output**: JSON graph of document relationships

```bash
./generate_cross_refs.py --scan ./frameworks/ --output ref_graph.json
```

---

### 7. Entity Health Checker
**Purpose**: Verify document structure integrity  
**Checks**: Required fields present, valid UUIDs, timestamp format, ka-signatures exist  
**Output**: Health report with warnings/errors

```bash
./entity_health.py --check ./frameworks/ --report health_report_20251120.txt
```

---

### 8. Archive Index Generator
**Purpose**: Create searchable index across all conversation packs  
**Features**: Full-text search, date range queries, ka-signature filtering

```bash
./index_archives.py \
  --scan ./conversation_packs/ \
  --output master_archive_index.json \
  --enable-search
```

---

## 🌐 DRIVE INTEGRATION TASKS

### A. Verify Access Method
**Need to determine**:
- Can we use `gcloud` commands?
- Is `rclone` configured?
- Do we need Drive API directly?
- What authentication is available?

**Test Commands**:
```bash
# Test 1: gcloud
gcloud drive files list --limit 5

# Test 2: rclone
rclone ls gdrive: --max-depth 1

# Test 3: Python gdrive library
python3 -c "from pydrive.auth import GoogleAuth; print('PyDrive available')"
```

---

### B. Folder Structure Discovery
**Once access verified**:
1. List top-level folders
2. Map folder hierarchy
3. Identify key locations (Archive, Active, Seeds)
4. Document folder IDs for scripts

---

### C. Sync Protocol Design
**Two-way sync considerations**:
- Local changes → Drive (push)
- Drive changes → Local (pull)
- Conflict resolution (timestamp-based)
- Version preservation

---

## 📦 FILE STRUCTURE PLANNING

```
/home/claude/
├── scripts/                    # All executable tools
│   ├── conversation_splitter_v2.py
│   ├── drive_lister.py
│   ├── symbol_search.py
│   ├── ka_analyzer.py
│   └── ...
├── templates/                  # Document templates
│   ├── framework_template.json
│   ├── conversation_pack_template.json
│   └── ...
├── conversation_packs/         # Split conversation archives
│   ├── α_20240101_20240215.json
│   ├── β_20240216_20240401.json
│   └── _MASTER_INDEX_2024.json
├── frameworks/                 # Living framework documents
│   ├── triadic_optimization_v1.json
│   ├── rzc_theory_v2.json
│   └── ...
├── entities/                   # Document entity profiles
│   ├── genesis_framework_entity.json
│   └── ...
├── catalogs/                   # Indexes and maps
│   ├── drive_catalog_20251120.json
│   ├── symbol_map.json
│   └── cross_reference_graph.json
└── cache/                      # Local caches
    ├── .drive_cache.json
    └── .search_index.json
```

---

## 🎯 THIS SESSION GOALS

**What We Should Build RIGHT NOW**:

1. **JSON Splitter** (if we have large conversation files to process)
2. **Drive Access Test** (verify what tools we have)
3. **Template Set** (so we can standardize new documents)

**Pick ONE to start with based on**:
- What's most urgent?
- What data do we have ready?
- What blocks other tasks?

---

## 💭 DECISION POINTS

**Question 1**: Do we have large conversation JSON files (10-16MB) ready to process?  
- YES → Build splitter first
- NO → Build templates and Drive tools first

**Question 2**: What's the Drive access situation?  
- Need to test terminal commands
- Determines Drive tool complexity

**Question 3**: What's the immediate use case?  
- Archiving conversations? → Splitter priority
- Organizing frameworks? → Templates priority  
- Discovering existing documents? → Drive lister priority

---

## 📝 BUILD LOG TEMPLATE

For each tool we build, document:

```markdown
# Tool: [Name]
**Built**: [Date/Time]
**Status**: ✅ Working / ⚠️ Partial / ❌ Needs Fix
**Location**: [File path]

## What It Does
[Brief description]

## How to Use
[Command examples]

## Testing Results
[What we tested, what worked, what didn't]

## Future Enhancements
[Ideas for v2.0]

## Related Tools
[What connects to this]
```

---

**Ready to build. What should we start with?** 🛠️

