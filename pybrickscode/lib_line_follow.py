from fll_robot import Robot
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch
from lib_move import start_tank, stop_tank

debug = False

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


def line_follow(robot: Robot, distance=None, time=None, condition=None, sensor="R", edge="BW"):
    """
    the func tion follows the black line
    :param robot: robot base instance
    :param distance: the distance limits the distance
    :param time: the time limits the time
    :param condition:  is a custom condition callback function
    :param sensor: can only be "L" or "R" (default) it specifies the sensors to be used
    :param edge: edge allows you to chose from
           a) "bw" black on the right white on the left
           b) "wb" white on the right black on the left
    :return:
    """
    wheels = robot.motor_pair
    eye = robot.left_sensor if sensor == "L" else robot.right_sensor
    eye.detectable_colors([Color.BLACK, Color.WHITE])

    def should_contin(robot):
        if distance is not None:
            if debug:
                print("limited by distance")
            return robot.motor_pair.distance() < distance
        if time is not None:
            if debug:
                print("limited by time")
            return clock.time() < time
        if condition is not None:
            if debug:
                print("custom condition")
            return condition(robot)

    while should_contin(robot):
        signal = eye.reflection()
        lspeed, rspeed = gain(signal)
        if edge == "BW":
            start_tank(robot, lspeed, rspeed)
        elif edge == "WB":
            start_tank(robot, rspeed, lspeed)
    wheels.stop()


def should_continue(bot: Robot):
    ri = bot.left_sensor
    if debug:
        print(ri.color())
    return ri.color() != Color.BLACK


def main():
    bot = Robot()
    eyel = bot.left_sensor
    eyer = bot.right_sensor
    eyer.detectable_colors([Color.BLACK, Color.WHITE])
    eyel.detectable_colors([Color.BLACK, Color.WHITE])
    line_follow(bot, distance=300, sensor="R", edge="WB")


if __name__ == "__main__":
    debug = True
    main()
