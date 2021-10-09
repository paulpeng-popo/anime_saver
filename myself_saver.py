import os
import tkinter as tk
from tkinter import ttk
from gui.views import View, AnimeBlock
from gui.models import GetHomePageAnime
from gui.controllers import Controller, HomePageController

class Application(ttk.Notebook):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Anime Download")
        self.master.configure(bg = "BlanchedAlmond")
        self.master.geometry("1400x750+180+80")
        self.master.resizable(False, False)
        self.master.iconbitmap(os.path.join(os.getcwd(), "src\logo.ico"))

    def new_tab(self, controller: Controller, view: View, name: str):
        view = view(self)
        controller.bind(view)
        self.add(view, text=name)
        self.pack(expand=1, fill='both')

if __name__ == "__main__":

    root = tk.Tk()
    style = ttk.Style()
    style.theme_create(
        "Default", parent="classic", settings={
            "TLabel": { "configure": { "background": "WhiteSmoke" } },
            "TFrame": { "configure": { "background": "WhiteSmoke" } },
            "TNotebook": { "configure": { "background": "WhiteSmoke", "tabmargins": [2, 0, 2, 0] } },
            "TNotebook.Tab": {
                "configure": { "padding": [30, 10], "font" : ('Times New Roman', '12', 'bold') },
                "map": { "background": [("selected", "BlanchedAlmond")], "expand": [("selected", [1, 1, 1, 0])] }
            }
        }
    )
    style.theme_use("Default")
    app = Application(master=root)

    HomePage_Controller = HomePageController()
    EveryWeekRenew_controller = HomePageController()
    Continue_Controller = HomePageController()
    app.new_tab(view=AnimeBlock, controller=HomePage_Controller, name="首頁/人氣排行")
    # app.new_tab(view=AnimeBlock, controller=EveryWeekRenew_controller, name="每週更新")
    # app.new_tab(view=AnimeBlock, controller=Continue_Controller, name="連載中")
    # app.new_tab(view=AnimeBlock, controller=HomePage_Controller, name="完結動畫")
    # app.new_tab(view=AnimeBlock, controller=HomePage_Controller, name="完結列表")
    # app.new_tab(view=AnimeBlock, controller=HomePage_Controller, name="動漫資訊")

    app.mainloop()
