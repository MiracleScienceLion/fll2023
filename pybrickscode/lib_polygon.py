from umath import *

from fll_robot import Robot

debug = False


def principle(angle):
    """
    Given an angle (degree), calculate the principle angle in the range (-180, 180]
    :param angle: any angle in degree
    :return: the principle angle corresponding to the input in the range (-180, 180]
    """
    return (angle + 180) % 360 - 180


# map size 2 m x 112 cm. let the 112 cm side be x; 2 m side be y
def trip_plan(vertices, heading=0, motion_type=1):
    """
    Given a polygon vertices and initial heading, generate the trip plan (a sequence of maneuvers)
    :param vertices: the ordered vertices of the polygon, as a list of 2d coordinates, such as [(x1, y1), (x2, y2) ...], with the starting position as the first element
    :param heading: starting heading direction (deg), follow pybricks orientation convention
    :param motion_type: the direction for all the maneuvers: move forward = 1 (default), move backward = -1, freeze = 0 (turn only with no straight motion)
    when motion_typ = 0 (freeze) turn angle is aimed at aligning the front of robot to the designated direction
    :return: the maneuver sequence, e.g. [(turn_angle, distance, heading), ...]
    """
    maneuvers = []
    for i in range(1, len(vertices)):
        turn_angle, distance, heading = route(vertices[i - 1], vertices[i], heading, motion_type)
        maneuvers.append((turn_angle, distance, heading))
    return maneuvers


def route(point1, point2, heading=0, motion_type=1):
    """
    Generate the routing parameters for a sequence of maneuvers, a turn plus a straight movement, that will ensure robot to traverse from point1 to point2.
    :param point1: starting point
    :param point2: ending point
    :param heading: starting heading direction (deg), follow pybricks orientation convention
    :param motion_type: the direction for all the maneuvers: move forward = 1 (default), move backward = -1, freeze = 0 (turn only with no straight motion)
    when motion_typ = 0 (freeze) turn angle is aimed at aligning the front of robot to the designated direction
    :return: a tuple of (turn angle, straight distance, ending orientation)
    """
    displacement = [point2[0] - point1[0], point2[1] - point1[1]]
    polar_angle = atan2(displacement[1], displacement[0]) * 180 / pi
    radius = sqrt(pow(displacement[1], 2) + pow(displacement[0], 2))
    new_heading = polar_angle + (180 if motion_type == -1 else 0)
    turn_angle = principle(new_heading - heading)
    distance = radius * motion_type
    if debug:
        print('original heading={} new heading={} dist={} turn={}'.format(
            heading, new_heading, radius, turn_angle))
    return turn_angle, distance, new_heading


def polygon(heading, vertices, robot: Robot, motion_type: int = 1, reverse: bool = False):
    """
    Given a polygon (vertices), plan the trip and execute the plan to traverse the polygon edges in order.
    heading = the initial orientation of the robot used for determining the first maneuver.
    If reverse = True, revert the entire trip backward back to the origin.
    :param heading: initial heading direction (deg), follow pybricks orientation convention
    :param vertices: the ordered vertices of the polygon, as a list of 2d coordinates, such as [(x1, y1), (x2, y2) ...], with the starting position as the first element
    :param robot: the robot
    :param motion_type: the direction for all the maneuvers: move forward = 1 (default), move backward = -1, freeze = 0 (turn only with no straight motion)
    :param reverse: if True, reverse course to undo all motions and retrack all the vertices back to the origin
    :return: final heading (deg), follow pybricks orientation convention
    """

    def execute(maneuvers, turn_first=True):
        for turn_angle, distance, _ in maneuvers:
            if debug:
                print(turn_angle, distance)
            if turn_first:
                robot.turn(turn_angle)
                robot.straight(distance)
            else:
                robot.straight(distance)
                robot.turn(turn_angle)

    base_maneuvers = trip_plan(vertices, heading, motion_type)
    execute(base_maneuvers)
    if not reverse:
        return base_maneuvers[-1][-1]

    # reverse course
    reverse_maneuvers = [(-a, -d, h) for a, d, h in base_maneuvers[::-1]]
    execute(reverse_maneuvers, turn_first=False)
    return reverse_maneuvers[-1][-1]


if __name__ == "__main__":
    bot = Robot()
    debug = True


    def tests():
        heading = polygon(0, [[0, 0], [600, 0]], bot, motion_type=1)
        heading = polygon(0, [[0, 0], [600, 0]], bot, motion_type=1, reverse=True)
        heading = polygon(180, [[0, 0], [100, 0]], bot, motion_type=-1)
        heading = polygon(180, [[0, 0], [100, 0]], bot, motion_type=-1, reverse=True)
        heading = polygon(0, [[100, -100], [0, -100], [0, 0]], bot)
        heading = polygon(180, [[100, -100], [0, -100], [0, 0]], bot)
        heading = polygon(0, [[100, -100], [0, -100], [0, 0]], bot, motion_type=-1)
        heading = polygon(0, [[0, 0], [100, 0], [100, -100], [0, -100], [0, 0]], bot, reverse=True)
        heading = polygon(0, [[0, 940], [500, 940], [800, 250], [850, 150]], bot, reverse=True)


    def roudtrip():
        heading = polygon(0, [[0, 940], [500, 940], [800, 250], [850, 150]], bot)
        heading = polygon(heading, [[850, 150], [800, 250]], bot, motion_type=-1)
        heading = polygon(heading, [[800, 250], [700, -200]], bot)
        heading = polygon(heading, [[700, -200], [200, -200], [500, 940]], bot)
        heading = polygon(heading, [[500, 940], [0, 940]], bot, motion_type=-1)


    # tests()
    roudtrip()
