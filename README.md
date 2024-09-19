# cfm_auto_aim
cf手游cfm的ai辅助瞄准程序，仅供娱乐，无法实战

**演示视频**

https://github.com/user-attachments/assets/debc4002-0adc-4847-ad24-b6a79e9ab3ae

**使用方式**

下载所需依赖包，和yolov8，其它版本的yolo不知道能不能用

在此处将路径改为模型文件的相对或绝对路径，ddx和ddy是瞄准位置偏移

![image](https://github.com/user-attachments/assets/9d16068e-17bf-4366-91c2-48846de3c1e3)

此处修改触发辅瞄的热键，0x01是鼠标左键，0x02是鼠标右键，其它热键请搜索“windows虚拟键码”

![image](https://github.com/user-attachments/assets/ba0f0265-4c23-4a74-a413-c837dcb99a25)

这是自动连点的函数，修改sleep参数控制频率

![image](https://github.com/user-attachments/assets/cde6d30a-ce2f-4d89-a93e-3aa3da14cb33)

当程序启动后想要结束程序时，先按下ctrl+L，再关闭程序创建的窗口

![image](https://github.com/user-attachments/assets/ad54a96e-7460-4604-8a95-546c8d827a7b)

根据目标距离控制瞄准速度，如果全程一个速度，要么太慢，要么瞄准过头。如果当前程序依然瞄准过头，尝试将游戏自带的辅助瞄准改为阻尼吸附，并降低游戏灵敏度

![image](https://github.com/user-attachments/assets/e43a5f9b-755b-4d0e-a72f-25f085870bf2)

程序可以在sk助手或者腾讯手游助手上使用，sk助手需要电脑连接手机投屏。这两个程序对应不同的分辨率

![image](https://github.com/user-attachments/assets/26fecf89-b201-4d56-95e6-c7c77d7fcb68)

如果不需要连点，可以注释这两行

![image](https://github.com/user-attachments/assets/ef1ce4f7-ca0d-4e29-b679-cbc581c495ca)
