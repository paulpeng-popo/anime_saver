import threading
from abc import ABC, abstractmethod

from gui.downloader import video_download
from gui.models import (GetEveryWeekAnime, GetFinishAnimeList,
                        GetHomePageAnime, GetR18HomePageAnime, GetSeriesAnime)
from gui.views import View


class Controller(ABC):

    @abstractmethod
    def bind(self, view: View):

        raise NotImplementedError


class HomePageController(Controller):

    def __init__(self):
        self.model = GetHomePageAnime()
        self.view = None
        self.url = "https://myself-bbs.com/"

    def bind(self, view: View):
        self.view = view
        self.view.create_view(self.model.start_crawler())
        self.view.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.view.canvas.bind('<Leave>', self._unbound_to_mousewheel)
        self.view.controll_frame.bind(
            '<Configure>',
            lambda e: self.view.canvas.configure(
                scrollregion=self.view.canvas.bbox("all")
            )
        )

        for item in self.view.images:
            obj = self.view.images[item][0]
            url = self.url+self.view.images[item][1]
            obj.bind("<Button-1>", self.step_func(url))

        for item in self.view.titles:
            obj = self.view.titles[item][0]
            url = self.url+self.view.titles[item][1]
            obj.bind("<Button-1>", self.step_func(url))

    def step_func(self, url):
        return lambda event: self.callback(event, url)

    def callback(self, event, url):
        t = threading.Thread(target=video_download, args = (url, 12,))
        t.start()

    def _bound_to_mousewheel(self, event):
        self.view.canvas.bind_all(
            '<MouseWheel>',
            lambda e: self.view.canvas.yview_scroll(int(-1*(e.delta/60)), "units")
        )

    def _unbound_to_mousewheel(self, event):
        self.view.canvas.unbind_all("<MouseWheel>")


class EveryWeekRenewController(Controller):

    def __init__(self):
        self.model = GetEveryWeekAnime()
        self.view = None
        self.url = "https://myself-bbs.com/"

    def bind(self, view: View):
        self.view = view
        self.view.create_view(self.model.start_crawler())
        self.view.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.view.canvas.bind('<Leave>', self._unbound_to_mousewheel)
        self.view.controll_frame.bind(
            '<Configure>',
            lambda e: self.view.canvas.configure(
                scrollregion=self.view.canvas.bbox("all")
            )
        )

        for item in self.view.titles:
            obj = self.view.titles[item][0]
            url = self.url+self.view.titles[item][1]
            obj.bind("<Button-1>", self.step_func(url))

    def step_func(self, url):
        return lambda event: self.callback(event, url)

    def callback(self, event, url):
        print(url)
        # t = threading.Thread(target=video_download, args = (url, 12,))
        # t.start()

    def _bound_to_mousewheel(self, event):
        self.view.canvas.bind_all(
            '<MouseWheel>',
            lambda e: self.view.canvas.yview_scroll(int(-1*(e.delta/60)), "units")
        )

    def _unbound_to_mousewheel(self, event):
        self.view.canvas.unbind_all("<MouseWheel>")


class SeriesController(Controller):

    def __init__(self, finish=False):
        if finish:
            self.model = GetSeriesAnime(url='https://myself-bbs.com/forum-113-1.html')
            self.pageUrl = "https://myself-bbs.com/forum-113-{}.html"
            self.text = "完結動畫"
        else:
            self.model = GetSeriesAnime(url='https://myself-bbs.com/forum-133-1.html')
            self.pageUrl = "https://myself-bbs.com/forum-133-{}.html"
            self.text = "連載動畫"
        self.view = None
        self.url = "https://myself-bbs.com/"

    def bind(self, view: View):
        self.view = view
        self.view.type = self.text
        self.view.create_view(self.model.start_crawler())
        self.view.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.view.canvas.bind('<Leave>', self._unbound_to_mousewheel)
        self.view.controll_frame.bind(
            '<Configure>',
            lambda e: self.view.canvas.configure(
                scrollregion=self.view.canvas.bbox("all")
            )
        )

        for item in self.view.images:
            obj = self.view.images[item][0]
            url = self.url+self.view.images[item][1]
            obj.bind("<Button-1>", self.step_func(url))

        for item in self.view.titles:
            obj = self.view.titles[item][0]
            url = self.url+self.view.titles[item][1]
            obj.bind("<Button-1>", self.step_func(url))

        for item in self.view.pages:
            obj = self.view.pages[item][0]
            url = self.pageUrl.format(self.view.pages[item][1])
            obj.config(command=lambda url=url: self.change_page(url))

    def step_func(self, url):
        return lambda event: self.callback(event, url)

    def callback(self, event, url):
        print(url)
        # t = threading.Thread(target=video_download, args = (url, 12,))
        # t.start()

    def change_page(self, url):
        for item in self.view.frames:
            item.place_forget()
        for item in self.view.labels:
            self.view.labels[item].place_forget()
        for item in self.view.pages:
            self.view.pages[item][0].grid_forget()
        self.view.canvas.yview_moveto(0)
        self.model.Url = url
        self.bind(self.view)

    def _bound_to_mousewheel(self, event):
        self.view.canvas.bind_all(
            '<MouseWheel>',
            lambda e: self.view.canvas.yview_scroll(int(-1*(e.delta/60)), "units")
        )

    def _unbound_to_mousewheel(self, event):
        self.view.canvas.unbind_all("<MouseWheel>")


