import tkinter as tk
from abc import abstractmethod

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
            width=1400, height=3500
        )

        # bg_image = ImageTk.PhotoImage(Image.open("src/body.jpg").resize((1400, 680), Image.ANTIALIAS))
        # bg_label = tk.Label(self.controll_frame, image=bg_image)
        # bg_label.image = bg_image
        # bg_label.place(x=0, y=0)

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
        instance = [ tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 8), wraplength=200, cursor="hand2"), link ]
        self.titles[name] = instance
        self.titles[name][0].grid(row=1, column=0, sticky=tk.W+tk.S+tk.E)


class AnimeList(View):

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
            width=1400, height=3500
        )

        # bg_image = ImageTk.PhotoImage(Image.open("src/body.jpg").resize((1400, 680), Image.ANTIALIAS))
        # bg_label = tk.Label(self.controll_frame, image=bg_image)
        # bg_label.image = bg_image
        # bg_label.place(x=0, y=0)

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
        instance = [ tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 8), wraplength=200, cursor="hand2"), link ]
        self.titles[name] = instance
        self.titles[name][0].grid(row=1, column=0, sticky=tk.W+tk.S+tk.E)
