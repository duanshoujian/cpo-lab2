import unittest


from src.disevent import  *


def start_tran(input):
    if input is 'up' or input is 'down':
        new_state = 'MOVE'
    elif input is 'open':
        new_state = 'OPEN'
    elif input is 'overweight':
        new_state = 'ERROR'  # The initial state "START" cannot be directly converted to the final state "Static" by "none" action
    else:
        new_state = "ERROR"
    return new_state

def move_tran(input):
    if input is 'up' or input is 'down':
        new_state = 'MOVE'
    elif input is 'open':
        new_state = 'OPEN'
    elif input is 'overweight':  # The elevator can only enter the final state "STAIC" through the "none" action when the door is open
        new_state = 'ERROR'
    else:
        new_state = "ERROR"
    return new_state

def open_tran(input):
    if input is 'up' or input is 'down':
        new_state = 'MOVE'
    elif input is 'open':
        new_state = 'OPEN'
    elif input is 'overweight':
        new_state = 'STATIC'
    else:
        new_state = 'ERROR'
    return new_state


class EventTest(unittest.TestCase):

    def test_set_start(self):
        st = StateMachine()
        st.set_start("START")
        self.assertEqual(st.startState, 'START')

    def test_add(self):

        m = StateMachine()
        m = StateMachine()
        m.add_state('MOVE', move_tran, ['MOVE', 'OPEN', 'ERROR'], 0)
        m.add_state('START', start_tran, ['MOVE', 'OPEN', 'ERROR'], 0)
        m.add_state('OPEN', open_tran, ['MOVE', 'OPEN', 'STATIC'], 0)
        m.add_state('STATIC', None, None, 1)
        m.add_state('ERROR', None, None, 1)
        self.assertEqual(m.handlers, {'MOVE':move_tran,'START':start_tran,'OPEN':open_tran,'STATIC': None,'ERROR': None})


    def test_run(self):
        m = StateMachine()
        m.add_state('MOVE', move_tran, ['MOVE', 'OPEN', 'ERROR'], 0)
        m.add_state('START', start_tran, ['MOVE', 'OPEN', 'ERROR'], 0)
        m.add_state('OPEN', open_tran, ['MOVE', 'OPEN', 'STATIC'], 0)
        m.add_state('STATIC', None, None, 1)
        m.add_state('ERROR', None, None, 1)

        m.add_trans_status('MOVE', 'up or down/0', )
        m.add_trans_status('OPEN', 'open/0')
        m.add_trans_status('ERROR', 'overweight/0')
        m.add_trans_status('STATIC', 'overweight/1')

        m.set_start('START')
        m.run(['down', 'overweight'])
        self.assertEqual(m.runResult,"arrived ERROR" )
        m.run(['down', 'down', 'open', 'down'])
        self.assertEqual(m.runResult, "not arrive end state")
        m.run(['down', 'down', 'open', 'overweight'])
        self.assertEqual(m.runResult, "arrived STATIC")


    def test_param(self):
        m=StateMachine()
        self.assertEqual(m.add_state('STATIC', None, None,'1'),'false property')
        self.assertEqual(m.set_start(0), 'false property')
        self.assertEqual(m.run('down'), 'false property')
        # Enter the correct or incorrect parameter property, result is different
        m.add_state('STATIC', None, None, 1)
        self.assertEqual(RESULT,['true property'])
        m.add_state('STATIC', None, None, '1')
        self.assertEqual(RESULT, ['false property'])

        m.add_state('START', start_tran, ['MOVE', 'OPEN', 'ERROR'], 0)
        # Enter the correct or incorrect parameter property, result is different
        m.set_start('START')
        self.assertEqual(RESULT, ['true property'])
        m.set_start(0)
        self.assertEqual(RESULT, ['false property'])

        m.add_state('START', start_tran, ['MOVE', 'OPEN', 'ERROR'], 0)
        m.add_state('MOVE', move_tran, ['MOVE', 'OPEN', 'ERROR'], 0)
        m.set_start('START')
        m.run(['down'])
        self.assertEqual(RESULT, ['true property'])
        m.run('down')
        self.assertEqual(RESULT, ['false property'])





if __name__ == '__main__':
  unittest.main()