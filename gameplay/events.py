class EventsManager:
    _events = {'w': False, 's': False, 'a': False, 'd': False, 'mouse1': False}

    @classmethod
    def key_down(cls, key):
        cls._events[key] = True

    @classmethod
    def key_up(cls, key):
        cls._events[key] = False

    def get_events(self, *args):
        result = {}
        for arg in args:
            if value := self._events.get(arg):
                result[arg] = value
        return result

    def get(self, arg):
        return self._events.get(arg)
