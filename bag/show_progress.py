# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime, timedelta
from nine import range


class ShowingProgress(object):
    '''A generator that encapsulates your iterable, printing the progress
    every so many seconds. Usage::

        p = ShowingProgress(iterable, seconds=6)
        # Then use p instead of your iterable:
        for index, something in p:
            process(something)
    '''
    def __init__(self, iterable, message='Item #{} done. Working...',
                 seconds=6, done='Done in {time}! Total items: {total}'):
        self.iterable = iterable
        self.seconds = timedelta(0, seconds)
        self.message = message
        self.done = done

    def __iter__(self):
        utcnow = datetime.utcnow
        seconds = self.seconds
        started = printed = utcnow()
        for index, o in enumerate(self.iterable, 1):  # Start counting at 1
            yield index, o

            if seconds > utcnow() - printed:
                continue
            print(self.message.format(index))
            printed = utcnow()
        if self.done:
            print(self.done.format(total=index, time=utcnow() - started))


class PercentageDone(object):
    '''When you are processing a long iterable and it takes minutes,
    you should let the user know that your application is still working.
    This class helps do that in the console, without creating too
    much output.
    '''
    def __init__(self, max, granularity=6):
        '''Parameters:
        *max*: The number of elements that shall be processed.
        *granularity*: how many seconds must elapse between printing
        the percentage done.
        '''
        self.max = int(max)
        self.granularity = timedelta(0, granularity)
        self.current = 0
        self.start = self.printed = datetime.utcnow()

    def calc(self, val):
        '''Takes *val* (the current position relative to *max* and
        calculates:

        * self.current (int): the current percentage done
        * self.delta (timedelta): time elapsed since self.start
        * self.estimate (timedelta): how long this is going to take (total)
        * self.remaining (timedelta): how long you still have to wait

        Returns self.remaining.
        '''
        percent = 100 * int(val) / self.max
        if percent > self.current:
            self.current = percent
            self.delta = datetime.utcnow() - self.start
            self.estimate = timedelta(0, 100 * self.delta.seconds / percent)
            self.remaining = self.estimate - self.delta
            if self.remaining < timedelta(0):
                self.remaining = timedelta(0)
            return self.remaining

    def display(self, val):
        '''Calls self.calc() and prints the percentage done and
        how long the user still has to wait.

        But only does so every X seconds, where X is *granularity*.
        Does nothing if the granularity has not elapsed yet.
        '''
        if self.granularity > datetime.utcnow() - self.printed:
            return
        remaining = self.calc(val)
        if not remaining:
            return
        print('{0}% done, {1} left...'.format(
            self.current, str(remaining)[:7]))
        self.printed = datetime.utcnow()


class ShowingPercentage(PercentageDone):
    '''A generator that encapsulates your iterable, printing the
    percentage done.

    Usage:

        p = ShowingPercentage(iterable, len(iterable), granularity=6)
        # Then use p instead of your iterable:
        for index, something in p:
            process(something)
    '''
    def __init__(self, iterable, max, **k):
        super(ShowingPercentage, self).__init__(max, **k)
        self.iterable = iterable

    def __iter__(self):
        for i, o in enumerate(self.iterable):
            yield i, o
            self.display(i)


def test_percentage():
    from time import sleep
    for index, item in ShowingPercentage(range(100), max=100, granularity=4):
        sleep(.5)


def test_progress():
    from time import sleep
    for index, item in ShowingProgress(range(100), seconds=4):
        sleep(.237)
