import sys

from twisted.internet import reactor
from twisted.python.log import startLogging
from twisted.python.filepath import FilePath
from twisted.internet.protocol import Protocol, Factory


class MyProtocol(Protocol):
  def connectionMade(self):
    print("Connection made.")

  def connectionLost(self, reason):
    print("Connection lost: {}".format(reason))


class MyFactory(Factory):
  def buildProtocol(self, addr):
    return MyProtocol()


def main():
  startLogging(sys.stdout)
  
  reactor.listenUNIX('./.sock', MyFactory)
  reactor.run()

if __name__ == '__main__':
  main()
