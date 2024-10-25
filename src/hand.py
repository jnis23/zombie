import os
import random
import firmware
import configparser

hamsa_config = os.path.join(os.path.dirname(__file__), "..", "hamsa.config")
config = configparser.ConfigParser()
config.read(hamsa_config)

robo_hand = firmware.Hand()


class Finger:
    def __init__(self, name: str):
        self.name = name
        self.data = config[f"{name} curl"]

    def curl(self, position: float, time: int) -> None:
        params = [
            self.data.getint("in"),
            self.data.getint("out"),
            self.data.getint("id"),
        ]
        if robo_hand.curl(position, time, *params) == 1:
            raise Exception(f"Failed to curl {self.name}")

    def curl_position(self) -> float:
        params = [
            self.data.getint("in"),
            self.data.getint("out"),
            self.data.getint("id"),
        ]
        return robo_hand.curl_position(*params)

    def wiggle(self, position: float, time: int) -> None:
        params = [
            self.data.getint("left"),
            self.data.getint("right"),
            self.data.getint("id"),
        ]
        robo_hand.wiggle(position, time, *params)

    def wiggle_position(self) -> float:
        params = [
            self.data.getint("left"),
            self.data.getint("right"),
            self.data.getint("id"),
        ]
        return robo_hand.wiggle_position(*params)


pinky = Finger("pinky")
ring = Finger("ring")
middle = Finger("middle")
index = Finger("index")
thumb = Finger("thumb")


def curl_wrist(position: float, time: int) -> None:
    finger_data = config["wrist"]
    params = [
        finger_data.getint("forwards"),
        finger_data.getint("backwards"),
        finger_data.getint("id"),
    ]
    robo_hand.curl(position, time, *params)


class Hand:
    def __init__(self):
        self.pinky = Finger("pinky")
        self.ring = Finger("ring")
        self.middle = Finger("middle")
        self.index = Finger("index")
        self.thumb = Finger("thumb")

    def curl_wrist_pos(self) -> float:
        finger_data = config["wrist curl"]
        params = [
            finger_data.getint("forwards"),
            finger_data.getint("backwards"),
            finger_data.getint("id"),
        ]
        return robo_hand.curl_position(*params)


    def twitch(self, twitch_speed: int) -> None:
        twitch_amount = 0.1  # 10% of the current position
        twitch_chance = 0.8  # 80% chance to twitch
        for finger in [self.pinky, self.ring, self.middle, self.index, self.thumb]:
            if random.random() > twitch_chance:
                curr_pos = finger.curl_position()
                direction = 1 if random.random() > 0.5 else -1
                # If the finger is at the extremes, reverse direction
                if curr_pos > 0.9:
                    direction = -1
                elif curr_pos < 0.1:
                    direction = 1
                finger.curl(curr_pos + direction * twitch_amount, twitch_speed)
