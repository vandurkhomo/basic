# basic
这是一个对大疆TT无人机sdk的简单开发
--------
预计实现  
1. *运动控制类MoveControl*
    - 主要是对robot.Drone().flight的封装
       - 封装了前后左右上下飞行、停止
       - 封装了电机的开关
       - 封装了起飞和降落
       - 封装了角度旋转
       - 封装了控制飞机遥控器的四个杆量（ 横滚 俯仰 油门 偏航）
       - 实现了速度控制，飞行的距离控制
       - 实现了键盘流控制飞机的功能
       - 速度获取，角速度获取不在此类中（可能在传感器类中）
       - ~~以后就不维护辣~~（bushi）
2. *传感器类*
    - 暂无
3. *视频流类*
   - 暂无
4. *ui界面*
   - 暂无
5.*视觉处理及算法类*
   - 暂无