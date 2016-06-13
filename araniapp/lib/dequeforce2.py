#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import deque, defaultdict


class Queue(deque):
    '''
        documentar codigo
    '''
    # Lista
    def __init__(self, iterable=(), maxlen=None):
        deque.__init__(self, iterable, maxlen)
        self.lib = defaultdict(dict)
        self.actlib = 0

    def __hash(self, r):
        self.lib[hash(r)] = r

    def length(self):
        def comp(x):
            n = 0
            if type(x) != int:
                n += 1
            return n

        return sum(comp(elem) for elem in deque(self))

    def append(self, e):
        if type(e) != int:
            e = e.lower()
            if hash(e) in deque(self):
                pass
            elif e in deque(self):
                pass
            else:
                deque.appendleft(self, e)
                if self.actlib == 1:
                    self.__hash(e)
        elif e not in deque(self):
            return deque.append(self, e)
        else:
            pass

    def next(self):
        if self.length() != 0:
            popleft = deque.popleft(self)
            self.append(hash(popleft))
            if type(popleft) != int:
                return popleft
        else:
            return 0

    def show(self):
        if self.actlib == 1:
            return dict(self.lib)
        else:
            return None

    def extend(self):
        pass
