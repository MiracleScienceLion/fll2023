from pybricks.parameters import Button, Color, Direction, Icon, Port, Side, Stop
from pybricks.tools import wait
from pybricks.hubs import PrimeHub

hub = PrimeHub()

from fll_robot import Robot
from lib_turn import gyro_turn, turn
from lib_move import move
from lib_line_follow import line_follow
from lib_polygon import polygon

def run(bot: Robot):
    print("mission_08_camera")
    intermissionDuration = 3500
    bot.reset_heading(-90)
    polygon(bot, vertices=[(90,700),(90,400)], forward=True, route_type='straight', reverse=True)
    polygon(bot, vertices=[(90,700),(410,920)], forward=False, route_type='curve')
    polygon(bot, vertices=[(410,920),(940, 600)], forward=False, route_type='straight')
    # turn(bot, angle=-1.5, speed=100, timeout_ms=0)
    # move(bot, distance_mm=420, heading=0, speed=200, timeout_ms=0)
    # move(bot, distance_mm=-410, heading=0, speed=200, timeout_ms=0)
    # print("Intermission for new attachment(s)")
    # print("Seconds/Milliseconds in Intermission: " + str(intermissionDuration / 1000) + " / " + str(intermissionDuration))
    # wait(intermissionDuration)
    # for i in range(15):
    #     gyro_turn(bot,angle=-5,speed=100)
    #     move(bot, distance_mm=-50, heading=0, speed=100, timeout_ms=0)
    #     i += 1
    # move(bot,distance_mm=830, heading=0, speed=200, timeout_ms=0)
    # move(bot, distance_mm=-820, heading=0, speed=200, timeout_ms=0)
    # bot.reset_heading(0)
    # polygon(bot,vertices=[(120,930),(120,585)])
    # polygon(bot,vertices=[(120,585),(120,930)])
    print("Done")
    # hub.system.shutdown()
def main(): #71.5
    bot = Robot()
    run(bot)

if __name__ == "__main__":
    main()
