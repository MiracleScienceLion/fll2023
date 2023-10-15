from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop
from pybricks.tools import wait
from pybricks.hubs import PrimeHub

hub = PrimeHub()

from fll_robot import Robot
from lib_turn import gyro_turn, turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon


def run(bot: Robot):
    angle = 270
    bot.reset_heading(-90)
    bot.left_motor.run_angle(speed=300, rotation_angle=-1 * angle)
    initial_positioñ = (120, 730)
    polygon(bot, vertices=[initial_positioñ, (120, 510)], forward=True, route_type='straight', reverse=True)
    bot.left_motor.run_angle(speed=300, rotation_angle=angle, wait=False)
    pivot_point = (410, 920)
    polygon(bot, vertices=[initial_positioñ, pivot_point], forward=False, route_type='curve')
    polygon(bot, vertices=[pivot_point, (955, 600)], forward=False, route_type='straight')


def main():  # 71.5
    bot = Robot()
    run(bot)


if __name__ == "__main__":
    main()
