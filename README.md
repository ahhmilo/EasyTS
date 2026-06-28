[![Windows](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows11&logoColor=white&labelColor=555555)](#)
[![Python](https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white&labelColor=555555)](#)
[![HTML](https://img.shields.io/badge/language-HTML-E34F26?logo=html5&logoColor=white&labelColor=555555)](#)
[![License](https://img.shields.io/badge/license-Proprietary-red)](#)

| Main page | Settings page |
|---|---|
| ![](https://files.catbox.moe/plle0l.png) | ![](https://files.catbox.moe/nbugml.png) |

Click to expand.

---

# EasyTS
A lightweight Windows utility that instantly applies True-Stretched resolutions to VALORANT accounts without requiring manual configuration edits.

EasyTS automatically handles resolution changes, fullscreen/windowed settings, stretch behavior, account management, presets, and backups through a simple graphical interface.

---

## True-Stretched in action

| Without True-Stretcedh | With True-Stretched |
|---|---|
| ![](https://files.catbox.moe/3wxgnu.png) | ![](https://files.catbox.moe/cr3qnr.png) |

Both screenshots use the same resolution (1440x1080).
EasyTS applies the stretched/fill behavior automatically.

---

## Features
- Instant True-Stretched applying
- Multi-account support with saved account switcher
- Resolution presets for quick re-applying
- Automatic config backup system with one-click restore
- VALORANT running detection — warns you before writing to a locked file
- Automatic read-only handling
- Automatic WebView2 check with guided install if missing
- Automatic update checker on startup
- Lightweight standalone executable
- Black bars fix for laptop users via registry scaling

---

## Download
[Latest release](https://github.com/ahhmilo/EasyTS/releases/latest)

---

## Installation
1. Download the latest `.exe`
2. Move it somewhere accessible (`Desktop`, `Downloads`, etc.)
3. Run it directly — no installer required

---

## Requirements
- Windows 10 or Windows 11
- Riot Client installed and logged in
- VALORANT installed and **closed** while using EasyTS
- Microsoft WebView2 Runtime — pre-installed on Windows 11, may need manual install on Windows 10. EasyTS will prompt you automatically if it is missing.

---

## How to use EasyTS

### Applying True-Stretched to a new account
1. Close VALORANT completely.
2. Open EasyTS.
3. Make sure Riot Client is open and logged into the desired account.
4. Enter a resolution using the format `WIDTHxHEIGHT` — e.g. `1440x1080`
5. Optionally save it as a preset for quick re-use later.
6. Click **Start — Auto-detect Account**.
7. Wait for the success confirmation in the log output.

### Using saved accounts
After a successful apply, EasyTS saves the account automatically.

Saved accounts appear in the account switcher where you can:
- Re-apply True-Stretched with the current resolution in one click
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
| `FullscreenMode` | `2` (Windowed) |
| `LastConfirmedFullscreenMode` | `2` |
| `PreferredFullscreenMode` | `2` |
| `bShouldLetterbox` | `False` |
| `bLastConfirmedShouldLetterbox` | `False` |

If `GameUserSettings.ini` is marked as read-only, EasyTS removes the attribute automatically before applying changes.

---

## Backup System
EasyTS automatically creates a backup before modifying any configuration file.

Backups are stored in:
```
%localappdata%\EasyTS\Backups\
```

Each account keeps:
- The latest backup only
- The backup creation timestamp
- One-click restore support directly inside the UI

---

## FAQ

### Is EasyTS safe?
- EasyTS only reads and writes VALORANT's local configuration files.
- The application does not communicate with Riot servers.
- No game files are modified.

Because EasyTS is unsigned independent software, Windows Defender or SmartScreen may show a warning. This is common for unsigned applications.

If SmartScreen appears:
```
More info -> Run anyway
```

If you are uncomfortable running the tool, do not use it.

---

### Why does EasyTS require Riot Client?
VALORANT stores configuration files separately for every Riot account. EasyTS uses Riot Client to detect the currently active account automatically.

---

### Can I get banned?
EasyTS only edits local configuration values and does not inject into the game or interact with Riot services during gameplay.

Use at your own discretion.

---

### Why is True-Stretch not working?
Check the following:
- Sometimes the fill mode might glitch — before running EasyTS, set your game to **Fullscreen** mode with **Fill** checked.
- Your monitor supports custom resolutions.
- GPU scaling is enabled in NVIDIA Control Panel or AMD Software if necessary.

EasyTS attempts to configure these settings automatically, but some systems may override them on launch.

---

### Popular resolutions

| Resolution |
|---|
| 1440x1080 |
| 1280x1024 |
| 1600x1080 |
| 1154x1080 |
| 1080x1080 |

---

### How do I uninstall EasyTS?
Delete the executable.

To completely undo changes:
1. Use the built-in **Restore** button in the saved accounts section
2. Or manually reset VALORANT video settings in-game
3. Or delete `GameUserSettings.ini`

Config location:
```
%localappdata%\VALORANT\Saved\Config\
```

Deleting the config file will also reset graphics settings.

---

### My question is not listed here
Open an issue on GitHub or contact me on Discord:
```
vestryman
```

---

## License

Copyright (c) 2026 ahhmilo. All rights reserved.

This software and its source code are proprietary.
Unauthorized copying, modification, or distribution of this software, via any medium, is strictly prohibited.
