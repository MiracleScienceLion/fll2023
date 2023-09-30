from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon


def run(bot: Robot):
    bot.reset_heading(0)
    polygon(bot, vertices=[(700,-700)], forward=True, reverse=True)
def main():
    bot = Robot()
    run(bot)


if __name__ == "__main__":
    main()
