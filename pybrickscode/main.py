from pybricks.parameters import Button

from fll_robot import Robot
from lib_logger import Logger


############### CHANGE CONTENT BELOW ###############
def trip_01(bot: Robot):
    from trip_01 import run
    run(bot)


def trip_02(bot: Robot):
    from trip_02 import run
    run(bot)


def trip_03(bot: Robot):
    from trip_03 import run
    run(bot)


def trip_04(bot: Robot):
    from trip_04 import run
    run(bot)


def trip_05(bot: Robot):
    from trip_05 import run
    run(bot)


def trip_06(bot: Robot):
    from trip_06 import run
    run(bot)


def trip_07(bot: Robot):
    from trip_07 import run
    run(bot)


def trip_08(bot: Robot):
    from trip_08 import run
    run(bot)


############### CHANGE CONTENT ABOVE ###############

############### DO NOT CHANGE BELOW ###############
TRIP_START = 1
TRIP_END = 8

logger = Logger(Logger.DEBUG)


def left_button_event(bot: Robot, trip_num: int) -> int:
    logger.info('left_button_event')
    if trip_num <= TRIP_START:
        logger.warning('At leftmost already')
        return trip_num
    return trip_num - 1


def right_button_event(bot: Robot, trip_num: int) -> int:
    logger.info('right_button_event')
    if trip_num >= TRIP_END:
        logger.warning('At rightmost already')
        return trip_num
    return trip_num + 1


def bluetooth_button_event(bot: Robot, trip_num: int) -> int:
    logger.info('bluetooth_button_event and stop')
    return trip_num


def center_button_event(bot: Robot, trip_num: int) -> int:
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


def run_trip(bot: Robot, trip_num: int):
    if trip_num in trip_num_to_func:
        logger.info(f'Running {trip_num:02d}')
        trip_num_to_func[trip_num](bot)
        bot.stop_robot()
    else:
        logger.error(f"No function associated with trip_num {trip_num}")


def load_trip_num(bot: Robot) -> int:
    """Try to load trip num from hub memory, if non-existant use TRIP_START."""
    data = bot.hub.system.storage(0, read=2)
    try:
        trip_num = int(data)
        if TRIP_START <= trip_num <= TRIP_END:
            return trip_num
        else:
            return TRIP_START
    except ValueError:
        return TRIP_START


def save_trip_num(bot: Robot, trip_num: int):
    trip_num_str = f'{trip_num:02d}'
    bot.hub.system.storage(0, write=trip_num_str)


def main():
    bot = Robot()
    bot.hub.system.set_stop_button(Button.BLUETOOTH)
    trip_num = load_trip_num(bot)
    prev_buttons = None
    while True:
        bot.hub.display.char(str(trip_num))
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
            save_trip_num(bot, trip_num)
        prev_buttons = buttons
    print('event loop ended.')


if __name__ == "__main__":
    main()
############### DO NOT CHANGE ABOVE ###############
