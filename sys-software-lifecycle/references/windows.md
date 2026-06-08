# Windows

## Managers

- WinGet search: `winget list <name>` and `winget search <name>`.
- WinGet install: `winget install --id <id> --exact`.
- WinGet update: `winget upgrade --id <id> --exact` or `winget upgrade --all` when requested.
- WinGet uninstall: `winget uninstall --id <id> --exact`; add `--scope user` or `--scope machine` when needed.
- WinGet portable cleanup: use `winget uninstall --id <id> --exact --purge` for portable packages when supported.
- Chocolatey install/update/uninstall: `choco install <pkg>`, `choco upgrade <pkg>`, `choco uninstall <pkg>`.
- Chocolatey dry-run: add `--noop` when supported by the command.
- Scoop install/update/uninstall/cleanup: `scoop install <app>`, `scoop update <app>`, `scoop uninstall <app>`, `scoop cleanup <app>`, `scoop cache rm <app>`.
- Microsoft Store apps may require Settings, PowerShell appx commands, or WinGet Store source handling.

## Common Leftover Locations

- Machine installs: `C:\Program Files\<AppOrVendor>`, `C:\Program Files (x86)\<AppOrVendor>`.
- Shared app data: `C:\ProgramData\<AppOrVendor>`.
- Roaming user data: `%APPDATA%\<AppOrVendor>`.
- Local user data: `%LOCALAPPDATA%\<AppOrVendor>`.
- LocalLow user data: `%USERPROFILE%\AppData\LocalLow\<AppOrVendor>`.
- Temp files: `%TEMP%`, `C:\Windows\Temp`.
- Start Menu shortcuts: `%APPDATA%\Microsoft\Windows\Start Menu\Programs`, `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`.
- Startup shortcuts: `shell:startup`, `shell:common startup`.
- Services: `services.msc`, PowerShell `Get-Service`, and `sc.exe query`.
- Scheduled tasks: Task Scheduler Library and PowerShell `Get-ScheduledTask`.
- Registry user keys: `HKCU:\Software\<VendorOrApp>`.
- Registry machine keys: `HKLM:\Software\<VendorOrApp>`, `HKLM:\Software\WOW6432Node\<VendorOrApp>`.
- Uninstall registry keys: `HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall`, `HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall`, `HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall`.

## Discovery

1. Identify exact package ID, display name, product code, vendor, install scope, and uninstall string.
2. Use `winget list`, Settings Apps, Chocolatey/Scoop lists, and uninstall registry keys to avoid ambiguous matches.
3. Check running processes before uninstalling: `Get-Process | Where-Object ProcessName -like '*<name>*'`.
4. Check services and scheduled tasks by both app name and vendor name.
5. Search common leftover paths after the native uninstaller completes.

## Cleanup Rules

- Always run the app's registered uninstaller before deleting folders.
- Delete matching app data, cache, logs, shortcuts, and startup entries by default after uninstall unless a safety stop applies.
- Back up registry keys before deleting them; registry cleanup remains high risk and requires explicit confirmation.
- Remove only registry keys clearly tied to the uninstalled app or vendor.
- Prefer disabling a suspicious service or startup entry before deleting it if ownership is unclear.
- Avoid deleting shared runtimes, drivers, `C:\Windows`, `System32`, `WinSxS`, browser profiles, and cloud-sync folders.
- Empty temp files only after uninstall is complete and the installer is not running.
- Reboot when services, drivers, shell extensions, VPN clients, antivirus, or locked files were involved.
