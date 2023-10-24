from robomaster import robot
import time
from pynput import keyboard
import threading


class MoveControl:
    def __init__(self, flight, speed=10):
        self.move = flight
        self.speed = speed
        self.keyboard = KeyBoard(self)

    def motor_on(self, timeout=0):
        """
        开启电机（机身非水平无法开启）

        Args:
            timeout: 等待动作完成最大的时间（启用则有阻塞）

        Returns:无

        """
        action = self.move.motor_on()
        if timeout:
            action.wait_for_completed(timeout)

    def motor_off(self, timeout=0):
        """
        关闭电机

        Args:
            timeout: 等待动作完成最大的时间（启用则有阻塞）

        Returns:无

        """
        action = self.move.motor_off()
        if timeout:
            action.wait_for_completed(timeout)

    def fly(self, direction: str = None, distance: float = 0, retry: bool = True, timeout=0):
        """
        飞行控制（前后左右上下）

        Args:
            direction:
                飞行的方向，”forward” 向前飞行， “back” 向后飞行， “up” 向上飞行， “down” 向下飞行， “left” 向左飞行， “right” 向右飞行
            distance:
                [20, 500]，飞行的距离，单位 cm
            retry:
                是否重发命令
            timeout:
                等待动作完成最大的时间（启用则有阻塞）
        Returns:无

        """
        if direction:
            action = self.move.fly(direction, distance, retry)
            if timeout:
                action.wait_for_completed(timeout)

    def flip(self, direction: str, retry=True, timeout=0):
        """

        :param direction:
            当电量低于50%时无法完成翻滚
                飞机翻转的方向， ’l‘ 向左翻滚，’r‘ 向右翻滚，’f‘ 向前翻滚， ’b‘ 向后翻滚
        :param retry:
            是否重发命令
        :param timeout:
            等待动作完成最大的时间（启用则有阻塞）
        :return:无
        """
        if direction:
            action = self.move.flip(direction, retry)
            if timeout:
                action.wait_for_completed(timeout)

    def land(self, retry=True, timeout=0):
        """

        :param retry:
            是否重发命令
        :param timeout:
            等待动作完成最大的时间（启用则有阻塞）
        :return: 无
        """
        action = self.move.land(retry)
        if timeout:
            action.wait_for_completed(timeout)

    def rotate(self, angle: float = 0, retry=True, timeout=0):
        """
        :param angle:
            [-360, 360] 旋转的角度，俯视飞机时，顺时针为正角度，逆时针为负角度
        :param retry:
            是否重发命令
        :param timeout:
            等待动作完成最大的时间（启用则有阻塞）
        :return:无
        """
        action = self.move.rotate(angle, retry)
        if timeout:
            action.wait_for_completed(timeout)

    def stop(self, retry=True):
        """

        :param retry:
            是否重发命令

        :return:
            bool:控制结果
        """
        return self.move.stop(retry)

    def _speed(self, speed: float = 0):
        """
        无参数传入:获取当前速度
        有参数传入：修改当前速度

        :param
            speed:[10, 100]
        :return:
            更改后的速度
        """
        if speed:
            self.speed = speed
        if not self.move.set_speed(self.speed):
            print('fail to set speed')
        return self.speed

    def rc(self, a=0, b=0, c=0, d=0):
        """
        控制飞机遥控器的四个杆量

        参数:
            a – float:[-100, 100] 横滚
            b – float:[-100, 100] 俯仰
            c – float:[-100, 100] 油门
            d – float:[-100, 100] 偏航
        """
        self.move.rc(a, b, c, d)

    def keyboard_listen(self):
        self.keyboard._start()
        while self.keyboard.listening:
            pass

    # def move_flow(self, move_flow_list: list, ):
    #     pass


class KeyBoard:
    def __init__(self, father):
        self.listening = 0
        self.father = father
        self.listener = keyboard.Listener(
            on_press=self.key_in,
        )

    def key_in(self, key):

        if key == keyboard.Key.esc:
            print("end")
            self.listening = 0
            self.listener.stop()
        elif key == keyboard.Key.up:
            self.father.fly("forward", 20)
        elif key == keyboard.Key.down:
            self.father.fly("back", 20)
        elif key == keyboard.Key.left:
            self.father.fly("left", 20)
        elif key == keyboard.Key.right:
            self.father.fly("right", 20)
        else:
            print("up down left right only! "
                  "press esc to quit~")

    def _start(self):
        listener_thread = threading.Thread(target=self.listener.start)
        listener_thread.daemon = True
        listener_thread.start()
        self.listening = 1


if __name__ == '__main__':
    # tl_drone = robot.Drone()
    # tl_drone.initialize()
    # tl_flight = tl_drone.flight
    tl_flight = 1
    move_ = MoveControl(tl_flight)
    move_.keyboard_listen()
    # del move_.speed
    # time.sleep(6)
    # tl_drone.close()
