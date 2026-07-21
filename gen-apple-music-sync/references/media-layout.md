# Media Layout

Use separate library roots for codec variants:

```text
Media/
├── Music-ALAC/
│   └── Album Artist/Album/Disc-Track Title.m4a
└── Music-Atmos/
    └── Album Artist/Album/Disc-Track Title.m4a
```

Register each root as a separate music library. Do not use movie edition or multi-version suffix rules for music.

Requirements:

- One album per directory.
- Use embedded album artist, album, disc, track, title, date, and compilation tags.
- Keep all discs in one album directory; disc-prefixed filenames are acceptable.
- Name external lyrics exactly like the audio file, with `.lrc`, `.elrc`, or `.txt` as supported.
- Store album art as `cover.jpg` or embed it in each track.
- Keep compilations grouped consistently; embedded album-artist and compilation tags take precedence.
- Keep playlists under `Playlists/` with paths relative to the playlist file.

Sources:

- Jellyfin music: https://jellyfin.org/docs/general/server/media/music/
- Plex music folders: https://support.plex.tv/articles/200265296-adding-music-media-from-folders/
