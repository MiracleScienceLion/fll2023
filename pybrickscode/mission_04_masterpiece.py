from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow

def run(bot: Robot):
    wheels = bot.motor_pair
    wheels.straight(510)
    wheels.curve(0,-69.49)
    wheels.straight(850)
    wheels.straight(-830)
    wheels.curve(0,69.49)
    wheels.straight(-510)
def main():
    bot = Robot()
    run(bot)

if __name__ == "__main__":
    main()
