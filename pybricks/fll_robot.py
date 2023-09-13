from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase, GyroDriveBase
from pybricks.tools import wait, StopWatch

def add_number(a, b):
    return a + b

class Robot:
    def __init__(
        self,
        left_wheel_port=Port.B, 
        right_wheel_port=Port.A, 
        left_sensor_port=Port.F,
        right_sensor_port=Port.E,
        left_motor_port=Port.D,
        right_motor_port=Port.C,
        wheel_diameter=56.0,
        axle_track=87.3125
    ):
        self.left_wheel = Motor(left_wheel_port,Direction.COUNTERCLOCKWISE)
        self.right_wheel = Motor(right_wheel_port,Direction.CLOCKWISE)
        self.motor_pair = GyroDriveBase(
            left_motor=self.left_wheel,
            right_motor=self.right_wheel,
            wheel_diameter=wheel_diameter,
            axle_track=axle_track)
        self.motor_pair.use_gyro(True)
        self.left_sensor = ColorSensor(left_sensor_port)
        self.right_sensor = ColorSensor(right_sensor_port)
        self.left_motor = Motor(left_motor_port,Direction.CLOCKWISE)
        self.right_motor = Motor(right_motor_port,Direction.CLOCKWISE)
        self.hub = PrimeHub()
        while not self.hub.imu.stationary():  # Reset IMU
            wait(100)
        self.hub.imu.reset_heading(0)
        # self.hub.speaker.beep()
        print('Robot Created!')

def main():
    bot = Robot(
        left_wheel_port=Port.A, 
        right_wheel_port=Port.E, 
        left_sensor_port=Port.B,
        right_sensor_port=Port.F,
        )


if __name__ == "__main__":
    main()