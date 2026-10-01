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
import re
import json
import time
import base64
import ctypes
import winreg
import threading
import subprocess
import tempfile
import textwrap
import webbrowser
import urllib.request
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple

CURRENT_VERSION = "v4.0.0"
GITHUB_URL      = "https://github.com/ahhmilo/EasyTS"
HTML_URL        = "https://raw.githubusercontent.com/ahhmilo/EasyTS/refs/heads/main/index.html"

WEBVIEW2_DOWNLOAD_URL = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"
WEBVIEW2_REGISTRY_KEYS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
    (winreg.HKEY_CURRENT_USER,  r"Software\Microsoft\EdgeUpdate\ClientState\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
]

CREATE_NO_WINDOW      = 0x08000000
ENUM_CURRENT_SETTINGS = 0xFFFFFFFF
DM_PELSWIDTH          = 0x00080000
DM_PELSHEIGHT         = 0x00100000
SEE_MASK_NOCLOSEPROCESS = 0x00000040
SW_HIDE               = 0
ERROR_CANCELLED       = 1223
MAX_ELEVATED_PARAMS   = 1900

DISPLAY_CHANGE_MESSAGES = {
    1:  "Windows needs a restart before it can apply {w}x{h}.",
    -1: "The display driver could not switch to {w}x{h}.",
    -2: "Windows rejected {w}x{h}. This usually means the resolution is not registered as a custom resolution in your GPU driver yet. Check the setup guide.",
    -3: "Windows could not save the display settings for {w}x{h}.",
    -4: "Windows rejected the display change request for {w}x{h}.",
    -5: "Windows rejected the display change request for {w}x{h}.",
    -6: "Windows could not apply {w}x{h} with the current multi-display setup.",
}

VALORANT_PROCESS        = "valorant-win64-shipping.exe"
WATCH_INTERVAL          = 4
WATCH_MISSES_REQUIRED   = 2
MIN_DIMENSION           = 200
MAX_DIMENSION           = 16384

RESOLUTION_PATTERN = re.compile(r"^\s*(\d{3,5})\s*[x\u00d7,\s]\s*(\d{3,5})\s*$", re.IGNORECASE)

DEFAULT_SETTINGS = {"auto_restore": True}

DRIVER_STATUS_SCRIPT = (
    "Get-PnpDevice -Class Monitor -PresentOnly -ErrorAction SilentlyContinue | "
    "Select-Object InstanceId,FriendlyName,Status | ConvertTo-Json -Compress"
)

BLACK_BARS_SCRIPT = (
    r"$b='HKLM:\SYSTEM\ControlSet001\Control\GraphicsDrivers\Configuration';$c=0;$f=0;"
    r"try{$k=Get-ChildItem $b -ErrorAction Stop}catch{exit 2};"
    r"foreach($i in $k){$p=Join-Path $i.PSPath '00\00';"
    r"if($null -ne (Get-ItemProperty $p -Name Scaling -ErrorAction SilentlyContinue)){"
    r"try{Set-ItemProperty $p -Name Scaling -Value 3 -Type DWord -ErrorAction Stop;$c++}catch{$f++}}};"
    r"if($f -gt 0){exit 2};if($c -eq 0){exit 3};exit 0"
)


class DisplayError(Exception):
    pass


class ElevationDenied(Exception):
    pass


class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName",         ctypes.c_uint16 * 32),
        ("dmSpecVersion",        ctypes.c_uint16),
        ("dmDriverVersion",      ctypes.c_uint16),
        ("dmSize",               ctypes.c_uint16),
        ("dmDriverExtra",        ctypes.c_uint16),
        ("dmFields",             ctypes.c_uint32),
        ("dmPositionX",          ctypes.c_int32),
        ("dmPositionY",          ctypes.c_int32),
        ("dmDisplayOrientation", ctypes.c_uint32),
        ("dmDisplayFixedOutput", ctypes.c_uint32),
        ("dmColor",              ctypes.c_int16),
        ("dmDuplex",             ctypes.c_int16),
        ("dmYResolution",        ctypes.c_int16),
        ("dmTTOption",           ctypes.c_int16),
        ("dmCollate",            ctypes.c_int16),
        ("dmFormName",           ctypes.c_uint16 * 32),
        ("dmLogPixels",          ctypes.c_uint16),
        ("dmBitsPerPel",         ctypes.c_uint32),
        ("dmPelsWidth",          ctypes.c_uint32),
        ("dmPelsHeight",         ctypes.c_uint32),
        ("dmDisplayFlags",       ctypes.c_uint32),
        ("dmDisplayFrequency",   ctypes.c_uint32),
        ("dmICMMethod",          ctypes.c_uint32),
        ("dmICMIntent",          ctypes.c_uint32),
        ("dmMediaType",          ctypes.c_uint32),
        ("dmDitherType",         ctypes.c_uint32),
        ("dmReserved1",          ctypes.c_uint32),
        ("dmReserved2",          ctypes.c_uint32),
        ("dmPanningWidth",       ctypes.c_uint32),
        ("dmPanningHeight",      ctypes.c_uint32),
    ]


