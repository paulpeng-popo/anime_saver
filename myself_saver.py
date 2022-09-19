import os
import tkinter as tk
from tkinter import ttk

from gui.controllers import (Controller, EveryWeekRenewController,
                             FinishListController, HomePageController,
                             R18HomePageController, SeriesController)
from gui.views import AnimeBlock, AnimeList, AnimeListFinished, AnimePage, View


class Application(ttk.Notebook):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master

        self.master.title("Anime Download")
        self.master.configure(bg = "BlanchedAlmond")
        self.master.geometry("1400x750+180+80")
        self.master.resizable(False, False)
        self.master.iconbitmap(os.path.join(os.getcwd(), "src/logo.ico"))

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
    EveryWeekRenew_controller = EveryWeekRenewController()
    Continue_Controller = SeriesController()
    Finish_Controller = SeriesController(finish=True)
    FinishList_Controller = FinishListController()
    R18HomePage_Controller = R18HomePageController()
    # R18List_Controller = R18ListController()

    app.new_tab(view=AnimeBlock, controller=HomePage_Controller, name="首頁/新番")
    app.new_tab(view=AnimeList, controller=EveryWeekRenew_controller, name="每週更新")
    app.new_tab(view=AnimePage, controller=Continue_Controller, name="連載中")
    app.new_tab(view=AnimePage, controller=Finish_Controller, name="完結動畫")
    app.new_tab(view=AnimeListFinished, controller=FinishList_Controller, name="完結列表")
    # app.new_tab(view=R18AnimeBlock, controller=R18HomePage_Controller, name="R18首頁")
    # app.new_tab(view=AnimePage, controller=R18List_Controller, name="R18動畫列表")

    app.mainloop()
