# EasyTS
# Copyright (c) 2026 ahhmilo. All rights reserved.
#
# This software is proprietary. The source code is publicly viewable for
# transparency, but copying, modification, redistribution, reuploading,
# repackaging, or publishing modified versions is not allowed without
# explicit permission from the author.
#
# See LICENSE.md for full license terms.

import webview
import os
import json
import stat
import base64
import urllib.request
import urllib.error
import ssl
import re
import time
import shutil
import winreg
import subprocess
import tempfile
import textwrap
import webbrowser
import tkinter as tk
import threading
from typing import Optional, Tuple

CURRENT_VERSION = "v3.0.4"
GITHUB_URL      = "https://github.com/ahhmilo/EasyTS"

WEBVIEW2_DOWNLOAD_URL = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"
WEBVIEW2_REGISTRY_KEYS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
    (winreg.HKEY_CURRENT_USER,  r"Software\Microsoft\EdgeUpdate\ClientState\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
]

REGION_MAP = {
    "NA": "na", "BR": "br", "EUN1": "eu", "EUW1": "eu",
    "KR": "kr", "JP": "jp", "OCE": "oce", "AP": "ap", "LATAM": "latam",
}


class ValorantConfigError(Exception):
    pass


def log_to_ui(window, message: str, msg_type: str = "info"):
    window.evaluate_js(f"window.appendLog({json.dumps(message)}, {json.dumps(msg_type)});")


def get_easysts_dir() -> str:
    path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "EasyTS")
    os.makedirs(path, exist_ok=True)
    return path

def get_accounts_path() -> str:
    return os.path.join(get_easysts_dir(), "accounts.json")

def get_presets_path() -> str:
    return os.path.join(get_easysts_dir(), "presets.json")

def get_settings_path() -> str:
    return os.path.join(get_easysts_dir(), "settings.json")

def load_settings() -> dict:
    defaults = {"lock_config_read_only": False}
    path = get_settings_path()
    if not os.path.isfile(path):
        return defaults
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return defaults
        merged = defaults.copy()
        merged.update(data)
        return merged
    except Exception:
        return defaults

def save_settings(settings: dict) -> None:
    with open(get_settings_path(), "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

def is_read_only_lock_enabled() -> bool:
    return bool(load_settings().get("lock_config_read_only", False))

def set_read_only_lock_enabled(enabled: bool) -> None:
    settings = load_settings()
    settings["lock_config_read_only"] = bool(enabled)
    save_settings(settings)


def load_accounts() -> list:
    path = get_accounts_path()
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_accounts(accounts: list) -> None:
    with open(get_accounts_path(), "w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=2, ensure_ascii=False)

def upsert_account(name_tag: str, folder: str) -> None:
    accounts = load_accounts()
    now = time.strftime("%Y-%m-%d %H:%M")
    for acc in accounts:
        if acc["folder"] == folder:
            acc["name_tag"] = name_tag
            acc["last_applied"] = now
            break
    else:
        accounts.append({"name_tag": name_tag, "folder": folder, "last_applied": now})
    save_accounts(accounts)

def load_presets() -> list:
    path = get_presets_path()
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_presets(presets: list) -> None:
    with open(get_presets_path(), "w", encoding="utf-8") as f:
        json.dump(presets, f, indent=2, ensure_ascii=False)

def get_backup_path(folder: str, create_dir: bool = True) -> str:
    backup_dir = os.path.join(get_easysts_dir(), "Backups", folder)
    if create_dir:
        os.makedirs(backup_dir, exist_ok=True)
    return os.path.join(backup_dir, "GameUserSettings.ini.bak")

def backup_config(config_file: str, folder: str) -> None:
    backup_path = get_backup_path(folder, create_dir=True)
    shutil.copy2(config_file, backup_path)
    make_file_writable(backup_path)

def make_file_writable(path: str) -> None:
    file_mode = os.stat(path).st_mode
    if not (file_mode & stat.S_IWRITE):
        os.chmod(path, file_mode | stat.S_IWRITE)

def make_file_read_only(path: str) -> None:
    file_mode = os.stat(path).st_mode
    if file_mode & stat.S_IWRITE:
        os.chmod(path, file_mode & ~stat.S_IWRITE)

def get_backup_date(folder: str) -> Optional[str]:
    path = get_backup_path(folder, create_dir=False)
    if not os.path.isfile(path):
        return None
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(path)))


