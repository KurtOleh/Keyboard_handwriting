from tkinter import *
from tkinter import messagebox as mb
from keyboard_script import WriteDown, Training, Authentication
import pickle


class Authorization(Frame):
    def __init__(self, win):
        super(Authorization, self).__init__()
        self.win = win
        self.attempts = 0
        self.win_input()

    def win_input(self):
        button_input = Button(self.win, text="Вход", font=("Times New Roman", 15), width=12, relief=FLAT, background="#c4c4cc",
                              foreground="black", height=3,
                              command=lambda: self.win_authorization(objects))
        button_input.place(x=110, y=110)

        button_reg = Button(self.win, text="Регистрация", font=("Times New Roman", 15), width=12, relief=FLAT,
                            background="#c4c4cc",
                            foreground="black", height=3, command=lambda: Registration())
        button_reg.place(x=255, y=110)

        objects = (button_input, button_reg)


    def win_authorization(self, objects):
        for items in objects:
            items.destroy()

        WriteDown()
        label = Label(self.win, text="Авторизация", font=("Arial 32", 22), bg='#2d557d', fg="White", width=25, height=1)
        label.pack()

        msg_login = Label(self.win, text="Логин", font=("Arial 32", 12), height=2)
        msg_login.pack()
        entry_login = Entry(self.win, width=43, textvariable=StringVar(), highlightthickness=1, relief=GROOVE,
                            font=("Arial 32", 10))
        entry_login.pack()

        msg_pass = Label(self.win, text="Пароль", font=("Arial 32", 13), height=2)
        msg_pass.pack()
        entry_pass = Entry(self.win, width=43, textvariable=StringVar(), show="●", relief=GROOVE, highlightthickness=1,
                           font=("Arial 32", 10))
        entry_pass.pack()

        button = Button(self.win, text="Вход", font=("Arial 32", 11), width=10, relief=FLAT, background="#34506b",
                        foreground="#ccc", height=1, command=lambda: self.authorization(entry_login.get(), entry_pass.get(), objects))
        button.place(relx=0.15, rely=0.60)

        bottom_login = Label(self.win, text="После ввода пароля нажмите 'Esc'", font=("System", 11), height=2)
        bottom_login.pack(side=BOTTOM)

        objects = (label, msg_login, entry_login, msg_pass, entry_pass, bottom_login, button)


    def authorization(self, login, password, objects):
        with open('pass_etalon.pickle', 'rb') as file:
            data_read = pickle.load(file)

        user = False
        if login:
            for i in data_read.keys():
                if i == password:
                    user = True
                    if Authentication(password).validation_check() is True:
                        for items in objects:
                            items.destroy()

                        Label(self.win, text="Добро пожаловать, {}!".format(login), font=("Arial 32", 22), fg="Black",
                              height=1).pack(pady=130)
                        break
                    else:
                        mb.showerror("Ошибка", "Вы не прошли этап биометрической проверки!")
                        self.quit_app()
                        break


            if user is False and self.attempts < 3:
                mb.showwarning("Внимание",
                               "Неверный пароль, попробуйте еще раз!\n"
                               "Или нажмите 'Регистрация' чтоб создать аккаунт!\n\n"
                               "Количество попыток для входа {}".format(3 - self.attempts))

                self.attempts += 1
            elif self.attempts == 3:
                mb.showerror("Ошибка", "Вы изчерпали все возможные попытки\nПопробуйте в другой раз!")
                self.quit_app()

        else:
            mb.showwarning("Внимание", "Пожалуйста, введите имя аккаунта!")

    def quit_app(self):
        self.destroy()
        exit()


class Registration(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("504x350+{0}+{1}".format(int(self.winfo_screenwidth() / 2) - 225, int(self.winfo_screenheight() / 2) - 225))
        self.title("Регистрация")
        self.resizable(False, False)
        self.win_registration()


    def win_registration(self):
        log_label = Label(self, text="Введите логин:", font=("Times new Roman", 15))
        log_label.pack()
        entry_login = Entry(self, width=35, textvariable=StringVar(), highlightthickness=1, relief=GROOVE,
                            font=("Times new Roman", 15))
        entry_login.pack()

        pass_label = Label(self, text="Введите пароль:", font=("Times new Roman", 15))
        pass_label.pack()

        entry_pass = Entry(self, width=35, textvariable=StringVar(), show="●", relief=GROOVE,
                           highlightthickness=1, font=("Times new Roman", 15))
        entry_pass.pack()

        repeat_pass_label = Label(self, text="Повторите пароль:", font=("Times new Roman", 15))
        repeat_pass_label.pack()

        entry_repeat_pass = Entry(self, width=35, textvariable=StringVar(), show="●", relief=GROOVE,
                                  highlightthickness=1, font=("Times new Roman", 15))
        entry_repeat_pass.pack()

        button = Button(self, text="Добавить", font=("Times new Roman", 13), width=10, relief=FLAT,
                        background="#34506b",
                        foreground="#ccc", command=lambda: self.win_keyboard_script(objects, entry_pass.get(), entry_repeat_pass.get()))
        button.pack(pady=10)

        objects = (log_label, entry_login, pass_label, entry_pass, repeat_pass_label, entry_repeat_pass, button)


    def win_keyboard_script(self, objects, entry_pass, repeat_pass):
        for items in objects:
            items.destroy()

        WriteDown()
        top_label = Label(self, text="Повторите еще раз пароль", font=("Times new Roman", 18))
        top_label.pack()
        top_child_label = Label(self, text="Это нужно для того, чтоб определить Ваш клавиатурный почерк.", font=("Times new Roman", 12))
        top_child_label.pack()
        center_label = Label(self, text="После ввода нажмите 'Esc', чтоб сохранить данные.",
                             font=("Times new Roman", 11))
        center_label.pack()

        password = Entry(self, width=35, textvariable=StringVar(), show="●", relief=GROOVE,
                         highlightthickness=1, font=("Times new Roman", 15))
        password.pack(pady=20)
        button = Button(self, text="Отправить", font=("Arial 32", 11), width=10, relief=FLAT,
                        background="white",
                        foreground="black", command=lambda: ValidPassword(password.get(), entry_pass, repeat_pass))

        button.pack()


class ValidPassword:
    def __init__(self, password1, password2, password3):
        self.password1 = password1
        self.password2 = password2
        self.password3 = password3
        self.valid_pass_registration()

    def valid_pass_registration(self):
        valid = False
        if self.password2 == self.password3:
            if 6 <= len(self.password3):
                if self.password1 == self.password2:
                    valid = True
                    Training(self.password1)
                    mb.showinfo("Информация", "Поздравляю, Вы зарегистрировались!")
                else:
                    mb.showerror("Ошибка", "Вы ввели неправильный пароль, повторите попытку еще раз!")
            else:
                mb.showerror("Ошибка", "Придумайте пароль от 6 символов!")
        else:
            mb.showerror("Ошибка", "Пароли не совпадают!")

        if valid is False:
            Registration()


def main():
    win = Tk()
    win.geometry("504x350+{0}+{1}".format(int(win.winfo_screenwidth() / 2) - 225, int(win.winfo_screenheight() / 2) - 225))
    win.title("РГР")
    win.resizable(False, False)

    Authorization(win)

    win.mainloop()


if __name__ == '__main__':
    main()