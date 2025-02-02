from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port, Stop, Color
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.robotics import GyroDriveBase
from pybricks.tools import wait

MIN_SPEED = 4
MAX_SPEED = 977

MIN_ACCELERATION = 24
MAX_ACCELERATION = 9775

MIN_TURN_RATE = 6
MAX_TURN_RATE = 1282

MIN_TURN_ACCELERATION = 32
MAX_TURN_ACCELERATION = 12828


def assert_speed(speed):
    if speed is not None:
        assert MIN_SPEED <= speed <= MAX_SPEED, f"Invalid speed, must between [{MIN_SPEED}, {MAX_SPEED}]"


def assert_acceleration(acceleration):
    if acceleration is not None:
        if isinstance(acceleration, int):
            assert MIN_ACCELERATION <= acceleration <= MAX_ACCELERATION, f"Invalid acceleration, must between [{MIN_ACCELERATION}, {MAX_ACCELERATION}]"
        else:
            acc, dec = acceleration
            assert MIN_ACCELERATION <= acc <= MAX_ACCELERATION, f"Invalid acceleration, must between [{MIN_ACCELERATION}, {MAX_ACCELERATION}]"
            assert MIN_ACCELERATION <= dec <= MAX_ACCELERATION, f"Invalid deceleration, must between [{MIN_ACCELERATION}, {MAX_ACCELERATION}]"


def assert_turn_rate(turn_rate):
    if turn_rate is not None:
        assert MIN_TURN_RATE <= turn_rate <= MAX_TURN_RATE, f"Invalid turn_rate, must between [{MIN_TURN_RATE}, {MAX_TURN_RATE}]"


def assert_turn_acceleration(turn_acceleration):
    if turn_acceleration is not None:
        if isinstance(turn_acceleration, int):
            assert MIN_TURN_ACCELERATION <= turn_acceleration <= MAX_TURN_ACCELERATION, f"Invalid turn_acceleration, must between [{MIN_TURN_ACCELERATION}, {MAX_TURN_ACCELERATION}]"
        else:
            acc, dec = turn_acceleration
            assert MIN_TURN_ACCELERATION <= acc <= MAX_TURN_ACCELERATION, f"Invalid turn_acceleration, must between [{MIN_TURN_ACCELERATION}, {MAX_TURN_ACCELERATION}]"
            assert MIN_TURN_ACCELERATION <= dec <= MAX_TURN_ACCELERATION, f"Invalid turn_deceleration, must between [{MIN_TURN_ACCELERATION}, {MAX_TURN_ACCELERATION}]"


class Robot:
    def __init__(
            self,
            right_wheel_port=Port.A,
            left_wheel_port=Port.B,

            right_motor_port=Port.C,
            left_motor_port=Port.D,

            left_sensor_port=Port.F,
            right_sensor_port=Port.E,

            wheel_diameter=56.0,
            axle_track=87.3125,
            speed=None,
            acceleration=None,
            turn_rate=None,
            turn_acceleration=None,
    ):
        self.left_wheel = Motor(left_wheel_port, Direction.COUNTERCLOCKWISE)
        self.right_wheel = Motor(right_wheel_port, Direction.CLOCKWISE)
        self.axle_track = axle_track
        self.motor_pair = GyroDriveBase(
            left_motor=self.left_wheel,
            right_motor=self.right_wheel,
            wheel_diameter=wheel_diameter,
            axle_track=axle_track)
        self.motor_pair.use_gyro(True)
        self.left_sensor = ColorSensor(left_sensor_port)
        self.right_sensor = ColorSensor(right_sensor_port)
        self.left_motor = Motor(left_motor_port, Direction.COUNTERCLOCKWISE)
        self.right_motor = Motor(right_motor_port, Direction.CLOCKWISE)
        self.hub = PrimeHub()
        self.wait_for_stationary()
        self.hub.imu.reset_heading(0)
        self.motor_pair.settings(straight_speed=speed, straight_acceleration=acceleration, turn_rate=turn_rate, turn_acceleration=turn_acceleration)
        # self.hub.speaker.beep()
        print('Robot Created!')

    def wait_for_stationary(self):
        while not self.hub.imu.stationary():  # Reset IMU
            wait(100)

    def start_tank(self, left_speed, right_speed):
        speed = (right_speed + left_speed) / 2
        turn_rate = (right_speed - left_speed) / self.axle_track
        self.motor_pair.drive(speed, turn_rate)

    def stop_robot(self) -> None:
        self.motor_pair.stop()
        self.left_motor.stop()
        self.right_motor.stop()

    def stop(self) -> None:
        self.motor_pair.stop()

    def brake(self) -> None:
        self.left_wheel.brake()
        self.right_wheel.brake()

    def straight(self, distance, speed=None, acceleration=None, then: Stop = Stop.HOLD, wait: bool = True):
        """
        :param distance:
        :param speed: optional. if set, must be in the range [4, 977]
        :param acceleration: optional. if set, must be in the range [24, 9775]
        :param then: default Stop.HOLD
        :param wait: default True
        :return:
        """
        assert_speed(speed)
        assert_acceleration(acceleration)
        settings = self.motor_pair.settings()
        self.motor_pair.settings(straight_speed=speed, straight_acceleration=acceleration)
        # heading & timeout are not used
        self.motor_pair.straight(distance, then, wait)
        self.motor_pair.settings(*settings)

    def turn(self, angle, turn_rate=None, turn_acceleration=None, then: Stop = Stop.HOLD, wait: bool = True) -> None:
        """
        :param angle:
        :param turn_rate: optional. if set, must be in the range [6, 1282]
        :param turn_acceleration: optional. if set, must be in the range [32, 12828]
        :param then: default Stop.HOLD
        :param wait: default True
        :return:
        """
        assert_turn_rate(turn_rate)
        assert_turn_acceleration(turn_acceleration)
        settings = self.motor_pair.settings()
        self.motor_pair.settings(turn_rate=turn_rate, turn_acceleration=turn_acceleration)
        # timeout are not used
        self.motor_pair.turn(angle, then, wait)
        self.motor_pair.settings(*settings)

    def curve(self, radius, angle, speed=None, acceleration=None, turn_rate=None, turn_acceleration=None, then: Stop = Stop.HOLD, wait: bool = True) -> None:
        assert_speed(speed)
        assert_acceleration(acceleration)
        assert_turn_rate(turn_rate)
        assert_turn_acceleration(turn_acceleration)
        settings = self.motor_pair.settings()
        self.motor_pair.settings(straight_speed=speed, straight_acceleration=acceleration, turn_rate=turn_rate, turn_acceleration=turn_acceleration)
        # timeout are not used
        self.motor_pair.curve(radius, angle, then, wait)
        self.motor_pair.settings(*settings)

    def drive(self, speed, turn_rate) -> None:
        self.motor_pair.drive(speed, turn_rate)

    def left_color(self) -> Color:
        return self.left_sensor.color()

    def right_color(self) -> Color:
        return self.right_sensor.color()

    def left_reflection(self) -> int:
        return self.left_sensor.reflection()

    def right_reflection(self) -> int:
        return self.right_sensor.reflection()

    def heading(self) -> float:
        return self.hub.imu.heading()

    def reset_heading(self, heading: float) -> None:
        return self.hub.imu.reset_heading(heading)


def main():
    bot = Robot()
    bot.curve(100, 60, turn_rate=100)
    bot.curve(100, -60, acceleration=50)
    bot.curve(-100, -60, speed=30)
    bot.curve(-100, 60, turn_acceleration=32)


if __name__ == "__main__":
    main()
