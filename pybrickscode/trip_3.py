from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon
from pickup_sam import deploy, undeploy
from mission_11_light import run as run_light

light_show_y = -15


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
    polygon(bot, vertices=[pivot_point, (650, light_show_y), (600, light_show_y)])
    polygon(bot, vertices=[(600, light_show_y), (1000, light_show_y)], forward=False)


def trip_03_part_2(bot: Robot):
    bot.reset_heading(180)
    light_show_point = (960,  -10)
    polygon(bot, vertices=[(1125, light_show_y), light_show_point])
    run_light(bot)
    m05_deploy = (1000, 100)
    m05_finishing = (900, 200)
    polygon(bot, vertices=[light_show_point, m05_deploy, m05_finishing])
    polygon(bot, vertices=[m05_finishing, (890, 520), (350, 950)])


def run(bot: Robot):
    trip_03_part_1(bot)
    trip_03_part_2(bot)


def main():
    bot = Robot()
    run(bot)


if __name__ == "__main__":
    main()
