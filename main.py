import clipboard
import re
import sqlite3
import tkinter as tk
import customtkinter as ck
import ui
import sqlite3
from PIL import Image, ImageTk
import os
import time

PATH = os.path.dirname(os.path.realpath(__file__))


ck.set_appearance_mode("dark")
ck.set_default_color_theme("green")


class App(ck.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("PyWallet")
        self.resizable(False, False)

        screenHeight = self.winfo_screenheight()
        screenWidth = self.winfo_screenwidth()

        x = (screenWidth / 2) - (ui.Dimension.WIDTH / 2)
        y = (screenHeight / 2) - (ui.Dimension.HEIGHT / 2)

        self.geometry(f"{ui.Dimension.WIDTH}x{ui.Dimension.HEIGHT}+{int(x)}+{int(y)}")

        self.configure(background=ui.Color.MAIN)

        self.BottomBar = ck.CTkFrame(
            self, corner_radius=0, fg_color=ui.Color.BOTBAR, height=20
        )
        self.BottomBar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        self.space = ck.CTkFrame(
            self, fg_color=ui.Color.MAIN, width=10, corner_radius=0
        )
        self.space.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        self.space = ck.CTkFrame(
            self, fg_color=ui.Color.MAIN, width=10, corner_radius=0
        )
        self.space.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.space = ck.CTkFrame(
            self, fg_color=ui.Color.MAIN, height=10, corner_radius=0
        )
        self.space.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.MainFrame = tk.Frame(self, bg=ui.Color.MAIN)
        self.MainFrame.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.DisplayWalletCards()

        self.InsertCardBtn = ck.CTkButton(
            self.MainFrame,
            corner_radius=15,
            fg_color=ui.Color.MAIN,
            text="Insert",
            command=self.EntryCard,
            hover="disabled",
        )
        self.InsertCardBtn.pack(side=tk.LEFT, fill=tk.X, expand=False)

        self.CancelCardBtn = ck.CTkButton(
            self.MainFrame,
            corner_radius=15,
            fg_color=ui.Color.MAIN,
            text="Cancel",
            command=self.CancelEntry,
            hover="disabled",
        )
        self.CancelCardBtn.pack(side=tk.RIGHT, fill=tk.X, expand=False)
        self.CancelCardBtn.configure(state="disabled")

        self.ClickFrame = tk.Frame(self, bg=ui.Color.MAIN)
        self.ClickFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ClickFrame.bind("<Button-1>", self.CheckEntryCard)

        self.CopyFrame = ck.CTkFrame(
            self,
            corner_radius=15,
            height=30,
            fg_color=ui.Color.ENTRYCARD,
        )
        self.CopyFrame.grid_rowconfigure((0, 2), minsize=5)
        self.CopyFrame.grid_rowconfigure(1, weight=0)
        self.CopyFrame.grid_columnconfigure((0, 2), minsize=65)

        self.CopyLabel = tk.Label(
            self.CopyFrame, bg=ui.Color.ENTRYCARD, font=ui.Font.SMALL
        )
        self.CopyLabel.grid(row=1, column=1, sticky="nswe", padx=3, pady=3)

        self.ErrorFrame = ck.CTkFrame(
            self,
            corner_radius=15,
            height=30,
            fg_color=ui.Color.RED,
        )
        self.ErrorFrame.grid_rowconfigure((0, 2), minsize=5)
        self.ErrorFrame.grid_rowconfigure(1, weight=0)
        self.ErrorFrame.grid_columnconfigure((0, 2), minsize=65)

        self.ErrorLabel = tk.Label(self.ErrorFrame, bg=ui.Color.RED, font=ui.Font.SMALL)
        self.ErrorLabel.grid(row=1, column=1, sticky="nswe", padx=3, pady=3)

        self.EntryCard = ck.CTkFrame(
            self,
            corner_radius=40,
            width=ui.Dimension.WIDTH,
            fg_color=ui.Color.ENTRYCARD,
        )

        self.frame = tk.Frame(self.EntryCard, bg=ui.Color.ENTRYCARD)
        self.frame.grid(row=0, column=0, sticky="nswe", pady=12, padx=15)

        self.frame.grid_rowconfigure((0), minsize=20)
        self.frame.grid_rowconfigure((9), minsize=10)
        self.frame.grid_rowconfigure((12), minsize=10)

        self.frame.grid_rowconfigure((6), minsize=15)
        self.frame.grid_rowconfigure(7, minsize=10)
        self.frame.grid_rowconfigure(8, minsize=30)
        self.frame.grid_rowconfigure(10, minsize=10)
        self.frame.grid_rowconfigure(11, minsize=30)
        self.frame.grid_rowconfigure(13, minsize=30)
        self.frame.grid_rowconfigure(14, minsize=30)
        self.frame.grid_rowconfigure((15), minsize=50)

        self.frame.grid_columnconfigure((0, 3), minsize=35)
        self.frame.grid_columnconfigure((1, 2), weight=1)

        vcmd = (self.register(self.onValidate), "%P")
        vcmd2 = (self.register(self.onValidate2), "%P")

        self.LabelEntry = tk.Label(
            self.frame,
            text="Card Number",
            bg=ui.Color.ENTRYCARD,
            justify="left",
            font=ui.Font.SMALL,
        )
        self.LabelEntry.grid(row=7, column=1, sticky="nsw")

        self.CardNumber = ck.CTkEntry(
            self.frame,
            fg_color=None,
            border_color=None,
            justify="left",
            validate="key",
            validatecommand=vcmd,
        )
        self.CardNumber.grid(row=8, column=1, sticky="swe")
        self.underLine = ck.CTkFrame(self.CardNumber, height=1, fg_color="grey").grid(
            row=5, column=0, sticky="swe"
        )

        self.LabelEntry = tk.Label(
            self.frame,
            text="CVV Number",
            bg=ui.Color.ENTRYCARD,
            justify="left",
            font=ui.Font.SMALL,
        )
        self.LabelEntry.grid(row=10, column=1, sticky="nsw")

        self.SecurityNumber = ck.CTkEntry(
            self.frame,
            fg_color=None,
            border_color=None,
            justify="left",
            validate="key",
            validatecommand=vcmd2,
        )
        self.SecurityNumber.grid(row=11, column=1, sticky="swe")
        self.underLine = ck.CTkFrame(
            self.SecurityNumber, height=1, fg_color="grey"
        ).grid(row=11, column=0, sticky="swe")

        self.InsertButton = ck.CTkButton(
            self.frame,
            text="Submit",
            corner_radius=10,
            width=0,
            command=self.InsertDataIntotable,
        )
        self.InsertButton.grid(row=13, column=1, sticky="we")

        self.ClearButton = ck.CTkButton(
            self.frame,
            text="Clear",
            width=0,
            corner_radius=10,
            command=self.ClearEntries,
        )
        self.ClearButton.grid(row=14, column=1, pady=5, sticky="we")

    def CheckEntryCard(self, event):
        BtnState = self.CancelCardBtn.state
        if BtnState == "normal":
            self.CancelEntry()
        else:
            pass

    def LoadImage(self, path, image_size):
        return ImageTk.PhotoImage(
            Image.open(PATH + path).resize((image_size, image_size))
        )

    def DisplayWalletCards(self):
        db = Database.ConnectDatabase()
        records = Database.ShowWalletTable(db)

        self.space = ck.CTkFrame(self, height=10, fg_color=ui.Color.MAIN)
        self.space.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        self.visa = self.LoadImage("/visa.png", 38)
        self.mastercard = self.LoadImage("/mastercard.png", 38)
        self.amex = self.LoadImage("/amex.png", 38)

        for i in records:
            self.frame = ck.CTkFrame(
                self,
                fg_color=ui.Color.BOTBAR,
                corner_radius=10,
            )
            self.frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

            self.frame.grid_rowconfigure(1, minsize=0)
            self.frame.grid_rowconfigure((2, 3), weight=1)
            self.frame.grid_rowconfigure((0, 4), minsize=5)

            self.frame.grid_columnconfigure((0, 3), minsize=10)
            self.frame.grid_columnconfigure((1, 2), weight=1)

            if i[2] == "visa.png":
                self.CardTypeLabel = ck.CTkButton(
                    self.frame,
                    fg_color=ui.Color.BOTBAR,
                    width=0,
                    height=0,
                    text=None,
                    image=self.visa,
                    hover="disabled",
                )

                self.CardTypeLabel.grid(row=2, column=1, rowspan=2, sticky="nsw")
            elif i[2] == "mastercard.png":
                self.CardTypeLabel = ck.CTkButton(
                    self.frame,
                    fg_color=ui.Color.BOTBAR,
                    width=0,
                    height=0,
                    text=None,
                    image=self.mastercard,
                    hover="disabled",
                )

                self.CardTypeLabel.grid(row=2, column=1, rowspan=2, sticky="nsw")
            else:
                self.CardTypeLabel = ck.CTkButton(
                    self.frame,
                    fg_color=ui.Color.BOTBAR,
                    width=0,
                    height=0,
                    text=None,
                    image=self.amex,
                    hover="disabled",
                )

                self.CardTypeLabel.grid(row=2, column=1, rowspan=2, sticky="nsw")

            self.var = tk.StringVar(value=f"•••• •••• •••• {i[0][-4:]}")
            self.CardNumber = ck.CTkButton(
                self.frame,
                width=0,
                height=0,
                fg_color=ui.Color.BOTBAR,
                text_font=ui.Font.MID,
                textvariable=self.var,
                hover="disabled",
                command=lambda e=i[0]: self.click(e),
            )
            self.CardNumber.grid(row=2, column=2, sticky="e")

            self.var = tk.StringVar(value=f"•• {i[1][-1]}")
            self.CardSecurity = ck.CTkButton(
                self.frame,
                width=0,
                height=0,
                fg_color=ui.Color.BOTBAR,
                text_font=ui.Font.MID,
                textvariable=self.var,
                hover="disabled",
                command=lambda e=i[1]: self.click(e),
            )
            self.CardSecurity.grid(row=3, column=2, sticky="e")

            self.space = ck.CTkFrame(self, height=10, fg_color=ui.Color.MAIN)
            self.space.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    def click(self, e):
        clipboard.copy(e)
        self.CopyLabel.configure(text="Number copied!")
        for y in range(0, 6, 1):
            self.CopyFrame.update()
            self.CopyFrame.place(
                anchor="center",
                in_=self,
                relx=0.5,
                y=y**2,
            )

        time.sleep(1.5)

        for y in range(5, -1, -1):
            self.CopyFrame.update()
            self.CopyFrame.place(
                anchor="center",
                in_=self,
                relx=0.5,
                y=(y**2),
            )

        self.CopyFrame.place_forget()

    def CreateNewEntry(self):
        db = Database.ConnectDatabase()
        records = Database.ShowWalletTable(db)
        record = records[-1]

        self.frame = ck.CTkFrame(
            self,
            fg_color=ui.Color.BOTBAR,
            corner_radius=12,
        )
        self.frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        self.frame.grid_rowconfigure(1, minsize=0)
        self.frame.grid_rowconfigure((2, 3), weight=1)
        self.frame.grid_rowconfigure((0, 4), minsize=5)

        self.frame.grid_columnconfigure((0, 3), minsize=10)
        self.frame.grid_columnconfigure((1, 2), weight=1)

        if record[2] == "visa.png":
            self.CardTypeLabel = ck.CTkButton(
                self.frame,
                fg_color=ui.Color.BOTBAR,
                width=0,
                height=0,
                text=None,
                image=self.visa,
                hover="disabled",
            )

            self.CardTypeLabel.grid(row=2, column=1, rowspan=2, sticky="nsw")
        elif record[2] == "mastercard.png":
            self.CardTypeLabel = ck.CTkButton(
                self.frame,
                fg_color=ui.Color.BOTBAR,
                width=0,
                height=0,
                text=None,
                image=self.mastercard,
                hover="disabled",
            )

            self.CardTypeLabel.grid(row=2, column=1, rowspan=2, sticky="nsw")
        else:
            self.CardTypeLabel = ck.CTkButton(
                self.frame,
                fg_color=ui.Color.BOTBAR,
                width=0,
                height=0,
                text=None,
                image=self.amex,
                hover="disabled",
            )

            self.CardTypeLabel.grid(row=2, column=1, rowspan=2, sticky="nsw")

        self.var = tk.StringVar(value=f"•••• •••• •••• {record[0][-4:]}")
        self.c_n = ck.CTkButton(
            self.frame,
            width=0,
            height=0,
            fg_color=ui.Color.BOTBAR,
            text_font=ui.Font.MID,
            textvariable=self.var,
            hover="disabled",
            command=lambda e=record[0]: self.click(e),
        )
        self.c_n.grid(row=2, column=2, sticky="e")

        self.var = tk.StringVar(value=f"•• {record[1][-1]}")
        self.c_s = ck.CTkButton(
            self.frame,
            width=0,
            height=0,
            fg_color=ui.Color.BOTBAR,
            text_font=ui.Font.MID,
            textvariable=self.var,
            hover="disabled",
            command=lambda e=record[1]: self.click(e),
        )
        self.c_s.grid(row=3, column=2, sticky="e")

        self.space = ck.CTkFrame(self, height=10, fg_color=ui.Color.MAIN)
        self.space.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        self.frame.lower()
        self.space.lower()

        self.CardNumber.delete(0, "end")
        self.SecurityNumber.delete(0, "end")

    def EntryError(self):
        self.ErrorLabel.configure(
            text="Incorrect entry!",
            fg="white",
        )

        for y in range(0, 6, 1):
            self.ErrorFrame.update()
            self.ErrorFrame.place(
                anchor="center",
                in_=self,
                relx=0.5,
                y=y**2,
            )

        time.sleep(1)

        for y in range(5, -1, -1):
            self.ErrorFrame.update()
            self.ErrorFrame.place(
                anchor="center",
                in_=self,
                relx=0.5,
                y=(y**2),
            )

        self.ErrorFrame.place_forget()

    def InsertDataIntotable(self):
        db = Database.ConnectDatabase()

        try:

            self.Card_Number = self.CardNumber.get()
            self.Sec_Number = self.SecurityNumber.get()
            self.values = [self.Card_Number, self.Sec_Number]

            if self.Card_Number[0] == "4":
                self.CardType = "visa.png"
                self.values.append(self.CardType)
            elif self.Card_Number[0] == "5":
                self.CardType = "mastercard.png"
                self.values.append(self.CardType)
            elif self.Card_Number[0] == "3":
                self.CardType = "amex.png"
                self.values.append(self.CardType)

            if (
                (len(self.values) == 3)
                and (len(self.Card_Number) == 19)
                and (len(self.Sec_Number) == 3)
            ):
                Database.InsertIntoDatabase(db, self.values)
                db.commit()
                db.close()
                self.CardNumber.delete(0, "end")
                self.SecurityNumber.delete(0, "end")
                self.CancelEntry()
                self.CreateNewEntry()

            else:
                self.ClearEntries()
                self.EntryError()

        except:
            pass

    def CancelEntry(self):
        self.CardNumber.delete(0, "end")
        self.SecurityNumber.delete(0, "end")
        for y in range(21, 31, 1):
            self.EntryCard.update()
            self.EntryCard.place(
                anchor="center",
                in_=self,
                relx=0.5,
                y=y**2,
            )

        self.CancelCardBtn.configure(state="disabled")
        self.InsertCardBtn.configure(state="normal")

    def EntryCard(self):
        for y in range(-31, -21, 1):
            self.EntryCard.update()
            self.EntryCard.place(
                anchor="center",
                in_=self,
                relx=0.5,
                y=y**2,
            )
        self.CardNumber.focus()
        self.CancelCardBtn.configure(state="normal")
        self.InsertCardBtn.configure(state="disabled")

    def onValidate2(self, P):
        pattern = re.compile(r"^[0-9]{0,3}$")
        if re.fullmatch(pattern, P):
            return True
        else:
            self.bell()
            return False

    def onValidate(self, P):
        pattern = re.compile(r"^[0-9 ]{0,19}$")
        if re.fullmatch(pattern, P):
            return True
        else:
            self.bell()
            return False

    def ClearEntries(self):
        self.CardNumber.delete(0, "end")
        self.SecurityNumber.delete(0, "end")
        self.CardNumber.focus()

    def on_close(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


class Database:
    def ConnectDatabase():
        db = sqlite3.connect("wallet.db")
        c = db.cursor()
        c.execute(
            "CREATE TABLE if not exists wallet (CardNumber Text, SecurityNumber Text, CardType Text)"
        )
        db.commit()
        return db

    def ShowWalletTable(db):
        c = db.cursor()
        c.execute("SELECT CardNumber, SecurityNumber, CardType FROM wallet")
        records = c.fetchall()
        return records

    def InsertIntoDatabase(db, values):
        c = db.cursor()
        c.execute("INSERT INTO wallet VALUES (?, ?, ?)", values)


if __name__ == "__main__":
    app = App()
    app.start()
