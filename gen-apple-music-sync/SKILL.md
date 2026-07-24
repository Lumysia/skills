---
name: gen-apple-music-sync
description: Install and operate gamdl with wrapper-v2 for Apple Music ALAC and Dolby Atmos libraries, create playlist snapshots, run full or incremental synchronization, verify media, build credential-free support bundles, and organize output for Plex or Jellyfin. Use for first-time setup, playlist migration, repeat synchronization, codec validation, or portable recovery packaging.
compatibility: Requires an active Apple Music subscription, a user-supplied compatible Apple Music Android APK/APKM, Docker, Python 3, and sufficient storage. ALAC and Atmos availability depends on the catalog.
---

# Apple Music Library Sync

## Startup

Infer the user's language. Identify the OS, CPU architecture, package manager, playlist URLs, output roots, requested codecs, and whether the run is full or incremental. Read `references/workflow.md`, `references/security.md`, and `references/media-layout.md` before writing files.

## Flow

1. Discover current official gamdl and wrapper-v2 releases; keep their API versions compatible.
2. Install gamdl, MediaInfo, Docker, and wrapper build dependencies through the host's managed source.
3. Obtain the user-supplied APK/APKM, select the matching wrapper architecture, extract Apple libraries, stage Android system files, and pass all pinned hash checks.
4. Build and start wrapper-v2 with persistent runtime state outside any support bundle. Authenticate interactively without logging credentials or tokens.
5. Create separate ALAC and Atmos configs, databases, temp paths, and media roots. Keep overwrite disabled.
6. Fetch the live Apple Music playlist first and capture an ordered catalog-ID snapshot before inspecting the old snapshot as the incremental baseline.
7. For a first run, download the playlist once per codec. For later runs, compare the live snapshot with the previous snapshot by stable catalog ID, download additions, apply removals, then rebuild playlists. Keep diff artifacts in a runtime temp directory and remove them after success unless the user asks to retain them.
8. Verify every output with MediaInfo, database/path consistency, lyrics pairing, cover presence, and wrapper health.
9. Expose ALAC and Atmos as separate Plex/Jellyfin music libraries using the layout in `references/media-layout.md`.
10. Build a credential-free support bundle containing only non-reproducible inputs, the latest snapshot, exact dependency references, and checksums.

For incremental runs, report playlist additions and removals separately from each codec's actual downloads, skips, and deletions.

Use `references/workflow.md` for commands and decision rules. Use `references/security.md` as a mandatory packaging gate.
