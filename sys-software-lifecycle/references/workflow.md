# Workflow

## Principles

- Prefer the exact manager, installer, app store, or vendor uninstaller that installed the software.
- For installs and targeted updates, compare package managers, official downloads, app stores, source repositories, and release feeds before choosing a source.
- Search for software-specific uninstall and cleanup notes before using generic leftovers.
- Separate app removal from user-data removal; ask before deleting settings, credentials, saves, profiles, or license data.
- Treat registry edits, services, drivers, launch daemons, kernel extensions, and system directories as high risk.
- Prefer dry-run, list, search, info, preview, or what-if commands before write operations.
- When a confirmed operation needs elevation, use the platform's standard authorization flow to continue instead of stopping at non-interactive `sudo`; limit elevated commands to the exact verified paths or manager actions.
- Treat platform references as common patterns, not exhaustive policy; adapt to the detected OS, distribution, package manager, installer, and software vendor.
- Prefer moving leftovers to Trash, Recycle Bin, quarantine, or a timestamped backup over permanent deletion when feasible.

## Discovery

1. Detect OS and version.
2. Identify operation scope: global package-manager update/upgrade, targeted software lifecycle action, or unknown.
3. If an update or upgrade request does not name specific software, choose global scope and do not ask for a software identifier.
4. Identify install source: native package manager, app store, vendor installer, portable archive, source build, containerized package, managed endpoint tooling, or unknown.
5. For targeted actions, resolve the exact package identifier, cask token, bundle ID, product code, app ID, service name, or executable path.
6. Compare available versions across trusted sources and prefer the newest stable compatible source unless the user requests a channel, version, or manager.
7. For targeted actions, search official docs, package metadata, and common issue reports for software-specific cleanup paths.
8. Find active processes, services, startup items, scheduled jobs, agents, daemons, and open files before uninstalling.

## Install

1. Prefer the newest stable compatible package from a trusted source with update and uninstall support.
2. Verify source trust, package name, architecture, requested version, and release channel.
3. Explain why the selected source beats alternatives such as package manager, official site, app store, or GitHub release.
4. Preview dependencies and post-install services.
5. Install with the selected source's current command or installer path.
6. Verify executable path, version, service status, and manager registration.
7. Run manager cleanup only when it will not remove newly needed artifacts.

## Update

1. For global scope, list candidate package managers and outdated packages, then present one confirmation covering metadata refresh, upgrades, autoremove, cache cleanup, logging, and verification.
2. For targeted scope, check whether the app self-updates or should be updated by the package manager, app store, vendor installer, or release feed.
3. Snapshot current version and config locations when rollback matters.
4. Compare available versions, then upgrade from the newest stable compatible trusted source.
5. If the manager fails only because it cannot prompt for elevation, retry with the platform authorization mechanism for the specific privileged cleanup or service action, then rerun the manager command as the normal user.
6. Run dependency and cache cleanup appropriate to the manager.
7. Verify the new version or global outdated status and note any restart or logout requirement.

## Uninstall

1. Stop the app and related services cleanly.
2. Run the native uninstaller or package-manager remove command.
3. If removal needs elevation, use the platform authorization mechanism for the exact privileged uninstall, service, or known package path instead of asking the user to run it manually.
4. Run dependency cleanup and package cache cleanup.
5. Search software-specific leftover paths from docs and package metadata.
6. Search generic platform leftover locations for app name, vendor name, bundle ID, product code, service name, and executable name.
7. Present candidate leftovers with risk level before deletion.
8. Remove confirmed leftovers, then verify no package, service, startup item, or process remains.

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
