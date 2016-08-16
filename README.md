
# raspimouse_lefthand  

##使い方
  1. Ubuntu Linux 14.04をインストール  
    * 参考：https://wiki.ubuntu.com/ARM/RaspberryPi  
  2. ROSインストール  
    * 参考：https://github.com/ryuichiueda/ros_setup_scripts_Ubuntu14.04_server  
  3. Raspberry Pi Mouseのドライバセットアップ
    * 参考：https://github.com/rt-net/RaspberryPiMouse
  4. Raspberry Pi Mouse制御用基盤ROSパッケージ
    * 参考：https://github.com/ryuichiueda/raspimouse_ros
  
  5. raspimouse_lefthandのclone  
~~~~
     $ roscd raspimouse_ros/  
     $ git clone https://github.com/kudouakira/raspimouse_lefthand.git  
     $ cd ../..  
     $ catkin_make
~~~~  
  
  6. lefthand.py 使用  
~~~~
     $ rosrun raspimouse_ros lefthand.py
~~~~

##動作確認済環境  
  * Ubuntu Linux 14.04 server on Raspberry Pi2



