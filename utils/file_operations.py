from typing import Callable
from tkinter.messagebox import showerror
import sys
import globals
import json
import os
import time
import shutil
import datetime


def remake_old_data() -> None:
    if "runned" and "times" in get_data():
        def remake_data(data: dict) -> dict:
            new_tracked: dict = {process: {"time": data["times"][process], "pid": data["programs"][process],
                                           "display_name": name, "last_run_time": 0}
                                 for process, name in data["tracked"].items()}
            return {"tracked": new_tracked, "runned": data["runned"]}

        change_data(remake_data)
    else:
        def add_last_run_time(data: dict) -> dict:
            for process, other in data["tracked"].items():
                if "last_run_time" not in other:
                    data["tracked"][process]["last_run_time"] = 0
            return data

        change_data(add_last_run_time)


def is_data_file(file_path: str, old_pattern: bool = False):
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
        autosave_path: str = f"Autosaves\\{find_save_by_data("Autosaves", max)}"
        if not is_data_file(autosave_path):
            os.remove(autosave_path)
        else:
            with open(autosave_path, "r") as file:
                save: dict = json.load(file)

            with open("data.json", "w") as file:
                json.dump(save, file, indent=4)

            remake_old_data()
            return
    if os.path.exists("data.json"):
        os.remove("data.json")
    create_data_file()


def find_save_by_data(folder_path: str, min_or_max: Callable) -> str:
    list_of_saves_paths: list = list(map(lambda x: f"{folder_path}/{x}", os.listdir(folder_path)))
    return min_or_max(list_of_saves_paths, key=os.path.getctime).removeprefix(f"{folder_path}/")


def delete_unnecessary_save(max_file_count: int) -> None:
    if len(os.listdir("Autosaves")) == max_file_count:
        os.remove(f"Autosaves/{find_save_by_data("Autosaves", min_or_max=min)}")


def save_data(folder_path: str) -> None:
    try:
        shutil.copy("data.json",
                    f"{folder_path}/data_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json")
    except Exception as e:
        showerror("Error", str(e))


def auto_save(delay_min: int | float, max_file_count: int) -> None:
    while not globals.requested_to_quit:
        for _ in range(int(delay_min*60*2)):
            if not globals.requested_to_quit:
                time.sleep(0.5)
            else:
                break
        if is_data_file("data.json"):
            if not os.path.exists("Autosaves"):
                os.makedirs("Autosaves")
            delete_unnecessary_save(max_file_count)
            save_data("Autosaves")


def wait_for_file_operations() -> None:
    while globals.wait_for_write_data:
        time.sleep(0.45)

    globals.wait_for_write_data = True


def create_data_file() -> None:
    json_template = {
        "runned": globals.default_runned_apps,
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
