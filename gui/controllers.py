from gui.models import GetHomePageAnime
from gui.views import View, AnimeBlock
from abc import ABC, abstractmethod

class Controller(ABC):

    @abstractmethod
    def bind(view: View):
        raise NotImplementedError

class HomePageController(Controller):

    def __init__(self):
        self.model = GetHomePageAnime()
        self.view = None

    def bind(self, view: View):
        self.view = view
        self.view.create_view(self.model.start_crawler())
