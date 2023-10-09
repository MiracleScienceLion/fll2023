from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop
from pybricks.robotics import DriveBase, GyroDriveBase
from pybricks.tools import wait, StopWatch

from fll_robot import Robot
from lib_turn import gyro_turn
from lib_move import move
from lib_logger import Logger

############### CHANGE CONTENT BELOW ###############
def trip_01(bot):
    logger.info('trip_01')

def trip_02(bot):
    logger.info('trip_02')

def trip_03(bot):
    logger.info('trip_03')

def trip_04(bot):
    logger.info('trip_04')

def trip_05(bot):
    logger.info('trip_05')

def trip_06(bot):
    logger.info('trip_06')

def trip_07(bot):
    logger.info('trip_07')

def trip_08(bot):
    logger.info('trip_08')
############### CHANGE CONTENT ABOVE ###############

############### DO NOT CHANGE BELOW ###############
TRIP_START = 1
TRIP_END = 8

logger = Logger(Logger.DEBUG)

def left_button_event(bot, trip_num) -> int:
    logger.info('left_button_event')
    if trip_num <= TRIP_START:
        logger.warning('At leftmost already')
        return trip_num
    return trip_num - 1
    
def right_button_event(bot, trip_num) -> int:
    logger.info('right_button_event')
    if trip_num >= TRIP_END:
        logger.warning('At rightmost already')
        return trip_num
    return trip_num + 1

def bluetooth_button_event(bot, trip_num) -> int:
    logger.info('bluetooth_button_event and stop')
    return trip_num
    
def center_button_event(bot, trip_num) -> int:
    logger.info('center_button_event')
    run_trip(bot, trip_num)
    return trip_num

trip_num_to_func = {
    1: trip_01,
    2: trip_02,
    3: trip_03,
    4: trip_04,
    5: trip_05,
    6: trip_06,
    7: trip_07,
    8: trip_08,
}

def run_trip(bot, trip_num):
    if trip_num in trip_num_to_func:
        return trip_num_to_func[trip_num](bot)
    else:
        return f"No function associated with trip_num {trip_num}"

def main():
    bot = Robot()
    bot.hub.system.set_stop_button(Button.BLUETOOTH)
    trip_num = TRIP_START
    prev_buttons = None
    while True:
        bot.hub.display.number(trip_num)
        buttons = bot.hub.buttons.pressed()
        if buttons and not prev_buttons: 
            # Only process the 1st event of a button press,
            # As a single button press may trigger in multiple button events
            if Button.LEFT in buttons:
                trip_num = left_button_event(bot, trip_num)
            elif Button.RIGHT in buttons:
                trip_num = right_button_event(bot, trip_num)
            elif Button.BLUETOOTH in buttons:
                trip_num = bluetooth_button_event(bot, trip_num)
            elif Button.CENTER in buttons:
                trip_num = center_button_event(bot, trip_num)
        prev_buttons = buttons
    print('event loop ended.')

if __name__ == "__main__":
    main()
############### DO NOT CHANGE ABOVE ###############
