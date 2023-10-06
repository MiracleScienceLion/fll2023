from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon


def run(bot: Robot):
    bot.reset_heading(0)
    skate_park = (850, -580)
    front_point = (675, -660)
    back_point = (600, -570)
    polygon(bot, vertices=[(0, -900), (790, -670), skate_park])
    polygon(bot, vertices=[skate_park, front_point], forward=False)
    polygon(bot, vertices=[front_point, back_point], forward=False)
    for i in range(3):
        polygon(bot, vertices=[back_point, front_point])
        polygon(bot, vertices=[front_point, back_point], forward=False)
    # polygon(bot, vertices=[(730,-730),(630,-580)])
    # polygon(bot, vertices=[(730,-730),(), (910,60),(840,60)])
    # polygon(bot, vertices=[(840,60),(910,60)], forward=False)
    # polygon(bot, vertices=[(910,60),(880,120),(940,180),(890,520),(290,950)])


def main():
    bot = Robot()
    run(bot)


if __name__ == "__main__":
    main()
