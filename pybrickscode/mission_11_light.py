from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch

from fll_robot import Robot

motor_gear = 12
load_gear = 36
gear_ratio = load_gear / motor_gear

init_angle = 0
deploy_angle = -130
lift_target_angle = -30

rotation_speed = 150
lift_speed = 100
straight_speed = 66
deploy_distance = 170

def backoff(bot: Robot):
    bot.left_motor.run_target(rotation_speed, deploy_angle * gear_ratio)
    bot.left_motor.run_target(rotation_speed, init_angle, wait=False)
    bot.straight(-deploy_distance, straight_speed)
    # while bot.right_color() != Color.BLUE:
    #     bot.motor_pair.drive(-straight_speed, turn_rate=0)
    bot.stop()
    bot.left_motor.run_target(rotation_speed, init_angle)


def pulse(bot: Robot):
    angle = bot.left_motor.angle()
    amp = 20
    translation = amp * 1.
    rotation = -amp * gear_ratio * 2
    bot.straight(translation, wait=False)
    bot.left_motor.run_target(2 * rotation_speed, angle + rotation, wait=False)
    wait(500)
    bot.straight(-translation, wait=False)
    bot.left_motor.run_target(2 * rotation_speed, angle - rotation, wait=False)
    wait(500)


def lift(bot, timeout=7000):
    # lift may be obstructed if alignment is off as there are a bunch of uneven side surface on the tower
    # if this becomes a problem, one can add a two-block stopper on the right-hand side
    target = lift_target_angle * gear_ratio
    watch = StopWatch()
    begin = watch.time()
    bot.left_motor.run_target(rotation_speed, target, wait=False)
    while bot.left_motor.angle() < target - 5:
        wait(100)
        time = watch.time()
        # print('time= {}'.format(time))
        if time - begin > timeout:
            break
        elif time - begin > timeout / 2:
            pulse(bot)


def deploy(bot: Robot):
    bot.left_motor.reset_angle(0)
    deploy_speed = 300
    bot.left_motor.run_target(deploy_speed, deploy_angle * gear_ratio)
    bot.straight(deploy_distance)


def run(bot: Robot):
    deploy(bot)
    lift(bot)
    backoff(bot)


if __name__ == "__main__":
    bot = Robot()
    # while True:
    #     pulse(bot.left_motor)

    run(bot)
