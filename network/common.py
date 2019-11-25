import json

TYPE_FIELD = 1
TYPE_MOVE = 2
TYPE_GAME_OVER = 3


def make_message(type, payload):
    data = json.dumps({
        'type': type,
        'payload': payload
    }).encode()

    return len(data), data


def send_message(sock, msg_len, msg):
    sock.send(msg_len.to_bytes(1, 'big'))
    sock.send(msg)


def recv_message(sock):
    msg_len = int.from_bytes(sock.recv(1), 'big')
    msg = json.loads(
        sock.recv(msg_len).decode()
    )

    return msg['type'], msg['payload']
