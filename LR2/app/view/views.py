import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('1280x720')
        self.title('Facility Account')

        self.main_window()

    def main_window(self):
        show_departments_btn = ctk.CTkButton(self, text='Просмотр подразделений', width=350,
                                             height=150)
        show_employees_btn = ctk.CTkButton(self, text='Просмотр сотрудников', width=350,
                                           height=150)

        show_departments_btn.place(relx=0.5, rely=0.7, anchor='center')
        show_employees_btn.place(relx=0.5, rely=0.2, anchor='center')
