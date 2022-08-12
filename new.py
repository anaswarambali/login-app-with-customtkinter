import sqlite3 as sql
import customtkinter
from tkinter import messagebox
import bcrypt

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


def create():
    try:
        con = sql.connect("login.db")
        con.execute('''CREATE TABLE IF NOT EXISTS login (
                            username char(200) NOT NULL,
                            password char(200) NOT NULL,
                            pin int(4) NOT NULL
                            );''')
        user = bcrypt.hashpw(b'admin', bcrypt.gensalt())
        pssd = bcrypt.hashpw(b'root', bcrypt.gensalt())
        con.execute("INSERT INTO login (username, password, pin) VALUES(?, ?, 1234);", (user, pssd))
        con.commit()
        con.close()
    except sql.IntegrityError:
        print("tables present")
    except Exception:
        print("Errors are the key to success")
    else:
        print("Success")


class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.a = None
        self.con = None
        self.results = None
        self.title(" ")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.iconbitmap('log.ico')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        self.frame_left = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_middle = customtkinter.CTkFrame(master=self, corner_radius=5)

        self.frame_left.grid(row=0, column=0, sticky="news")
        self.frame_middle.grid(row=0, column=1, sticky="news", padx=5, pady=5)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=1)

        # ============ frame_left ============

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="HUBSPOT", width=200,
                                              text_font=("Roboto Medium", 16))
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.option_menu = customtkinter.CTkOptionMenu(master=self.frame_left, values=["Light", "Dark", "System"],
                                                       command=self.change_appearance_mode)

        self.label_1.grid(row=1, column=0, pady=10, sticky='EW')
        self.label_mode.grid(row=5, column=0, pady=0)
        self.option_menu.grid(row=6, column=0, pady=10)

        self.frame_left.grid_rowconfigure((0, 7), minsize=15)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(4, weight=1)  # empty row as spacing
        self.frame_left.columnconfigure(0, weight=1)  # to align the text

        # ============ frame_middle ============

        self.frame_login = customtkinter.CTkFrame(master=self.frame_middle)
        self.frame_login.grid(row=0, column=0, columnspan=2, rowspan=6, pady=20, padx=20, sticky="nsew")

        self.show_pass = customtkinter.IntVar(value=0)
        self.lab_inf = customtkinter.CTkLabel(master=self.frame_login, text='')
        self.label_0 = customtkinter.CTkLabel(master=self.frame_login, corner_radius=3, height=40, text="LOGIN")
        self.entry_1 = customtkinter.CTkEntry(master=self.frame_login, corner_radius=3, height=40, justify='center',
                                              placeholder_text="username")
        self.entry_2 = customtkinter.CTkEntry(master=self.frame_login, corner_radius=3, height=40, justify='center',
                                              placeholder_text="password", show='*')
        self.check_b = customtkinter.CTkCheckBox(master=self.frame_login, text='Show Password',
                                                 text_font=("Roboto Medium", 8), variable=self.show_pass,
                                                 onvalue=1, offvalue=0, command=self.show_password)
        self.button2 = customtkinter.CTkButton(master=self.frame_login, corner_radius=6, height=40, text="Login",
                                               command=self.login_button)

        self.lab_inf.grid(column=0, row=0, sticky="nwe", padx=10, pady=10)
        self.label_0.grid(column=0, row=1, sticky="nwe", padx=10, pady=10)
        self.entry_1.grid(column=0, row=2, sticky="nwe", padx=10, pady=10)
        self.entry_2.grid(column=0, row=3, sticky="nwe", padx=10, pady=10)
        self.check_b.grid(column=0, row=4, sticky="nwe", padx=10, pady=10)
        self.button2.grid(column=0, row=5, sticky="nwe", padx=10, pady=10)

        self.frame_middle.grid_columnconfigure(0, weight=1)  # To make the frame expand to fill
        self.frame_middle.grid_rowconfigure(0, weight=1)  # To vertically fill the frame
        self.frame_login.grid_rowconfigure(0, weight=1)
        self.frame_login.grid_rowconfigure(6, minsize=20)
        self.frame_login.grid_columnconfigure(0, weight=1)  # To make the entry field expand to fill

        # ============ frame_right ============

        self.radio_var = customtkinter.IntVar(value=0)
        self.label_rdio_grp = customtkinter.CTkLabel(master=self.frame_middle, text="Details :")

        self.switch_pss = customtkinter.StringVar(value='on')
        self.switch_enp = customtkinter.StringVar(value="on")
        self.switch_bio = customtkinter.StringVar(value="on")

        self.switch1 = customtkinter.CTkSwitch(master=self.frame_middle, text="WITHOUT SALT", variable=self.switch_pss,
                                               onvalue='on', offvalue='off',
                                               command=self.show_password)
        self.switch2 = customtkinter.CTkSwitch(master=self.frame_middle, text="  ENCRYPTION  ",
                                               variable=self.switch_enp, onvalue='on', offvalue='off')
        self.switch3 = customtkinter.CTkSwitch(master=self.frame_middle, text="  BIOMETRICS  ",
                                               variable=self.switch_bio, onvalue='on', offvalue='off')

        self.label_rdio_grp.grid(row=1, column=2, pady=10, padx=10, sticky="")
        self.switch3.grid(row=2, column=2, pady=10, padx=10, sticky="")
        self.switch2.grid(row=3, column=2, pady=10, padx=10, sticky="")
        self.switch1.grid(row=4, column=2, pady=10, padx=10, sticky="")
        self.frame_middle.grid_rowconfigure((0, 5), minsize=15)
        self.frame_middle.grid_rowconfigure((1, 5), weight=10)
        self.frame_middle.grid_rowconfigure((2, 3, 4), weight=1)

        # set default values
        self.option_menu.set("System")

    def show_password(self):
        if self.show_pass.get() == 1:
            print(self.show_pass.get())
            self.entry_2.configure(show='')
        else:
            self.entry_2.configure(show='*')

    def button_event(self):
        print("Button pressed")
        print(self.switch_pss.get())

    def login_button(self):
        print('Login pressed')
        username, password = self.entry_1.get(), self.entry_2.get()
        if username or password:
            self.con = sql.connect('login.db')
            self.a = self.con.cursor()
            self.a.execute("select * from login")

            self.results = self.a.fetchall()
            count = len(self.results)
            if count > 0:
                for i in self.results:
                    print(type(i[0]), 'type\n')
                    if bcrypt.checkpw(username.encode('utf-8'), i[0]):
                        if bcrypt.checkpw(password.encode('utf-8'), i[1]):
                            messagebox.showinfo("Success", "Correct Credentials")
                        else:
                            messagebox.showerror("Error", "Wrong password")
                        break
                else:
                    messagebox.askyesno("User Doesn't Exist", 'Do you want to create')
            else:
                messagebox.showinfo("message", "Wrong username or password")
        else:
            print('WTF')
            messagebox.showerror("Error", "Please enter some values")

    @staticmethod
    def change_appearance_mode(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
