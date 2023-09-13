from fll_robot import Robot
from pybricks.parameters import Port
from pybricks.tools import wait

def start_tank(robot, left_speed, right_speed):
    # print('speed: ', left_speed, right_speed)
    robot.left_wheel.run(left_speed)
    robot.right_wheel.run(right_speed)

def stop_tank(robot):
    robot.left_wheel.brake()
    robot.right_wheel.brake()

def move(robot: Robot, distance_mm, heading, speed, timeout_ms=1000):
    # heading & timeout are not used
    robot.motor_pair.distance_control.limits(speed=speed)
    robot.motor_pair.straight(distance=distance_mm)
    

def main():
    bot = Robot(
        left_wheel_port=Port.A, 
        right_wheel_port=Port.E, 
        left_sensor_port=Port.B,
        right_sensor_port=Port.F,
        )
    move(bot, distance_mm=-900, heading=0, speed=300)

if __name__ == "__main__":
    main()