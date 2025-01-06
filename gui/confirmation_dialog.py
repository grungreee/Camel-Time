import customtkinter as ctk


class ConfirmationDialog(ctk.CTk):
    def __init__(self, title: str = "Question", text: str = "Some question",
                 font_size: int = 20, destroy_after: int | float = None) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.geometry("290x170")
        self.title(title)

        self.answer: bool = False

        label_frame = ctk.CTkFrame(self, fg_color="#242424")
        label_frame.pack(padx=20, pady=(20, 0), fill=ctk.BOTH, expand=True)

        ctk.CTkLabel(label_frame, text=text, font=("Bold", font_size), anchor=ctk.CENTER).pack(expand=True)

        buttons_frame = ctk.CTkFrame(self, fg_color="#242424")
        buttons_frame.pack(padx=15, pady=(40, 20), fill=ctk.X)

        ctk.CTkButton(buttons_frame, text="Yes", width=120, command=self.answer_yes).pack(side=ctk.LEFT)
        ctk.CTkButton(buttons_frame, text="No", width=120, command=self.destroy_).pack(side=ctk.RIGHT)

        self.destroy_after_id = self.after(int(destroy_after*1000), self.destroy_)

        self.mainloop()

    def destroy_(self):
        self.after_cancel(self.destroy_after_id)
        self.withdraw()
        self.after(400, self.destroy)

    def answer_yes(self) -> None:
        self.answer = True
        self.destroy_()

    def get_answer(self) -> bool:
        return self.answer


def ask_yes_or_no(title: str = "Question", text: str = "Some question",
                  font_size: int = 20, destroy_after: int | float = 7) -> bool:
    return ConfirmationDialog(title, text, font_size, destroy_after).get_answer()


if __name__ == '__main__':
    ask_yes_or_no()
