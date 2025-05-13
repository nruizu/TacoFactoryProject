#Autor: Nicolas Ruiz

from abc import ABC, abstractmethod
from django.http import HttpRequest

class DownloadOrderInterface(ABC):
    @abstractmethod
    def download_order(self, request: HttpRequest):
        pass

    @abstractmethod
    def get_content_type(self):
        pass

    @abstractmethod
    def get_filename(self):
        pass