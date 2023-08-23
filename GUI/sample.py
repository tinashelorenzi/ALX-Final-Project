import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path
import zxcvbn
_style_code_ran = 0
# ... (other code above)

class Toplevel1:
    def __init__(self, top=None):
        top.geometry("541x240+358+183")
        top.minsize(1, 1)
        top.maxsize(1351, 738)
        top.resizable(1, 1)
        top.title("Create Password")

        self.top = top

        self.Frame1 = tk.Frame(self.top)
        self.Frame1.place(relx=0.033, rely=0.042, relheight=0.871
                          , relwidth=0.922)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")

        # ... (other widget configurations)

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(relx=0.02, rely=0.048, height=30, width=471)
        self.Label1.configure(anchor='w')
        self.Label1.configure(compound='left')
        self.Label1.configure(cursor="fleur")
        self.Label1.configure(text='''This is the first time running CipherGuard or there is a missing Database.''')

        # ... (other label configurations)

        self.Entry1 = tk.Entry(self.Frame1)
        self.Entry1.place(relx=0.381, rely=0.206, height=22, relwidth=0.551)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(show="*")

        # ... (other entry configurations)

        self.Entry2 = tk.Entry(self.Frame1)
        self.Entry2.place(relx=0.381, rely=0.354, height=22, relwidth=0.553)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(show="*")

        _style_code()
        
        # ... (other widget configurations)

        self.TProgressbar1 = ttk.Progressbar(self.Frame1)
        self.TProgressbar1.place(relx=0.02, rely=0.67, relwidth=0.381
                                 , relheight=0.0, height=19)
        self.TProgressbar1.configure(length="190")

        # ... (other widget configurations)

        self.Label4 = tk.Label(self.Frame1)
        self.Label4.place(relx=0.02, rely=0.474, height=26, width=255)
        self.Label4.configure(anchor='w')
        self.Label4.configure(compound='left')
        self.Label4.configure(text='''Password Strength(Ensure that it is full!)''')

        # ... (other label configurations)

        self.Button1 = tk.Button(self.Frame1)
        self.Button1.place(relx=0.601, rely=0.464, height=32, width=168)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(borderwidth="2")

        self.Button1.configure(command=self.calculate_strength)
        self.Button1.configure(compound='left')
        self.Button1.configure(text='''Check password strength''')

        # ... (other widget configurations)

        self.Button2 = tk.Button(self.Frame1)
        self.Button2.place(relx=0.741, rely=0.67, height=32, width=98)
        self.Button2.configure(activebackground="beige")
        self.Button2.configure(borderwidth="2")
        self.Button2.configure(compound='left')
        self.Button2.configure(text='''Create''')

    def calculate_strength(self):
        password = self.Entry1.get()
        confirm_password = self.Entry2.get()

        if password != confirm_password:
            # Handle password mismatch here, e.g., show an error message
            return

        # Check password strength using zxcvbn library
        password_strength = zxcvbn.password_strength(password)
        strength_score = password_strength['score']

        # Update progress bar based on the strength score
        self.TProgressbar1['value'] = strength_score * 25

        # Optionally, update some label to show the password strength description
        strength_description = password_strength['feedback']['suggestions'][0]
        self.Label4.config(text=strength_description)

def _style_code():
    global _style_code_ran
    if _style_code_ran:
       return
    style = ttk.Style()
    if sys.platform == "win32":
       style.theme_use('winnative')
    style.configure('.',background=_bgcolor)
    style.configure('.',foreground=_fgcolor)
    style.configure('.',font='TkDefaultFont')
    style.map('.',background =
       [('selected', _compcolor), ('active',_ana2color)])
    if _bgmode == 'dark':
       style.map('.',foreground =
         [('selected', 'white'), ('active','white')])
    else:
       style.map('.',foreground =
         [('selected', 'black'), ('active','black')])
    _style_code_ran = 1
def start_up():
    Main_support.main()


if __name__ == '__main__':
    root = tk.Tk()
    app = Toplevel1(root)
    root.mainloop()
