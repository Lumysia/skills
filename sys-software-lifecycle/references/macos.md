# macOS

## Managers

- Homebrew formula install: `brew install <formula>`.
- Homebrew cask install: `brew install --cask <cask>`.
- Homebrew update chain: `brew update && brew upgrade && brew autoremove && brew cleanup -s`.
- Homebrew formula uninstall: `brew uninstall <formula> && brew autoremove && brew cleanup -s`.
- Homebrew cask clean uninstall: `brew uninstall --zap <cask> && brew autoremove && brew cleanup -s`.
- Homebrew dry-run checks: `brew info <name>`, `brew uses --installed <formula>`, `brew autoremove --dry-run`, `brew cleanup --dry-run`.
- Mac App Store apps are normally removed through Finder, Launchpad, or `mas` if the user already uses it.
- Vendor `.pkg` installers may need vendor uninstallers, package receipts, launch daemon cleanup, and reboot checks.

## Common Leftover Locations

- App bundles: `/Applications`, `~/Applications`.
- User data: `~/Library/Application Support/<app-or-vendor>`.
- Preferences: `~/Library/Preferences/<bundle-id>.plist`.
- Caches: `~/Library/Caches/<app-or-bundle-id>`.
- Containers: `~/Library/Containers/<bundle-id>`.
- Group containers: `~/Library/Group Containers/<team-or-bundle-id>`.
- Logs: `~/Library/Logs/<app-or-vendor>`.
- Saved state: `~/Library/Saved Application State/<bundle-id>.savedState`.
- HTTP/WebKit storage: `~/Library/HTTPStorages`, `~/Library/WebKit`.
- User launch agents: `~/Library/LaunchAgents/<bundle-id>.plist`.
- System app support: `/Library/Application Support/<app-or-vendor>`.
- System caches and logs: `/Library/Caches`, `/Library/Logs`.
- System launch items: `/Library/LaunchAgents`, `/Library/LaunchDaemons`.
- Package receipts: `/private/var/db/receipts`, query with `pkgutil --pkgs | grep -i <name>`.
- Crash reports: `~/Library/Logs/DiagnosticReports`, `/Library/Logs/DiagnosticReports`.

## Discovery

1. Resolve cask token and bundle ID with `brew info --cask <name>`, `mdls -name kMDItemCFBundleIdentifier /Applications/<App>.app`, or app `Info.plist`.
2. Read Homebrew cask `zap` stanza when available; treat it as software-specific cleanup guidance, not an automatic delete list.
3. Check services with `brew services list`, `launchctl list | grep -i <name>`, and matching plist paths.
4. Search common locations by app name, vendor name, cask token, and bundle ID.

## Cleanup Rules

- Prefer `brew uninstall --zap` for casks installed by Homebrew, but warn that `--zap` can remove shared files.
- Stop Homebrew services before uninstalling: `brew services stop <formula>`.
- Use `brew services cleanup` after removing Homebrew-managed services.
- Move manual leftovers to Trash when possible instead of using `rm -rf` directly.
- Do not delete `/Library` items without admin confirmation and a clear app/vendor match.
- Do not delete package receipts unless the package is fully removed and receipts are confirmed stale.
