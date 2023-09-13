"""
this is only for beta byricks
it has HEADING code!
*hub_imu = hub.imu.heading()*
https://beta.pybricks.com/
"""
ik = 0.01
pk = 1
delta = .3



def test():
    from fll_robot import Robot
    robot = Robot()
    wheels = robot.motor_pair
    heading_control = wheels.heading_control
    h_old_pid = heading_control.pid()
    # heading_control.pid(1, 1, 1)

    h_old_limits = heading_control.limits()
    # heading_control.limits(1, 1, 1)

    # h_old_scale = heading_control.scale
    # Control.scale = 3

    distance_control = wheels.distance_control

    d_old_pid = distance_control.pid()
    # distance_control.pid(2, 2, 2)

    d_old_limits = distance_control.limits()
    # distance_control.limits(1, 1, 1)

    # d_old_scale = distance_control.scale
    # distance_control.scale = 3

    print(f'{h_old_pid}, {h_old_limits}')
    print(f'{d_old_pid}, {d_old_limits}')
    wheels.turn(90)


test()
