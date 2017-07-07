import sys
import wormhole
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from wormhole.cli.public_relay import RENDEZVOUS_RELAY


@inlineCallbacks
def send():
    print("sending")
    w = wormhole.create("apabepa", RENDEZVOUS_RELAY, reactor)
    #w.allocate_code()
    w.set_code("wot ")
    #code = yield w.get_code()
    #print("code:", code)
    w.send_message(b"outbound data")
    inbound = yield w.get_message()
    print(inbound)
    yield w.close()


@inlineCallbacks
def receive():
    w = wormhole.create("apabepa", RENDEZVOUS_RELAY, reactor)
    #code = input("Input code")
    #print("Inputted: " + code)
    w.set_code("wot ")
    w.send_message(b"inbound data")
    inbound = yield w.get_message()
    print("asd")
    print(inbound)
    yield w.close()


if __name__ == '__main__':
    print(sys.argv)
    if sys.argv[1] == "send":
        s = send()
    else:
        receive()

    reactor.run()