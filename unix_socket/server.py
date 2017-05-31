# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Server-side of an example for sending file descriptors between processes over
UNIX sockets.  This server accepts connections on a UNIX socket and sends one
file descriptor to them, along with the name of the file it is associated with.

To run this example, run this program with two arguments: a path giving a UNIX
socket to listen on (must not exist) and a path to a file to send to clients
which connect (must exist).  For example:

    $ python sendfd.py /tmp/sendfd.sock /etc/motd

It will listen for client connections until stopped (eg, using Control-C).  Most
interesting behavior happens on the client side.

See recvfd.py for the client side of this example.
"""

import sys

from twisted.python.log import startLogging
from twisted.python.filepath import FilePath
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

class SendFDProtocol(Protocol):
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


def main():
    address = FilePath(sys.argv[1])

    if address.exists():
        raise SystemExit("Cannot listen on an existing path")

    startLogging(sys.stdout)

    serverFactory = Factory()
    serverFactory.protocol = SendFDProtocol

    port = reactor.listenUNIX(address.path, serverFactory)
    reactor.run()

if __name__ == '__main__':
    main()
