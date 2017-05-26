from twisted.internet.defer import Deferred

def myErrback(failure):
    print failure

d = Deferred()
d.addErrback(myErrback)
d.errback("Triggering errback.")
