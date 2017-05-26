"""
The argument passed to callback is propagated as an argument to the first 
function in the callback chain.
"""
from twisted.internet.defer import Deferred

def myCallback(result):
    print(result)

d = Deferred()
d.addCallback(myCallback)
d.callback("Triggering callback.")
