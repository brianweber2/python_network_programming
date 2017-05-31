"""
Client-side of an example for UNIX sockets.  This client connects to a server
listening on a UNIX socket.

To run this example, run this program with one argument: a path giving the UNIX
socket the server side of this example is already listening on.  For example:

    $ python client.py /tmp/test.sock

See server.py for the server side of this example.
"""
import os, sys

from twisted.python.log import startLogging
from twisted.python.filepath import FilePath
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.internet import reactor

class ClientProtocol(Protocol):

    def __init__(self):
        self.whenDisconnected = Deferred()

    def connectionMade(self):
        print("Connection made on Client side.")

    def connectionLost(self, reason):
        print("Connection lost on Client side: {}".format(reason))
        self.whenDisconnected.callback(None)


class ClientFactory(Factory):
    def buildProtocol(self, addr):
        return ClientProtocol()


def main():
    address = FilePath(sys.argv[1])

    startLogging(sys.stdout)

    factory = ClientFactory()
    # factory.protocol = ReceiveFDProtocol
    factory.quiet = True

    endpoint = UNIXClientEndpoint(reactor, address.path)
    connected = endpoint.connect(factory)

    def succeeded(client):
        return client.whenDisconnected
    def failed(reason):
        print "Could not connect:", reason.getErrorMessage()
    def disconnected(ignored):
        reactor.stop()

    connected.addCallbacks(succeeded, failed)
    connected.addCallback(disconnected)

    reactor.run()

if __name__ == '__main__':
    main()
