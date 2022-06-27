"""
Date: 2022.05.11 13:39
Description: Automaton
LastEditors: Rustle Karl
LastEditTime: 2022.05.11 13:39
"""
import random

from scapy.automaton import ATMT, Automaton

"""
When more logic is needed, Scapy provides a clever way abstraction to define 
an automaton. In a nutshell, you need to define an object that inherits from 
`Automaton`, and implement specific methods:

- states: using the `@ATMT.state` decorator. They usually do nothing
- conditions: using the `@ATMT.condition` and `@ATMT.receive_condition` 
decorators. They describe how to go from one state to another
- actions: using the `ATMT.action` decorator. They describe what to do, 
like sending a back, when changing state
"""


class TCPScanner(Automaton):
    """The following example does nothing more than trying to mimic a TCP scanner"""

    @ATMT.state(initial=1)
    def BEGIN(self):
        pass

    @ATMT.state()
    def SYN(self):
        print("-> SYN")

    @ATMT.state()
    def SYN_ACK(self):
        print("<- SYN/ACK")
        raise self.END()

    @ATMT.state()
    def RST(self):
        print("<- RST")
        raise self.END()

    @ATMT.state()
    def ERROR(self):
        print("!! ERROR")
        raise self.END()

    @ATMT.state(final=1)
    def END(self):
        pass

    @ATMT.condition(BEGIN)
    def condition_BEGIN(self):
        raise self.SYN()

    @ATMT.condition(SYN)
    def condition_SYN(self):

        if random.randint(0, 1):
            raise self.SYN_ACK()
        else:
            raise self.RST()

    @ATMT.timeout(SYN, 1)
    def timeout_SYN(self):
        raise self.ERROR()


TCPScanner().run()
