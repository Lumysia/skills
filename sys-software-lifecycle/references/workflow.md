# Workflow

## Principles

- Prefer the exact manager, installer, app store, or vendor uninstaller that installed the software.
- For installs and updates, compare package managers, official downloads, app stores, source repositories, and release feeds before choosing a source.
- Search for software-specific uninstall and cleanup notes before using generic leftovers.
- Separate app removal from user-data removal; ask before deleting settings, credentials, saves, profiles, or license data.
- Treat registry edits, services, drivers, launch daemons, kernel extensions, and system directories as high risk.
- Prefer dry-run, list, search, info, preview, or what-if commands before write operations.
- Treat platform references as common patterns, not exhaustive policy; adapt to the detected OS, distribution, package manager, installer, and software vendor.
- Prefer moving leftovers to Trash, Recycle Bin, quarantine, or a timestamped backup over permanent deletion when feasible.

## Discovery

1. Detect OS and version.
2. Identify install source: native package manager, app store, vendor installer, portable archive, source build, containerized package, managed endpoint tooling, or unknown.
3. Resolve the exact package identifier, cask token, bundle ID, product code, app ID, service name, or executable path.
4. Compare available versions across trusted sources and prefer the newest stable compatible source unless the user requests a channel, version, or manager.
5. Search official docs, package metadata, and common issue reports for software-specific cleanup paths.
6. Find active processes, services, startup items, scheduled jobs, agents, daemons, and open files before uninstalling.

## Install

1. Prefer the newest stable compatible package from a trusted source with update and uninstall support.
2. Verify source trust, package name, architecture, requested version, and release channel.
3. Explain why the selected source beats alternatives such as package manager, official site, app store, or GitHub release.
4. Preview dependencies and post-install services.
5. Install with the selected source's current command or installer path.
6. Verify executable path, version, service status, and manager registration.
7. Run manager cleanup only when it will not remove newly needed artifacts.

## Update

1. Check whether the app self-updates or should be updated by the package manager, app store, vendor installer, or release feed.
2. Snapshot current version and config locations when rollback matters.
3. Compare available versions, then upgrade from the newest stable compatible trusted source.
4. Run dependency and cache cleanup appropriate to the manager.
5. Verify the new version and note any restart or logout requirement.

## Uninstall

1. Stop the app and related services cleanly.
2. Run the native uninstaller or package-manager remove command.
3. Run dependency cleanup and package cache cleanup.
4. Search software-specific leftover paths from docs and package metadata.
5. Search generic platform leftover locations for app name, vendor name, bundle ID, product code, service name, and executable name.
6. Present candidate leftovers with risk level before deletion.
7. Remove confirmed leftovers, then verify no package, service, startup item, or process remains.

## Cleanup Output

- Show commands grouped by lifecycle actions, leftover discovery, and confirmed cleanup.
- Mark destructive commands clearly.
- Include exact paths before deleting anything.
- State what was preserved, removed, skipped, and still needs manual review.

## Safety Stops

- Stop before deleting credentials, browser profiles, game saves, cloud-sync data, databases, or shared runtimes.
- Stop before editing Windows Registry without a backup plan.
- Stop before removing Linux packages that would remove desktop environments, kernels, shells, package managers, or large dependency sets unexpectedly.
- Stop before using broad wildcards in system paths.
