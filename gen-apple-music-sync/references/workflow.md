# Workflow

## 1. Discover

Record OS, architecture, package manager, Docker architecture, free space, playlist URLs, and target roots. Resolve current gamdl and wrapper-v2 releases from official sources. Confirm wrapper API compatibility before installation.

Map host architecture to the APK ABI and wrapper target: `arm64` or `aarch64` to `arm64-v8a`; `x86_64` or `amd64` to `x86_64`.

## 2. Install

Prefer the system package manager. Otherwise use an isolated Python installer for gamdl. Install MediaInfo and Docker from official managed sources. Verify versions and executable paths.

Clone the compatible wrapper-v2 release at an exact tag. Obtain the user-supplied Apple Music Android APK/APKM version required by that release. Run wrapper-provided extraction and staging scripts. Stop unless every pinned digest passes.

## 3. Configure Wrapper

Create a private `.env` from `.env.example` with the target architecture, Docker platforms, host ports, and session restore. Do not place account values in `.env`.

Build and start with Docker Compose. Verify `/health` and `/me`: version compatibility, loader readiness, playback readiness, and authentication state. Parse responses locally and print only required status fields; never print complete `/me` responses or token-bearing fields. Complete login and 2FA interactively. Persist runtime state in the wrapper data volume.

## 4. Configure Libraries

Create one config and SQLite database per codec. Required settings:

```ini
use_wrapper = true
song_codec_piority = alac
overwrite = false
save_cover = true
save_playlist = true
synced_lyrics_format = lrc
album_folder_template = {album_artist}/{album}
compilation_folder_template = Compilations/{album}
single_disc_file_template = {track:02d} {title}
multi_disc_file_template = {disc}-{track:02d} {title}
```

Use `song_codec_piority = atmos` for the Atmos config. Use separate output roots such as `Music-ALAC` and `Music-Atmos`. Set private directories to mode `700` and configs/databases to `600` where supported.

## 5. Snapshot

Capture the live public playlist page before each run. This is the first playlist-state operation in an incremental run: do not read or present the old snapshot as though it describes the current Apple Music playlist. Parse the page's `serialized-server-data` JSON and select the track list whose ID matches the playlist ID from the URL.

Write a JSON snapshot containing schema version, playlist ID, URL, title, capture time, declared track count, and ordered tracks. Each track must contain contiguous one-based position, string catalog ID, title, artist, album, album ID, duration, explicit flag, and canonical song URL.

Validate declared count, unique non-empty IDs, contiguous positions, and non-empty URLs before accepting the snapshot.

## 6. Full Sync

Run each playlist URL once per codec config:

```bash
gamdl --config-path ALAC_CONFIG PLAYLIST_URL
gamdl --config-path ATMOS_CONFIG PLAYLIST_URL
```

Database registration and `overwrite=false` prevent repeated replacement. Catalog items without the requested codec are expected omissions.

## 7. Incremental Sync

After the live snapshot has been captured and validated, load the previous snapshot only as the comparison baseline. Reject comparisons with different schema versions or playlist IDs.

Build previous and current maps by catalog ID:

- Added: IDs present only in current, preserving current order.
- Removed: IDs present only in previous, preserving previous order.
- Reordered: compare the previous and current sequences after filtering both to common IDs. Report an ID as moved only when its index within the common-ID sequence changes. Additions and removals alone must not create move records.
- Common count: size of the ID intersection.

Write `current.json`, `diff.json`, `added-urls.txt`, and `removed-ids.txt` under a per-run system temporary directory outside the media library. An empty change set must overwrite stale run files with empty files. Do not create or retain a `changes/` directory under the target music or snapshot directory unless the user explicitly requests audit artifacts.

Download additions only:

```bash
gamdl --config-path ALAC_CONFIG --read-urls-as-txt RUNTIME_DIR/added-urls.txt
gamdl --config-path ATMOS_CONFIG --read-urls-as-txt RUNTIME_DIR/added-urls.txt
```

For each codec library, resolve only removed IDs through that library's SQLite `media` table. Require every resolved path to remain inside the configured library root. Delete the audio file and same-basename lyric sidecars, then delete the matching database rows in one transaction.

Rebuild the M3U in current snapshot order by joining current catalog IDs to existing database paths. Use paths relative to the M3U directory. Skip catalog items unavailable in that codec and report their IDs.

Repeat for every codec. Promote `current.json` to `previous.json` only after all libraries pass verification. Optionally retain the promoted dated snapshot, then remove the per-run temporary directory.

Report two distinct result layers:

- Playlist diff: titles and counts added, removed, and reordered between previous and live snapshots.
- Codec execution: files actually downloaded, skipped as unavailable, and deleted for each codec. Do not describe a playlist addition as an Atmos addition when Atmos was unavailable.

## 8. Verify

Confirm wrapper health without printing token-bearing fields. Compare database rows with existing paths. Run MediaInfo over every audio file.

ALAC acceptance: `Format=ALAC`; record bit-depth and sample-rate distribution.

Atmos acceptance: `Format=E-AC-3`, `Format_AdditionalFeatures=JOC`; record sample rate, channel count, dynamic objects, and commercial name.

Confirm each M3U non-empty entry resolves, each external lyric file shares the audio basename, and each album has embedded or external cover art.

## 9. Support Bundle

Include only the user-supplied APK/APKM, current snapshot, exact dependency versions and official source URLs, and checksums. Do not include cloneable source, extracted libraries, configs, reports, tools, media, or this skill. Apply `references/security.md` before archiving.

Write a manifest with versions, architecture, source URLs, checksums, expected media roots, and restore commands. Create a ZIP or tar archive supported by the host. List and scan the final archive before delivery.
