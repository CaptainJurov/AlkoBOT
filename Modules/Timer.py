import time
import threading


class Timer:
    class Point:
        def __init__(self, func, user_id: int = None, *args):
            self.func = func
            self.user_id: int = user_id
            self.args = args

        def __del__(self):
            if len(self.args)>0:
                self.func(self.args)
            else:
                self.func()

        def get_id(self):
            return self.user_id

    def __init__(self):
        self.items: {int: [Timer.Point]} = {}
        self.timer = threading.Timer(1, self.update_kd)
        self.timer.start()

    def add_timer(self, point: Point, time_point: int = 1):
        timer = int(time.time())
        try:
            self.items[timer+time_point].append(point)
        except:
            self.items[timer+time_point] = [point]

    def update_kd(self):
        timer = int(time.time())
        if len(self.items)>0:
            for tim in self.items:
                if tim <= timer:
                    del self.items[tim]
                    break
        self.timer = threading.Timer(1, self.update_kd)
        self.timer.start()

    def check_user(self, user_id: int) -> bool:
        i: [Timer.Point]
        j: Timer.Point
        if len(self.items)>0:
            for i in self.items:
                for j in self.items[i]:
                    if j.get_id()==user_id:
                        return True
        return False

    def get_time(self, user_id: int):
        if len(self.items) > 0:
            for i in self.items:
                for j in self.items[i]:
                    if j.get_id() == user_id:
                        return i-int(time.time())
        return 0
