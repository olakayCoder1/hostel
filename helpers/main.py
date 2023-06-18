from client.models import Hostel


class Injector:


    def __init__(self, request) -> None:
        self.request = request
        self.context = {}