from lib_polygon import polygon
from pickup_sam import deploy, undeploy
from mission_11_light import run as run_light
from fll_robot import Robot

light_show_y = -25


def trip_03_part_1(bot: Robot):
    bot.reset_heading(0)
    skate_park = (860, -540)
    front_point = (675, -675)
    back_point = (590, -590)
    pivot_point = (680, -570)
    pivot_point_r = (500, -620)
    polygon(bot, vertices=[(20, -900), (790, -670), skate_park])
    polygon(bot, vertices=[skate_park, front_point], forward=False, route_type='curve')
    deploy(bot, wait=True)
    # 1
    polygon(bot, vertices=[back_point, front_point])
    undeploy(bot, wait=True)
    polygon(bot, vertices=[front_point, back_point], forward=False)

    # 2
    polygon(bot, vertices=[back_point, front_point])
    polygon(bot, vertices=[front_point, back_point], forward=False)

    # 3
    polygon(bot, vertices=[back_point, front_point])
    polygon(bot, vertices=[front_point, pivot_point_r], forward=False, route_type='curve')

    polygon(bot, vertices=[pivot_point_r, pivot_point], route_type='curve')
    light_show_deploy = (650, light_show_y)
    polygon(bot, vertices=[pivot_point, light_show_deploy])
    # polygon(bot, vertices=[light_show_deploy, (660, light_show_y)], forward=False)
    bot.turn(92, turn_rate=66, turn_acceleration=100)
    # polygon(bot, vertices=[(600, light_show_y), (1000, light_show_y)], forward=False)


def trip_03_part_2(bot: Robot):
    # bot.reset_heading(180)
    light_show_point = (960, light_show_y)
    # polygon(bot, vertices=[(1125, light_show_y), light_show_point])
    run_light(bot)
    m05_deploy = (1000, 120)
    m05_finishing = (880, 200)
    polygon(bot, vertices=[light_show_point, m05_deploy, m05_finishing])
    polygon(bot, vertices=[m05_finishing, (890, 570), (600, 750), (280, 750)])


def run(bot: Robot):
    trip_03_part_1(bot)
    trip_03_part_2(bot)


if __name__ == "__main__":
    bot = Robot()
    run(bot)
