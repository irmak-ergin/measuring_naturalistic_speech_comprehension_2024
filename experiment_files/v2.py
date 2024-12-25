import serial
import time
import serial.tools.list_ports
import multiprocessing as mp
import csv
import sys

def workerBody(participant, session, stop, trial, ready, queue):
    output_data = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if desc == "Feather M0 Express":
            port2 = port

    ser = serial.Serial(port2, 500000, timeout=0.01)
    ready.set()
    while not stop.is_set():
        ser.readline()
        if trial.is_set():
            ready.clear()
            trial_start_time = time.monotonic()
            trial_offset = 0
            while trial.is_set():
                line = ser.readline()
                if trial_offset == 0:
                    trial_offset = time.monotonic()
                    
                try:
                    output_data.append(
                        (int(line.decode("utf-8").split(' ')[0]), int(line.decode("utf-8").split(' ')[1])))
                except:
                    print("Warning: missing frame")

            try:
                real_time_elapsed = 1000 * (time.monotonic() - trial_start_time)
                drift = real_time_elapsed - (output_data[-1][1] - output_data[0][1])
                print((drift / (output_data[-1][1] - output_data[0][1])) * 100)
                
                offset = output_data[0][1]
                for i, pt in enumerate(output_data):
                    output_data[i] = (pt[0], pt[1] - offset + ((trial_offset - trial_start_time) * 1000))
                
                with open(f"{_thisDir}/data/slider_{participant}_{session}_{queue.get()}.csv",'w') as out:
                    csv_out=csv.writer(out)
                    csv_out.writerow([drift, real_time_elapsed])
                    csv_out.writerow(['value','time'])
                    for row in output_data:
                        csv_out.writerow(row)

            except Exception as error:
                print("Error occured while processing last trial. Data discarded")
                print(error)

            output_data.clear()
            ready.set()
    ser.close()


class Slider:
    def __init__(self, participant, session):
        mp.set_start_method('spawn')
        self.stop = mp.Event()
        self.trial = mp.Event()
        self.ready = mp.Event()
        self.queue = mp.Queue()
        self.proc = mp.Process(target=workerBody, args=(
            participant, session, self.stop, self.trial, self.ready, self.queue))
        self.proc.start()

        while not self.ready.is_set():
            if not self.proc.is_alive():
                raise Exception("Error: Slider process exited")
            time.sleep(0.01)

    def start_trial(self, wav_file):
        if not self.proc.is_alive():
            raise Exception("Error: Slider process exited")
        else:
            while not self.ready.is_set():
                if not self.proc.is_alive():
                    raise Exception("Error: Slider process exited")
                time.sleep(0.01)
            self.trial.set()
            self.queue.put(wav_file)

    def stop_trial(self):
        self.trial.clear()
        if not self.proc.is_alive():
            raise Exception("Error: Slider process exited")
        else:
            while not self.ready.is_set():
                if not self.proc.is_alive():
                    raise Exception("Error: Slider process exited")
                time.sleep(0.01)

    def __del__(self):
        self.stop.set()
        self.proc.join()
