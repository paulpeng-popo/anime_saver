import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from abc import abstractmethod
import io, requests, webbrowser, os
import gui.downloader as cdd

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

        self.canvas = tk.Canvas(self, width=1400, height=680)
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all(
            '<MouseWheel>',
            lambda e: self.canvas.yview_scroll(int(-1*(e.delta/60)), "units")
        )

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def create_view(self, AnimeData: list):
        BaseUrl = "https://myself-bbs.com/"

        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

        vertical_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.canvas.configure(yscrollcommand=vertical_scrollbar.set)

        controll_frame = tk.Frame(self.canvas, bg='BlanchedAlmond', width=1400, height=3200)
        controll_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=controll_frame, anchor="nw")

        padding = 80
        for num, item in enumerate(AnimeData):
            self.create_label(controll_frame, item['area_name'], 60, padding)
            anime_num = 0
            if num == 2 or num == 4:
                for anime in item['block_content']:
                    if anime_num // 5:
                        anime_num = anime_num - 5
                        padding = padding + 350
                    anime_frame = tk.Frame(controll_frame, bg = "BlanchedAlmond", width = 200, height = 320)
                    anime_frame.place(x = 100+250*anime_num, y = 80+padding)
                    self.create_image_and_link(anime_frame, anime['image'], anime['link'], BaseUrl, 200, 275)
                    self.create_title_and_link(anime_frame, anime['title'], anime['link'], BaseUrl)
                    anime_num = anime_num + 1
                padding = padding + 450
            else:
                for anime in item['block_content']:
                    if anime_num // 5:
                        anime_num = anime_num - 5
                        padding = padding + 190
                    anime_frame = tk.Frame(controll_frame, bg = "BlanchedAlmond", width = 200, height = 180)
                    anime_frame.place(x = 100+250*anime_num, y = 80+padding)
                    self.create_image_and_link(anime_frame, anime['image'], anime['link'], BaseUrl, 200, 135)
                    self.create_title_and_link(anime_frame, anime['title'], anime['link'], BaseUrl)
                    anime_num = anime_num + 1
                padding = padding + 300

    def callback(self, url):
        webbrowser.open_new(url)
        cdd.video_download(url, 12)

    def create_label(self, frame, name, posx, posy):
        self.labels[name] = tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 16))
        self.labels[name].place(x = posx, y = posy)

    def create_image_and_link(self, frame, data, link, url, w, h):
        load = Image.open("src/animes/"+data.split("/")[-1])
        raw_image = load.resize((w, h), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(raw_image)
        self.images[data] = tk.Label(frame, image=image, cursor="hand2")
        self.images[data].bind("<Button-1>", lambda e: self.callback(url+link))
        self.images[data].image = image
        self.images[data].grid(row=0, column=0, sticky=tk.W+tk.N+tk.E)

    def create_title_and_link(self, frame, name, link, url):
        self.titles[name] = tk.Label(frame, text=name, bg="BlanchedAlmond", font=("", 8), wraplength=200, cursor="hand2")
        self.titles[name].bind("<Button-1>", lambda e: self.callback(url+link))
        self.titles[name].grid(row=1, column=0, sticky=tk.W+tk.S+tk.E)
