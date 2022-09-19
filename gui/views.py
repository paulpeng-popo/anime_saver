import tkinter as tk
from abc import abstractmethod
from tkinter import ttk

from PIL import Image, ImageTk


class View(tk.Frame):

    @abstractmethod
    def create_view():
        raise NotImplementedError

class AnimeBlock(View):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.labels = {}
        self.images = {}
        self.titles = {}

        self.folder = "src/animes/"
        self.canvas = tk.Canvas(self, width=1400, height=680)
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.controll_frame = tk.Frame(
            self.canvas,
            bg='BlanchedAlmond',
            width=1400, height=3350
        )

    def create_view(self, AnimeData: list):

        vertical_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.canvas.configure(yscrollcommand=vertical_scrollbar.set)
        self.canvas.create_window((0, 0), window=self.controll_frame, anchor="nw")

        padding = 80
        for num, item in enumerate(AnimeData):
            anime_num = 0
            self.create_label(self.controll_frame, item['area_name'], 60, padding)
            if num == 2 or num == 4:
                for anime in item['block_content']:
                    if anime_num // 5:
                        anime_num = anime_num - 5
                        padding = padding + 350
                    anime_frame = tk.Frame(self.controll_frame, bg = "BlanchedAlmond", width = 200, height = 315)
                    anime_frame.place(x = 100+250*anime_num, y = 80+padding)
                    self.create_image(anime_frame, anime['image'], anime['link'], 200, 275)
                    self.create_title(anime_frame, anime['title'], anime['link'])
                    anime_num = anime_num + 1
                padding = padding + 450
            else:
                for anime in item['block_content']:
                    if anime_num // 5:
                        anime_num = anime_num - 5
                        padding = padding + 190
                    anime_frame = tk.Frame(self.controll_frame, bg = "BlanchedAlmond", width = 200, height = 180)
                    anime_frame.place(x = 100+250*anime_num, y = 80+padding)
                    self.create_image(anime_frame, anime['image'], anime['link'], 200, 140)
                    self.create_title(anime_frame, anime['title'], anime['link'])
                    anime_num = anime_num + 1
                padding = padding + 300

    def create_label(self, frame, name, posx, posy):
        self.labels[name] = tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 16))
        self.labels[name].place(x = posx, y = posy)

    def create_image(self, frame, data, link, width, height):
        load = Image.open(self.folder+data.split("/")[-1])
        raw_image = load.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(raw_image)
        instance = [ tk.Label(frame, image=image, cursor="hand2"), link ]
        self.images[data.split("/")[-1].split(".")[0]] = instance
        self.images[data.split("/")[-1].split(".")[0]][0].image = image
        self.images[data.split("/")[-1].split(".")[0]][0].grid(row=0, column=0, sticky=tk.W+tk.N+tk.E)

    def create_title(self, frame, name, link):
        instance = [ tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 10), wraplength=200, cursor="hand2"), link ]
        self.titles[name] = instance
        self.titles[name][0].grid(row=1, column=0, sticky=tk.W+tk.S+tk.E)


class AnimeList(View):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.labels = {}
        self.titles = {}

        self.canvas = tk.Canvas(self, width=1400, height=680)
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.controll_frame = None

    def create_view(self, AnimeData: dict):

        text_num = 0
        total_padding = 0
        for item in AnimeData.values():
            text_num = text_num + len(item)
        total_padding = 80 + text_num * 50 + 560

        self.controll_frame = tk.Frame(
            self.canvas,
            bg='BlanchedAlmond',
            width=1400, height=total_padding
        )

        weeks_map = {1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六", 7:"日"}

        vertical_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.canvas.configure(yscrollcommand=vertical_scrollbar.set)
        self.canvas.create_window((0, 0), window=self.controll_frame, anchor="nw")

        padding = 80
        for week in AnimeData:
            title_text = "星期" + weeks_map[week]
            self.create_label(self.controll_frame, title_text, 60, padding)
            for anime in AnimeData[week]:
                padding = padding + 50
                link_text = anime['title'] + " " + anime['text']
                anime_frame = tk.Frame(self.controll_frame, bg = "BlanchedAlmond", width = 1000, height = 30)
                anime_frame.place(x = 200, y = padding)
                self.create_title(anime_frame, link_text, anime['link'])
            padding = padding + 80

    def create_label(self, frame, name, posx, posy):
        self.labels[name] = tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 16))
        self.labels[name].place(x = posx, y = posy)

    def create_title(self, frame, name, link):
        instance = [ 
            tk.Label(
                frame,
                text=name,
                bg="BlanchedAlmond",
                fg="Blue",
                font=("", 14),
                wraplength=1000,
                cursor="hand2"
            ),
            link
        ]
        self.titles[name] = instance
        self.titles[name][0].grid(row=1, column=0, sticky=tk.W+tk.S+tk.E)


