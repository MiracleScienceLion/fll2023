from fll_robot import Robot
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch
from lib_move import start_tank, stop_tank

SENSOR_DIFF_FACTOR = 1.0  # Range ~ (0 to 1.5)

clock = StopWatch()
margin = 1000
slow_tingy = 70
default_speed = 130
target = 70
p = 65


def gain(signal):
    error = signal - target
    diff = error * p
    if diff < -margin or diff > margin:
        speed = slow_tingy
    else:
        speed = default_speed
    return speed + diff, speed - diff


def line_follow(robot: Robot, distance=None, time=None, condition=None):
    wheels = robot.motor_pair
    eyel = robot.left_sensor
    eyer = robot.right_sensor
    eyer.detectable_colors([Color.BLACK, Color.WHITE])
    eyel.detectable_colors([Color.BLACK, Color.WHITE])

    def should_contin(robot):
        if distance is not None:
            return robot.motor_pair.distance() < distance
        if time is not None:
            return clock.time() < time
        if condition is not None:
            return condition(robot)

    while should_contin(robot):
        signal = eyel.reflection()
        lspeed, rspeed = gain(signal)
        start_tank(robot, lspeed, rspeed)
    wheels.stop()
    print("done!")


def should_continue(bot: Robot):
    ri = bot.left_sensor
    print(ri.color())
    return ri.color() != Color.BLACK


def main():
    bot = Robot()
    eyel = bot.left_sensor
    eyer = bot.right_sensor
    eyer.detectable_colors([Color.BLACK, Color.WHITE])
    eyel.detectable_colors([Color.BLACK, Color.WHITE])
    line_follow(bot, condition=should_continue)


if __name__ == "__main__":
    main()
