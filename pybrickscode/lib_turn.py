from fll_robot import Robot
from pybricks.parameters import Port
from pybricks.tools import wait

from lib_move import start_tank, stop_tank


def gyro_turn(robot: Robot, angle, speed, timeout_ms=1000):
    # TODO: this gyro turn is NOT acccurate. someone needs to fix it.
    robot.hub.imu.reset_heading(0)
    print('gyro_turn: angle', angle, 'speed', speed)
    if angle > 0:  # turn right
        while robot.hub.imu.heading() < angle:
            start_tank(robot, speed, -speed)
    else:
        while robot.hub.imu.heading() > angle:
            start_tank(robot, -speed, speed)
    stop_tank(robot)
    print('angle after stop_tank:', robot.hub.imu.heading())
    wait(200)
    print('angle after wait:', robot.hub.imu.heading())


def turn(robot: Robot, angle, speed, timeout=1000):
    robot.motor_pair.distance_control.limits(speed=speed)
    robot.motor_pair.turn(angle=angle)


def main():
    bot = Robot(
        left_wheel_port=Port.A,
        right_wheel_port=Port.E,
        left_sensor_port=Port.B,
        right_sensor_port=Port.F,
    )
    turn(bot, 90, 300)
    wait(time=500)
    print(bot.hub.imu.heading())
    turn(bot, -90, 300)
    wait(time=500)
    print(bot.hub.imu.heading())

    gyro_turn(bot, angle=90, speed=300)
    wait(time=500)
    gyro_turn(bot, angle=-90, speed=300)
    wait(time=500)

    # turn(robot, -90, 300)


if __name__ == "__main__":
    main()
