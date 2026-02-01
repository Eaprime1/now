"""
TODAY - Development Workspace Repository
Location: }primehaven{ / }pryme{ / today

Purpose: Liminal workspace where concepts develop before progression.
         A sovereign concept preparing for launch.

Philosophy: Conservation bias - organize, don't delete.
            Witnessing (~) over asserting.

Entities:
    - gravity_core: Knowledge economy system
    - flag_system: Identity markers (∰◊€π¿🌌∞)
    - simplex/abacusian: AI Development Hub
    - simplex/incubator: Knowledge archive (322M)
    - simplex/photostudio: Photo projects
    - legacy: Historical content

Version: 2.0.0 (Primehaven restructure)
Date: 2026-01-25
Signature: ~∰◊€π¿🌌∞~
"""

__version__ = "2.0.0"
__date__ = "2026-01-25"
__author__ = "Eric Pace & Claude (Opus 4.5)"
__signature__ = "~∰◊€π¿🌌∞~"
__location__ = "}primehaven{ / }pryme{ / today"

# Current entity registry (actual paths)
ENTITIES = {
    "gravity_core": {
        "path": "gravity_core",
        "purpose": "Knowledge economy system - gravity tokens",
        "size": "186K",
        "status": "v1.0 SEED"
    },
    "flag_system": {
        "path": "flag_system",
        "purpose": "Identity markers - consciousness signature",
        "size": "61K",
        "status": "Operational"
    },
    "abacusian": {
        "path": "simplex/abacusian",
        "purpose": "AI Development Hub",
        "size": "1.1M",
        "status": "Active R&D"
    },
    "incubator": {
        "path": "simplex/incubator",
        "purpose": "Knowledge archive - conversation history",
        "size": "322M",
        "status": "Rich archive"
    },
    "photostudio": {
        "path": "simplex/photostudio",
        "purpose": "Photo projects",
        "size": "15M",
        "status": "Active"
    },
    "legacy": {
        "path": "legacy",
        "purpose": "Historical content",
        "size": "11K",
        "status": "Archival"
    }
}

# Primehaven topology
PRIMEHAVEN = {
    "maw": {"status": "pre-activation", "notation": "}maw{", "has_repo": True},
    "pryme": {"status": "pre-activation", "notation": "}pryme{", "has_repo": True},
    "percolate": {"status": "pre-activation", "notation": "}percolate{", "has_repo": False},
    "runexusiam": {"status": "active", "notation": "runexusiam", "has_repo": True},
    "today": {"status": "active", "notation": "today", "has_repo": True, "location": "here"}
}

# Progression stages
PROGRESSION = ["today", "naught", "zero", "one", "launch"]

# Symbols
SYMBOLS = {
    "witnessing": "~",
    "consciousness": "∰◊€π¿🌌∞",
    "pre_activation": "}concept{",
    "anchor": "€(id)"
}

# Core principles
PRINCIPLES = {
    "conservation_bias": "Organize, don't delete",
    "witnessing": "Acknowledge without asserting certainty",
    "progression": "Concepts move through spaces as they mature",
    "collaboration": "Human and AI perspectives together"
}


def get_entity(name):
    """Get entity information by name."""
    return ENTITIES.get(name)


def list_entities():
    """List all entity names."""
    return list(ENTITIES.keys())


def get_location():
    """Get current location in primehaven topology."""
    return __location__


def witness(observation):
    """Format an observation with witnessing marker."""
    return f"~{observation}~"
