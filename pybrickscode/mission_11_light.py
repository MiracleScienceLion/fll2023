from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon

black_gear = 12
gray_gear = 28
black_gear = 36
angle = -370
rotation_speed = 150
lift_speed = 100
straight_speed = 66


def backoff(bot: Robot):
    bot.left_motor.run_target(rotation_speed, 270, wait=False)
    bot.right_motor.run_target(rotation_speed, 270)
    bot.left_motor.run_target(rotation_speed, 0, wait=False)
    bot.right_motor.run_target(rotation_speed, 0, wait=False)
    while bot.right_color() != Color.BLUE:
        bot.motor_pair.drive(-straight_speed, 0)


def lift(bot: Robot, speed, target, straight):
    bot.left_motor.run_target(speed, target, wait=False)
    bot.right_motor.run_target(speed, target, wait=False)
    a = bot.left_motor.angle()
    t = abs((target - a) / speed)
    bot.motor_pair.settings(straight_speed=straight / t)
    bot.motor_pair.straight(straight)


def init(bot: Robot):
    bot.left_motor.reset_angle(0)
    bot.right_motor.reset_angle(0)
    bot.left_motor.run_target(rotation_speed, 270, wait=False)
    bot.right_motor.run_target(rotation_speed, 270)


def deploy(bot: Robot):
    bot.straight(120)


def run(bot: Robot):
    # polygon(bot, vertices=[(0, -960),(-540,830),(0,210),(0,500), forward=True, reverse=True])
    init(bot)
    # run deploy when robot is facing the tower and right eye on purple line
    deploy(bot)
    # power lift
    lift(bot, rotation_speed, 150, straight=100)
    # fine lift
    lift(bot, lift_speed, 30, straight=10)
    backoff(bot)


def main():
    bot = Robot()
    run(bot)


if __name__ == "__main__":
    main()
