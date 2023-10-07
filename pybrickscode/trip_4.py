from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon

def run(bot: Robot):
    bot.reset_heading(-90)
    a_number = 340
    polygon(bot, vertices=[(a_number, 1110), (a_number, 101)])
    bot.left_motor.run_angle(800,-1300, wait=False)
    bot.right_motor.run_angle(800,-1290)
    bot.left_motor.run_angle(800,1300, wait=False)
    bot.right_motor.run_angle(800,1290)
    polygon(bot, vertices=[(a_number, 105), (a_number, -1008)])


def main():
    bot = Robot()
    run(bot)

if __name__ == "__main__":
    main()
