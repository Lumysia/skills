# Security Gate

Never package or print:

- cookies or browser exports
- Apple IDs, usernames, passwords, app-specific passwords, or 2FA codes
- wrapper `data/`, `mpl_db`, token snapshots, device state, or account databases
- `.env` files from a live installation
- gamdl SQLite databases from a live installation
- logs or shell histories containing authentication requests

Exclude every reproducible file. Search archive paths and extracted text for `cookie`, `token`, `password`, `username`, `apple_id`, `mpl_db`, `.env`, and known credential filenames. Inspect any match manually. Verify the archive from a clean extraction directory.

Treat the user-supplied APK/APKM and extracted libraries as private licensed material. Do not publish or upload the bundle without the user's authorization.
