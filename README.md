![Platform](https://img.shields.io/badge/platform-Windows-blue?style=flat-square)
![Language](https://img.shields.io/badge/built%20with-Python-yellow?style=flat-square)
![License](https://img.shields.io/badge/license-Proprietary-red?style=flat-square)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)

# EasyTS
A lightweight Windows tool that instantly applies a True-Stretch resolution to any VALORANT account — no manual config editing required.

---

## Download
Choose the version that fits your needs:

### Stable version (terminal)
- Recommended for most users
- Most tested and reliable

[Latest release](https://github.com/ahhmilo/EasyTS/releases/latest)

---

### Beta version (GUI, experimental)
- New graphical interface (pywebview)
- May contain bugs or incomplete features

[Download beta release](https://github.com/ahhmilo/EasyTS/releases/tag/v2.0.0-beta)

---

## Installation
- Download the `.exe`
- Move it somewhere accessible (Desktop, Downloads, etc.)
- Run it directly (no installer required)

---

## Requirements
- Windows 10 or 11
- Riot Client installed and logged in
- VALORANT installed

---

## How to use EasyTS
1. Open EasyTS.
2. Make sure you are logged in to the account you want to apply True-Stretch on, with Riot Client open as a visible window and VALORANT closed.
3. Enter your desired `Width` and `Height`.
4. Press Enter — if everything goes as planned, you will receive a confirmation message.

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
* Your monitor needs to support custom resolutions without black bars for True-Stretch to work. If your display already supports a custom resolution natively, it should work.

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
* **Note this will also reset your graphics settings.**

### My question isn't listed here.
* Open an [issue](https://github.com/ahhmilo/EasyTS/issues) and I'll get back to you. You can also reach me on Discord: `x2kc`

---

## License
Copyright (c) 2026 ahhmilo. All rights reserved.

This software and its source code are proprietary. Unauthorized copying, modification, or distribution of this software, via any medium, is strictly prohibited.
