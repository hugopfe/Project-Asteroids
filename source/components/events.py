from types import FunctionType
from typing import Dict, Tuple, Union


class EventGrouping:

    def register(self, d_event: Dict):
        ev_command = d_event

        for ev, sub_ev in ev_command.items():
            self_ev = self.__dict__.get(ev)
            if isinstance(sub_ev, dict):
                for sub, func_list in sub_ev.items():
                    if self_ev:
                        if self_ev.get(sub):
                            self.__dict__[ev][sub].extend(func_list)
                        else:
                            self.__dict__[ev][sub] = func_list
                    else:
                        self.__dict__[ev] = {sub: func_list}

            else:
                if self_ev:
                    self.__dict__[ev].extend(sub_ev)
                else:
                    self.__dict__[ev] = sub_ev

    def get(self, k1=None, k2=None):
        if k1:
            ret = self.__dict__.get(k1)
            if k2:
                d = self.__dict__.get(k1)
                ret = d.get(k2) if d is not None else None
        else:
            ret = self.__dict__

        return ret

    def __getitem__(self, k):
        return self.__dict__.get(k) or []


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
                reg_funcs = self.events.get(ev_keys[0], ev_keys[1])
                if reg_funcs:
                    if func in reg_funcs:
                        continue

                d_out = {ev_keys[0]: {ev_keys[1]: [func]}}
                self.events.register(d_out)

            else:
                reg_funcs = self.events.get(ev_keys)
                if reg_funcs:
                    if func in reg_funcs:
                        continue

                d_out = {ev_keys: [func]}
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