def is_valorant_running() -> bool:
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq VALORANT-Win64-Shipping.exe", "/NH"],
            capture_output=True, text=True
        )
        return "VALORANT-Win64-Shipping.exe" in result.stdout
    except Exception:
        return False

def get_valorant_config_path() -> str:
    localappdata = os.environ.get("LOCALAPPDATA")
    if not localappdata:
        raise ValorantConfigError("LOCALAPPDATA not found.")
    valorant_root = os.path.join(localappdata, "VALORANT")
    saved_config  = os.path.join(valorant_root, "Saved", "Config")
    if not os.path.isdir(valorant_root):
        raise ValorantConfigError("VALORANT user directory not found.")
    if not os.path.isdir(saved_config):
        raise ValorantConfigError(r"VALORANT Saved\Config directory not found.")
    return saved_config

def get_config_file_for_folder(saved_config_dir: str, folder: str) -> Optional[str]:
    for platform_folder in ("WindowsClient", "Windows"):
        config_file = os.path.join(saved_config_dir, folder, platform_folder, "GameUserSettings.ini")
        if os.path.isfile(config_file):
            return config_file
    return None

def sort_config_matches(matches: list, preferred_folder: Optional[str] = None) -> list:
    preferred = preferred_folder.lower() if preferred_folder else None

    def sort_key(item):
        folder, config_file = item
        preferred_rank = 0 if preferred and folder.lower() == preferred else 1
        try:
            mtime = os.path.getmtime(config_file)
        except OSError:
            mtime = 0
        return (preferred_rank, -mtime, folder.lower())

    return sorted(matches, key=sort_key)

def get_config_files_for_puuid(saved_config_dir: str, puuid: str, preferred_folder: Optional[str] = None) -> list:
    prefix = f"{puuid.lower()}-"
    matches = []
    try:
        for name in os.listdir(saved_config_dir):
            folder_path = os.path.join(saved_config_dir, name)
            if os.path.isdir(folder_path) and name.lower().startswith(prefix):
                config_file = get_config_file_for_folder(saved_config_dir, name)
                if config_file:
                    matches.append((name, config_file))
    except OSError:
        pass
    return sort_config_matches(matches, preferred_folder)

def resolve_account_configs(saved_config_dir: str, puuid: str, region_folder: str) -> list:
    expected_folder = f"{puuid}-{region_folder}"
    matches = get_config_files_for_puuid(saved_config_dir, puuid, expected_folder)
    if matches:
        return matches

    raise ValorantConfigError(
        "GameUserSettings.ini was not found for this Riot account. "
        "EasyTS detected the account, but could not find any VALORANT config folder matching the account ID. "
        "Please launch VALORANT once on this account, change any video setting, close the game, and try again."
    )

def resolve_saved_configs(saved_config_dir: str, folder: str) -> list:
    if "-" in folder:
        puuid = folder.rsplit("-", 1)[0]
        matches = get_config_files_for_puuid(saved_config_dir, puuid, folder)
        if matches:
            return matches

    config_file = get_config_file_for_folder(saved_config_dir, folder)
    if config_file:
        return [(folder, config_file)]

    raise ValorantConfigError(
        "Config file not found for this account. "
        "Please launch VALORANT at least once with this account."
    )

def find_riot_lockfile() -> Optional[str]:
    localappdata = os.environ.get("LOCALAPPDATA")
    if not localappdata:
        return None
    path = os.path.join(localappdata, "Riot Games", "Riot Client", "Config", "lockfile")
    return path if os.path.isfile(path) else None

def read_riot_lockfile(lockfile_path: str) -> Tuple[str, str, int, str, str]:
    with open(lockfile_path, "r", encoding="utf-8") as f:
        parts = f.read().strip().split(":")
    if len(parts) != 5:
        raise ValueError("Invalid lockfile format.")
    name, pid, port, password, protocol = parts
    return name, pid, int(port), password, protocol

