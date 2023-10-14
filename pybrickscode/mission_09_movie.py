from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import turn
from lib_move import move
from lib_line_follow import line_follow

def run(bot: Robot):
    print("mission_09_movie")
    bot.straight(distance=250, speed=200)
    bot.right_motor.run_angle(speed=200, rotation_angle=220)
    bot.straight(distance=-30, speed=200)
    bot.turn(angle=-50, turn_rate=100)
    bot.straight(distance=-50, speed=200)
    bot.right_motor.run_angle(speed=900, rotation_angle=-190)
    bot.turn(angle=-20, speed=300) 
    bot.straight(distance=330, speed=200) 
    bot.turn(angle=90, speed=300) 
    bot.straight(distance=3000, speed=200)

def main():
    bot = Robot()
    run(bot)

if __name__ == "__main__":
    main()
