#!/usr/bin/env python3
"""
Locate Tool - Report current position in primehaven topology

Usage:
    python locate.py              # Show current location
    python locate.py --full       # Show full topology
    python locate.py --json       # Output as JSON

Part of the sovereign concept toolkit.
Location: }primehaven{ / }pryme{ / today
"""

import argparse
import json

# Primehaven topology
TOPOLOGY = {
    "primehaven": {
        "notation": "}primehaven{",
        "type": "virtual_root",
        "status": "pre-activation",
        "children": ["maw", "pryme", "percolate", "runexusiam"]
    },
    "maw": {
        "notation": "}maw{",
        "type": "gravity_pool",
        "status": "pre-activation",
        "has_repo": True,
        "purpose": "Recycle cistern - collects before routing to ells"
    },
    "pryme": {
        "notation": "}pryme{",
        "type": "domos",
        "status": "pre-activation",
        "has_repo": True,
        "purpose": "AI perspective guardian for laptop",
        "children": ["today"]
    },
    "today": {
        "notation": "today",
        "type": "workspace",
        "status": "active",
        "has_repo": True,
        "purpose": "Development workspace - concepts incubate here",
        "current": True
    },
    "percolate": {
        "notation": "}percolate{",
        "type": "domos",
        "status": "pre-activation",
        "has_repo": False,
        "purpose": "Private workspace - ideas steep without sync"
    },
    "runexusiam": {
        "notation": "runexusiam",
        "type": "iteration",
        "status": "active",
        "has_repo": True,
        "purpose": "Current active iteration"
    }
}

CURRENT_PATH = "}primehaven{ / }pryme{ / today"


def show_location():
    """Show current location."""
    print(f"Location: {CURRENT_PATH}")
    print(f"Status: active workspace")
    print(f"Purpose: Development - concepts incubate here")


def show_topology():
    """Show full primehaven topology."""
    print("""
}primehaven{                    # Virtual root (laptop)
│
├── }maw{                       # Recycle gravity pool
│   └── [collects → routes to ells]
│   └── [will have repo]
│
├── }pryme{                     # AI perspective guardian
│   └── today/  ◄── YOU ARE HERE
│   └── [will have repo]
│
├── }percolate{                 # Private workspace
│   └── [no repo - ideas steep]
│
└── runexusiam/                 # Active iteration
    └── [has repo - operational]
""")


def show_json():
    """Output topology as JSON."""
    output = {
        "current_location": CURRENT_PATH,
        "topology": TOPOLOGY
    }
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Show location in primehaven topology")
    parser.add_argument("--full", action="store_true", help="Show full topology")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.json:
        show_json()
    elif args.full:
        show_topology()
    else:
        show_location()


if __name__ == "__main__":
    main()
