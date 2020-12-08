#MADE BY SPYROS CHATZIARGYROS 

import argparse
import socket 
from colorama import init, Fore

from threading import Thread, Lock
from queue import Queue

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX
RED = Fore.RED
WHITE = Fore.WHITE

N_THREADS = 200
q = Queue()
print_lock = Lock()

def port_scan(port):
    try:
        s = socket.socket()
        s.connect((host, port))
    except:
        with print_lock:
            print(f"{GRAY}{host}-{[port]} is {RED}closed  {RESET}", end='\r')
    else:
        with print_lock:
            print(f"{WHITE}{host}================>{[port]} is {GREEN}open    {RESET}")
    finally:
        s.close()


def scan_thread():
    global q
    while True:
        worker = q.get()
        port_scan(worker)
        q.task_done()


def main(host, ports):
    global q
    for thread in range(N_THREADS):
        thread = Thread(target=scan_thread)
        thread.daemon = True
        thread.start()

    for worker in ports:
        q.put(worker)
    
    q.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("host", help="Host to scan.")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
    parser.add_argument("-T", "--threads", dest="NumOfThreads", default=200, help="Number of Threads")
    
    args = parser.parse_args()
    host, port_range, N_THREADS = args.host, args.port_range, args.NumOfThreads

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)

    ports = [ p for p in range(start_port, end_port)]
    print(f"{WHITE}Starting[{GREEN}Proccess Running -> {RED}{N_THREADS}{GREEN}]")

    main(host, ports)
