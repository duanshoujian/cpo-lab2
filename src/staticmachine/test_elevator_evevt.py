import unittest

from src.staticmachine.elevator_event import *


class DiscreteEventTest(unittest.TestCase):

    def test_elevator(self):
        m = DiscreteEvent("elevator")
        m.input_port("A", latency=1)
        m.input_port("B", latency=1)
        m.input_port("C", latency=1)

        m.output_port("D", latency=1)

        # Here is just a simple test, the specific operation process can refer to 'elevator.py'


         # Determine how the elevator is going to run based on the current floor, enter the floor, and whether the elevator door is switched
        # a: floor to go
        # b: current floor
        # c: Elevator door switch
        # d: The elevator goes up and down or stops
        def direction(a,b,c):
            if(a<b):
                if(c==1):
                    d=0
                else:
                    d=-1
            else:
                if (c == 1):
                    d = 0
                else:
                    d = -1
            return d


        test_data = [({'A': 1, 'B': 2, 'C': 1}, {'D': direction(1, 2, 1)}),
                     ({'A': 0, 'B': 0, 'C': 0}, {'D': direction(0, 0, 0)}),
                     ({'A': '1', 'B': 2, 'C': 3}, {'D': None}),
                     ]

        for a, d in test_data:
            source_events = [source_event(k, v, 0) for k, v in a.items()]
            actual, inter = m.execute(*source_events)
            expect = {}
            expect.update(actual)
            self.assertEqual(actual, expect)


class NodeTest(unittest.TestCase):
    def test_logic_not(self):
        n = Node("not", lambda a: not a if isinstance(a, bool) else None)
        n.input("A", 1)
        n.output("B", 1)
        test_data = [(False, True),
                     (False, True),
                     (None, None)]
        for a, b in test_data:
            self.assertEqual(n.activate({"A": a}), [source_event("B", b, 1)])

        def test_logic_and(self):
            n = Node("and", lambda a, b: a and b if isinstance(a, bool) and isinstance(b, bool) else None)
            n.input("A", 1)
            n.input("B", 1)
            n.output("C", 1)
            test_data = [(None, False, None),
                         (False, False, False),
                         (True, False, False),
                         (False, True, False),
                         (True, True, True)]
            for a, b, c in test_data:
                self.assertEqual(n.activate({"A": a, "B": b}), [source_event("C", c, 1)])

        def test_1_to_2_decoder(self):
            def decoder(a):
                if a == 0: return (0, 1)
                if a == 1: return (1, 0)
                return (None, None)

            n = Node("decoder", decoder)
            n.input("A", 1)
            n.output("D1", 1)
            n.output("D0", 2)
            test_data = [(0, 0, 1),
                         (1, 1, 0),
                         (None, None, None)]
            for a, d1, d0 in test_data:
                self.assertEqual(n.activate({"A": a}), [source_event("D1", d1, 1), source_event("D0", d0, 2)])


if __name__ == '__main__':
    unittest.main()