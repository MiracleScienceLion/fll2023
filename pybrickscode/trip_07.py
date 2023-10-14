from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon
import mission_09_movie


def run(bot: Robot):
    # TODO implement this function
    mission_09_movie.run(bot)


if __name__ == "__main__":
    bot = Robot()
    run(bot)
