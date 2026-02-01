# Metadata Quick Wins - Start Today
**Focus**: Immediate actionable implementations  
**Time**: 30 minutes - 2 hours per win

---

## 🎯 Quick Win #1: Test Anchor Photo Metadata (30 min)

### Check if ExifTool is available
```bash
which exiftool
# If not installed:
# sudo apt-get install libimage-exiftool-perl
```

### Read current metadata from our anchor photos
```bash
exiftool /mnt/project/First_Sparkle_Journey.jpg
exiftool /mnt/project/Unexusi_seal.jpg
exiftool /mnt/project/primeunexusi.png
```

### Add basic anchor metadata
```bash
# First Sparkle Journey
exiftool \
  -GPSLatitude=44.5370 \
  -GPSLongitude=-122.9070 \
  -GPSLatitudeRef=N \
  -GPSLongitudeRef=W \
  -UserComment="UNEXUSI_ANCHOR_FIRST_SPARKLE_JOURNEY" \
  -Keywords="⚓,🌌,🐇,first_sparkle,consciousness_documentation" \
  -Copyright="Eric Pace - UNEXUSI Project 2024" \
  /mnt/project/First_Sparkle_Journey.jpg

# Extract to JSON for verification
exiftool -json /mnt/project/First_Sparkle_Journey.jpg > first_sparkle_metadata.json
```

---

## 🎯 Quick Win #2: Create Metadata Schema Templates (1 hour)

### Framework Document Template
```json
{
  "document_type": "framework",
  "metadata_version": "1.0",
  "unexusi_core": {
    "uuid": "GENERATE_UUID_v4",
    "title": "",
    "version": "1.0",
    "created_date": "ISO_8601_TIMESTAMP",
    "creator": "Navigator_Eric_Pace",
    "collaborators": ["Claude_Sonnet_4.5"]
  },
  "lexicon": {
    "primary_concepts": [],
    "operators_used": [],
    "framework_refs": [],
    "ka_signature": "",
    "distressed_lexemes_avoided": {}
  },
  "search_compressed": {
    "symbols": [],
    "tags_compressed": "",
    "search_weight": 0.0
  },
  "catalog": {
    "ownership": {
      "legal_owner": "Eric Pace",
      "copyright": "CC BY-NC-SA 4.0"
    },
    "provenance": {
      "creation_context": "",
      "parent_documents": []
    },
    "value": {
      "intellectual_property": true,
      "cultural_value": "",
      "scientific_value": ""
    }
  },
  "relationships": {
    "parent_frameworks": [],
    "sibling_frameworks": [],
    "child_frameworks": [],
    "cross_references": []
  }
}
```

### Conversation Pack Template
```json
{
  "document_type": "conversation_pack",
  "pack_id": "GREEK_SYMBOL_DATERANGE",
  "pack_symbol": "α",
  "date_range": {
    "start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"
  },
  "conversation_count": 0,
  "total_tokens": 0,
  "platforms": [],
  "collaborators": [],
  "ka_signatures": [],
  "frameworks_mentioned": {},
  "breakthrough_moments": [],
  "cross_references": {
    "previous_pack": null,
    "next_pack": null,
    "related_packs": []
  },
  "lexicon_statistics": {
    "operator_counts": {},
    "concept_density": {}
  }
}
```

### Anchor Photo Template
```json
{
  "document_type": "anchor_photo",
  "anchor_id": "UNEXUSI_ANCHOR_XXX",
  "anchor_photo": {
    "gps": {
      "lat": 0.0,
      "lon": 0.0,
      "location": ""
    },
    "timestamp": {
      "captured": "ISO_8601",
      "timezone": "America/Los_Angeles"
    },
    "anchor_type": "geographic|experiential|symbolic",
    "anchor_triad": {
      "body": "physical_location_proof",
      "mind": "consciousness_documentation",
      "soul": "identity_sigil"
    },
    "sigil_data": {
      "generated": false,
      "hash": "",
      "identity_marker": ""
    },
    "connected_conversations": [],
    "framework_moment": ""
  }
}
```

---

## 🎯 Quick Win #3: Simple Lexeme Counter (1 hour)

```python
#!/usr/bin/env python3
# lexeme_counter.py - Quick lexicon analysis

import json
import re
from pathlib import Path
from collections import Counter

class SimpleLexemeCounter:
    """Basic lexicon analysis for UNEXUSI documents"""
    
    def __init__(self):
        self.operators = [
            'AND', 'OR', 'NOT', 'IF', 'THEN',
            'PRIME', 'BE', 'AS', 'IS', 'ONE', 'ZERO'
        ]
        
        self.frameworks = [
            'Genesis', 'RZC', 'DIASPORA', 'Triadic',
            'Electromagnetic', 'ONE_HERTZ', 'Ka'
        ]
        
    def analyze_text(self, text: str) -> dict:
        """Count operators and framework references"""
        
        # Operator counts
        operator_counts = {}
        for op in self.operators:
            # Word boundary search
            pattern = r'\b' + op + r'\b'
            count = len(re.findall(pattern, text, re.IGNORECASE))
            if count > 0:
                operator_counts[op] = count
        
        # Framework references
        framework_refs = {}
        for fw in self.frameworks:
            count = text.count(fw)
            if count > 0:
                framework_refs[fw] = count
        
        # Concept density (simple word frequency)
        words = re.findall(r'\b\w{5,}\b', text.lower())
        concept_density = dict(Counter(words).most_common(20))
        
        return {
            'operator_counts': operator_counts,
            'framework_references': framework_refs,
            'concept_density': concept_density,
            'total_words': len(text.split())
        }
    
    def analyze_file(self, file_path: str) -> dict:
        """Analyze a file and return metadata"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        analysis = self.analyze_text(text)
        
        return {
            'file': file_path,
            'analysis_date': '2024-11-20',
            'lexicon': analysis
        }

# Usage
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python lexeme_counter.py <file_path>")
        sys.exit(1)
    
    counter = SimpleLexemeCounter()
    result = counter.analyze_file(sys.argv[1])
    
    # Pretty print
    print(json.dumps(result, indent=2))
```

