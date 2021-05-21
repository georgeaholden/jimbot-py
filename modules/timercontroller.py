import datetime
import time


class TimerController:
    """Class to handle a dictionary of different timers and implement methods for resetting and checking them"""

    def __init__(self, timers=None):
        """Creates a dictionary called timers, which stores string:datetime entries. Optional parameter timers, a list
        of string timer names to add"""
        self.timers = {}
        if timers:
            for timer in timers:
                self.add_timer(timer)

    def add_timer(self, timer, hours=0, minutes=0, seconds=0):
        """Adds a new str timer to the dictionary"""
        self.timers[timer] = datetime.datetime.now() - datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def time_has_elapsed(self, timer, hours=0, minutes=0, seconds=0):
        """Checks if the provided timer has passed the provided hours, minutes, seconds"""
        original = self.timers[timer]
        return datetime.datetime.now() - original > datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def reset_timer(self, timer):
        """Updates a timer to the current time"""
        self.timers[timer] = datetime.datetime.now()


if __name__ == '__main__':
    """Test code"""
    timer_controller = TimerController()
    timer_controller.add_timer('test', hours=3)
    print(timer_controller.time_has_elapsed('test', hours=4))

