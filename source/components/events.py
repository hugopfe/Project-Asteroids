from types import FunctionType
from typing import Dict, Tuple, Union


class EventGrouping:

    def register(self, d_event: Dict):
        ev = d_event
        if isinstance(ev[1], dict):
            self.__dict__.get(ev[0]).update(ev[1])

        self.__dict__.update(d_event)

    def get(self):
        return self.__dict__

    def __getitem__(self, k):
        return self.__dict__.get(k)


class EventsHandler:

    def __init__(self):
        self.events = EventGrouping()

    def register_event(self, *command: Tuple[FunctionType, Union[int, Tuple[int, Tuple[str, int]]]]):
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

            if isinstance(c[1], tuple):
                funcs_list = self.events[ev_keys[0]
                                         ][ev_keys[1]]  # TODO: Fix it!

                if funcs_list and func not in funcs_list:
                    d_out = {ev_keys[0]: {ev_keys[1]: func}}
                    self.events.register(d_out)

            else:
                funcs_list = self.events[ev_keys]

                if funcs_list and func not in funcs_list:
                    d_out = {ev_keys: func}
                    self.events.register(d_out)

    def trigger_event(self, k1, k2=None):
        if k2 is not None:
            for func in self.events[k1][k2]:
                func()
        else:
            for func in self.events[k1]:
                func()


events_handler = EventsHandler()

__all__ = ['events_handler']
