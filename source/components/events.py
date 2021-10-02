from pygame.event import get

from types import FunctionType
from typing import Tuple, Union


class EventsReg:

    def register(self, **d_event: dict):
        pass

    def get(self, k1, k2=None):
        ret = self.__dict__.get(k1)

        if k2:
            ev = self.__dict__.get(k1)
            ret = ev.get(k2) 

        return ret

    def __getitem__(self, k):
        return self.__dict__.get(k) or []


class SingleEvents(EventsReg):

    def register(self, **d_event: dict):
        # {ev_keys: [func]}

        k1 = d_event['k1']
        funcs = d_event['funcs']

        if self.__dict__.get(k1):
            self.__dict__[k1].extend(funcs)
        else:
            self.__dict__[k1] = funcs

    def get(self, k1):
        return super().get(k1)

class MultiEvents(EventsReg):

    def register(self, **d_event: dict):
        # {ev_keys: {ev_keys[1]: [func]}}
        
        k1 = d_event['k1']
        k2 = d_event['k2']
        funcs = d_event['funcs']

        self_dict = self.__dict__
        
        if self_dict.get(k1):
            if self_dict[k1].get(k2):
                self_dict[k1][k2].extend(funcs)
            else:
                self_dict[k1][k2] = funcs
        else:
            self_dict[k1] = {k2: funcs}

    def get(self, k1, k2=None):
        return super().get(k1, k2)


class EventsHandler:

    def __init__(self):
        self.single_events = SingleEvents()
        self.multi_events = MultiEvents()

    def register_events(self, *command: Tuple[FunctionType, Union[int, Tuple[str, Tuple[str, int]]]]):
        """
        Adds many function to event's list.

        :param: command -> A tuple with 2 values:

            1st Value-> The funtion to be stored. \n
            2nd Value -> The event identifier, it can be a pygame constant or a tuple, \
            being the first value the constant identifier and the second value another tuple\
            with the event attibute to get.

        Example:
            (key_down, (KEYDOWN, ('key', K_UP)))
        """

        for c in command:
            func = c[0]
            ev = c[1]
            d_out = {}

            if isinstance(ev, tuple):
                d_out = {'k1': ev[0], 'k2': ev[1], 'funcs': [func]}
                self.multi_events.register(**d_out)
                print(f'> Event registered: {func.__qualname__} -> {ev}')

            else:
                d_out = {'k1': ev, 'funcs': [func]}
                self.single_events.register(**d_out)
                print(f'> Event registered: {func.__qualname__} -> {ev}')

        print()

    def remove_event(self, *command: Tuple[FunctionType, Union[int, Tuple[str, int]]]):
        """
        Removes many function to event's list.

        :param: command -> A tuple with 2 values:

            1st Value-> The funtion to be removed. \n
            2nd Value -> The event identifier, it can be a pygame constant or a tuple, \
            being the first value the constant identifier and the second value another tuple\
            with the event attibute to get.

        Example:
            (key_down, (KEYDOWN, ('key', K_UP)))
        """

        for c in command:
            func = c[0]
            ev = c[1]
            
            if isinstance(ev, tuple):
                funcs_registrated = self.multi_events[ev[0]][ev[1]]
                if func in funcs_registrated:
                    funcs_registrated.remove(func)
                    print(f'> Event removed: {func.__qualname__} -> {ev}')
            else:
                funcs_registrated = self.single_events[ev]
                if func in funcs_registrated:
                    funcs_registrated.remove(func)
                    print(f'> Event removed: {func.__qualname__} -> {ev}')

        print()

    def trigger_event(self, k1, k2=None):
        if k2:
            funcs = self.multi_events[k1][k2].copy()
            for func in funcs:
                func()
        else:
            funcs = self.single_events[k1].copy()
            for func in funcs:
                func()

    def events_loop(self):
        """ Checks events registrated. """

        for event in get():
            if self.multi_events[event.type]:
                sub_ev = self.check_sub_ev(event)
                if sub_ev and self.multi_events[event.type][sub_ev]:
                    self.trigger_event(event.type, sub_ev)
                    continue
            if self.single_events[event.type]:
                self.trigger_event(event.type)
    
    def check_sub_ev(self, event) -> Tuple:

        events = self.multi_events
        sub_events = events.get(event.type) or dict()
        
        for sub_event in sub_events.keys():
            ev_attr = getattr(event, sub_event[0])
            if ev_attr == sub_event[1]:
                return sub_event
        
        return None


def register_ev(*ev):
    if ev:
        if None in ev:
            ev = list(ev)
            ev.remove(None)
        events_handler.register_events(*ev)


def remove_ev(*ev):
    if ev:
        if None in ev:
            ev = list(ev)
            ev.remove(None)
        events_handler.remove_event(*ev)


def test_events():
    events_handler.events_loop()    


events_handler = EventsHandler()

__all__ = [
    'register_ev',
    'remove_ev',
    'test_events'
]
