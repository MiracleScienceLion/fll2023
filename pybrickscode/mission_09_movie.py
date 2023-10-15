from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import turn
from lib_move import move
from lib_line_follow import line_follow

def run(bot: Robot):
    print("mission_09_movie")
    bot.straight(distance=250, speed=500)
    bot.right_motor.run_angle(speed=500, rotation_angle=320)
    bot.straight(distance=-30, speed=500)
    bot.turn(angle=-55, turn_rate=60, turn_acceleration=300)
    bot.straight(distance=-30, speed=300)
    bot.right_motor.run_angle(speed=900, rotation_angle=-300)
    bot.turn(angle=-35, turn_rate=100)
    bot.straight(distance=340, speed=500)
    bot.turn(angle=100, turn_rate=100)
    bot.straight(distance=1300, speed=900)


def main():
    bot = Robot()
    run(bot)

if __name__ == "__main__":
    main()