class SHELLEXECUTEINFOW(ctypes.Structure):
    _fields_ = [
        ("cbSize",         ctypes.c_uint32),
        ("fMask",          ctypes.c_uint32),
        ("hwnd",           ctypes.c_void_p),
        ("lpVerb",         ctypes.c_wchar_p),
        ("lpFile",         ctypes.c_wchar_p),
        ("lpParameters",   ctypes.c_wchar_p),
        ("lpDirectory",    ctypes.c_wchar_p),
        ("nShow",          ctypes.c_int),
        ("hInstApp",       ctypes.c_void_p),
        ("lpIDList",       ctypes.c_void_p),
        ("lpClass",        ctypes.c_wchar_p),
        ("hkeyClass",      ctypes.c_void_p),
        ("dwHotKey",       ctypes.c_uint32),
        ("hIconOrMonitor", ctypes.c_void_p),
        ("hProcess",       ctypes.c_void_p),
    ]


_user32_cache = None

def _user32():
    global _user32_cache
    if _user32_cache is None:
        lib = ctypes.WinDLL("user32", use_last_error=True)
        lib.EnumDisplaySettingsW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.POINTER(DEVMODE)]
        lib.EnumDisplaySettingsW.restype  = ctypes.c_int
        lib.ChangeDisplaySettingsW.argtypes = [ctypes.POINTER(DEVMODE), ctypes.c_uint32]
        lib.ChangeDisplaySettingsW.restype  = ctypes.c_int32
        _user32_cache = lib
    return _user32_cache

def get_display_resolution() -> Tuple[int, int]:
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)
    if not _user32().EnumDisplaySettingsW(None, ENUM_CURRENT_SETTINGS, ctypes.byref(dm)):
        raise DisplayError("Could not read the current display resolution.")
    return int(dm.dmPelsWidth), int(dm.dmPelsHeight)

def change_display_resolution(width: int, height: int) -> None:
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)
    _user32().EnumDisplaySettingsW(None, ENUM_CURRENT_SETTINGS, ctypes.byref(dm))
    dm.dmPelsWidth  = width
    dm.dmPelsHeight = height
    dm.dmFields     = DM_PELSWIDTH | DM_PELSHEIGHT
    code = _user32().ChangeDisplaySettingsW(ctypes.byref(dm), 0)
    if code != 0:
        template = DISPLAY_CHANGE_MESSAGES.get(code, "Windows could not apply {w}x{h} (code {c}).")
        raise DisplayError(template.format(w=width, h=height, c=code))

def parse_resolution(text) -> Tuple[int, int]:
    match = RESOLUTION_PATTERN.match(str(text))
    if not match:
        raise ValueError("Invalid format. Use WIDTHxHEIGHT, for example 1440x1080.")
    width, height = int(match.group(1)), int(match.group(2))
    if not (MIN_DIMENSION <= width <= MAX_DIMENSION and MIN_DIMENSION <= height <= MAX_DIMENSION):
        raise ValueError("That resolution is outside the supported range.")
    return width, height


def log_to_ui(window, message: str, msg_type: str = "info"):
    window.evaluate_js(f"window.appendLog({json.dumps(message)}, {json.dumps(msg_type)});")


def get_easysts_dir() -> str:
    path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "EasyTS")
    os.makedirs(path, exist_ok=True)
    return path

def read_json_file(name: str, fallback):
    path = os.path.join(get_easysts_dir(), name)
    if not os.path.isfile(path):
        return fallback
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return fallback

