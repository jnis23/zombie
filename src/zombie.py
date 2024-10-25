from enum import Enum
from hand import Hand

class ZState(Enum):
    IDLE = 0
    STIRRING = 1
    LUNGING = 2

class Zombie:
    state: ZState
    stopped: bool
    twitch_speed: int

    def __init__(self, twitch_speed: int):
        self.state = ZState.IDLE
        self.hand = Hand()
        self.stopped = False
        self.twitch_speed = twitch_speed

    def is_connected(self) -> bool:
        try:
            self.hand.index.curl(0, 1000)
            return True
        except Exception:
            return False

    def run(self):
        if not self.is_connected():
            print("Hand not connected")
            return

        while not self.stopped:
            match self.state:
                case ZState.IDLE:
                    self.idle()
                case ZState.STIRRING:
                    self.stirring()
                case ZState.LUNGING:
                    self.lunging()

    def stop(self):
        self.stopped = True

    def update(self, state: ZState):
        self.state = state

    def idle(self):
        pass

    def stirring(self):
        """Zombie senses something nearby and starts twitching"""
        self.hand.twitch(self.twitch_speed)

    def lunging(self):
        """Hand fully extends and then slowly curls back"""
        pass
