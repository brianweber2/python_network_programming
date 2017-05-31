"""
To run this example, run this program with one argument: a path giving a UNIX
socket to listen on (must not exist).  For example:

    $ python server.py /tmp/test.sock

It will listen for client connections until stopped (eg, using Control-C).  Most
interesting behavior happens on the client side.

See client.py for the client side of this example.
"""

import sys

from twisted.python.log import startLogging
from twisted.python.filepath import FilePath
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

class MyProtocol(Protocol):
    def connectionMade(self):
        print("Connection made on Server side.")

        # Give the other side a minute to deal with this.  If they don't close
        # the connection by then, we will do it for them.
        self.timeoutCall = reactor.callLater(60, self.transport.loseConnection)

    def connectionLost(self, reason):
        print("Connection lost on Server side: {}".format(reason))

        # Clean up the timeout, if necessary.
        if self.timeoutCall.active():
            self.timeoutCall.cancel()
            self.timeoutCall = None


class MyFactory(Factory):
    def buildProtocol(self, addr):
        return MyProtocol()


def main():
    address = FilePath(sys.argv[1])

    if address.exists():
        raise SystemExit("Cannot listen on an existing path")

    startLogging(sys.stdout)

    # serverFactory = Factory()
    # serverFactory.protocol = SendFDProtocol

    reactor.listenUNIX(address.path, MyFactory())
    reactor.run()

if __name__ == '__main__':
    main()