def write_json_file(name: str, data) -> None:
    with open(os.path.join(get_easysts_dir(), name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_settings() -> dict:
    data = read_json_file("settings.json", {})
    settings = DEFAULT_SETTINGS.copy()
    if isinstance(data, dict):
        for key in DEFAULT_SETTINGS:
            if key in data:
                settings[key] = bool(data[key])
    return settings

def save_settings(settings: dict) -> None:
    write_json_file("settings.json", settings)

def load_presets() -> list:
    data = read_json_file("presets.json", [])
    if not isinstance(data, list):
        return []
    return [p for p in data if isinstance(p, dict) and "name" in p and "resolution" in p]

def save_presets(presets: list) -> None:
    write_json_file("presets.json", presets)

def load_display_state() -> dict:
    data = read_json_file("display_state.json", {})
    if not isinstance(data, dict):
        return {}
    original = data.get("original")
    if not (isinstance(original, list) and len(original) == 2 and all(isinstance(v, int) for v in original)):
        return {}
    return data

def save_display_state(state: dict) -> None:
    write_json_file("display_state.json", state)

def clear_display_state() -> None:
    path = os.path.join(get_easysts_dir(), "display_state.json")
    if os.path.isfile(path):
        os.remove(path)


def is_valorant_running() -> bool:
    try:
        result = subprocess.run(
            ["tasklist", "/NH", "/FO", "CSV"],
            capture_output=True, text=True, errors="replace",
            creationflags=CREATE_NO_WINDOW
        )
        return VALORANT_PROCESS in result.stdout.lower()
    except Exception:
        return False


def run_powershell(script: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
         "-Command", "[Console]::OutputEncoding=[Text.Encoding]::UTF8;" + script],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=timeout, creationflags=CREATE_NO_WINDOW
    )

def build_elevated_params(script: str) -> str:
    encoded = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
    params = f"-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -EncodedCommand {encoded}"
    if len(params) > MAX_ELEVATED_PARAMS:
        raise ValueError("The elevated script is too long.")
    return params

def run_elevated_powershell(script: str, timeout_ms: int = 120000) -> int:
    params = build_elevated_params(script)

    shell32  = ctypes.WinDLL("shell32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    shell32.ShellExecuteExW.argtypes = [ctypes.POINTER(SHELLEXECUTEINFOW)]
    shell32.ShellExecuteExW.restype  = ctypes.c_int
    kernel32.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel32.WaitForSingleObject.restype  = ctypes.c_uint32
    kernel32.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32)]
    kernel32.GetExitCodeProcess.restype  = ctypes.c_int
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel32.CloseHandle.restype  = ctypes.c_int

    info = SHELLEXECUTEINFOW()
    info.cbSize       = ctypes.sizeof(SHELLEXECUTEINFOW)
    info.fMask        = SEE_MASK_NOCLOSEPROCESS
    info.lpVerb       = "runas"
    info.lpFile       = "powershell.exe"
    info.lpParameters = params
    info.nShow        = SW_HIDE

    if not shell32.ShellExecuteExW(ctypes.byref(info)):
        if ctypes.get_last_error() == ERROR_CANCELLED:
            raise ElevationDenied()
        raise OSError("Could not start the elevated process.")
    if not info.hProcess:
        raise OSError("The elevated process did not return a handle.")

    try:
        if kernel32.WaitForSingleObject(info.hProcess, timeout_ms) != 0:
            raise TimeoutError("The elevated process took too long to finish.")
        code = ctypes.c_uint32()
        kernel32.GetExitCodeProcess(info.hProcess, ctypes.byref(code))
        return int(code.value)
    finally:
        kernel32.CloseHandle(info.hProcess)


def list_monitor_devices() -> list:
    try:
        result = run_powershell(DRIVER_STATUS_SCRIPT)
        raw = result.stdout.strip()
        if not raw:
            return []
        data = json.loads(raw)
    except Exception:
        return []
    if isinstance(data, dict):
        data = [data]
    devices = []
    for item in data if isinstance(data, list) else []:
        if isinstance(item, dict) and item.get("InstanceId"):
            devices.append({
                "instance_id": item["InstanceId"],
                "name":        item.get("FriendlyName") or "Monitor",
                "status":      str(item.get("Status") or ""),
            })
    return devices

def get_driver_status() -> str:
    devices = list_monitor_devices()
    if not devices:
        return "not_found"
    return "enabled" if any(d["status"].upper() == "OK" for d in devices) else "disabled"

def build_driver_script(enable: bool) -> str:
    cmdlet = "Enable-PnpDevice" if enable else "Disable-PnpDevice"
    return (
        "$d=@(Get-PnpDevice -Class Monitor -PresentOnly -ErrorAction SilentlyContinue);"
        "if($d.Count -eq 0){exit 3};$f=0;"
        f"foreach($m in $d){{try{{{cmdlet} -InstanceId $m.InstanceId -Confirm:$false -ErrorAction Stop}}catch{{$f++}}}};"
        "if($f -eq $d.Count){exit 2};exit 0"
    )



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



def black_bars_needed() -> bool:
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


def download_html(url: str) -> str:
    with urllib.request.urlopen(url, timeout=15) as response:
        return response.read().decode("utf-8")


def show_fatal_error(message: str) -> None:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showerror("EasyTS", message, parent=root)
    root.destroy()


