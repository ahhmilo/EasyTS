[![Windows](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows11&logoColor=white&labelColor=555555)](#)
[![Python](https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white&labelColor=555555)](#)
[![HTML](https://img.shields.io/badge/language-HTML-E34F26?logo=html5&logoColor=white&labelColor=555555)](#)
[![License](https://img.shields.io/badge/license-Proprietary-red)](#)

<p align="center">
  <img src="assets/EasyTS_logo.png" width="160" alt="EasyTS logo">
</p>

# EasyTS

A simple Windows tool for applying VALORANT True Stretch resolutions without manually editing config files or messing around with Device Manager.

Supports custom resolutions, saved accounts, presets, automatic backups, one-click restore, and an advanced Fullscreen Mode for lower input delay.

---

## Preview

| Main page | Settings page |
|---|---|
| ![](https://raw.githubusercontent.com/ahhmilo/EasyTS/main/assets/main_page.png) | ![](https://raw.githubusercontent.com/ahhmilo/EasyTS/main/assets/settings_page.png) |

---

## True Stretch in action

| Without True Stretch | With True Stretch |
|---|---|
| ![](https://raw.githubusercontent.com/ahhmilo/EasyTS/main/assets/without_true_stretch.png) | ![](https://raw.githubusercontent.com/ahhmilo/EasyTS/main/assets/with_true_stretch.png) |

Both screenshots use the same resolution (`1440x1080`). EasyTS applies the stretched/fill behavior automatically.

---

## Features

- Instant VALORANT True Stretch setup
- Custom stretched resolutions such as `1440x1080`, `1280x1024`, `1600x1080`, and more
- Fullscreen Mode (v3.0.0+) — true fullscreen stretched resolution via temporary monitor disabling, for lower input delay than Windowed mode
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

### Applying True Stretch to a new account (Config Mode)

1. Close VALORANT completely.
2. Make sure Riot Client is open and logged into the account you want to use.
3. Open EasyTS.
4. Enter a resolution using the format `WIDTHxHEIGHT`, for example `1440x1080`.
5. Optionally save the resolution as a preset.
6. Click **Start — Auto-detect Account**.
7. Wait for the success message in the log output.
8. Launch VALORANT.

Config Mode runs VALORANT in Windowed mode and does not touch any system display settings. It is the safest and most reversible option, and is recommended for most users.

### Fullscreen Mode (advanced, v3.0.0+)

Fullscreen Mode is for users who want true fullscreen stretched resolution with the lowest possible input delay. It works by temporarily disabling your monitor device(s) in Windows so VALORANT cannot detect its native aspect ratio and is forced to use the resolution set in the config file instead.

1. Close VALORANT completely.
2. Switch to **Fullscreen Mode** at the top of EasyTS.
3. Enter a resolution and choose which monitor(s) to disable. Disabling all monitors is recommended for the most reliable result.
4. Click **Apply Fullscreen Mode** and accept the UAC prompt.
5. Your screen will briefly flicker. This is expected, and you will still be able to see and use your screen normally.
6. A confirmation prompt appears for 15 seconds. Click **Keep** if everything looks correct, or **Revert**, or let it time out, to undo automatically.

**Important: EasyTS does not watch for VALORANT closing and does not automatically restore your display after you finish playing.** Once you click Keep, your monitor(s) stay disabled until you manually restore them. After you are done playing, go to **Settings → Re-enable Monitors** to restore your normal display state.

The Re-enable Monitors button in Settings always works regardless of EasyTS's current state, so it can also be used as a manual recovery option if anything goes wrong.

Player models may appear visually wider in Fullscreen Mode, similar to other stretched-resolution games. VALORANT's actual hit detection is not affected by this.

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

### Config Mode

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

### Fullscreen Mode

| Setting | Value |
|---|---|
| `ResolutionSizeX / Y` | Custom resolution |
| `LastConfirmedResolutionSizeX / Y` | Custom resolution |
| `LastUserConfirmedResolutionSizeX / Y` | Custom resolution |
| `FullscreenMode` | `0` (Fullscreen) |
| `LastConfirmedFullscreenMode` | `0` |
| `PreferredFullscreenMode` | `0` |
| `bShouldLetterbox` | `False` |
| `bLastConfirmedShouldLetterbox` | `False` |

Selected monitor device(s) are also temporarily disabled in Fullscreen Mode.

If `GameUserSettings.ini` is marked as read-only, EasyTS removes the read-only attribute automatically before applying changes.

---

## Backup system

EasyTS automatically creates a backup before modifying any VALORANT configuration file, in both Config Mode and Fullscreen Mode.

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

EasyTS only reads and writes VALORANT's local configuration files, and in Fullscreen Mode, temporarily disables monitor devices through Windows' built-in device management.

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

EasyTS only edits local configuration values and, in Fullscreen Mode, temporarily disables monitor devices through standard Windows functionality. It does not inject into the game, modify game files, or interact with Riot services during gameplay.

Use at your own discretion.

---

### Why should VALORANT be closed?

VALORANT should be completely closed while EasyTS applies changes. This prevents the game from overwriting the config file or keeping settings locked while the tool is trying to edit them.

EasyTS checks if VALORANT is running and warns you before applying changes, in both Config Mode and Fullscreen Mode.

---

### Why is True Stretch not working?

Check the following:

- VALORANT was closed before applying changes
- Your custom resolution exists and is supported by your monitor/GPU
- Your GPU scaling settings allow stretching
- Your in-game display mode/fill behavior is not overriding the config
- If needed, set VALORANT to **Fullscreen** with **Fill** checked, close the game, then run EasyTS again
- If using Fullscreen Mode, make sure you selected the correct monitor(s) to disable

EasyTS attempts to configure the required settings automatically, but some systems may override them on launch.

---

### Black bars still appear. What should I do?

Some laptops and display setups may still show black bars because of GPU or display scaling behavior.

EasyTS includes a black bars fix option for some laptop users through registry scaling. This may not work on every system.

You may also need to check your NVIDIA Control Panel, AMD Software, Intel Graphics Command Center, or monitor scaling settings.

---

### Does Fullscreen Mode automatically restore my display after I close VALORANT?

No. EasyTS does not watch for VALORANT closing and does not automatically restore your display. You must manually click **Re-enable Monitors** in Settings once you are done playing.

---

### My monitor seems stuck disabled. How do I fix it?

Open EasyTS, go to **Settings → Re-enable Monitors**, and click **Re-enable**. This works independently of any other state in the app and is always available as a recovery option.

If EasyTS itself will not open, you can also manually re-enable your monitor through Windows Device Manager: right-click the Start button → Device Manager → expand Monitors → right-click the disabled monitor → Enable device.

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
2. If you used Fullscreen Mode, use **Re-enable Monitors** in Settings first.
3. Or manually reset VALORANT video settings in-game.
4. Or delete `GameUserSettings.ini`.

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
