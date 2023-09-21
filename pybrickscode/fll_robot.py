from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.robotics import GyroDriveBase
from pybricks.tools import wait


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
            axle_track=87.3125
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
        self.left_motor = Motor(left_motor_port, Direction.CLOCKWISE)
        self.right_motor = Motor(right_motor_port, Direction.CLOCKWISE)
        self.hub = PrimeHub()
        while not self.hub.imu.stationary():  # Reset IMU
            wait(100)
        self.hub.imu.reset_heading(0)
        # self.hub.speaker.beep()
        print('Robot Created!')

    def start_tank(self, left_speed, right_speed):
        speed = (right_speed + left_speed) / 2
        turn_rate = (right_speed - left_speed) / self.axle_track
        self.motor_pair.drive(speed, turn_rate)

    def stop(self) -> None:
        self.motor_pair.stop()

    def brake(self) -> None:
        self.left_wheel.brake()
        self.right_wheel.brake()

    def straight(self, distance, then: Stop = Stop.HOLD, wait: bool = True):
        # heading & timeout are not used
        self.motor_pair.straight(distance, then, wait)

    def turn(self, angle, then: Stop = Stop.HOLD, wait: bool = True) -> None:
        self.motor_pair.turn(angle, then, wait)

    def curve(self, radius, angle, then: Stop = Stop.HOLD, wait: bool = True) -> None:
        self.motor_pair.curve(radius, angle, then, wait)

    def drive(self, speed, turn_rate) -> None:
        self.motor_pair.drive(speed, turn_rate)


def main():
    bot = Robot()
    while True:
        print(bot.left_sensor.color())


if __name__ == "__main__":
    main()
