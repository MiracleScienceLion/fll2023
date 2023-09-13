"""
this is only for beta byricks
it has HEADING code!
*hub_imu = hub.imu.heading()*
https://beta.pybricks.com/
"""
ik = 0.01
pk = 1
delta = .3


def turn(angle, imu=None, drive_base=None):
    drive_base = drive_base
    init_angle = imu.heading()
    target = angle + init_angle
    history = 0

    while True:
        measure = imu.heading()
        diff = target - measure
        if abs(diff) < delta:
            break
        history += diff
        print("{:+04.5}, {:+04.5}, {:+04.5}, {:+04.5}, {:+04.5}".format(init_angle, measure, target, history, diff))
        drive_base.turn(diff * pk + history * ik)


def test():
    from pybricks.hubs import PrimeHub
    from pybricks.pupdevices import Motor, ColorSensor
    from pybricks.parameters import Direction, Port
    from pybricks.robotics import DriveBase

    hub = PrimeHub()

    # Initialize a motor on port A.
    drivingl = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)
    drivingr = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
    wheels = DriveBase(left_motor=drivingl, right_motor=drivingr, wheel_diameter=56, axle_track=60)

    heading_control = wheels.heading_control
    h_old_pid = heading_control.pid()
    heading_control.pid(1, 1, 1)

    h_old_limits = heading_control.limits()
    # heading_control.limits(1, 1, 1)

    # h_old_scale = heading_control.scale
    # Control.scale = 3

    distance_control = wheels.distance_control

    d_old_pid = distance_control.pid()
    distance_control.pid(2, 2, 2)

    d_old_limits = distance_control.limits()
    # distance_control.limits(1, 1, 1)

    # d_old_scale = distance_control.scale
    # distance_control.scale = 3

    print(f'{h_old_pid}, {h_old_limits}')
    print(f'{d_old_pid}, {d_old_limits}')
    leftboi = ColorSensor(Port.C)
    rightboi = ColorSensor(Port.E)
    turn(90.00, hub.imu, wheels)


test()