def riot_request(port: int, auth_token: str, endpoint: str):
    url = f"https://127.0.0.1:{port}{endpoint}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Basic {auth_token}")
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    try:
        return urllib.request.urlopen(req, context=ssl_ctx, timeout=5)
    except (urllib.error.URLError, ConnectionRefusedError, TimeoutError, OSError):
        raise ValorantConfigError(
            "Riot Client is not open or not responding. Please open Riot Client, "
            "log into the account you want to use, keep VALORANT closed, and try again."
        )

def get_riot_account_info(port: int, auth_token: str) -> Tuple[str, str, str]:
    response  = riot_request(port, auth_token, "/rso-auth/v1/authorization/userinfo")
    data      = json.loads(response.read().decode())
    user_info = json.loads(data.get("userInfo"))

    puuid    = user_info.get("sub")
    acct     = user_info.get("acct", {})
    name_tag = f"{acct.get('game_name', 'Unknown')}#{acct.get('tag_line', 'Unknown')}"

    region_info = user_info.get("region", {})
    region_raw  = (region_info.get("id") if region_info else None) \
                  or user_info.get("affinity", {}).get("pp")
    if not region_raw:
        raise ValorantConfigError("Could not determine account region.")

    region_folder = REGION_MAP.get(region_raw.upper(), region_raw.lower())
    return puuid, region_folder, name_tag

