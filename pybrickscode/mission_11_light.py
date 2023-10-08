from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon

motor_gear = 12
load_gear = 36
gear_ratio = load_gear / motor_gear

init_angle = 0
deploy_angle = 140 * gear_ratio
power_lift_target = 90
fine_lift_target = 30

rotation_speed = 150
lift_speed = 100
straight_speed = 66


def backoff(bot: Robot):
    bot.left_motor.run_target(rotation_speed, deploy_angle)
    bot.left_motor.run_target(rotation_speed, init_angle, wait=False)
    while bot.right_color() != Color.BLUE:
        bot.motor_pair.drive(-straight_speed, turn_rate=0)
    bot.stop()
    bot.left_motor.run_target(rotation_speed, init_angle)


def lift(bot: Robot, speed, target, straight=0):
    bot.left_motor.run_target(speed, target * gear_ratio)


def deploy(bot: Robot):
    bot.left_motor.reset_angle(0)
    deploy_speed = 300
    bot.left_motor.run_target(deploy_speed, deploy_angle)
    bot.straight(150)


def run(bot: Robot):
    deploy(bot)
    # power lift
    lift(bot, rotation_speed, power_lift_target, straight=20)
    # fine tune height
    lift(bot, lift_speed, fine_lift_target, straight=10)
    backoff(bot)


if __name__ == "__main__":
    bot = Robot()
    run(bot)
