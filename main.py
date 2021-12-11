import socket, json
from PIL import ImageGrab
import io, struct, time, subprocess
import os
import sys
def restart():
    os.execv(sys.executable, ['python3'] + sys.argv)
    sys.exit()

CONFIG = json.load(open("config.json", "r"))

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)
def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

terminated = False

if __name__ == "__main__":
    DATA = {"id":"first"}
    process = None
    currentLog = ""
    if CONFIG["run_command_on_launch"] and not terminated:
        process = subprocess.Popen(CONFIG["run_command"], stdout=subprocess.PIPE, shell=True)
    
    running = True
    while running:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((CONFIG["host"], CONFIG["port"]))
                print("connected")
                while running:
                    s.sendall(json.dumps(DATA).encode("utf-8"))
                    data = json.loads(s.recv(1028).decode('utf-8'))
                    if data["order"] == "get screen":
                        frame = ImageGrab.grab()
                        buf = io.BytesIO()
                        frame.save(buf, format='JPEG')
                        byt = buf.getvalue()
                        # ooooo = "{0:30d}".format(len(byt))
                        # s.sendall(ooooo.encode("utf-8"))
                        # s.recv(1)
                        send_msg(s, byt)
                    elif data["order"] == "get limited shell" or   data["order"] == "get shell" :
                        print("shell", currentLog)
                    elif data["order"] == "get data":
                        send_msg(s, json.dumps({
                            "isRunning": False if process is None else process.poll() is None
                            }).encode("utf-8"))
                    elif data["order"] == "send data":
                        s.sendall(b" ")
                        data = json.loads(recv_msg(s).decode("utf-8"))
                        cmd = ""
                        if (data.get("cmd"))!=None:
                            cmd = data.get("cmd")
                            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    elif data["order"] == "restart":
                        print("restart")
                        s.close()
                        restart()
                        running=False
                        break
                    elif data["order"] == "terminate":
                        process.terminate()

        except ConnectionResetError  as e:
            print(e)
            time.sleep(3)
        except ConnectionRefusedError as e:
            print(e)
            time.sleep(3)
