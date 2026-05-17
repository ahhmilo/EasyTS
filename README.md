[![Windows](https://custom-icon-badges.demolab.com/badge/Windows-0078D6?logo=windows11&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![HTML](https://img.shields.io/badge/HTML-%23E34F26.svg?logo=html5&logoColor=white)](#)
[![License](https://img.shields.io/badge/license-Proprietary-red)](#)

# EasyTS
A lightweight Windows tool that instantly applies a True-Stretch resolution to any VALORANT account — no manual config editing required.

---

## Download
[Latest release](https://github.com/ahhmilo/EasyTS/releases/latest)

---

## Installation
- Download the `.exe`
- Move it somewhere accessible (Desktop, Downloads, etc.)
- Run it directly (no installer required)

---

## Requirements
- Windows 10 or 11
- Riot Client installed and logged in
- VALORANT installed and closed

---

## How to use EasyTS

1. **Close VALORANT** before running EasyTS. The tool writes to a config file that VALORANT locks while running — having it open may cause the changes to be overwritten or fail silently.
2. Open EasyTS.
3. Make sure you are logged in to the account you want to apply True-Stretch on, with Riot Client open as a visible window.
4. Enter your desired resolution in the format `WIDTHxHEIGHT` (e.g. `1440x1080`).
5. Click **Start** — if everything goes as planned, you will receive a confirmation in the log.

### What EasyTS sets automatically
EasyTS handles all of the following config changes for you:

| Setting | Value set |
|---|---|
| `ResolutionSizeX / Y` | Your chosen resolution |
| `LastConfirmedResolutionSizeX / Y` | Your chosen resolution |
| `LastUserConfirmedResolutionSizeX / Y` | Your chosen resolution |
| `FullscreenMode` | `2` (Windowed) |
| `LastConfirmedFullscreenMode` | `2` (Windowed) |
| `PreferredFullscreenMode` | `2` (Windowed) |
| `bShouldLetterbox` | `False` (Fill / stretch, no black bars) |
| `bLastConfirmedShouldLetterbox` | `False` |

If the config file is marked as read-only, EasyTS removes that attribute automatically before writing to avoid complications.

---

## FAQ

### Is EasyTS safe to run?
* EasyTS only reads and writes to VALORANT's local configuration file on your machine. It makes no contact with Riot's servers and does not modify any game files.
* Because EasyTS is unsigned software from an independent developer, Windows Defender and SmartScreen may flag it as unrecognized — this is a standard false positive, not an indication of malware. If SmartScreen blocks it, click **More info → Run anyway**.
* If you are not comfortable running my tool, please do **not** use EasyTS.

### Why do I need to be logged in to an account?
* VALORANT uses a per-account config system. Each account has its own separate configuration file, so True-Stretch must be set individually per account.

### Will I get banned?
* This tool only modifies a local config file and makes no contact with Riot's servers during gameplay. The method has been used consistently across multiple accounts in high elo without any issues.

### My True-Stretch isn't working after the confirmation message. Why?
* Make sure VALORANT is running in **Windowed** mode. EasyTS sets this automatically, but if VALORANT overrides it on launch, go to **Settings → Video → Display Mode** and set it to **Windowed** manually.
* Your monitor needs to support custom resolutions without black bars for True-Stretch to work visually. If your display does not stretch natively, you may need to enable GPU scaling in your graphics card settings (NVIDIA Control Panel or AMD Software).

### What are some popular resolutions?
| Popular Resolutions |
|---------------------|
| 1440x1080           |
| 1280x1024           |
| 1600x1080           |
| 1154x1080           |
| 1080x1080           |

### How do I uninstall EasyTS?
* Just delete the file. No installer, no leftover files.
* To undo the changes EasyTS made, you have two options:
  1. **Easy:** Go into VALORANT's video settings and switch the window mode or resolution to something else and apply. VALORANT will regenerate the config.
  2. **Manual:** Navigate to `%localappdata%\VALORANT\Saved\Config\`, find your account folder (you can get the ID from `RiotLocalMachine.ini` → `LastKnownUser`), open the `WindowsClient` folder inside it, and delete `GameUserSettings.ini`.
* **Note: this will also reset your graphics settings.**

### My question isn't listed here.
* Open an [issue](https://github.com/ahhmilo/EasyTS/issues) and I'll get back to you. You can also reach me on Discord: `x2kc`

---

## License
Copyright (c) 2026 ahhmilo. All rights reserved.

This software and its source code are proprietary. Unauthorized copying, modification, or distribution of this software, via any medium, is strictly prohibited.
