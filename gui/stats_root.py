from utils.file_operations import get_data, resource_path
from utils.tray_icon import close_app
from utils.process_monitor import delete_tracked_process, add_tracked_process
from PIL import Image
from typing import Literal
import globals
import time
import customtkinter as ctk


class StatsRoot(ctk.CTk):
    def __init__(self, debug: bool = False) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.geometry("640x400")
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

        self.debug: bool = debug
        self.sorted_by_time: dict = {}
        self.recently_used_programs: dict = {}
        self.answer: str | None = None
        self.back_button: ctk.CTkButton | None = None
        self.top_by_time_programs: ctk.CTkScrollableFrame | None = None
        self.last_runned_programs_frame: ctk.CTkScrollableFrame | None = None

        self.arrow_icon = ctk.CTkImage(Image.open(resource_path("assets/arrow.png", "arrow.png")),
                                       size=(15, 15))

        self.init_main_page()

        if not self.debug:
            self.withdraw()

        if not globals.requested_to_quit:
            self.update_stats()

    def clear_root(self, without_back_button: bool = False) -> None:
        for widget in self.winfo_children():
            if without_back_button and widget == self.back_button and self.back_button.winfo_exists():
                continue

            widget.destroy()

    def init_main_page(self) -> None:
        self.clear_root()
        self.title(f"Camel Time {globals.__version__}")
        self.minsize(503, 120)

        upper_frame = ctk.CTkFrame(self, height=30, fg_color="#242424")
        upper_frame.pack_propagate(False)
        upper_frame.pack(padx=(15, 0), pady=(15, 0), fill=ctk.X, anchor=ctk.N)

        upper_frame_left = ctk.CTkFrame(upper_frame, height=30, fg_color="#242424", width=290)
        upper_frame_left.pack_propagate(False)
        upper_frame_left.pack(side=ctk.LEFT, expand=True, fill=ctk.X, padx=(0, 15))

        upper_frame_right = ctk.CTkFrame(upper_frame, height=30, fg_color="#242424", width=290)
        upper_frame_right.pack_propagate(False)
        upper_frame_right.pack(side=ctk.RIGHT, expand=True, fill=ctk.X)

        settings_icon = ctk.CTkImage(Image.open(resource_path("assets/settings.png", "settings.png")),
                                     size=(24, 24))
        ctk.CTkButton(upper_frame_left, image=settings_icon, text="", command=self.open_settings,
                      width=30).pack(side=ctk.LEFT)
        ctk.CTkLabel(upper_frame_left, text="Top programs by usage time", font=("Arial", 16)).pack(side=ctk.RIGHT,
                                                                                                   padx=(0, 10))
        ctk.CTkLabel(upper_frame_right, text="Recently run programs", font=("Arial", 16)).pack(side=ctk.RIGHT, padx=15)

        lower_frame = ctk.CTkFrame(self, fg_color="#242424")
        lower_frame.pack_propagate(False)
        lower_frame.pack(padx=15, pady=15, expand=True, fill=ctk.BOTH)

        self.top_by_time_programs = ctk.CTkScrollableFrame(lower_frame, width=275, height=330,
                                                           scrollbar_button_color="#3b3b3b",
                                                           scrollbar_button_hover_color="#4d4d4d")
        self.top_by_time_programs.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH, padx=(0, 15))

        self.last_runned_programs_frame = ctk.CTkScrollableFrame(lower_frame, width=275, height=330,
                                                                 scrollbar_button_color="#3b3b3b",
                                                                 scrollbar_button_hover_color="#4d4d4d")
        self.last_runned_programs_frame.pack(side=ctk.RIGHT, expand=True, fill=ctk.BOTH)

        self.update_stats()

    def open_settings(self) -> None:
        self.title(f"Camel Time {globals.__version__} - Settings")
        self.minsize(320, 270)

        if self.back_button is None or not self.back_button.winfo_exists():
            self.clear_root()
            self.back_button = ctk.CTkButton(self, image=self.arrow_icon, text="Back", command=self.init_main_page,
                                             width=70)
            self.back_button.pack(pady=(15, 0), padx=15, anchor=ctk.W)
        else:
            self.clear_root(without_back_button=True)
            self.back_button.configure(command=self.init_main_page)

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill=ctk.BOTH, padx=15, pady=15)

        central_frame = ctk.CTkFrame(frame, width=300, height=30)
        central_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkButton(central_frame, text="Delete tracked program",
                      command=lambda: self.enter_process("Enter tracked process to delete", command="Delete"),
                      width=175).pack(pady=(30, 0), padx=30)
        ctk.CTkButton(central_frame, text="Add tracked process",
                      command=lambda: self.enter_process("Enter the name of the process to track", command="Add"),
                      width=175).pack(pady=(15, 30), padx=30)

    def enter_process(self, text: str, command: Literal["Delete", "Add"]):
        def ok() -> None:
            status: bool = delete_tracked_process(process_entry.get()) if command == "Delete" else (
                add_tracked_process(process_entry.get(), name_entry.get()))
            if status:
                self.update_stats()
                return

        self.clear_root(without_back_button=True)
        self.title(f"Camel Time {globals.__version__} - {command} tracked process")
        self.minsize(390, 330 if command == "Add" else 290)
        self.back_button.configure(command=self.open_settings)

        frame = ctk.CTkFrame(self, width=300, height=30)
        frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(frame, text=text, font=("Arial", 17)).pack(pady=(30, 10))

        process_frame = ctk.CTkFrame(frame, width=300, height=30)
        process_frame.pack_propagate(False)
        process_frame.pack(pady=(0, 10 if command == "Add" else 20), padx=30)

        process_label = ctk.CTkLabel(process_frame, text="Process: ")
        process_label.pack(side=ctk.LEFT, padx=(5, 0))

        process_entry = ctk.CTkEntry(process_frame, width=200)
        process_entry.pack(side=ctk.RIGHT, padx=(0, 5))

        if command == "Add":
            name_frame = ctk.CTkFrame(frame, width=300, height=30)
            name_frame.pack_propagate(False)
            name_frame.pack(pady=(0, 20))

            name_label = ctk.CTkLabel(name_frame, text="Display name:")
            name_label.pack(side=ctk.LEFT, padx=(5, 0))

            name_entry = ctk.CTkEntry(name_frame, width=200)
            name_entry.pack(side=ctk.RIGHT, padx=(0, 5))

        button_frame = ctk.CTkFrame(frame, height=45, width=300)
        button_frame.pack_propagate(False)
        button_frame.pack(pady=(0, 30))

        ctk.CTkButton(button_frame, text="Ok", width=100, command=ok).pack(pady=7, padx=10, expand=True, fill=ctk.BOTH)

    def update_stats(self) -> None:
        if not (self.top_by_time_programs.winfo_exists() or self.last_runned_programs_frame.winfo_exists()):
            return

        data: dict = get_data()
        dict_of_programs: dict = {program_data["display_name"]: {"hours": round(program_data["time"] / 3600, 1),
                                                                 "in_game": program_data["pid"] is not None,
                                                                 "last_run_time": program_data["last_run_time"]}
                                  for program_data in data["tracked"].values()}

        self.sorted_by_time = dict(sorted(dict_of_programs.items(), key=lambda item: item[1]["hours"], reverse=True))
        self.recently_used_programs = dict(sorted(dict_of_programs.items(),
                                                  key=lambda item: (item[1]["in_game"], item[1]["last_run_time"]),
                                                  reverse=True))

        for widget in self.top_by_time_programs.winfo_children() + self.last_runned_programs_frame.winfo_children():
            widget.destroy()

        for program, other in self.sorted_by_time.items():
            ctk.CTkLabel(self.top_by_time_programs, text=f"{program} - {other["hours"]}h",
                         font=("Arial", 17), text_color="#40a16a" if other["in_game"] else None).pack(pady=4)

        for program, other in self.recently_used_programs.items():
            if time.time() - other["last_run_time"] < 604800:
                ctk.CTkLabel(self.last_runned_programs_frame, text=f"{program} - {other["hours"]}h",
                             font=("Arial", 17), text_color="#40a16a" if other["in_game"] else None).pack(pady=4)

    def on_window_close(self) -> None:
        if self.debug:
            close_app()
        else:
            self.withdraw()

    def show_stats_window(self) -> None:
        self.update_stats()
        self.deiconify()