class FinishListController(Controller):

    def __init__(self):
        self.model = GetFinishAnimeList()
        self.data = self.model.start_crawler()
        self.menu = list(self.data.keys())
        self.selected = self.menu[0]
        self.view = None
        self.url = "https://myself-bbs.com/"

    def bind(self, view: View):
        self.view = view
        self.view.create_view(self.menu, self.selected, self.data[self.selected])
        self.view.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.view.canvas.bind('<Leave>', self._unbound_to_mousewheel)
        self.view.controll_frame.bind(
            '<Configure>',
            lambda e: self.view.canvas.configure(
                scrollregion=self.view.canvas.bbox("all")
            )
        )

        self.view.combobox.bind("<<ComboboxSelected>>", self.change_entry)

        for item in self.view.titles:
            obj = self.view.titles[item][0]
            url = self.url+self.view.titles[item][1]
            obj.bind("<Button-1>", self.step_func(url))

    def step_func(self, url):
        return lambda event: self.callback(event, url)

    def callback(self, event, url):
        print(url)
        # t = threading.Thread(target=video_download, args = (url, 12,))
        # t.start()

    def change_entry(self, event):
        self.selected = self.view.combobox.get()
        for item in self.view.frames:
            item.place_forget()
        self.view.canvas.yview_moveto(0)
        self.bind(self.view)

    def _bound_to_mousewheel(self, event):
        self.view.canvas.bind_all(
            '<MouseWheel>',
            lambda e: self.view.canvas.yview_scroll(int(-1*(e.delta/60)), "units")
        )

    def _unbound_to_mousewheel(self, event):
        self.view.canvas.unbind_all("<MouseWheel>")


class R18HomePageController(Controller):

    def __init__(self):
        self.model = GetR18HomePageAnime()
        self.view = None
        self.url = "https://myself-bbs.com/"

    def bind(self, view: View):
        self.view = view
        self.view.create_view(self.model.start_crawler())
        self.view.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.view.canvas.bind('<Leave>', self._unbound_to_mousewheel)
        self.view.controll_frame.bind(
            '<Configure>',
            lambda e: self.view.canvas.configure(
                scrollregion=self.view.canvas.bbox("all")
            )
        )

        for item in self.view.images:
            obj = self.view.images[item][0]
            url = self.url+self.view.images[item][1]
            obj.bind("<Button-1>", self.step_func(url))

        for item in self.view.titles:
            obj = self.view.titles[item][0]
            url = self.url+self.view.titles[item][1]
            obj.bind("<Button-1>", self.step_func(url))

    def step_func(self, url):
        return lambda event: self.callback(event, url)

    def callback(self, event, url):
        t = threading.Thread(target=video_download, args = (url, 12,))
        t.start()

    def _bound_to_mousewheel(self, event):
        self.view.canvas.bind_all(
            '<MouseWheel>',
            lambda e: self.view.canvas.yview_scroll(int(-1*(e.delta/60)), "units")
        )

    def _unbound_to_mousewheel(self, event):
        self.view.canvas.unbind_all("<MouseWheel>")
