from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon

motor_gear = 12
transfer_gear = 28
load_gear = 36
gear_ratio = load_gear / motor_gear

init_angle = 0
deploy_angle = 180 * gear_ratio

rotation_speed = 150
lift_speed = 100
straight_speed = 66


def backoff(bot: Robot):
    bot.left_motor.run_target(rotation_speed, deploy_angle, wait=False)
    bot.right_motor.run_target(rotation_speed, deploy_angle)
    bot.left_motor.run_target(rotation_speed, init_angle, wait=False)
    bot.right_motor.run_target(rotation_speed, init_angle, wait=False)
    while bot.right_color() != Color.BLUE:
        bot.motor_pair.drive(-straight_speed, turn_rate=0)
    bot.left_motor.run_target(rotation_speed, init_angle, wait=False)
    bot.right_motor.run_target(rotation_speed, init_angle, wait=False)


def lift(bot: Robot, speed, target, straight):
    bot.left_motor.run_target(speed, target, wait=False)
    bot.right_motor.run_target(speed, target, wait=False)
    a = bot.left_motor.angle()
    t = abs((target - a) / speed)
    bot.motor_pair.settings(straight_speed=straight / t)
    bot.motor_pair.straight(straight)


def deploy(bot: Robot):
    bot.left_motor.reset_angle(0)
    bot.right_motor.reset_angle(0)
    deploy_speed = 300
    bot.left_motor.run_target(deploy_speed, deploy_angle, wait=False)
    bot.right_motor.run_target(deploy_speed, deploy_angle)
    bot.straight(120)


def run(bot: Robot):
    # polygon(bot, vertices=[(0, -960),(-540,830),(0,210),(0,500), forward=True, reverse=True])
    # run deploy when robot is facing the tower and right eye on purple line
    deploy(bot)
    # power lift
    power_angle = 140 * gear_ratio
    lift(bot, rotation_speed, power_angle, straight=100)
    # fine tune height
    fine_tune_angle = 100 * gear_ratio
    lift(bot, lift_speed, fine_tune_angle, straight=10)
    backoff(bot)


def main():
    bot = Robot()
    run(bot)


if __name__ == "__main__":
    main()
