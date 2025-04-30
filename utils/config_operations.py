import configparser as cp
import winreg
import sys
import os
import globals
from tkinter.messagebox import showerror

DEFAULT_CONFIG = {
    "general": {
        "max_autosaves": 20,
        "autosave_delay_sec": 300,
        "new_process_window_time_sec": 10,
        "runned_process_time_sec": 259200,
        "open_window_on_start": True,
        "autostart": False
    }
}


def reset_config(cfg: cp.ConfigParser) -> None:
    cfg.read_dict(DEFAULT_CONFIG)
    with open("config.ini", "w") as file:
        cfg.write(file)


def repair_config(cfg: cp.ConfigParser) -> None:
    try:
        read_files: dict = cfg.read("config.ini")
    except Exception as e:
        showerror(str(type(e).__name__), str(e))
        reset_config(cfg)
        return

    if not read_files or "general" not in cfg.sections():
        reset_config(cfg)
    else:
        for key in DEFAULT_CONFIG["general"]:
            try:
                if key in cfg["general"]:
                    if (isinstance(DEFAULT_CONFIG["general"][key], int) and
                            not isinstance(DEFAULT_CONFIG["general"][key], bool)):
                        _ = cfg.getint("general", key)
                    elif isinstance(DEFAULT_CONFIG["general"][key], bool):
                        _ = cfg.getboolean("general", key)
                    else:
                        raise ValueError
                else:
                    raise ValueError
            except ValueError:
                cfg["general"][key] = str(DEFAULT_CONFIG["general"][key]).lower()

        with open("config.ini", "w") as file:
            cfg.write(file)


def get_config(cfg: cp.ConfigParser) -> None:
    cfg.read("config.ini")

    globals.config = {
        "max_autosaves": cfg.getint("general", "max_autosaves"),
        "autosave_delay": cfg.getint("general", "autosave_delay_sec"),
        "new_process_window_time": cfg.getint("general", "new_process_window_time_sec"),
        "open_window_on_start": cfg.getboolean("general", "open_window_on_start"),
        "runned_process_time": cfg.getint("general", "runned_process_time_sec"),
    }

    set_autostart(cfg.getboolean("general", "autostart"))


def set_autostart(enable: bool) -> None:
    try:
        if not isinstance(enable, bool):
            raise ValueError("Enable parameter must be boolean")

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                             winreg.KEY_ALL_ACCESS)

        app_path = os.path.abspath(sys.argv[0])
        app_name = os.path.splitext(os.path.basename(app_path))[0]

        try:
            winreg.QueryValueEx(key, app_name)
            key_exists = True
        except WindowsError:
            key_exists = False

        if enable:
            if not key_exists:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{app_path}"')
        else:
            if key_exists:
                winreg.DeleteValue(key, app_name)

        winreg.CloseKey(key)
    except Exception as e:
        showerror(str(type(e).__name__), str(e))


def handle_config() -> None:
    config = cp.ConfigParser()
    repair_config(config)
    get_config(config)


if __name__ == '__main__':
    handle_config()
