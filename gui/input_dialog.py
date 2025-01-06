import customtkinter as ctk
import re
import tkinter.messagebox


class InputDialog(ctk.CTk):
    def __init__(self, process_name: str | None = None, text: str = "Entry", title: str = "Input Dialog") -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.answer: str | None = process_name
        self.process_name = process_name

        self.geometry("300x240" if process_name is not None else "300x200")
        self.title(title)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.get_answer(None))

        self.label = ctk.CTkLabel(self, text=text, font=("Arial", 15, "bold"))
        self.label.pack(pady=(25, 15))

        self.entry = ctk.CTkEntry(self, width=250)
        self.entry.pack(pady=(0, 25))

        self.buttons_frame = ctk.CTkFrame(self, height=40, width=250)
        self.buttons_frame.pack()
        self.buttons_frame.pack_propagate(False)

        self.cancel_button = ctk.CTkButton(self.buttons_frame, text="Cancel",
                                           width=100, command=lambda: self.get_answer(None))
        self.cancel_button.pack(side=ctk.LEFT, padx=(15, 0))

        self.ok_button = ctk.CTkButton(self.buttons_frame, text="Ok", width=100, command=lambda: self.get_answer("ok"))
        self.ok_button.pack(side=ctk.RIGHT, padx=(0, 15))

        if process_name is not None:
            self.get_answer("keep", False)

            self.keep_button = ctk.CTkButton(self, text=f'Keep "{self.answer}"',
                                             width=220, command=lambda: self.get_answer("keep"))
            self.keep_button.pack(side=ctk.BOTTOM, pady=25)

        self.mainloop()

    def get_answer(self, answer: str | None, with_destroy: bool = True) -> None:
        if answer == "ok":
            if not self.entry.get():
                tkinter.messagebox.showwarning("Warning", "You can't leave an empty string")
                return
            self.answer = self.entry.get()
        elif answer == "keep":
            self.answer = re.search(r"^(.*)\..*$", self.process_name).group(1)
        elif answer is None:
            self.answer = None

        if with_destroy:
            self.withdraw()
            self.after(400, self.destroy)

    def get_input(self) -> str:
        return self.answer


def get_name(process_name: str | None = None, text: str = "Entry", title: str = "Input Dialog") -> str:
    return InputDialog(process_name, text, title).get_input()


if __name__ == '__main__':
    print(get_name(*["Process.exe" for _ in range(3)]))
