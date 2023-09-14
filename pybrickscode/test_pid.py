"""
this is only for beta byricks
it has HEADING code!
*hub_imu = hub.imu.heading()*
https://beta.pybricks.com/
"""
from pybricks.parameters import Color

ik = 0.01
pk = 1
delta = .3

def test():
    from fll_robot import Robot
    robot = Robot()
    wheels = robot.motor_pair
    heading_control = wheels.heading_control
    h_old_pid = heading_control.pid()
    heading_control.pid(14000, 0, 1000)

    h_old_limits = heading_control.limits()
    # heading_control.limits(1, 1, 1)

    # h_old_scale = heading_control.scale
    # Control.scale = 3

    distance_control = wheels.distance_control

    d_old_pid = distance_control.pid()
    distance_control.pid(14000, 2, 2000)

    d_old_limits = distance_control.limits()
    # distance_control.limits(1, 1, 1)

    # d_old_scale = distance_control.scale
    # distance_control.scale = 3

    print(f'{h_old_pid}, {h_old_limits}')
    print(f'{d_old_pid}, {d_old_limits}')
    while True:
        distance = 500
        # wheels.turn(180)
        # while not robot.left_sensor.color(Color.RED):
        wheels.straight(distance)
        robot.left_motor.run_time(-1000, 1000, wait=False)
        robot.right_motor.run_time(-5000, 1000)
        wheels.turn(90)

test()
