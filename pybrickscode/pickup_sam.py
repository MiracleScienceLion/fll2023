from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon

motor_gear = 12
load_gear = 20
gear_ratio = load_gear / motor_gear

deploy_angle = 94 * gear_ratio

rotation_speed = 300


def deploy(bot: Robot, wait = False):
    bot.right_motor.run_angle(rotation_speed, deploy_angle, wait=wait)


def undeploy(bot:Robot, wait = False):
    bot.right_motor.run_angle(rotation_speed, -deploy_angle, wait=wait)


if __name__ == "__main__":
    from pybricks.tools import wait
    bot = Robot()
    deploy(bot)
    undeploy(bot)
