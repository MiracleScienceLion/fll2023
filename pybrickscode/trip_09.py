#This is the code that picks up the expert next to the sound mixer (Noah, I think), and drops him off to the music note section.

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
    print("trip_09")
    bot.reset_heading(0)
    polygon(bot, [(0, 0), (700, 600),(700,1320),(870,1320)], reverse=False,speed=800)
    

def main():
    bot = Robot()
    run(bot)

if __name__ == "__main__":
    main()

