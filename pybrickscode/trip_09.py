from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop
from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon

hub = InventorHub()

def run(bot: Robot):
    print("trip_09_ming-yi")
    bot.reset_heading(0)
    polygon(bot, [(0, 0), (700, 600),(700,1250),(850,1250)], reverse=False)
    

def main():
    bot = Robot()
    run(bot)

if __name__ == "__main__":
    main()

