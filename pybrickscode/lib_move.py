from fll_robot import Robot
from pybricks.parameters import Port
from pybricks.tools import wait


def start_tank(robot, left_speed, right_speed):
    speed = (right_speed + left_speed) / 2
    turn_rate = (right_speed - left_speed) / robot.axle_track
    robot.motor_pair.drive(speed, turn_rate)


def stop_tank(robot):
    robot.left_wheel.brake()
    robot.right_wheel.brake()


def move(robot: Robot, distance, speed, timeout=1000):
    # heading & timeout are not used
    robot.motor_pair.distance_control.limits(speed=speed)
    robot.motor_pair.straight(distance=distance)


def main():
    bot = Robot()
    move(bot, distance_mm=-900, heading=0, speed=300)


if __name__ == "__main__":
    main()