def modify_game_user_settings(config_file: str, width: int, height: int) -> None:
    make_file_writable(config_file)

    with open(config_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [l for l in lines if not l.startswith("FullscreenMode=")]

    pass1    = []
    inserted = False
    for line in lines:
        pass1.append(line)
        if "HDRDisplayOutputNits=" in line:
            pass1.append("FullscreenMode=2\n")
            inserted = True

    if not inserted:
        raise ValorantConfigError(
            "HDRDisplayOutputNits not found in config. The file may be outdated or corrupted."
        )

    all_text = "".join(pass1)
    if "bShouldLetterbox=" not in all_text or "bLastConfirmedShouldLetterbox=" not in all_text:
        raise ValorantConfigError(
            "bShouldLetterbox / bLastConfirmedShouldLetterbox not found in config. "
            "The file may be outdated or corrupted."
        )

    final = []
    for line in pass1:
        if line.startswith("ResolutionSizeX="):
            final.append(f"ResolutionSizeX={width}\n")
        elif line.startswith("ResolutionSizeY="):
            final.append(f"ResolutionSizeY={height}\n")
        elif line.startswith("LastConfirmedResolutionSizeX="):
            final.append(f"LastConfirmedResolutionSizeX={width}\n")
        elif line.startswith("LastConfirmedResolutionSizeY="):
            final.append(f"LastConfirmedResolutionSizeY={height}\n")
        elif line.startswith("LastUserConfirmedResolutionSizeX="):
            final.append(f"LastUserConfirmedResolutionSizeX={width}\n")
        elif line.startswith("LastUserConfirmedResolutionSizeY="):
            final.append(f"LastUserConfirmedResolutionSizeY={height}\n")
        elif line.startswith("LastConfirmedFullscreenMode="):
            final.append("LastConfirmedFullscreenMode=2\n")
        elif line.startswith("PreferredFullscreenMode="):
            final.append("PreferredFullscreenMode=2\n")
        elif line.startswith("bShouldLetterbox="):
            final.append("bShouldLetterbox=False\n")
        elif line.startswith("bLastConfirmedShouldLetterbox="):
            final.append("bLastConfirmedShouldLetterbox=False\n")
        else:
            final.append(line)

    with open(config_file, "w", encoding="utf-8") as f:
        f.writelines(final)



def is_webview2_installed() -> bool:
    for hive, key_path in WEBVIEW2_REGISTRY_KEYS:
        try:
            with winreg.OpenKey(hive, key_path):
                return True
        except OSError:
            continue
    return False

def download_webview2_bootstrapper() -> str:
    tmp = tempfile.mktemp(suffix=".exe", prefix="MicrosoftEdgeWebview2Setup_")
    urllib.request.urlretrieve(WEBVIEW2_DOWNLOAD_URL, tmp)
    return tmp

def run_webview2_installer(bootstrapper_path: str) -> None:
    bat = tempfile.mktemp(suffix=".bat", prefix="EasyTS_webview2_")
    script = textwrap.dedent(f"""
        @echo off
        echo ============================================================
        echo  EasyTS - WebView2 Installer
        echo ============================================================
        echo.
        echo  EasyTS will automatically install WebView2 and launch
        echo  EasyTS after a successful installation.
        echo.
        echo  Please do not close this window.
        echo ============================================================
        echo.
        "{bootstrapper_path}" /install
        echo.
        echo ============================================================
        echo  Installation complete. EasyTS will now launch.
        echo  You can close this window.
        echo ============================================================
        echo.
        pause
    """).strip()
    with open(bat, "w") as f:
        f.write(script)
    subprocess.Popen(["cmd.exe", "/c", bat], creationflags=subprocess.CREATE_NEW_CONSOLE).wait()
    try:
        os.remove(bat)
    except Exception:
        pass

def prompt_webview2() -> None:
    root = tk.Tk()
    root.withdraw()

    dialog = tk.Toplevel(root)
    dialog.title("EasyTS — WebView2 Required")
    dialog.resizable(False, False)
    dialog.configure(bg="#111111")
    dialog.attributes("-topmost", True)
    dialog.update_idletasks()
    w, h = 420, 210
    dialog.geometry(f"{w}x{h}+{(dialog.winfo_screenwidth()-w)//2}+{(dialog.winfo_screenheight()-h)//2}")

    choice = {"value": None}

    tk.Label(dialog, text="WebView2 Runtime Not Found",
             bg="#111111", fg="#ff4655", font=("Segoe UI", 13, "bold")).pack(pady=(22, 6))
    tk.Label(dialog,
             text="EasyTS requires the Microsoft WebView2 Runtime.\nIt is not installed on this machine.",
             bg="#111111", fg="#cccccc", font=("Segoe UI", 9), justify="center").pack(pady=(0, 18))

    btn_frame = tk.Frame(dialog, bg="#111111")
    btn_frame.pack()

    btn_style = {"font": ("Segoe UI", 9, "bold"), "relief": "flat", "cursor": "hand2", "padx": 14, "pady": 7, "bd": 0}

    def on_auto():   choice["value"] = "auto";   dialog.destroy()
    def on_manual(): choice["value"] = "manual"; dialog.destroy()
    def on_cancel(): choice["value"] = "cancel"; dialog.destroy()

    def make_btn(text, bg, fg, bg_h, fg_h, cmd, col):
        b = tk.Button(btn_frame, text=text, bg=bg, fg=fg,
                      activebackground=bg_h, activeforeground=fg_h, command=cmd, **btn_style)
        b.grid(row=0, column=col, padx=6)
        b.bind("<Enter>", lambda e: b.config(bg=bg_h, fg=fg_h))
        b.bind("<Leave>", lambda e: b.config(bg=bg,   fg=fg))

    make_btn("Auto-install",   "#ff4655", "#ffffff", "#cc2233", "#ffffff", on_auto,   0)
    make_btn("Manual install", "#2a2a2a", "#cccccc", "#3d3d3d", "#ffffff", on_manual, 1)
    make_btn("Cancel",         "#1a1a1a", "#777777", "#2a2a2a", "#aaaaaa", on_cancel, 2)

    dialog.protocol("WM_DELETE_WINDOW", on_cancel)
    dialog.wait_window()
    root.destroy()

    if choice["value"] in ("cancel", None):
        raise SystemExit(0)

    if choice["value"] == "manual":
        webbrowser.open(WEBVIEW2_DOWNLOAD_URL)
        raise SystemExit(0)

    if choice["value"] == "auto":
        root2 = tk.Tk()
        root2.withdraw()
        info = tk.Toplevel(root2)
        info.title("EasyTS — Downloading WebView2")
        info.resizable(False, False)
        info.configure(bg="#111111")
        info.attributes("-topmost", True)
        iw, ih = 340, 90
        info.geometry(f"{iw}x{ih}+{(info.winfo_screenwidth()-iw)//2}+{(info.winfo_screenheight()-ih)//2}")
        tk.Label(info, text="Downloading WebView2 installer...",
                 bg="#111111", fg="#cccccc", font=("Segoe UI", 10)).pack(expand=True)
        info.update()
        try:
            bootstrapper = download_webview2_bootstrapper()
        finally:
            info.destroy()
            root2.destroy()
        run_webview2_installer(bootstrapper)
        try:
            os.remove(bootstrapper)
        except Exception:
            pass

def ensure_webview2() -> None:
    if not is_webview2_installed():
        prompt_webview2()


def download_html(url: str) -> str:
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")


class Api:
    def __init__(self, window_ref=None):
        self._window = window_ref

    def close(self):
        if self._window:
            self._window.destroy()

    def minimize(self):
        if self._window:
            self._window.minimize()

    def open_url(self, url: str) -> None:
        webbrowser.open(url)

    def get_version(self) -> str:
        return CURRENT_VERSION

    def get_accounts(self) -> list:
        accounts = load_accounts()
        for acc in accounts:
            acc["backup_date"] = get_backup_date(acc["folder"])
        return accounts

    def clear_accounts(self) -> dict:
        try:
            save_accounts([])
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def open_backup_folder(self) -> None:
        folder = os.path.join(get_easysts_dir(), "Backups")
        os.makedirs(folder, exist_ok=True)
        subprocess.Popen(["explorer", folder])

    def get_read_only_lock_enabled(self) -> bool:
        return is_read_only_lock_enabled()

    def set_read_only_lock_enabled(self, enabled: bool) -> dict:
        try:
            set_read_only_lock_enabled(bool(enabled))
            return {"success": True, "enabled": is_read_only_lock_enabled()}
        except Exception as e:
            return {"success": False, "message": str(e)}


    def get_presets(self) -> list:
        return load_presets()

    def save_preset(self, name: str, resolution: str) -> dict:
        presets = load_presets()
        for p in presets:
            if p["name"] == name:
                p["resolution"] = resolution
                save_presets(presets)
                return {"success": True}
        presets.append({"name": name, "resolution": resolution})
        save_presets(presets)
        return {"success": True}

    def delete_preset(self, name: str) -> dict:
        presets = [p for p in load_presets() if p["name"] != name]
        save_presets(presets)
        return {"success": True}

    def _check_valorant_not_running(self) -> bool:
        if is_valorant_running():
            log_to_ui(self._window,
                      "VALORANT is currently running. Please close it before applying.", "error")
            return False
        return True

    def apply_stretched(self, resolution_str: str) -> dict:
        match = re.match(r"^(\d{3,4})x(\d{3,4})$", resolution_str.strip().lower())
        if not match:
            return {"success": False}

        if not self._check_valorant_not_running():
            return {"success": False}

        width  = int(match.group(1))
        height = int(match.group(2))

        try:
            log_to_ui(self._window, "Initializing...", "info")
            saved_config_dir = get_valorant_config_path()
            log_to_ui(self._window, "VALORANT config directory found.", "info")

            lockfile_path = None
            for attempt in range(3):
                lockfile_path = find_riot_lockfile()
                if lockfile_path:
                    break
                if attempt < 2:
                    retry = self._window.create_confirmation_dialog(
                        "Riot Client Not Found",
                        "Riot Client lockfile not found.\n\n"
                        "Please open Riot Client as a visible window, then click OK to retry."
                    )
                    if not retry:
                        log_to_ui(self._window, "Cancelled by user.", "muted")
                        return {"success": False}
                    time.sleep(2)
                else:
                    raise ValorantConfigError(
                        "Riot Client lockfile not found after 3 attempts. "
                        "Make sure Riot Client is open and visible."
                    )

            log_to_ui(self._window, "Lockfile found.", "info")
            name, pid, port, password, protocol = read_riot_lockfile(lockfile_path)
            auth_token = base64.b64encode(f"riot:{password}".encode()).decode()
            log_to_ui(self._window, f"Connected to Riot Client on port {port}.", "info")

            log_to_ui(self._window, "Fetching VALORANT account...", "info")
            puuid, region_folder, name_tag = get_riot_account_info(port, auth_token)
            expected_folder = f"{puuid}-{region_folder}"
            config_targets = resolve_account_configs(saved_config_dir, puuid, region_folder)
            account_folder = config_targets[0][0]

            if account_folder != expected_folder:
                log_to_ui(
                    self._window,
                    f"Region folder mismatch detected. Riot reported {expected_folder}, using {account_folder}.",
                    "info"
                )

            if len(config_targets) > 1:
                log_to_ui(
                    self._window,
                    f"Found {len(config_targets)} config folders for this account. Applying to all of them.",
                    "info"
                )

            log_to_ui(self._window, f"Account: {name_tag} - {account_folder}", "success")
            log_to_ui(self._window, "Backing up config...", "info")

            for target_folder, config_file in config_targets:
                backup_config(config_file, target_folder)

            log_to_ui(self._window, f"Applying {width}x{height} + fill mode...", "info")

            for target_folder, config_file in config_targets:
                modify_game_user_settings(config_file, width, height)
                if is_read_only_lock_enabled():
                    make_file_read_only(config_file)
                else:
                    make_file_writable(config_file)

            if is_read_only_lock_enabled():
                log_to_ui(self._window, "Read-only lock enabled. Config locked after applying.", "info")
            else:
                log_to_ui(self._window, "Read-only lock disabled. Config left writable after applying.", "info")

            upsert_account(name_tag, account_folder)
            log_to_ui(self._window,
                      f"Done! {width}x{height} applied for {name_tag}. You can now launch VALORANT.",
                      "success")
            self._window.evaluate_js("window.refreshAccounts();")
            return {"success": True}

        except Exception as e:
            log_to_ui(self._window, f"Error: {e}", "error")
            return {"success": False}


    def apply_to_saved(self, folder: str, resolution_str: str) -> dict:
        match = re.match(r"^(\d{3,4})x(\d{3,4})$", resolution_str.strip().lower())
        if not match:
            log_to_ui(self._window, "Invalid resolution format.", "error")
            return {"success": False}

        if not self._check_valorant_not_running():
            return {"success": False}

        width  = int(match.group(1))
        height = int(match.group(2))

        try:
            saved_config_dir = get_valorant_config_path()
            config_targets = resolve_saved_configs(saved_config_dir, folder)
            resolved_folder = config_targets[0][0]

            name_tag = next((a["name_tag"] for a in load_accounts() if a["folder"] == folder), folder)
            if resolved_folder != folder:
                log_to_ui(self._window, f"Saved folder moved from {folder} to {resolved_folder}.", "info")
                folder = resolved_folder

            if len(config_targets) > 1:
                log_to_ui(
                    self._window,
                    f"Found {len(config_targets)} config folders for this account. Applying to all of them.",
                    "info"
                )

            log_to_ui(self._window, f"Account: {name_tag} - {folder}", "success")
            log_to_ui(self._window, "Backing up config...", "info")

            for target_folder, config_file in config_targets:
                backup_config(config_file, target_folder)

            log_to_ui(self._window, f"Applying {width}x{height} + fill mode...", "info")

            for target_folder, config_file in config_targets:
                modify_game_user_settings(config_file, width, height)
                if is_read_only_lock_enabled():
                    make_file_read_only(config_file)
                else:
                    make_file_writable(config_file)

            if is_read_only_lock_enabled():
                log_to_ui(self._window, "Read-only lock enabled. Config locked after applying.", "info")
            else:
                log_to_ui(self._window, "Read-only lock disabled. Config left writable after applying.", "info")

            upsert_account(name_tag, folder)
            log_to_ui(self._window,
                      f"Done! {width}x{height} applied for {name_tag}. You can now launch VALORANT.",
                      "success")
            self._window.evaluate_js("window.refreshAccounts();")
            return {"success": True}

        except Exception as e:
            log_to_ui(self._window, f"Error: {e}", "error")
            return {"success": False}


    def check_black_bars_needed(self) -> bool:
        try:
            base_key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\ControlSet001\Control\GraphicsDrivers\Configuration"
            )
            found_any = False
            needs_fix = False
            i = 0
            while True:
                try:
                    config_name = winreg.EnumKey(base_key, i)
                    try:
                        sub_key = winreg.OpenKey(base_key, config_name + r"\00\00")
                        try:
                            val, _ = winreg.QueryValueEx(sub_key, "Scaling")
                            found_any = True
                            if val != 3:
                                needs_fix = True
                        except FileNotFoundError:
                            pass
                        winreg.CloseKey(sub_key)
                    except OSError:
                        pass
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(base_key)
            return found_any and needs_fix
        except Exception:
            return False

    def fix_black_bars(self) -> dict:
        ps_script = r"""
$regBase = "HKLM:\SYSTEM\ControlSet001\Control\GraphicsDrivers\Configuration"
$changed = 0
$failed  = 0

Write-Host ""
Write-Host "  EasyTS - Fix Black Bars" -ForegroundColor Red
Write-Host "  ========================" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Setting display scaling to Full Panel for all configurations..." -ForegroundColor Gray
Write-Host ""

try {
    $configs = Get-ChildItem -Path $regBase -ErrorAction Stop
} catch {
    Write-Host "  ERROR: Could not open registry path." -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)"
    Write-Host ""
    Read-Host "  Press ENTER to exit"
    exit 1
}

foreach ($config in $configs) {
    $sub00 = Join-Path $config.PSPath "00"
    if (-not (Test-Path $sub00)) { continue }
    $sub0000 = Join-Path $sub00 "00"
    if (-not (Test-Path $sub0000)) { continue }

    $scalingPath = $sub0000
    $val = Get-ItemProperty -Path $scalingPath -Name "Scaling" -ErrorAction SilentlyContinue
    if ($null -eq $val) { continue }

    try {
        Set-ItemProperty -Path $scalingPath -Name "Scaling" -Value 3 -Type DWord -ErrorAction Stop
        Write-Host "  [OK] $($config.PSChildName)" -ForegroundColor Green
        $changed++
    } catch {
        Write-Host "  [FAIL] $($config.PSChildName): $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}

Write-Host ""
if ($changed -eq 0 -and $failed -eq 0) {
    Write-Host "  No Scaling registry keys found on this system." -ForegroundColor Yellow
    Write-Host "  This fix may not apply to your GPU or driver." -ForegroundColor Yellow
} else {
    Write-Host "  Done. $changed key(s) updated, $failed failed." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Please RESTART your PC for changes to take effect." -ForegroundColor Yellow
}

Write-Host ""
Read-Host "  Press ENTER to close"
"""
        try:
            ps_file = tempfile.mktemp(suffix=".ps1", prefix="EasyTS_blackbars_")
            with open(ps_file, "w", encoding="utf-8") as f:
                f.write(ps_script)

            ps_cmd = (
                "Start-Process powershell -ArgumentList "
                "'-ExecutionPolicy Bypass -File \"" + ps_file + "\"' "
                "-Verb RunAs -Wait"
            )

            def _launch():
                result = subprocess.run(["powershell.exe", "-Command", ps_cmd])
                if result.returncode != 0:
                    log_to_ui(self._window,
                              "UAC prompt was denied. Administrator permissions are required to apply this fix.",
                              "error")

            threading.Thread(target=_launch, daemon=True).start()
            log_to_ui(self._window,
                      "Black bars fix launched — accept the UAC prompt to continue.", "info")
            return {"success": True}
        except Exception as e:
            log_to_ui(self._window, f"Error launching fix: {e}", "error")
            return {"success": False}


    def restore_account(self, folder: str) -> dict:
        try:
            saved_config_dir = get_valorant_config_path()
            config_targets = resolve_saved_configs(saved_config_dir, folder)

            restored = 0
            for target_folder, config_file in config_targets:
                bak_path = get_backup_path(target_folder, create_dir=False)
                if not os.path.isfile(bak_path):
                    continue
                make_file_writable(config_file)
                shutil.copy2(bak_path, config_file)
                make_file_writable(config_file)
                restored += 1

            if restored == 0:
                log_to_ui(self._window, "No backup found for this account.", "error")
                return {"success": False}

            name_tag = next((a["name_tag"] for a in load_accounts() if a["folder"] == folder), folder)
            log_to_ui(self._window, f"Backup restored for {name_tag} across {restored} config folder(s).", "success")
            return {"success": True}

        except Exception as e:
            log_to_ui(self._window, f"Error: {e}", "error")
            return {"success": False}




def main():
    ensure_webview2()

    html_content = download_html(
        "https://raw.githubusercontent.com/ahhmilo/EasyTS/refs/heads/main/index.html"
    )

    api    = Api.__new__(Api)
    window = webview.create_window(
        title     = "EasyTS",
        html      = html_content,
        js_api    = api,
        width     = 800,
        height    = 620,
        resizable = False,
        frameless = True,
        easy_drag = True,
    )
    api._window = window
    webview.start()


if __name__ == "__main__":
    main()
