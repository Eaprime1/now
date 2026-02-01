#!/usr/bin/env python3
"""
Witness Tool - Format observations with tilde notation

Usage:
    python witness.py "observation"           # Simple witness
    python witness.py -d "observation"        # Double witness (confirmed)
    python witness.py -? "observation"        # Uncertain witness
    python witness.py -! "observation"        # Important witness
    python witness.py -t "observation"        # With timestamp

Part of the sovereign concept toolkit.
Location: }primehaven{ / }pryme{ / today
"""

import sys
import argparse
from datetime import datetime


def witness(observation, mode="simple", timestamp=False):
    """Format an observation with tilde notation."""

    markers = {
        "simple": ("~", "~"),
        "double": ("~~", "~~"),
        "uncertain": ("~?", "~"),
        "important": ("~!", "~"),
        "ongoing": ("~", "...~"),
        "flow_to": ("~>", ""),
        "flow_from": ("~<", ""),
    }

    prefix, suffix = markers.get(mode, ("~", "~"))

    if timestamp:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        return f"{prefix}{observation} [{ts}]{suffix}"
    else:
        return f"{prefix}{observation}{suffix}"


def main():
    parser = argparse.ArgumentParser(description="Format observations with tilde notation")
    parser.add_argument("observation", help="The observation to witness")
    parser.add_argument("-d", "--double", action="store_true", help="Double witness (confirmed)")
    parser.add_argument("-?", "--uncertain", dest="uncertain", action="store_true", help="Uncertain witness")
    parser.add_argument("-!", "--important", dest="important", action="store_true", help="Important witness")
    parser.add_argument("-o", "--ongoing", action="store_true", help="Ongoing observation")
    parser.add_argument("-t", "--timestamp", action="store_true", help="Add timestamp")

    args = parser.parse_args()

    # Determine mode
    if args.double:
        mode = "double"
    elif args.uncertain:
        mode = "uncertain"
    elif args.important:
        mode = "important"
    elif args.ongoing:
        mode = "ongoing"
    else:
        mode = "simple"

    result = witness(args.observation, mode, args.timestamp)
    print(result)


if __name__ == "__main__":
    main()
