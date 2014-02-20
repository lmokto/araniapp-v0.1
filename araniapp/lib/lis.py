#!/usr/bin/python
# -*- coding: utf-8 -*-


class li(object):
    def __new__(cls, iterable=(), *args, **kw):
        self = super(li, cls).__new__(cls, *args, **kw)
        self.clear()
        return self
    def __init__(self, iterable=()):
        self.clear()
        add = self.append
        for value in iterable:
            add(value)
    def clear(self):
        self.R = 60
        self.L = -60
        self.BLOCKSIZE = 60+7
        self.block =  [None] * self.BLOCKSIZE
        self.blockleft = [None] * self.BLOCKSIZE
        self.right = 0 #DERECHA self.block
        self.left = self.L #IZQUIERDA self.blockleft
        self.hashblock = list()
        self.lengthhash = 0
        self.length = 0
        self.i = -1
    def __appendhash(self, value):
        valuehash = abs(hash(value))
        if valuehash not in self.hashblock:
            self.hashblock.append(valuehash)
            self.lengthhash += 1
    def __get(self, value):
        if isinstance(value, str):
            value = value.lower()
        else:
            value = value
        valuehash = abs(hash(value))
        return valuehash, value
    def append(self, value): #derecha
        valuehash, value = self.__get(value)
        if self.right == self.R:
            newblock = self.BLOCKSIZE * [None]
            self.block = self.block + newblock
            self.R += 60
        if valuehash not in self.hashblock:
            self.block[self.right] = value
            self.length += 1
            self.right += 1
            self.__appendhash(valuehash)
    def pop(self):
        if self.length == 0:
            return
        index = self.__index(self.block)
        value = self.block[index]
        self.block[index] = None
        self.length -= 1
        return value
    def appendleft(self, value): #izquierda
        valuehash, value = self.__get(value)
        if self.left == self.L:
            newblock = self.BLOCKSIZE * [None]
            self.blockleft = newblock + self.blockleft
            self.L -= 60
        if valuehash not in self.hashblock:
            self.blockleft[self.left] = value
            self.__appendhash(value)
            self.length += 1
            self.left -= 1
    def popleft(self): #izquierda
        if self.length == 0:
            return
        index = self.__index(self.blockleft)
        value = self.blockleft[index]
        self.length -= 1
        del self.blockleft[index]
        return value
    def __index(self, block):
        it = iter(block)
        r = 0
        num = [n for n, i in enumerate(it) if n == r or n > r and i]
        index = min(num, key=lambda x:abs(x-len(block)))
        return index
    def extend(self, iterable):
        if iterable is self.block:
            iterable = list(iterable)
        for value in iterable:
            if abs(hash(value)) not in self.hashblock or value not in [self.blockleft + self.block]:
                self.append(value)
    def extendleft(self, iterable):
        if iterable is self.blockleft:
            iterable = list(iterable)
        for value in iterable:
            if abs(hash(value)) not in self.hashblock or value not in [self.blockleft + self.block]:
                self.appendleft(value)
    def count(self, value):
        c = sum([1 for i in [self.blockleft + self.block][0] if i == value])
        return c
    def cache(self, value):
        valuehash = abs(hash(value))
        pos = self.hashblock.index(valuehash)
        c = self.count(value)
        return {'count': c, 'value': value, 'hash': valuehash}
    def __len__(self):
        return self.length
    def __iter__(self):
        if self.i is not -1:
            self.i = -1
        return self
    def next(self):
        if self.length:
            block = [x for x in self.blockleft + self.block if not isinstance(x, type(None))]
        if self.i<len(block)-1:
            self.i += 1
            return block[self.i]
        else:
            raise StopIteration
    def __getitem__(self, index):
        try:
            value = [x for x in self.blockleft + self.block if not isinstance(x, type(None))][index]
            return value
        except:
            return
    def __delitem__(self, index):
        try:
            value = [x for x in self.blockleft + self.block if not isinstance(x, type(None))][index]
            if value in self.block:
                index = self.block.index(value)
                self.length -= 1
                del self.block[index]
            elif value in self.blockleft:
                index = self.blockleft.index(value)
                self.length -= 1
                del self.block[index]
        except:
            return
    def __dir__(self):
        return(['BLOCKSIZE', 'L', 'R', '__class__', '__contains__', '__copy__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'append', 'appendleft', 'blockleft', 'cache', 'clear', 'count', 'extend', 'extendleft', 'length', 'lengthhash', 'next', 'pop', 'popleft'])
    def __contains__(self, value):
        block = [x for x in self.blockleft + self.block if not isinstance(x, type(None))]
        if value in block:
            return True
        else:
            return False
    def __repr__(self):
        result = sum([1 for x in self.blockleft + self.block if not isinstance(x, type(None))])
        if result:
           block = [x for x in self.blockleft + self.block if not isinstance(x, type(None))]
        else:
            block = []
        return 'lis(%r)' % (block,)
    def __copy__(self):
        return self.__class__(self)
    def __eq__(self, other):
        if isinstance(other, li):
            return list(self) == list(other)
        else:
            return NotImplemented
    def __ne__(self, other):
        if isinstance(other, l):
            return list(self) != list(other)
        else:
            return NotImplemented
    def __lt__(self, other):
        if isinstance(other, li):
            return list(self) < list(other)
        else:
            return NotImplemented
    def __le__(self, other):
        if isinstance(other, li):
            return list(self) <= list(other)
        else:
            return NotImplemented
    def __gt__(self, other):
        if isinstance(other, li):
            return list(self) > list(other)
        else:
            return NotImplemented
    def __ge__(self, other):
        if isinstance(other, li):
            return list(self) >= list(other)
        else:
            return NotImplemented

if __name__ == '__main__':
    
    lista = li()
    test1 = ['a', 'b', 'c', 'd', 'f']
    test2 = ['g', 1, 2, 3, 'abc', 'dfg', 'A']
    
    for i in lis:
        lista.append(i)
    
    for i in lis2:
        lista.append(i)
    
    print len(a)