[![Windows](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows11&logoColor=white&labelColor=555555)](#)
[![Python](https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white&labelColor=555555)](#)
[![HTML](https://img.shields.io/badge/language-HTML-E34F26?logo=html5&logoColor=white&labelColor=555555)](#)
[![License](https://img.shields.io/badge/license-Proprietary-red)](#)

![](https://files.catbox.moe/hnut3y.png)

# EasyTS
A lightweight Windows utility that instantly applies True-Stretch resolutions to VALORANT accounts without requiring manual configuration edits.

EasyTS automatically handles resolution changes, fullscreen/windowed settings, stretch behavior, account management, and backups through a simple graphical interface.

---

## True-Stretch in action

| Without True-Stretch | With True-Stretch |
|---|---|
| ![](https://files.catbox.moe/3wxgnu.png) | ![](https://files.catbox.moe/cr3qnr.png) |

Both screenshots use the same resolution (1440x1080).
EasyTS applies the stretched/fill behavior automatically.

---

## Features
- Instant True-Stretch applying
- Multi-account support with saved account switching
- Automatic config backup system
- One-click restore for previous settings
- Automatic read-only handling
- Lightweight standalone executable
- Live status log and cleaner error messages

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
- VALORANT installed
- Microsoft WebView2 Runtime — pre-installed on Windows 11, may need manual install on Windows 10. EasyTS will prompt you automatically if it is missing.

---

## How to use EasyTS
### Applying True-Stretch to a new account
1. Close VALORANT completely.
2. Open EasyTS.
3. Make sure Riot Client is open and logged into the desired account.
4. Enter a resolution using the format `WIDTHxHEIGHT`
   - Example: `1440x1080`
5. Click **Start**
6. Wait for the success confirmation in the log output

### Using saved accounts
After a successful apply, EasyTS automatically saves the account locally.

Saved accounts appear inside the account switcher where you can:
- Re-apply True-Stretch instantly
- Restore the latest backup
- View the latest backup timestamp

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
EasyTS automatically creates a backup before modifying a configuration file.

Backups are stored in:

```text
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
```text
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
- Your monitor supports custom resolutions
- GPU scaling is enabled in NVIDIA Control Panel or AMD Software if necessary

EasyTS attempts to configure these settings automatically, but some systems override them on launch.

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
1. Use the built-in **Restore** button
2. Or manually reset VALORANT video settings
3. Or delete `GameUserSettings.ini`

Config location:
```text
%localappdata%\VALORANT\Saved\Config\
```

Deleting the config file will also reset graphics settings.

---

### My question is not listed here
Open an issue on GitHub or contact me on Discord:

```text
vestryman
```

---

## License

Copyright (c) 2026 ahhmilo. All rights reserved.

This software and its source code are proprietary.
Unauthorized copying, modification, or distribution of this software, via any medium, is strictly prohibited.
