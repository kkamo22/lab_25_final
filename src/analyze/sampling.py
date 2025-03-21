import csv
from datetime import datetime
import os
import sys
import time

import bitalino


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

MAC_ADDRESS = "98:D3:91:FE:44:E9"

SAMPLING_RATE = 1000  # Hz
N_SAMPLES = 100

MEASUREMENT_TIME = 10.0  # s


def get_device(mac_address):
    device = None
    try:
        device = bitalino.BITalino(mac_address)
    except Exception as e:
        print("ERROR: The MAC address or serial port for the device is "
              "invalid.", file=sys.stderr)
    return device


if __name__ == "__main__":
    # デバイスの取得
    device = get_device(MAC_ADDRESS)
    if type(device) !=  bitalino.BITalino:
        print("ERROR: Could not get the device.", file=sys.stderr)
        exit(1)
    print("Succeeded in getting the device!")
    time.sleep(1.0)

    # 計測準備
    pin = int(input("Input the number of a pin > "))
    device.start(SAMPLING_RATE, [pin])

    # データ計測
    label = input("Input the label > ")
    mode = input("Input the name of the mode > ")

    print("Ready to start measurement...")
    time.sleep(3.0)
    print("Go!")

    start_time = time.time()
    result = [[label]]
    while True:
        data = device.read(N_SAMPLES)
        data_a1 = data[:, 5]

        result.extend([[float(i)] for i in data_a1])

        if time.time() - start_time > MEASUREMENT_TIME:
            break

    # CSV ファイルに保存
    dt_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(DATA_DIR, f"{dt_str}_v1_{mode}.csv")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(result)
