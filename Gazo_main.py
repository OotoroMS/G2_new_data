import cv2
from datetime import datetime
import serial
import threading
from cmd_list import *
from time import sleep

import IMG_DTRMN.ImgDtrmn_Lib as ImgDtrmn_Lib
from SERIAL.serial_gate import SerialGate

# シリアル通信の設定
SERIAL_PARAMS_GUI = {
    "port": "COM3",
    "baudrate": 9600,
    "parity": serial.PARITY_NONE,
    "stopbits": serial.STOPBITS_ONE,
    "timeout": 0.1
}