class AnimePage(View):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.type = "未分類"
        self.labels = {}
        self.images = {}
        self.titles = {}
        self.frames = []
        self.pages = {}

        self.folder = "src/animes/"
        self.canvas = tk.Canvas(self, width=1400, height=680)
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.controll_frame = tk.Frame(
            self.canvas,
            bg='BlanchedAlmond',
            width=1400, height=1050
        )

    def create_view(self, AnimeData: dict):

        vertical_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.canvas.configure(yscrollcommand=vertical_scrollbar.set)
        self.canvas.create_window((0, 0), window=self.controll_frame, anchor="nw")

        page_text = "第" + str(AnimeData["page"]) + "頁/共" + str(AnimeData["total_page"]) + "頁"
        self.create_label(self.controll_frame, "連載動漫", 60, 80)
        self.create_label(self.controll_frame, page_text, 200, 80)

        padding = 80
        anime_num = 0
        for anime in AnimeData["content"]:
            if anime_num // 5:
                anime_num = anime_num - 5
                padding = padding + 190
            anime_frame = tk.Frame(self.controll_frame, bg = "BlanchedAlmond", width = 200, height = 180)
            anime_frame.place(x = 100+250*anime_num, y = 80+padding)
            self.create_image(anime_frame, anime['image'], anime['link'], 200, 140)
            self.create_title(anime_frame, anime['title'], anime['link'])
            self.frames.append(anime_frame)
            anime_num = anime_num + 1

        padding = padding + 300

        self.create_label(self.controll_frame, page_text, 200, padding)
        button_frame = tk.Frame(self.controll_frame, bg = "BlanchedAlmond", width = 200, height = 50)
        button_frame.place(x = 590, y = padding)
        prev_page = AnimeData["page"] - 1 if AnimeData["page"] > 1 else 1
        next_page = AnimeData["page"] + 1 if AnimeData["page"] < AnimeData["total_page"] else AnimeData["total_page"]
        self.create_button(button_frame, "Prev Page", prev_page, 0, 0)
        self.create_button(button_frame, "Next Page", next_page, 0, 1)

    def create_label(self, frame, name, posx, posy):
        self.labels[name] = tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 16))
        self.labels[name].place(x = posx, y = posy)

    def create_image(self, frame, data, link, width, height):
        load = Image.open(self.folder+data.split("/")[-1])
        raw_image = load.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(raw_image)
        instance = [ tk.Label(frame, image=image, cursor="hand2"), link ]
        self.images[data.split("/")[-1].split(".")[0]] = instance
        self.images[data.split("/")[-1].split(".")[0]][0].image = image
        self.images[data.split("/")[-1].split(".")[0]][0].grid(row=0, column=0, sticky=tk.W+tk.N+tk.E)

    def create_title(self, frame, name, link):
        instance = [ tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 10), wraplength=200, cursor="hand2"), link ]
        self.titles[name] = instance
        self.titles[name][0].grid(row=1, column=0, sticky=tk.W+tk.S+tk.E)

    def create_button(self, frame, text, target, row, column):
        instance = [ tk.Button(frame, text=text, bg="Yellow", font=("", 12), cursor="hand2"), target ]
        self.pages[text] = instance
        self.pages[text][0].grid(row=row, column=column, sticky=tk.W+tk.S+tk.E)


