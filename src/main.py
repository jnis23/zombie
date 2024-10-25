import threading
from zombie import ZState, Zombie

def controller(zombie: Zombie):
    while True:
        command = input("Enter command:\n1: Twitch\n2: Lunge\n3: Stop\nq: Quit\n>>")
        match command:
            case "1":
                zombie.update(ZState.STIRRING)
            case "2":
                zombie.update(ZState.LUNGING)
            case "3":
                zombie.stop()
            case "q":
                print("Quitting")
                zombie.stop()
                return
            case _:
                print("Invalid command")


if __name__ == "__main__":
    twitch_speed = 100
    zombie = Zombie(twitch_speed)

    zombie_thread = threading.Thread(target=zombie.run)
    zombie_thread.start()

    controller(zombie)

    zombie_thread.join()
    print("Zombie thread finished")
