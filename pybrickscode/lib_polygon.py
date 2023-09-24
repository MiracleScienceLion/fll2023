from umath import *

from fll_robot import Robot

debug = False
MAX_LENGTH = 500  # we use this to validate the curve radius.


def principle(angle):
    """
    Given an angle (degree), calculate the principle angle in the range (-180, 180]
    :param angle: any angle in degree
    :return: the principle angle corresponding to the input in the range (-180, 180]
    """
    return (angle + 180) % 360 - 180


# map size 2 m x 112 cm. let the 112 cm side be x; 2 m side be y
def trip_plan(vertices, heading=0, motion_type=1, route_type='straight'):
    """
    Given a polygon vertices and initial heading, generate the trip plan (a sequence of maneuvers)
    :param vertices: the ordered vertices of the polygon, as a list of 2d coordinates, such as [(x1, y1), (x2, y2) ...], with the starting position as the first element
    :param heading: starting heading direction (deg), follow pybricks orientation convention
    :param motion_type: the direction for all the maneuvers: move forward = 1 (default), move backward = -1, pivot = 0 (turn only with no straight motion)
    when motion_typ = 0 (pivot) turn angle is aimed at aligning the front of robot to the designated direction
    :param route_type: 'straight'=using straight edges; 'curve'= using curve for smooth connections
    :return: the maneuver sequence, e.g. [(turn_angle, distance, heading), ...]
    """
    maneuvers = []
    for i in range(1, len(vertices)):
        ms = route(vertices[i - 1], vertices[i], heading, motion_type, route_type)
        maneuvers.extend(ms)
        heading = ms[-1][-1]  # update heading
    return maneuvers


def route(point1, point2, heading=0, motion_type=1, route_type='straight'):
    """
    Generate the routing parameters for a sequence of maneuvers, a turn plus a straight movement, that will ensure robot to traverse from point1 to point2.
    :param point1: starting point
    :param point2: ending point
    :param heading: starting heading direction (deg), follow pybricks orientation convention
    :param motion_type: the direction for all the maneuvers: move forward = 1 (default), move backward = -1, pivot = 0 (turn only with no straight motion)
    when motion_typ = 0 (pivot) turn angle is aimed at aligning the front of robot to the designated direction
    :param route_type: 'straight' straight-edged polygon, 'curve' smoothed arc to connect vertices
    :return: a list of maneuvers, each as a tuple of (maneuver, param, ending orientation). Example, ('turn', angle, heading), ('straight', distance, heading)
    """
    displacement = [point2[0] - point1[0], point2[1] - point1[1]]
    polar_angle = atan2(displacement[1], displacement[0]) * 180 / pi
    new_heading = polar_angle + (180 if motion_type == -1 else 0)
    distance = sqrt(pow(displacement[1], 2) + pow(displacement[0], 2))
    if route_type == 'curve':
        r, a, h = arc(distance, new_heading, heading)
        if debug:
            print('heading={} displacement={} polar_angle={} new_heading={}'.format(heading, displacement, polar_angle, new_heading))
            print('curve radius={} curve angle={} new_heading={}'.format(r, a, h))
        if abs(r) < MAX_LENGTH:
            return [('curve', (r * motion_type, a), h)]
        # else fall back to straight routing
    return edge(distance * motion_type, new_heading, heading)


def arc(distance, new_heading, current_heading):
    """
    Generate the routing parameters for a sequence of maneuvers, a turn plus a straight movement, that will ensure robot to traverse from point1 to point2.
    :param distance: length of the edge to traverse
    :param new_heading: the finishing heading (deg)
    :param current_heading: the current robot heading (deg)
    :return: the radius, turn angle, and the finishing heading (deg) of the arc
    """
    angle = principle(new_heading - current_heading)
    sv = abs(sin(angle))
    radius = distance / sv / 2 if sv else MAX_LENGTH
    return radius, 2 * angle, new_heading + angle


def edge(distance, new_heading, heading):
    """
    Generate the routing parameters for a sequence of maneuvers, turns and/or straight movements, that will ensure robot to traverse from point1 to point2.
    :param distance: length of the edge to traverse
    :param new_heading: the finishing heading (deg)
    :param heading: starting heading direction (deg), follow pybricks orientation convention
    when motion_typ = 0 (pivot) turn angle is aimed at aligning the front of robot to the designated direction
    :return: a list of maneuvers, each as a tuple of (maneuver, param, ending orientation). Example, ('turn', angle, heading), ('straight', distance, heading)
    """
    turn_angle = principle(new_heading - heading)
    if debug:
        print('original heading={} new heading={} dist={} turn={}'.format(
            heading, new_heading, distance, turn_angle))
    maneuvers = [('turn', turn_angle, new_heading)]
    if distance != 0:
        maneuvers.append(('straight', distance, new_heading))
    return maneuvers


