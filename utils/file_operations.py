from typing import Callable
from tkinter.messagebox import showerror
import sys
import globals
import json
import os
import time
import shutil
import datetime


def clear_runned_programs() -> None:
    def clear_runned(data: dict) -> dict:
        runned: dict = data["runned"].copy()
        for process, time_ in runned.items():
            if time_ < time.time() - globals.config["runned_process_time"] and process not in data["tracked"]:
                del data["runned"][process]
        return data

    change_data(clear_runned)


def remake_old_data() -> None:
    data: dict = get_data()

    if "times" in data and "programs" in data and "tracked" in data and "runned" in data:
        def remake_data(data: dict) -> dict:
            new_tracked: dict = {process: {"time": data["times"][process], "pid": data["programs"][process],
                                           "display_name": name, "last_run_time": 0}
                                 for process, name in data["tracked"].items()}
            return {"tracked": new_tracked, "runned": data["runned"]}

        change_data(remake_data)
        
    if isinstance(data["runned"], list):
        def convert_runned_to_dict(data: dict) -> dict:
            data["runned"] = {process: int(time.time()) for process in data["runned"]}
            return data

        change_data(convert_runned_to_dict)

    else:
        def add_last_run_time(data: dict) -> dict:
            for process, other in data["tracked"].items():
                if "last_run_time" not in other:
                    data["tracked"][process]["last_run_time"] = 0
            return data

        change_data(add_last_run_time)


def is_data_file(file_path: str, old_pattern: bool = False) -> bool:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        if content.strip():
            try:
                data: dict = json.loads(content)

                _, _ = data["tracked"], data["runned"]
                if old_pattern:
                    _, _ = data["programs"], data["times"]

                return True
            except (json.JSONDecodeError, KeyError):
                return False
        return False


def load_last_save() -> None:
    while os.listdir("Autosaves"):
        last_autosave: str = max(get_files_sorted_by_time("Autosaves"))

        if not is_data_file(last_autosave):
            os.remove(last_autosave)
        else:
            with open(last_autosave, "r") as file:
                save: dict = json.load(file)

            with open("data.json", "w") as file:
                json.dump(save, file, indent=4)

            remake_old_data()
            return
    if os.path.exists("data.json"):
        os.remove("data.json")
    create_data_file()


def get_files_sorted_by_time(folder_path: str) -> list[str]:
    all_file_paths: list = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]
    sorted_files: list = list(sorted(all_file_paths, key=os.path.getctime, reverse=True))

    return sorted_files


def delete_unnecessary_saves(max_file_count: int) -> None:
    files_sorted_by_time: list = get_files_sorted_by_time("Autosaves")

    if len(files_sorted_by_time) > max_file_count:
        for file_path in files_sorted_by_time[max_file_count:]:
            if os.path.exists(file_path):
                os.remove(file_path)


def save_data(folder_path: str) -> None:
    try:
        shutil.copy("data.json",
                    f"{folder_path}/data_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json")
    except Exception as e:
        showerror("Error", str(e))


def auto_save(delay_sec: int, max_file_count: int) -> None:
    while not globals.requested_to_quit:
        for _ in range(int(delay_sec*2)):
            if not globals.requested_to_quit:
                time.sleep(0.5)
            else:
                break
        if is_data_file("data.json"):
            if not os.path.exists("Autosaves"):
                os.makedirs("Autosaves")
            delete_unnecessary_saves(max_file_count-1)
            save_data("Autosaves")


def wait_for_file_operations() -> None:
    while globals.wait_for_write_data:
        time.sleep(0.45)

    globals.wait_for_write_data = True


def create_data_file() -> None:
    json_template = {
        "runned": {},
        "tracked": {}
    }

    wait_for_file_operations()

    with open("data.json", "w") as file:
        json.dump(json_template, file, indent=4)

    globals.wait_for_write_data = False


def get_data() -> dict:
    if not os.path.exists("data.json") and not os.path.exists("Autosaves"):
        create_data_file()
        return get_data()
    elif not os.path.exists("data.json") or not is_data_file("data.json"):
        load_last_save()
        return get_data()
    else:
        wait_for_file_operations()

        with open("data.json", "r") as file:
            data = json.load(file)

        globals.wait_for_write_data = False

        return data


def change_data(func: Callable) -> None:
    data: dict = func(get_data())

    wait_for_file_operations()

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    globals.wait_for_write_data = False


def resource_path(path: str, exe_path: str):
    # noinspection PyProtectedMember
    return os.path.join(sys._MEIPASS, exe_path) if getattr(sys, 'frozen', False) else (
        os.path.join(os.path.abspath('.'), path))
