from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop
from pybricks.robotics import DriveBase, GyroDriveBase
from pybricks.tools import wait, StopWatch

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_line_follow import line_follow

def left_button_event(bot):
    print('left')
    bot.right_motor.run_angle(100, 180, wait=False)
    bot.left_motor.run_angle(100, -360, wait=False)
    line_follow(bot, speed=200, time_out_ms=3000)    

def right_button_event(bot):
    print('right')
    gyro_turn(bot, angle=45, speed=200)

def bluetooth_button_event(bot):
    print('bluetooth')
    bot.hub.display.icon(icon=Icon.HAPPY)
    bot.right_motor.reset_angle(0)
    print('angle before',bot.right_motor.angle())
    bot.right_motor.run_angle(100, 180, wait=True)
    print('angle after',bot.right_motor.angle())
    wait(3000)
    print('angle after wait',bot.right_motor.angle())
    bot.right_motor.run_target(100, 50)
    print('angle after run_target',bot.right_motor.angle())
    bot.left_motor.run_angle(100, -360, wait=False)
    bot.motor_pair.straight(distance=500)  # Built-in gyro straight!!!
    bot.hub.speaker.beep()

def center_button_event(bot):
    print('center and stop')

def main():
    bot = Robot()
    while True:
        # Set light to green if pressed, else red.
        buttons = bot.hub.buttons.pressed()
        if Button.LEFT in buttons:
            left_button_event(bot)
        elif Button.RIGHT in buttons:
            right_button_event(bot)
        elif Button.BLUETOOTH in buttons:
            bluetooth_button_event(bot)
        elif Button.CENTER in buttons:
            center_button_event(bot)
    print('event loop ended.')

if __name__ == "__main__":
    main()
