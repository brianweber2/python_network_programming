from twisted.internet import reactor, defer

class HeadlineRetreiver(object):
    def processHeadline(self, headline):
        if len(headline) > 50:
            self.d.errback("The headline '{}' is too long!".format(headline))
        else:
            self.d.callback(headline)

    def _toHTML(self, result):
        return "<h1>{}</h1>".format(result)

    def getHeadline(self, input):
        self.d = defer.Deferred()
        reactor.callLater(1, self.processHeadline, input)
        self.d.addCallback(self._toHTML)
        return self.d

def printData(result):
    print(result)
    reactor.stop()

def printError(failure):
    print(failure)
    reactor.stop()


h = HeadlineRetreiver()
d = h.getHeadline("Breaking News: Twisted Takes Us to the Moon!")
d.addCallbacks(printData, printError)

reactor.run()
