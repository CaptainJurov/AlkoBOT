import time
import threading
from typing import Callable
import pickle


class Timer:

    def __init__(self, Map, players, Coin):
        self.timer = threading.Timer(150, self.update_kd, args=(Map, players, Coin))
        self.timer.start()

    def update_kd(self, Map, players, Coin):
        print("saving...")
        with open("Map.pickle", "wb") as file:
            goal = [Map, Coin, players]
            pickle.dump(goal, file)
        print("saved")
        self.timer = threading.Timer(150, self.update_kd, args=(Map, players, Coin))
        self.timer.start()