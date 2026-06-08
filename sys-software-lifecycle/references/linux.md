# Linux

## Managers

- Debian/Ubuntu install/update: `sudo apt update && sudo apt install <pkg>`; system update: `sudo apt update && sudo apt upgrade && sudo apt autoremove && sudo apt clean`.
- Debian/Ubuntu uninstall cleanly: `sudo apt purge <pkg> && sudo apt autoremove --purge && sudo apt clean`.
- Fedora/RHEL install/update: `sudo dnf install <pkg>`, `sudo dnf upgrade <pkg>`, `sudo dnf upgrade`.
- Fedora/RHEL uninstall cleanup: `sudo dnf remove <pkg> && sudo dnf autoremove && sudo dnf clean all`.
- Arch install/update: `sudo pacman -S <pkg>`, `sudo pacman -Syu`.
- Arch uninstall cleanup: `sudo pacman -Rns <pkg>`; orphan cleanup: `pacman -Qdtq | sudo pacman -Rns -` after reviewing the list.
- openSUSE install/update/remove: `sudo zypper install <pkg>`, `sudo zypper update <pkg>`, `sudo zypper remove --clean-deps <pkg>`.
- Flatpak install/update/remove: `flatpak install <remote> <app-id>`, `flatpak update`, `flatpak uninstall <app-id>`, `flatpak uninstall --unused`.
- Flatpak clean uninstall: use `flatpak uninstall --delete-data <app-id>` for uninstall requests unless the user asks to preserve app data.
- Snap install/update/remove: `sudo snap install <snap>`, `sudo snap refresh <snap>`, `sudo snap remove <snap>`.

## Common Leftover Locations

- User config: `~/.config/<app-or-vendor>`.
- User cache: `~/.cache/<app-or-vendor>`.
- User data: `~/.local/share/<app-or-vendor>`.
- User state: `~/.local/state/<app-or-vendor>`.
- Autostart entries: `~/.config/autostart`.
- User systemd units: `~/.config/systemd/user`, check with `systemctl --user list-unit-files`.
- System config: `/etc/<app-or-vendor>`.
- System data: `/var/lib/<app-or-vendor>`.
- System logs: `/var/log/<app-or-vendor>`.
- Systemd units: `/etc/systemd/system`, `/usr/lib/systemd/system`, `/lib/systemd/system`.
- Desktop entries: `~/.local/share/applications`, `/usr/share/applications`.
- Icons and MIME data: `~/.local/share/icons`, `/usr/share/icons`, `~/.local/share/mime`.
- Flatpak user data: `~/.var/app/<app-id>`.
- Flatpak system installs: `/var/lib/flatpak/app/<app-id>`.
- Snap user data: `~/snap/<snap>`.
- Snap packages and data: `/var/snap/<snap>`, `/snap/<snap>`.

## Discovery

1. Identify distro and package manager with `/etc/os-release` and available package commands.
2. Determine whether the software came from distro packages, Flatpak, Snap, AppImage, source build, vendor repo, or manual archive.
3. Inspect package ownership before deleting system files: `dpkg -S <path>`, `rpm -qf <path>`, or `pacman -Qo <path>`.
4. Check services with `systemctl list-unit-files | grep -i <name>` and user services with `systemctl --user list-unit-files | grep -i <name>`.
5. Search user leftovers by app name, vendor name, executable name, desktop ID, and Flatpak app ID.

## Cleanup Rules

- Use package-manager purge/remove commands before deleting files.
- Review dependency removals before confirming; do not remove large dependency sets unexpectedly.
- Delete matching user config/cache/data by default for uninstall requests unless the user asks to preserve app data or a safety stop applies.
- Prefer cache cleanup commands over manual deletion of package manager cache directories.
- Do not delete files owned by another installed package.
- Run `sudo systemctl daemon-reload` after removing system unit files, and `systemctl --user daemon-reload` after removing user units.
- For AppImage or manual archive installs, remove the app file, desktop entry, icon, update metadata, and matching user config/cache by default after presenting the paths.
