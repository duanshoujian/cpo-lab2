from src.stateMachine.elevator.FSM import StateMachine


def start_tran(input):
    if input is 'rise' or input is 'down':
        new_state = 'MOVE'
    elif input is 'open':
        new_state = 'OPEN'
    elif input is 'none':
        new_state = 'ERROR' #The initial state "START" cannot be directly converted to the final state "Static" by "none" action
    else:
        new_state = "ERROR"
    return new_state


def move_tran(input):
    if input is 'rise' or input is 'down':
        new_state = 'MOVE'
    elif input is 'open':
        new_state = 'OPEN'
    elif input is 'none':  #The elevator can only enter the final state "STAIC" through the "none" action when the door is open
        new_state = 'ERROR'
    else:
        new_state = "ERROR"
    return new_state


def open_tran(input):
    if input is 'rise' or input is 'down':
        new_state = 'MOVE'
    elif input is 'open':
        new_state = 'OPEN'
    elif input is 'none':
        new_state = 'STATIC'
        print("final state")
    else:
        new_state = 'ERROR'
    return new_state



if __name__== "__main__":
    m = StateMachine()
    m.add_state('MOVE', move_tran,0)
    m.add_state('START', start_tran,0)
    m.add_state('OPEN', open_tran,0)
    m.add_state('STATIC', None, 1)
    m.add_state('ERROR', None, 1)

    m.set_start('START')

    m.run(['down','none'])#use "down" action to transfer state from "start" to "move",then use none action to transfer state from "action" to "static"
    # ,because the rule says we cant tranfer state from "action" to "static",so transfer to "error" state
    m.run(['down','down','open','down'])#dont arrive at final state
    m.run(['down', 'down', 'open', 'none'])#arrive at the final state "STATIC"

#rules
# 4 kinds of action：rise,down,open,none。use none to enter "static" state ,we can only enter "static" state when current state is "open"
# 5 kinds of state：START，MOVE，OPEN，STATIC（the final state），ERROR（the final state）
# for more details,you can reference state transfer function "move_tran","start_tran","open_tran"
