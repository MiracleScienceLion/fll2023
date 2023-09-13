from fll_robot import Robot
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch
from lib_move import start_tank, stop_tank

SENSOR_DIFF_FACTOR = 1.0  # Range ~ (0 to 1.5)

def line_follow(robot, speed,time_out_ms):
    timer = StopWatch()
    while timer.time() < time_out_ms:
        left_light = robot.left_sensor.reflection()
        right_light = robot.right_sensor.reflection()
        sensor_diff = right_light - left_light
        speed_factor = SENSOR_DIFF_FACTOR * sensor_diff / 100.0
        print('light: ', left_light, right_light)
        print('speed_factor: ', speed_factor)
        start_tank(robot, speed * (1 - speed_factor), speed + (1 + speed_factor))
    stop_tank(robot)


def main():
    bot = Robot(
        left_wheel_port=Port.A, 
        right_wheel_port=Port.E, 
        left_sensor_port=Port.B,
        right_sensor_port=Port.F,
        )
    line_follow(bot, speed=500, time_out_ms=3000)

if __name__ == "__main__":
    main()