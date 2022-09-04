from abc import ABC, abstractmethod

from gui.models import GetEveryWeekAnime, GetHomePageAnime
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
        print(url)
        # t = threading.Thread(target=downloader.video_download, args = (url, 12,))
        # t.start()

    def _bound_to_mousewheel(self, event):
        self.view.canvas.bind_all(
            '<MouseWheel>',
            lambda e: self.view.canvas.yview_scroll(int(-1*(e.delta/60)), "units")
        )

    def _unbound_to_mousewheel(self, event):
        self.view.canvas.unbind_all("<MouseWheel>")
