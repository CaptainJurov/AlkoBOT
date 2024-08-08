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
            pickle.dump(Map, file)
        with open("Coin.pickle", "wb") as file:
            pickle.dump(Coin.course, file)
        with open("Players.pickle", "wb") as file:
            pickle.dump(players, file)
        print("saved")
        self.timer = threading.Timer(150, self.update_kd, args=(Map, players, Coin))
        self.timer.start()