from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon


def run(bot: Robot):
    bot.reset_heading(0)
    polygon(bot, vertices=[(0,-900),(790,-670),(850,-580)])
    polygon(bot, vertices=[(850,-580),(730,-730)], forward=False)
    polygon(bot, vertices=[(730,-730),(630,-580)],forward=False)
    for i in range(2):
        polygon(bot, vertices=[(630,-580), (730,-730)], reverse=True)
    # polygon(bot, vertices=[(640,-760),(700,-630)])
    # polygon(bot, vertices=[(700,-630),(720,-700)],reverse=True)
    # polygon(bot, vertices=[(720,-700),(910,60),(840,60)])
    # polygon(bot, vertices=[(840,60),(910,60)], forward=False)
    # polygon(bot, vertices=[(910,60),(880,120),(940,180),(890,520),(290,950)])
def main():
    bot = Robot()
    run(bot)


if __name__ == "__main__":
    main()
