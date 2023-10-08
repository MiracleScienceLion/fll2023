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
deploy_angle = 120
lift_target_angle = 30
power_lift_percent = 90

rotation_speed = 150
lift_speed = 100
straight_speed = 66


def backoff(bot: Robot):
    bot.left_motor.run_target(rotation_speed, deploy_angle * gear_ratio)
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
    bot.left_motor.run_target(deploy_speed, deploy_angle * gear_ratio)
    bot.straight(150)


def run(bot: Robot):
    deploy(bot)
    # power lift
    power_lift = lift_target_angle * power_lift_percent / 100
    lift(bot, rotation_speed, power_lift, straight=20)
    # fine tune height
    fine_tune = lift_target_angle * (100 - power_lift_percent) / 100
    lift(bot, lift_speed, lift_target_angle, straight=10)
    backoff(bot)


if __name__ == "__main__":
    bot = Robot()
    run(bot)