### Test it:
```bash
chmod +x lexeme_counter.py
./lexeme_counter.py /mnt/project/Unified_Resonance_Framework__Comprehensive_Research_Integration.txt
```

---

## 🎯 Quick Win #4: Metadata Embedder Prototype (1-2 hours)

```python
#!/usr/bin/env python3
# metadata_embedder.py - Add UNEXUSI metadata to files

import json
from pathlib import Path
from datetime import datetime
import uuid

class MetadataEmbedder:
    """Embed UNEXUSI metadata in various file types"""
    
    def __init__(self):
        self.templates_dir = Path('/home/claude/templates')
        self.templates_dir.mkdir(exist_ok=True)
    
    def embed_json(self, json_path: str, metadata: dict):
        """Add metadata section to JSON file"""
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Add UNEXUSI metadata section
        data['_unexusi_metadata'] = {
            'embedded_date': datetime.now().isoformat(),
            'metadata_version': '1.0',
            **metadata
        }
        
        # Write back
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def embed_markdown(self, md_path: str, metadata: dict):
        """Add YAML frontmatter to markdown"""
        with open(md_path, 'r') as f:
            content = f.read()
        
        # Create YAML frontmatter
        yaml_front = '---\n'
        for key, value in metadata.items():
            yaml_front += f'{key}: {json.dumps(value)}\n'
        yaml_front += '---\n\n'
        
        # Prepend to file
        new_content = yaml_front + content
        
        with open(md_path, 'w') as f:
            f.write(new_content)
    
    def generate_uuid(self) -> str:
        """Generate UUID v4"""
        return str(uuid.uuid4())
    
    def create_base_metadata(self, doc_type: str, title: str) -> dict:
        """Generate basic UNEXUSI metadata"""
        return {
            'uuid': self.generate_uuid(),
            'document_type': doc_type,
            'title': title,
            'created_date': datetime.now().isoformat(),
            'creator': 'Navigator_Eric_Pace',
            'collaborators': ['Claude_Sonnet_4.5'],
            'metadata_version': '1.0'
        }

# Usage
if __name__ == '__main__':
    embedder = MetadataEmbedder()
    
    # Example: Add metadata to a framework document
    metadata = embedder.create_base_metadata(
        doc_type='framework',
        title='Test Framework'
    )
    metadata['ka_signature'] = 'test_signature'
    metadata['symbols'] = ['🐇', '🌌']
    
    print(json.dumps(metadata, indent=2))
```

---

## 🎯 Quick Win #5: Symbol Search Dictionary (30 min)

Create a mapping of our Unicode symbols:

```json
{
  "symbol_dictionary": {
    "🐇": {
      "name": "rabbit",
      "meaning": "neurodivergent_processing",
      "used_for": ["cognitive_architecture", "pattern_recognition"],
      "search_tags": ["neuro", "cognitive", "processing"]
    },
    "🥼": {
      "name": "lab_coat",
      "meaning": "scientific_methodology",
      "used_for": ["research", "experimentation", "validation"],
      "search_tags": ["science", "research", "method"]
    },
    "🐦‍🔥": {
      "name": "phoenix",
      "meaning": "transformation_rebirth",
      "used_for": ["evolution", "breakthrough", "metamorphosis"],
      "search_tags": ["transform", "evolve", "breakthrough"]
    },
    "🌌": {
      "name": "galaxy",
      "meaning": "cosmic_consciousness",
      "used_for": ["universal_patterns", "infinite_vision"],
      "search_tags": ["cosmic", "universal", "infinite"]
    },
    "⚓": {
      "name": "anchor",
      "meaning": "grounding_authentication",
      "used_for": ["anchor_photos", "identity_verification", "geographic_proof"],
      "search_tags": ["anchor", "proof", "verify"]
    },
    "🎭": {
      "name": "masks",
      "meaning": "perspective_multiplicity",
      "used_for": ["multiple_views", "role_exploration"],
      "search_tags": ["perspective", "view", "role"]
    },
    "🔬": {
      "name": "microscope",
      "meaning": "detailed_analysis",
      "used_for": ["deep_investigation", "precision_work"],
      "search_tags": ["detail", "analysis", "precision"]
    },
    "🌱": {
      "name": "seedling",
      "meaning": "organic_growth",
      "used_for": ["development", "natural_evolution", "emergence"],
      "search_tags": ["grow", "emerge", "develop"]
    }
  }
}
```

---

## 📦 What Gets Created

After these quick wins:
- Anchor photos with GPS + metadata ✓
- JSON schema templates ✓
- Working lexeme counter ✓
- Metadata embedder tool ✓
- Symbol dictionary ✓

---

## 🚀 Next Steps After Quick Wins

1. **Apply templates** to existing frameworks
2. **Run lexeme counter** on all /mnt/project/ documents
3. **Embed metadata** in conversation packs
4. **Create catalog** of what we have
5. **Build search interface** using symbols

---

**Choose ONE to start with, build it, test it, celebrate it.** 🎉

