import logging
import math
import random
import time

DEFAULT_STD = 0.1
MAX_INTERVAL = 1.2
MIN_TIMEOUT = 0.3


# a class to ignore keyboard input, but only when it keyboard input should be ignored
class SmartIgnorer:

    def __init__(self):
        # the word that was just selected (this is the time we possibly ignore keyboard input)
        self.just_selected = ''
        self.index = -1
        # the cumulative mean time between characters typed and std
        self.mean = -1
        self.count = 0
        self.m2 = 0
        # the last timestamp
        self.last_time = 0

    # welford's online algorithm for cumulative variance
    def update_stats(self, new_value):
        self.count += 1
        if self.mean <= 0:
            self.mean = new_value
        delta = new_value - self.mean
        self.mean += delta / self.count
        delta2 = new_value - self.mean
        self.m2 += delta * delta2

    def _std(self):
        if self.count < 2:
            return DEFAULT_STD
        return math.sqrt(self.m2 / self.count)

    def _get_interval(self):
        new_last_time = time.time()
        interval = new_last_time - self.last_time
        self.last_time = new_last_time
        # avoid massive outliers bringing the average way up
        return min(interval, MAX_INTERVAL)

    def add_interval(self, word_start: bool, just_selected='', selected_index=-1):

        self.just_selected = just_selected
        self.index = selected_index
        if word_start:
            self.last_time = time.time()
            return
        self.update_stats(self._get_interval())

    def should_ignore(self, ch: int) -> bool:
        # we should only ignore after a word was selected
        if self.just_selected == '':
            return False
        # any non-alpha character implies intent and therefore we should not ignore
        if not (ord('A') <= ch <= ord('Z') or ord('a') <= ch <= ord('z')):
            return False
        interval = self._get_interval()

        ch = chr(ch).upper()
        # if the character is the continuing character in the string they selected
        if self.index < len(self.just_selected) and self.just_selected[self.index] == ch:
            self.index += 1
            # looks unlikely they are continuing word, even though
            if interval > self.mean + 3.2 * self._std():
                return False

            return True
        else:
            # anything within MIN_TIMEOUT is probably an accident
            if interval < MIN_TIMEOUT:
                return True
        return False
