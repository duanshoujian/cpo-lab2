import unittest

from src.stateMachine.elevator.FSM import StateMachine
from src.stateMachine.elevator.elevator import move_tran, start_tran, open_tran


class EventTest(unittest.TestCase):


    def test_set_start(self):
        st = StateMachine()
        st.set_start("START")
        self.assertEqual(st.startState, 'START')

    def test_add(self):
        m = StateMachine()
        m.add_state('MOVE', move_tran, 0)
        m.add_state('START', start_tran, 0)
        m.add_state('OPEN', open_tran, 0)
        m.add_state('STATIC', None, 1)
        m.add_state('ERROR', None, 1)
        self.assertEqual(m.handlers, {'MOVE':move_tran,'START':start_tran,'OPEN':open_tran,'STATIC': None,'ERROR': None})

    def test_run(self):
        m = StateMachine()
        m = StateMachine()
        m.add_state('MOVE', move_tran, 0)
        m.add_state('START', start_tran, 0)
        m.add_state('OPEN', open_tran, 0)
        m.add_state('STATIC', None, 1)
        m.add_state('ERROR', None, 1)

        m.set_start('START')
        m.run(['down', 'none'])
        self.assertEqual(m.runResult,"arrived ERROR" )
        m.run(['down', 'down', 'open', 'down'])  # dont arrive at final state
        self.assertEqual(m.runResult, "not arrive end state")
        m.run(['down', 'down', 'open', 'none'])  # arrive at the final state "STATIC"
        self.assertEqual(m.runResult, "arrived STATIC")

if __name__ == '__main__':
  unittest.main()