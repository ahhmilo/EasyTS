[![Windows](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows11&logoColor=white&labelColor=555555)](#)
[![Python](https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white&labelColor=555555)](#)
[![HTML](https://img.shields.io/badge/language-HTML-E34F26?logo=html5&logoColor=white&labelColor=555555)](#)
[![License](https://img.shields.io/badge/license-Proprietary-red)](#)

<p align="center">
  <img src="assets/EasyTS_logo.png" width="160" alt="EasyTS logo">
</p>

# EasyTS

A lightweight Windows utility for applying VALORANT True Stretch resolutions without manually editing `GameUserSettings.ini`.

EasyTS automatically finds the correct Riot account config and applies custom stretched resolutions like `1440x1080`, `1280x1024`, or `1600x1080` through a simple graphical interface. It also supports saved accounts, resolution presets, automatic backups, and one-click restore.

---

## Preview

| Main page | Settings page |
|---|---|
| ![](assets/main_page.png) | ![](assets/settings_page.png) |

---

## True Stretch in action

| Without True Stretch | With True Stretch |
|---|---|
| ![](assets/without_true_stretch.png) | ![](assets/with_true_stretch.png) |

Both screenshots use the same resolution (`1440x1080`). EasyTS applies the stretched/fill behavior automatically.

---

## Features

- Instant VALORANT True Stretch setup
- Custom stretched resolutions such as `1440x1080`, `1280x1024`, `1600x1080`, and more
- Multi-account support with saved account switcher
- Resolution presets for quick re-applying
- Automatic config backup system with one-click restore
- VALORANT running detection before applying changes
- Automatic read-only config handling
- Automatic WebView2 check with guided install if missing
- Automatic update checker on startup
- Lightweight standalone executable
- Black bars fix for some laptop users through registry scaling
- Simple graphical interface, no terminal required

---

## Download

[Latest release](https://github.com/ahhmilo/EasyTS/releases/latest)

---

## Installation

1. Download the latest `.exe` from the official GitHub releases page.
2. Move it somewhere accessible, such as `Desktop` or `Downloads`.
3. Run it directly.

No installer is required.

---

## Requirements

- Windows 10 or Windows 11
- Riot Client installed and logged in
- VALORANT installed
- VALORANT completely closed while using EasyTS
- Microsoft WebView2 Runtime

WebView2 is usually pre-installed on Windows 11. Some Windows 10 or stripped-down Windows installs may need it installed manually. EasyTS will prompt you automatically if WebView2 is missing.

---

## How to use EasyTS

### Applying True Stretch to a new account

1. Close VALORANT completely.
2. Make sure Riot Client is open and logged into the account you want to use.
3. Open EasyTS.
4. Enter a resolution using the format `WIDTHxHEIGHT`, for example `1440x1080`.
5. Optionally save the resolution as a preset.
6. Click **Start — Auto-detect Account**.
7. Wait for the success message in the log output.
8. Launch VALORANT.

### Using saved accounts

After a successful apply, EasyTS saves the account automatically.

Saved accounts appear in the account switcher where you can:

- Re-apply True Stretch with the current resolution in one click
- Restore the latest backup
- View the last applied timestamp and backup date

### Presets

Type a resolution and click **+ Save current** to save it as a preset chip.

Click a preset chip to instantly fill the resolution input.

---

## What EasyTS changes automatically

| Setting | Value |
|---|---|
| `ResolutionSizeX / Y` | Custom resolution |
| `LastConfirmedResolutionSizeX / Y` | Custom resolution |
| `LastUserConfirmedResolutionSizeX / Y` | Custom resolution |
| `FullscreenMode` | `2` |
| `LastConfirmedFullscreenMode` | `2` |
| `PreferredFullscreenMode` | `2` |
| `bShouldLetterbox` | `False` |
| `bLastConfirmedShouldLetterbox` | `False` |

If `GameUserSettings.ini` is marked as read-only, EasyTS removes the read-only attribute automatically before applying changes.

---

## Backup system

EasyTS automatically creates a backup before modifying any VALORANT configuration file.

Backups are stored in:

```text
%localappdata%\EasyTS\Backups\
```

Each saved account keeps:

- The latest backup
- The backup creation timestamp
- One-click restore support directly inside the UI

---

## Safety and transparency

EasyTS only reads and writes VALORANT's local configuration files.

EasyTS does not:

- Inject into VALORANT
- Modify game files
- Interact with Riot servers
- Run during gameplay
- Bypass Vanguard
- Change account data

Because EasyTS is unsigned independent software, Windows Defender or SmartScreen may show a warning. This is common for unsigned applications.

If SmartScreen appears:

```text
More info -> Run anyway
```

If you are uncomfortable running the tool, do not use it.

The source code is publicly viewable on GitHub for transparency.

---

## FAQ

### Why does EasyTS require Riot Client?

VALORANT stores configuration files separately for every Riot account. EasyTS uses Riot Client to detect the currently active account automatically.

---

### Can I get banned?

EasyTS only edits local configuration values and does not inject into the game, modify game files, or interact with Riot services during gameplay.

Use at your own discretion.

---

### Why should VALORANT be closed?

VALORANT should be completely closed while EasyTS applies changes. This prevents the game from overwriting the config file or keeping settings locked while the tool is trying to edit them.

EasyTS checks if VALORANT is running and warns you before applying changes.

---

### Why is True Stretch not working?

Check the following:

- VALORANT was closed before applying changes
- Your custom resolution exists and is supported by your monitor/GPU
- Your GPU scaling settings allow stretching
- Your in-game display mode/fill behavior is not overriding the config
- If needed, set VALORANT to **Fullscreen** with **Fill** checked, close the game, then run EasyTS again

EasyTS attempts to configure the required settings automatically, but some systems may override them on launch.

---

### Black bars still appear. What should I do?

Some laptops and display setups may still show black bars because of GPU or display scaling behavior.

EasyTS includes a black bars fix option for some laptop users through registry scaling. This may not work on every system.

You may also need to check your NVIDIA Control Panel, AMD Software, Intel Graphics Command Center, or monitor scaling settings.

---

### Popular True Stretch resolutions

| Resolution |
|---|
| `1440x1080` |
| `1280x1024` |
| `1600x1080` |
| `1154x1080` |
| `1080x1080` |

---

### How do I uninstall EasyTS?

Delete the executable.

To completely undo changes:

1. Use the built-in **Restore** button in the saved accounts section.
2. Or manually reset VALORANT video settings in-game.
3. Or delete `GameUserSettings.ini`.

VALORANT config location:

```text
%localappdata%\VALORANT\Saved\Config\
```

Deleting `GameUserSettings.ini` will reset VALORANT graphics settings.

EasyTS local data is stored in:

```text
%localappdata%\EasyTS\
```

You can delete that folder if you also want to remove EasyTS presets, saved accounts, and backups.

---

### My question is not listed here

Open an issue on GitHub or contact me on Discord:

```text
vestryman
```

---

## License

Copyright (c) 2026 ahhmilo. All rights reserved.

EasyTS is free to download and use from the official GitHub releases page.

The source code is publicly viewable for transparency, but this software is proprietary. You may not copy, modify, redistribute, reupload, repackage, sell, or publish modified versions of the source code or executable without explicit permission from the author.

You may share links to the official EasyTS GitHub repository or official GitHub releases page.