def polygon(vertices, robot: Robot, heading=0, motion_type: int = 1, route_type='straight', reverse: bool = False):
    """
    Given a polygon (vertices), plan the trip and execute the plan to traverse the polygon edges in order.
    heading = the initial orientation of the robot used for determining the first maneuver.
    If reverse = True, revert the entire trip backward back to the origin.
    :param vertices: the ordered vertices of the polygon, as a list of 2d coordinates, such as [(x1, y1), (x2, y2) ...], with the starting position as the first element
    :param robot: the robot
    :param heading: initial heading direction (deg), follow pybricks orientation convention
    :param motion_type: the direction for all the maneuvers: move forward = 1 (default), move backward = -1, pivot = 0 (turn only with no straight motion)
    :param route_type: 'straight' straight-edged polygon, 'curve' smoothed arc to connect vertices
    :param reverse: if True, reverse course to undo all motions and retrack all the vertices back to the origin
    :return: final heading (deg), follow pybricks orientation convention
    """

    def execute(maneuvers):
        for m, param, _ in maneuvers:
            if debug:
                print(m, param)
            if m == 'turn':
                robot.turn(param)
            elif m == 'straight':
                robot.straight(param)
            elif m == 'curve':
                robot.curve(*param)
            # else: do nothing

    base_maneuvers = trip_plan(vertices, heading, motion_type, route_type)
    execute(base_maneuvers)
    if not reverse:
        return base_maneuvers[-1][-1]

    # reverse course
    reverse_maneuvers = [(m, negate(param), h) for m, param, h in base_maneuvers[::-1]]
    execute(reverse_maneuvers)
    return reverse_maneuvers[-1][-1]


def negate(param):
    if type(param) is float:
        return -param
    if type(param) is tuple:
        # if param = (radius, angle), negate radius and leave angle as is
        return -param[0], param[1]


if __name__ == "__main__":
    bot = Robot()
    debug = True


    def tests():
        heading = polygon([[0, 0], [600, 0]], bot, 0, motion_type=1)
        heading = polygon([[0, 0], [600, 0]], bot, 0, motion_type=1, reverse=True)
        heading = polygon([[0, 0], [100, 0]], bot, 180, motion_type=-1)
        heading = polygon([[0, 0], [100, 0]], bot, 180, motion_type=-1, reverse=True)
        heading = polygon([[100, -100], [0, -100], [0, 0]], bot, 0)
        heading = polygon([[100, -100], [0, -100], [0, 0]], bot, 180)
        heading = polygon([[100, -100], [0, -100], [0, 0]], bot, 0, motion_type=-1)
        heading = polygon([[0, 0], [100, 0], [100, -100], [0, -100], [0, 0]], bot, 0, reverse=True)
        heading = polygon([[0, 940], [500, 940], [800, 250], [850, 150]], bot, 0, reverse=True)


    def roundtrip():
        heading = polygon([[0, 940], [500, 940], [800, 250], [850, 150]], bot, 0)
        heading = polygon([[850, 150], [800, 250]], bot, heading, motion_type=-1)
        heading = polygon([[800, 250], [700, -200], [300, -200], [100, 940]], bot, heading)
        heading = polygon([[100, 940], [0, 940]], bot, heading, motion_type=-1)


    def undotrip():
        heading = polygon([[0, 940], [500, 940], [800, 250], [700, -200], [250, -200], [100, 940]], bot, 0, reverse=True)


    def arcs(heading):
        heading = polygon([[0, 0], [300, 300]], bot, route_type='curve', heading=heading, reverse=True)
        # heading = polygon([[300, 0], [550, 250], [800, 0], [550, -250], [300, 0]], bot, heading=90, route_type='curve', reverse=True)


    def rearcs():
        # heading = polygon([[300, 0], [550, 250]], bot, route_type='curve', heading=90)
        heading = polygon([[300, 0], [550, 250], [800, 0], [550, -250], [300, 0]], bot, heading=90, route_type='curve', reverse=True)


    def sway():
        # heading = polygon([[300, 0], [550, 250]], bot, route_type='curve', heading=90)
        heading = polygon([[300, 0], [300, 350], [300, 700], [300, 1050]], bot, heading=0, route_type='curve')
        # heading = polygon([[0, 0], [150, 150]], bot, heading=0, route_type='curve')


    # tests()
    # roundtrip()
    # undotrip()
    # arcs(360)
    rearcs()
    # sway()
