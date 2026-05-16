![Platform](https://img.shields.io/badge/platform-Windows-blue?style=flat-square)
![Language](https://img.shields.io/badge/built%20with-Python-yellow?style=flat-square)
![License](https://img.shields.io/badge/license-Proprietary-red?style=flat-square)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)

## EasyTS
A tool to set a True Stretched resolution in Valorant

## Download
* Go to [Releases](https://github.com/ahhmilo/EasyTS/releases/)
* Under **Assets**, click "EasyTS.exe"
* Move it to an accessible location (i.e., Downloads, Desktop, etc.)

### Is EasyTS a virus?
* No, it is not a virus. All that this tool does is change VALORANT's configuration file for a specific account to enable True Stretch, and additionally change the resolution in the game. The program is just making life easier -- that's it. There are other ways of enabling True Stretch and I do not force anyone into using my tool if they don't feel safe running it.
* Windows Defender will flag software without a certificate or from unknown sources, so there are often false positives. The solution to this is to purchase a certificate, but it can be expensive for a small developer.
* Windows SmartScreen will state that: "Microsoft Defender SmartScreen prevented an unrecognized app from starting. Running this app might put your PC at risk". However, if you press "More Info", then you will be able to run the program by pressing "Run anyway".
* If you are using a different anti-virus than Windows Defender and EasyTS is getting flagged as a virus, you can add it as an exception.
* **If you do not feel safe, then please do not download and use EasyTS. Alternatively, if you have experience in software, then you can review the code by deobfuscating it.**

### How do I use EasyTS?
* Open the "EasyTS" executable.
* Make sure you are logged in into the account that you want to set the True Stretch on, and have Riot Client opened as a visible window with VALORANT closed. 
* Enter the `Width` and `Height` to a desired resolution.
* Press Enter and if everything goes as planned, you should receive a message like this: "True-stretched has been set successfully for the resolution..."

### Why do i need to be logged in into an account? 
* VALORANT uses an account-set config system, so if you set up EasyTS on your alt account, the True-Stretch won't convert over to your main account! Every account has a different config file with different resolutions.

### How do I uninstall EasyTS?
* Just simply delete the exe file.
* If you want to "undo" the changes that EasyTS made, then there are two options:

1. **The easy one**
* Go into VALORANT and change the window mode to a different one (e.g. from Windowed to Fullscreen), if that doesn't work you can also do it by setting a different resolution.
2. **The hard one**
* Go into the VALORANT's config folder that's located in `%localappdata%`, then go to Saved/Config/Windows, you should see a `RiotLocalMachine.ini` file, open it and copy your `LastKnownUser`, then back out to the Config folder and find that ID you just copied by either searching or just remembering it. Continuing, open the folder, find the Windows folder and inside delete the `GameUserSettings.ini` file. This may mess up your resolution settings and maybe even graphics settings.

### After setting the resolution and having the correct confirmation message, my True-Stretch doesn't work. Why?
* Make sure your PC is True-Stretch compatible. I don't know **exactly** how it works, but I know if you're able to have a custom resolution set on your monitor without having black bars, the True-Stretch theoretically should work.

### What are popular resolution(s)?
* 1440x1080
* 1080x1080
* 1280x1024
* 1600x1080
* 1154x1080

### What can I do if my question or concern is not listed?
* You are welcome to open an issue, and I will attempt to respond when I can. If I don't seem to respond in a couple of weeks, you may contact me through Discord - `x2kc`

## Note
* This desecription was copied from [alphares](https://github.com/braycarlson/alphares) and changed to match EasyTS.
* This method is not bannable. People in high elo (Immortal 1+) with money spent on the accounts, and my friends have used it for a couple of months now without any issues or bans. My friend is risking an account worth over $1500+ so I am pretty confident you are not going to get banned for using EasyTS.

## License
Copyright (c) 2026 ahhmilo. All rights reserved.

This software and its source code are proprietary. Unauthorized copying, modification, or distribution of this software via any medium is strictly prohibited.
