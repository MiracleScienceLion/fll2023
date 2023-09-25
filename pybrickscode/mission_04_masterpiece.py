from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon


def run(bot: Robot):
    polygon(robot=bot, vertices=0, forward=1, reverse=True)
    # wheels.straight(510)
    # wheels.curve(0,-66)
    # wheels.straight(850)
    # wheels.straight(-830)
    # wheels.curve(0,69.3)
    # wheels.straight(-510)


def main():
    bot = Robot()
    run(bot)


if __name__ == "__main__":
    main()
