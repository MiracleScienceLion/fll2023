from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from pickup_sam import deploy, undeploy
from lib_line_follow import line_follow
from lib_polygon import polygon


def trip_03_part_1(bot: Robot):
    bot.reset_heading(0)
    skate_park = (850, -580)
    front_point = (660, -680)
    back_point = (570, -590)
    pivot_point = (700, -550)
    polygon(bot, vertices=[(20, -900), (790, -670), skate_park])
    polygon(bot, vertices=[skate_park, front_point], forward=False)
    deploy(bot, wait=True)
    # 1
    polygon(bot, vertices=[back_point, front_point])
    undeploy(bot, wait=True)
    polygon(bot, vertices=[front_point, back_point], forward=False)

    # 2
    polygon(bot, vertices=[back_point, front_point])
    polygon(bot, vertices=[front_point, back_point], forward=False)

    # 3
    pivot_point_r = (500, -620)
    polygon(bot, vertices=[back_point, front_point])
    polygon(bot, vertices=[front_point, pivot_point_r], forward=False, route_type='curve')

    polygon(bot, vertices=[pivot_point_r, pivot_point], route_type='curve')
    # polygon(bot, vertices=[(730,-730),(), (910,60),(840,60)])
    # polygon(bot, vertices=[pivot_point,(910,60)], forward=False)
    polygon(bot, vertices=[pivot_point, (650, 0), (600, 0)])
    # polygon(bot, vertices=[(600, 0), (1050, 0)], forward=False)


def trip_03_part_2(bot: Robot):
    # bot.wait_for_stationary()
    bot.reset_heading(180)
    light_show_point = (960, 0)
    polygon(bot, vertices=[(1125, 0), light_show_point])
    polygon(bot, vertices=[light_show_point, (700,120), (700,120)])
    # polygon(bot, vertices=[light_show_point, (700,120), (880,120),(940,180),(890,520),(290,950)])


def run(bot: Robot):
    trip_03_part_1(bot)
    trip_03_part_2(bot)



def main():
    bot = Robot()
    run(bot)


if __name__ == "__main__":
    main()