class Api:
    def __init__(self):
        self._window  = None
        self._lock    = threading.RLock()
        self._stop    = threading.Event()
        self._watcher = None
        self._seen    = False

    def _log(self, message: str, msg_type: str = "info") -> None:
        if self._window:
            try:
                log_to_ui(self._window, message, msg_type)
            except Exception:
                pass

    def _notify(self) -> None:
        if self._window:
            try:
                self._window.evaluate_js("window.refreshDisplay && window.refreshDisplay();")
            except Exception:
                pass

    def _watching(self) -> bool:
        return self._watcher is not None and self._watcher.is_alive() and not self._stop.is_set()

    def _start_watcher(self) -> None:
        if self._watching():
            return
        stop = threading.Event()
        self._stop    = stop
        self._seen    = False
        self._watcher = threading.Thread(target=self._watch_loop, args=(stop,), daemon=True)
        self._watcher.start()

    def _stop_watcher(self) -> None:
        self._stop.set()
        self._watcher = None

    def _watch_loop(self, stop: threading.Event) -> None:
        misses = 0
        while not stop.wait(WATCH_INTERVAL):
            if is_valorant_running():
                self._seen = True
                misses = 0
                continue
            if not self._seen:
                continue
            misses += 1
            if misses < WATCH_MISSES_REQUIRED:
                continue
            if stop.is_set():
                return
            self._log("VALORANT closed. Restoring your display resolution...", "info")
            self.restore_display()
            return

    def _snapshot(self) -> dict:
        current = get_display_resolution()
        state   = load_display_state()
        original = state.get("original")
        if original and tuple(original) == current:
            clear_display_state()
            self._stop_watcher()
            original = None
        return {
            "current":       list(current),
            "original":      original,
            "watching":      self._watching(),
            "valorant_seen": self._seen,
            "auto_restore":  load_settings()["auto_restore"],
        }

    def close(self):
        if not self._window:
            return
        try:
            snap = self._snapshot()
        except Exception:
            snap = {}
        if snap.get("original") and snap.get("watching"):
            cw, ch = snap["current"]
            ow, oh = snap["original"]
            message = (
                f"Your display is still {cw}x{ch}. EasyTS restores {ow}x{oh} automatically when VALORANT "
                "closes, but only while EasyTS is open.\n\nClose EasyTS anyway? You will need to restore "
                "your resolution yourself."
            )
            if not self._window.create_confirmation_dialog("EasyTS", message):
                return
        self._stop_watcher()
        self._window.destroy()

    def minimize(self):
        if self._window:
            self._window.minimize()

    def open_url(self, url: str) -> None:
        webbrowser.open(url)

    def get_version(self) -> str:
        return CURRENT_VERSION

    def open_data_folder(self) -> None:
        subprocess.Popen(["explorer", get_easysts_dir()])

    def get_display_state(self) -> dict:
        try:
            return self._snapshot()
        except Exception as e:
            return {"error": str(e)}

    def apply_resolution(self, resolution_str: str) -> dict:
        try:
            width, height = parse_resolution(resolution_str)
        except ValueError as e:
            self._log(str(e), "error")
            return {"success": False, "message": str(e)}

        with self._lock:
            try:
                current = get_display_resolution()
                if current == (width, height):
                    self._log(f"Display is already {width}x{height}. Nothing to change.", "muted")
                    self._notify()
                    return {"success": True, "changed": False}

                state = load_display_state()
                newly_saved = not state.get("original")
                if newly_saved:
                    state = {"original": list(current)}
                state["applied"] = [width, height]
                state["at"]      = time.strftime("%Y-%m-%d %H:%M")
                save_display_state(state)

                try:
                    change_display_resolution(width, height)
                except DisplayError:
                    if newly_saved:
                        clear_display_state()
                    raise

                ow, oh = state["original"]
                if (ow, oh) == (width, height):
                    clear_display_state()
                    self._stop_watcher()
                    self._log(f"Display restored to {width}x{height}.", "success")
                else:
                    self._log(f"Display set to {width}x{height}. Original resolution {ow}x{oh} saved.", "success")
                    if load_settings()["auto_restore"]:
                        self._start_watcher()
                        self._log("Auto-restore is on. Keep EasyTS open and it will restore your resolution when VALORANT closes.", "info")
            except DisplayError as e:
                self._log(str(e), "error")
                return {"success": False, "message": str(e)}
            except Exception as e:
                self._log(f"Error: {e}", "error")
                return {"success": False, "message": str(e)}

        self._notify()
        return {"success": True, "changed": True}

    def restore_display(self) -> dict:
        with self._lock:
            try:
                original = load_display_state().get("original")
                if not original:
                    self._stop_watcher()
                    self._log("There is no saved resolution to restore.", "muted")
                    self._notify()
                    return {"success": True, "changed": False}

                ow, oh = original
                if get_display_resolution() != (ow, oh):
                    change_display_resolution(ow, oh)
                    self._log(f"Display restored to {ow}x{oh}.", "success")
                else:
                    self._log("Display is already at its original resolution.", "muted")
                clear_display_state()
                self._stop_watcher()
            except DisplayError as e:
                self._log(str(e), "error")
                self._notify()
                return {"success": False, "message": str(e)}
            except Exception as e:
                self._log(f"Error: {e}", "error")
                self._notify()
                return {"success": False, "message": str(e)}

        self._notify()
        return {"success": True, "changed": True}

    def dismiss_saved_display(self) -> dict:
        with self._lock:
            clear_display_state()
            self._stop_watcher()
        self._log("Saved original resolution dismissed.", "muted")
        self._notify()
        return {"success": True}

    def get_driver_status(self) -> str:
        return get_driver_status()

    def set_driver_enabled(self, enabled: bool) -> dict:
        enable = bool(enabled)
        label  = "on" if enable else "off"
        self._log(f"Turning the monitor driver {label}. Accept the UAC prompt to continue...", "info")
        try:
            code = run_elevated_powershell(build_driver_script(enable))
        except ElevationDenied:
            self._log("UAC prompt was denied. Administrator permission is required for this step.", "error")
            return {"success": False, "denied": True, "status": get_driver_status()}
        except Exception as e:
            self._log(f"Error: {e}", "error")
            return {"success": False, "status": get_driver_status()}

        status = get_driver_status()
        if status == "not_found":
            self._log("No monitor device was found. This step is not needed on this system.", "muted")
            return {"success": True, "status": status}

        expected = "enabled" if enable else "disabled"
        if status != expected and code == 0:
            time.sleep(1.5)
            status = get_driver_status()

        if status == expected:
            if enable:
                self._log("Monitor driver is on again.", "success")
            else:
                self._log("Monitor driver is off. Launch VALORANT now so it picks up the change.", "success")
            return {"success": True, "status": status}

        self._log(f"Could not turn the monitor driver {label}.", "error")
        return {"success": False, "status": status}

    def get_settings(self) -> dict:
        return load_settings()

    def set_auto_restore(self, enabled: bool) -> dict:
        enable   = bool(enabled)
        settings = load_settings()
        settings["auto_restore"] = enable
        try:
            save_settings(settings)
        except Exception as e:
            return {"success": False, "message": str(e)}

        with self._lock:
            if not enable:
                self._stop_watcher()
            elif load_display_state().get("original"):
                self._start_watcher()
        self._notify()
        return {"success": True, "enabled": enable}

    def get_presets(self) -> list:
        return load_presets()

    def save_preset(self, name: str, resolution: str) -> dict:
        try:
            width, height = parse_resolution(resolution)
        except ValueError as e:
            return {"success": False, "message": str(e)}
        value   = f"{width}x{height}"
        presets = load_presets()
        for p in presets:
            if p["name"] == value:
                p["resolution"] = value
                save_presets(presets)
                return {"success": True}
        presets.append({"name": value, "resolution": value})
        save_presets(presets)
        return {"success": True}

    def delete_preset(self, name: str) -> dict:
        save_presets([p for p in load_presets() if p["name"] != name])
        return {"success": True}

    def check_black_bars_needed(self) -> bool:
        return black_bars_needed()

    def fix_black_bars(self) -> dict:
        self._log("Applying the black bars fix. Accept the UAC prompt to continue...", "info")
        try:
            code = run_elevated_powershell(BLACK_BARS_SCRIPT)
        except ElevationDenied:
            self._log("UAC prompt was denied. Administrator permission is required for this fix.", "error")
            return {"success": False, "denied": True}
        except Exception as e:
            self._log(f"Error: {e}", "error")
            return {"success": False}

        if code == 0:
            self._log("Black bars fix applied. Restart your PC for it to take effect.", "success")
            return {"success": True}
        if code == 3:
            self._log("No display scaling entries were found. This fix does not apply to this system.", "muted")
            return {"success": True}
        self._log("The fix could not be applied to every display entry.", "error")
        return {"success": False}


def main():
    ensure_webview2()

    try:
        html_content = download_html(HTML_URL)
    except Exception:
        show_fatal_error(
            "EasyTS could not load its interface.\n\n"
            "Check your internet connection and try again."
        )
        return

    api    = Api()
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
