import zmq
import json

def zmq_pub(port):
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.bind(f"tcp://*:{port}")
    return sock

def zmq_sub(ip, port):
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect(f"tcp://{ip}:{port}")
    sock.setsockopt(zmq.SUBSCRIBE, b'')
    return sock

def send_json(sock, data):
    sock.send_json(data)

def recv_json(sock):
    return sock.recv_json()
