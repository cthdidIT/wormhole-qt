import subprocess
import sys


def dummy(update):
    print(update)
    pass


class WormholeService(object):
    def __init__(self, sender_callback=dummy, receiver_callback=dummy):
        self._sender_callback = sender_callback
        self._receiver_callback = receiver_callback

    def send(self, path):
        cmd = ["wormhole", "send", path]
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        for line in iter(p.stdout.readline, b''):
            self._sender_callback(str(line.rstrip()))

    def receive(self, code):
        cmd = ["wormhole", "receive", code]

        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             stdin=subprocess.PIPE,
                             bufsize=1,
                             universal_newlines=True)

        for line in iter(p.stdout.readline, b''):
            l = str(line.rstrip())
            if l != '':
                lower = l.lower()
                if lower.startswith("receiving file"):
                    p.stdin.write('y\n')
                    p.stdin.flush()
                else:
                    split = l.split('|')
                    self._receiver_callback(split)


if __name__ == '__main__':
    args = sys.argv
    nbr = len(args)
    ws = WormholeService()
    print(args)
    if nbr == 3:
        if args[1] == 'send':
            print("Send")
            ws.send(args[2])
        elif args[1] == 'receive':
            print("Receive")
            ws.receive(args[2])
    else:
       print("send filepath")
       print("receive code")
