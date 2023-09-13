from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow

def run(bot: Robot):
    print("mission_08_camera")

def main():
    bot = Robot()
    run(bot)

if __name__ == "__main__":
    main()
