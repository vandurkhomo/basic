from robomaster import robot
from pynput import keyboard


class MoveControl:
    """
    动作控制类
    （没有封装含挑战卡的函数）
        主要是对robot.Drone().flight的封装
            封装了前后左右上下飞行、停止
            封装了电机的开关
            封装了起飞和降落
            封装了角度旋转
            封装了控制飞机遥控器的四个杆量（ 横滚 俯仰 油门 偏航）
            实现了速度控制，飞行的距离控制
            实现了键盘流控制飞机的功能
            速度获取，角速度获取不在此类中（可能在传感器类中）

    参数：
        self.step  ：每次飞行的步长
        self.move ： robot.Drone().flight的别名
            （控制同一飞机时传入相同的robot.Drone().flight对象）
        self.speed ：飞行的速度
        self.keyboard ：KeyBoard键盘捕获类
    """

    def __init__(self, flight, speed=10):
        self.step = 100
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
                [20, 500]，飞行的距离，单位 cm,无则默认为self.step
            retry:
                是否重发命令
            timeout:
                等待动作完成最大的时间（启用则有阻塞）
        Returns:无

        """
        if not distance:
            distance = self.step
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

    def speed_(self, speed: float = 0):
        """
        无参数传入:获取当前速度
        有参数传入：修改当前速度

        :param
            speed:[10, 100]
        :return:
            更改后的速度
        """
        if 100 < speed or speed < 10:
            speed = 0
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

    def takeoff(self, retry=True, timeout=0):
        """
        起飞（约40cm）
        :param retry:
            是否重发命令
        :param timeout:
            等待动作完成最大的时间（启用则有阻塞）

        :return: 无
        """
        action = self.move.takeoff(retry)
        if timeout:
            action.wait_for_completed(timeout)

    def keyboard_listen(self):
        """
        键盘捕获
            有阻塞，实现键盘流控制
                self.keyboard是类KeyBoard的实例（具体实现见类KeyBoard）
        结束后重置监听线程 keyboard.Listener
        :return: 无
        """
        print("up,down,left,right,1,2,3,4 only! "
              "press esc to quit~")
        self.keyboard.listening = 1
        self.keyboard.listener.start()
        while self.keyboard.listening:
            pass
        self.keyboard.listener = keyboard.Listener(
            on_press=self.keyboard.key_in,
        )

    def set_step(self, new_step):
        """
        设置新飞行步长
        :param new_step: 设置的新飞行步长
        :return: 无
        """
        if 500 >= new_step >= 20:
            self.step = new_step


class KeyBoard:
    """
    键盘捕获
        用keyboard.Listener实现（自带多线程）
        在MoveControl.keyboard_listen（）被调用（keyboard_listen有阻塞）
    由于self.father直接传入了MoveControl的实例对象，因此可以直接调用传入对象的方法

    """

    def __init__(self, father):
        self.listening = 0
        self.father = father
        self.listener = keyboard.Listener(
            on_press=self.key_in,
        )

    def key_in(self, key):
        """
        keyboard.Listener 的 on_press回调函数，按键摁下触发

        修改该函数可以自定义键盘流控制飞机行为

        目前行为：
            key 1:
                飞行步长增加（20）
            key 2:
                飞行步长减少（20）
            key 3:
                飞行速度增加（10）
            key 4:
                飞行步长减少（10）
            key up:
                向前飞
            key down:
                向后飞
            key left:
                向左飞
            key right:
                向右飞
        :param key: 键盘捕获
        :return: 无
        """
        try:
            if key.char == '1':
                self.father.set_step(self.father.step + 20)
            if key.char == '2':
                self.father.set_step(self.father.step - 20)
            if key.char == '3':
                self.father.speed_(self.father.speed + 10)
            if key.char == '4':
                self.father.speed_(self.father.speed - 10)
        except AttributeError:
            if key == keyboard.Key.esc:
                print("end")
                self.listening = 0
                self.listener.args = 0
                self.listener.stop()
                del self.listener
            elif key == keyboard.Key.up:
                self.father.fly("forward", self.father.step)
            elif key == keyboard.Key.down:
                self.father.fly("back", self.father.step)
            elif key == keyboard.Key.left:
                self.father.fly("left", self.father.step)
            elif key == keyboard.Key.right:
                self.father.fly("right", self.father.step)


if __name__ == '__main__':
    tl_drone = robot.Drone()
    tl_drone.initialize()
    tl_flight = tl_drone.flight

    move_ = MoveControl(tl_flight)
    move_.takeoff()
    move_.keyboard_listen()

# ERROR action.py:355 Robot is already performing 500 action(s) <action, name:FlightAction, state:action_started