class AnimeListFinished(View):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.labels = {}
        self.titles = {}
        self.frames = []

        self.canvas = tk.Canvas(self, width=1400, height=680)
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.controll_frame = None

    def create_view(self, Entry: list, EntryText: str, AnimeData: list):

        total_padding = 80 + len(AnimeData) * 50 + 80
        self.controll_frame = tk.Frame(
            self.canvas,
            bg='BlanchedAlmond',
            width=1400, height=total_padding
        )

        vertical_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.canvas.configure(yscrollcommand=vertical_scrollbar.set)
        self.canvas.create_window((0, 0), window=self.controll_frame, anchor="nw")

        self.combobox = ttk.Combobox(
            self.controll_frame, 
            state='readonly', 
            width=20, 
            font=("", 16), 
            justify='center', 
            values=Entry
        )
        self.combobox.current(Entry.index(EntryText))
        self.combobox.place(x = 60, y = 20)

        padding = 80
        self.create_label(self.controll_frame, EntryText, 60, padding)
        for anime in AnimeData:
            padding = padding + 50
            anime_frame = tk.Frame(self.controll_frame, bg = "BlanchedAlmond", width = 1000, height = 30)
            anime_frame.place(x = 200, y = padding)
            self.create_title(anime_frame, anime['title'], anime['link'])
            self.frames.append(anime_frame)
        padding = padding + 80

    def create_label(self, frame, name, posx, posy):
        self.labels[name] = tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 16))
        self.labels[name].place(x = posx, y = posy)

    def create_title(self, frame, name, link):
        instance = [ 
            tk.Label(
                frame,
                text=name,
                bg="BlanchedAlmond",
                fg="Blue",
                font=("", 14),
                wraplength=1000,
                cursor="hand2"
            ),
            link
        ]
        self.titles[name] = instance
        self.titles[name][0].grid(row=1, column=0, sticky=tk.W+tk.S+tk.E)


class R18AnimeBlock(View):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.labels = {}
        self.images = {}
        self.titles = {}

        self.folder = "src/animes/"
        self.canvas = tk.Canvas(self, width=1400, height=680)
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.controll_frame = tk.Frame(
            self.canvas,
            bg='BlanchedAlmond',
            width=1400, height=3350
        )

    def create_view(self, AnimeData: list):

        vertical_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.canvas.configure(yscrollcommand=vertical_scrollbar.set)
        self.canvas.create_window((0, 0), window=self.controll_frame, anchor="nw")

        padding = 80
        for num, item in enumerate(AnimeData):
            anime_num = 0
            self.create_label(self.controll_frame, item['area_name'], 60, padding)
            if num == 2 or num == 4:
                for anime in item['block_content']:
                    if anime_num // 5:
                        anime_num = anime_num - 5
                        padding = padding + 350
                    anime_frame = tk.Frame(self.controll_frame, bg = "BlanchedAlmond", width = 200, height = 315)
                    anime_frame.place(x = 100+250*anime_num, y = 80+padding)
                    self.create_image(anime_frame, anime['image'], anime['link'], 200, 275)
                    self.create_title(anime_frame, anime['title'], anime['link'])
                    anime_num = anime_num + 1
                padding = padding + 450
            else:
                for anime in item['block_content']:
                    if anime_num // 5:
                        anime_num = anime_num - 5
                        padding = padding + 190
                    anime_frame = tk.Frame(self.controll_frame, bg = "BlanchedAlmond", width = 200, height = 180)
                    anime_frame.place(x = 100+250*anime_num, y = 80+padding)
                    self.create_image(anime_frame, anime['image'], anime['link'], 200, 140)
                    self.create_title(anime_frame, anime['title'], anime['link'])
                    anime_num = anime_num + 1
                padding = padding + 300

    def create_label(self, frame, name, posx, posy):
        self.labels[name] = tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 16))
        self.labels[name].place(x = posx, y = posy)

    def create_image(self, frame, data, link, width, height):
        load = Image.open(self.folder+data.split("/")[-1])
        raw_image = load.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(raw_image)
        instance = [ tk.Label(frame, image=image, cursor="hand2"), link ]
        self.images[data.split("/")[-1].split(".")[0]] = instance
        self.images[data.split("/")[-1].split(".")[0]][0].image = image
        self.images[data.split("/")[-1].split(".")[0]][0].grid(row=0, column=0, sticky=tk.W+tk.N+tk.E)

    def create_title(self, frame, name, link):
        instance = [ tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 10), wraplength=200, cursor="hand2"), link ]
        self.titles[name] = instance
        self.titles[name][0].grid(row=1, column=0, sticky=tk.W+tk.S+tk.E)
