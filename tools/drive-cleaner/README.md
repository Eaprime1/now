# Ubuntu Drive Cleaner

A layered, interactive bash script for reclaiming disk space on Ubuntu laptops.

## Quick Start

```bash
# 1. Make executable (once)
chmod +x clean.sh

# 2. See what's eating space — no changes
sudo ./clean.sh --mode report

# 3. Safe clean (prompts for each step)
sudo ./clean.sh

# 4. Safe clean, non-interactive (answer yes to all)
sudo ./clean.sh --all

# 5. Deep clean (more aggressive, still prompts)
sudo ./clean.sh --mode deep

# 6. Preview without doing anything
sudo ./clean.sh --dry-run --all
```

## Modes

| Mode | What it does |
|------|-------------|
| `report` | Disk usage summary only — zero changes |
| `safe` | APT cache, old kernels, snap revisions, journals, thumbnails |
| `deep` | Everything in safe + user app cache, crash reports, temp files, locales |

## What Gets Cleaned

### Safe Mode
| Step | Command/action | Risk |
|------|---------------|------|
| APT orphan packages | `apt autoremove` | None |
| APT package cache | `apt clean` | None — redownloadable |
| Old kernels | `apt purge linux-image-X.X.X` | None if one newer kernel exists |
| Snap disabled revisions | `snap remove --revision` | None |
| systemd journal logs | `journalctl --vacuum-time=7d` | Loses old logs |
| Thumbnail cache | `rm ~/.cache/thumbnails/*` | Thumbnails regenerate |

### Deep Mode (adds)
| Step | Action | Risk |
|------|--------|------|
| User app cache (`~/.cache`) | `rm -rf ~/.cache/*` | Apps may be slower until cache rebuilds |
| Crash reports (`/var/crash`) | `rm /var/crash/*` | Lose crash diagnostics |
| Old temp files | `find /tmp -mtime +7 -delete` | None for files unmodified 7+ days |
| Unused locales | `localepurge` | Locale data for other languages removed |

## Config

Edit `config.sh` to adjust defaults (e.g. journal retention period).

## Log

Each run appends to `clean.log` in the same directory.

## Chain of Custody

```
now repo (origin)
  └── clone to Ubuntu laptop
        └── tools/drive-cleaner/
              └── clean.sh  ← run here
```

File it wherever makes sense — `/usr/local/bin/`, `~/bin/`, or run in place.

## Safety Notes

- Always run `--mode report` first to understand what's there
- `--dry-run` shows every command without executing
- Old kernel removal preserves the currently running kernel
- This tool does **not** do secure wipe / shred — that's a separate operation for decommissioning hardware
