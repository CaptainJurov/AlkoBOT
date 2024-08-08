import asyncio
import logging
import threading
import random
from Modules import Classes
logging.basicConfig(level=logging.INFO, filename="bot_log.log",filemode="w")

class Coin:
    def __init__(self, map: Classes.Map):
        self.kd_timer = 60
        self.timer = threading.Timer(self.kd_timer, self.update_course)
        self.timer.start()
        self.course = [1000]*(60*24)
        self.Map: Classes.Map = map
        self.correct_modifier = 1

    def update_course(self):
        del self.course[0]
        course_delta = (self.political_correct())*self.range_correct_system()+self.player_influence_correcting()+self.random_correct()
        self.course.append(int(self.political_correct()+course_delta))
        if self.course[-1]<100:
            self.course[-1]=1000
        logging.info(f"COIN - {self.course[-1]}")
        self.timer = threading.Timer(self.kd_timer, self.update_course)
        self.timer.start()

    def get_course(self) -> int:
        return self.course[-1]

    def random_correct(self) -> int:
        return random.randint(-10, 10)

    def political_correct(self) -> float:
        counter: int = 0
        for y in self.Map.map:
            for x in y:
                if x.fraction!=self.Map.fraction_list[0]:
                    counter+=1
        return int(counter/len(self.Map.fraction_list))

    def player_influence_correcting(self) -> int:
        delta:float = 0
        for y in self.Map.map:
            for x in y:
                match x.building.building_type:
                    case "work" | "shop" | "mine":
                        delta+=0.05
                    case "bank":
                        delta+=0.1
                    case "warriors":
                        delta-=0.05
                    case "casino":
                        delta-=0.1
                    case _:
                        continue
        return int(delta*1000)

    def range_correct_system(self) -> float:
        if self.get_course()>10000:
            self.correct_modifier-=0.01
        if self.get_course()<500:
            self.correct_modifier+=0.02
        return self.correct_modifier

