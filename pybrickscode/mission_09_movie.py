from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow

def run(bot: Robot):
    print("mission_09_movie")
    move(bot, distance_mm=250)
    bot.right_motor.run_angle(speed=200, rotation_angle=220)
    move(bot, distance_mm=-20, speed=200)
    gyro_turn(bot, -50, speed=50)
    move(bot, distance_mm=-50, speed=200)
    bot.right_motor.run_angle(speed=900, rotation_angle=-190)
    gyro_turn(bot, -20, speed=300) 
    move(bot, distance_mm=330, speed=200) 
    gyro_turn(bot, 90, speed=300) 
    move(bot, distance_mm=3000, speed=200)

def main():
    bot = Robot()
    run(bot)

if __name__ == "__main__":
    main()
