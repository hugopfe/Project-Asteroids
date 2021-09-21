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

        if self.__dict__.get(k1):  # TODO: Verificar se __dict__ é necessário
            if self.__dict__[k1].get(k2):
                self.__dict__[k1][k2].extend(funcs)
            else:
                self.__dict__[k1][k2] = funcs
        else:
            self.__dict__[k1] = {k2: funcs}

    def get(self, k1, k2):
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
            ev_keys = c[1]
            d_out = {}

            if isinstance(ev_keys, tuple):  # {KEYDOWN: {}} → {KEYDOWN: [[], {}]}
                d_out = {'k1': ev_keys[0], 'k2': ev_keys[1], 'funcs': [func]}
                self.multi_events.register(**d_out)

            else:
                d_out = {'k1': ev_keys, 'funcs': [func]}
                self.single_events.register(**d_out)

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
                self.multi_events[ev[0]][ev[1]].remove(func)
            else:
                self.single_events[ev].remove(func)

    def trigger_event(self, k1, k2=None):
        if k2:
            for func in self.multi_events[k1][k2]:
                func()
        else:
            for func in self.single_events[k1]:
                func()

    def events_loop(self):
        for event in get():
            self.test_events(event)
    
    def test_events(self, event):
        """
        Checks events from a dict.

        This dict must have pygame constants as keys that will be
        compared with event.type, it's value can be: 
        a list, containg the functions that will be called or another dict.

        Value as dict is for compare another attribute of event. Dict
        must have tuples as keys:
            1st element: event attribute 
            2nd element: another constant

        Example:

            dict_events = {
                QUIT: [something()],
                KEYDOWN: {
                    ('key', K_up): [another_thing()]
                }
            }

            if event.type == dict_events[type_event2]:
                if dict_events[type_event2]

        """

        events = self.events.get()

        if self.single_events[event.type]:  # TODO: Find a way to do it!!!
            if isinstance(events.get(event.type), dict):
                sub_events = events.get(event.type)

                for sub_event in sub_events.keys():
                    ev_attr = getattr(event, sub_event[0])
                    if ev_attr == sub_event[1]:
                        trigger_event(event.type, sub_event)

            else:
                trigger_event(event.type)


def register_ev(*ev):
    events_handler.register_events(*ev)


def remove_ev(*ev):
    events_handler.remove_event(*ev)


def trigger_event(k1, k2=None):
    events_handler.trigger_event(k1, k2)


def test_events(event):
    events_handler.events_loop(event)    


events_handler = EventsHandler()


__all__ = [
    'register_ev',
    'remove_ev',
    'trigger_event',
    'test_events'
]
