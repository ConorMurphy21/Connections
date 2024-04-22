import time


# a class to ignore keyboard input, but only when it keyboard input should be ignored
class SmartIgnorer:

    def __init__(self):
        # the word that was just selected (this is the time we possibly ignore keyboard input)
        self.just_selected = ''
        # the cumulative average time between characters typed
        self.cum_interval_average = 0
        # the number of samples for the cumulative average
        self.cum_n = 0
        # the average time
        self.current_interval_average = 0
        self.current_n = 0
        # the last timestamp
        self.last_time = 0

    def add_interval(self, word_start: bool, just_selected=''):
        self.just_selected = just_selected
        if word_start:
            # add current avg to cumulative and reset current
            # avoid possible divide by 0
            if self.cum_n + self.current_n > 0:
                self.cum_interval_average = (self.current_interval_average * self.current_n +
                                             self.cum_interval_average * self.cum_n) / (self.cum_n + self.current_n)
            self.cum_n += self.current_n
            self.current_interval_average = 0
            self.current_n = 0
            self.last_time = time.time()
            return

        interval = time.time() - self.last_time
        self.last_time = time.time()
        interval = max(interval, 1200)  # avoid massive outliers bringing the average way up
        self.current_interval_average = (self.current_interval_average * self.current_n + interval) \
                                        / (self.current_n + 1)
        self.current_n += 1

    def should_ignore(self, ch) -> bool:
        if self.just_selected == '':
            return False
