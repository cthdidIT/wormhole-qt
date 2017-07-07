import subprocess
import sys


def dummy(update):
    print(update)
    pass


class WormholeService(object):
    def __init__(self, sender_callback=dummy, receiver_callback=dummy):
        self._sender_callback = sender_callback
        self._receiver_callback = receiver_callback

    def _handle_status(self, split, cb):
        progress = int(split[0][:-1])
        cb(dict(progress=progress, data=split[1:]))

    def send(self, path):
        cmd = ["wormhole", "send", path]
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             bufsize=1,
                             universal_newlines=True)

        for line in iter(p.stdout.readline, b''):
            l = str(line.rstrip())
            if l != '':
                if l.lower().startswith('confirmation received'):
                    break
                else:
                    split = l.split('|')
                    if split[0].endswith('%'):
                        self._handle_status(split, self._sender_callback)
                    else:
                        self._sender_callback(dict(data=split))

        return_code = p.poll()
        self._receiver_callback(dict(data=return_code))

    def receive(self, code, path="."):
        cmd = ["cd %s && wormhole" % path, "receive", code]

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
                elif lower.startswith("received file written"):
                    break
                else:
                    split = l.split('|')
                    if split[0].endswith('%'):
                        self._handle_status(split, self._receiver_callback)
                    else:
                        self._receiver_callback(dict(data=split))

        return_code = p.poll()
        self._receiver_callback(dict(data=return_code))


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
