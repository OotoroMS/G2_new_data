import cv2
from datetime import datetime
from plc_pc import SerialManager
from do_serial import DoSerial
import serial
import threading
from cmd_list import *
from time import sleep

# シリアル通信の設定
SERIAL_PARAMS_GUI = {
    "port": "COM3",
    "baudrate": 9600,
    "parity": serial.PARITY_NONE,
    "stopbits": serial.STOPBITS_ONE,
    "timeout": 0.1
}

# シリアルマネージャーのインスタンスを作成
serial_manager = SerialManager(SERIAL_PARAMS_GUI)

# DoSerialのインスタンスを作成
do_serial = DoSerial(serial_manager)

# スレッドの起動.
threading.Thread(target=do_serial.receive_loop, daemon=True).start()

# 赤外線照明の点灯.
do_serial.send(do_serial.set_send_data(DOUSA_KAKUNIN))
sleep(1)  # 少し待つ
do_serial.send(do_serial.set_send_data(LIGHT_ON))

# デバック用.
# data = do_serial.send_to_ui()
# print(f"Received data: {data}")

# カメラを起動（通常は 0 が内蔵カメラ）
cap = cv2.VideoCapture(0)

# 解像度を設定（2592x1944）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)

if not cap.isOpened():
    print("カメラを開けませんでした。")
    exit()

print("カメラを起動しました。's'キーで画像を保存（.bmp）、'q'キーで終了します。")

while True:
    ret, frame = cap.read()
    if not ret:
        print("映像の取得に失敗しました。")
        break
    # グレースケール変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # グレースケール画像の表示
    cv2.imshow('Gray Camera', gray)


    # キー入力待ち
    key = cv2.waitKey(1) & 0xFF

    # 's'キーで画像を保存
    if key == ord('s'):
        filename = datetime.now().strftime("capture_%Y%m%d_%H%M%S.bmp")
        cv2.imwrite(filename, frame)
        print(f"画像を保存しました: {filename}")

    # 'q'キーで終了
    elif key == ord('q'):
        print("終了します。")
        # 赤外線照明の消灯.
        do_serial.send(do_serial.set_send_data(LIGHT_OFF))
        sleep(1)  # 少し待つ
        do_serial.send(do_serial.set_send_data(END))

        # デバック用.
        # data = do_serial.send_to_ui()
        # print(f"Received data: {data}")

        break

# リソースの解放
cap.release()
do_serial.colse()
cv2.destroyAllWindows()
