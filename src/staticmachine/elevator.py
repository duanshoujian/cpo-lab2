import time
import threading
import random

TOP = 5
BOTTOM = 1
STATE = {0: "The elevator stops and the door opens", 1: "The elevator stops and the door closes", 2: "elevator up", 3: "elevator down"}
DIR = {0: "go down", 1: "go up"}
# Message encoding：0 00door close ，01 door open, 02 people come
#           1 11 go 1L ，12 go 2L，13 go 3L，14go 4L，15 go 5L，16 GO 6L
#           2 21 on the first floor go up，22 on the second floor go up，23 on the third floor go up
#           3 32 on the second floor go down，33 on the third floor go down，34 on the fourty floor go down，35 on the fifty floor go down

msgLock = threading.Lock()  # Message lock
exitLock = threading.Lock()  # Switch door lock

responseInterval = 0.3  # Response interval 0.3 seconds
exitTime = 1.5  # Door opening and closing time


class Msg:
    msgDecode = [["close the door", "open the door", "Someone enters"], "Go to {} floor", "{} floor have someone want go up", "{} floor have someone want go down"]  # Message decoding table

    def __init__(self, type_, value):
        self.type = type_
        self.value = value
        if type_ == 0:
            self.info = self.msgDecode[0][value]
        else:
            self.info = self.msgDecode[type_].format(value)


class Exit:
    exitDecode = {0: "Closing", 1: "opening", 3: "no status", }

    def __init__(self, value):
        self.value = value
        self.info = self.exitDecode[value]


exitFlag = Exit(3)
msgQueue = []


def printMsg(name, queue):
    """
    Print message queue
    """
    if type(queue) is list:
        info = [m.info for m in queue]
    else:
        info = queue.info
    print(" "*50 + name+": "+str(info))


def update_msgQueue(action, target):

    global msgQueue, msgLock
    if msgLock.acquire():
        if action == "=":
            if msgQueue[:] == target[:]:
                msgLock.release()
                return
            msgQueue = target
        else:
            eval("msgQueue."+action)(target)
        printMsg("msgQueue",msgQueue)
        msgLock.release()


def update_exitFlag(target):

    global exitFlag, exitLock
    if exitLock.acquire():
        exitFlag = Exit(target)
        printMsg("exitFlag", exitFlag)
        exitLock.release()


def msgFunction():
    """
    Randomly generated messages
    :return:
    """
    global msgQueue
    for i in range(4):
        type = random.randint(0, 3)
        value = 0
        if type == 0:
            value = random.randint(0, 2)
        if type == 2:
            value = random.randint(BOTTOM, TOP-1)
        if type == 3:
            value = random.randint(BOTTOM+1, TOP)
        if type == 1:
            value = random.randint(BOTTOM, TOP)

        TIME = random.randint(1, 8)
        m = Msg(type, value)
        print("Message:", m.info)
        exist = False
        for each in msgQueue:
            if m.type == each.type and m.value == each.value:
                exist = True
                break
        if not exist:
            update_msgQueue("append",m)
        time.sleep(TIME)


class StateThreed(threading.Thread):

    def run(self):
        global msgQueue, exitFlag
        # Initialize elevator status, floor and direction
        state, new_state = 0, 0
        cur, new_cur = 1, 1
        d, new_d = 0, 0
        timeout = 3  # Timeout 3 seconds
        print("Current status:% s, current floor:% d, running direction：%s" % (STATE[state], cur, DIR[d]))
        while True:
            time.sleep(responseInterval)  # Action response interval is responseInterval seconds
            if (state, cur, d) != (new_state, new_cur, new_d):
                state, cur, d = new_state, new_cur, new_d
                print("Current status:% s, current floor:% d, running direction:% s" % (STATE[state], cur, DIR[d]))
            else:
                print("............")

            if state == 0:  # The door is open, including when the door is being opened
                if exitFlag.value == 3:  # Timeout is not calculated during door opening and closing
                    timeout -= responseInterval
                tmp_list = msgQueue[:]
                for m in msgQueue:
                    if m.type == 0:
                        tmp_list.remove(m)
                        if m.value == 0:  # Close news
                            new_state = 1  # Set the status as the door stops and closes first, then close the door
                            self.closeDoor()
                            timeout = 3
                            break
                        else:  # When the door is open, someone presses to open the door or someone enters
                            timeout = 3
                    if m.value == cur:  # Someone is pressing the button in the same direction as the elevator running with the door open
                        if (d == 1 and m.type == 2) or (d == 2 and m.type == 3):
                            tmp_list.remove(m)
                            timeout = 3
                update_msgQueue("=", tmp_list)
                if timeout <= 0:
                    print("time out")
                    new_state = 1
                    self.closeDoor()

            elif state == 1: # The door is closed, including when the door is closing
                tmp_list = msgQueue[:]
                for m in msgQueue:
                    if m.type == 0:
                        tmp_list.remove(m)
                        if m.value:
                            new_state = 0
                            self.openDoor()
                            timeout = 3
                            break
                    if m.value == cur: # Someone is pressing the button in the same direction as the elevator running when the door is closed
                        if (d == 1 and m.type == 2) or (d == 2 and m.type == 3):
                            tmp_list.remove(m)
                            new_state = 0
                            self.openDoor()
                            timeout = 3
                            break
                        if m.type == 1:
                            tmp_list.remove(m)

                update_msgQueue("=", tmp_list)

                if new_state == 1 and exitFlag.value == 3:  # The door is closed and the state is not activated
                    timeout = 3
                    new_state, new_cur, new_d = self.closed(state, cur, d)

            else:  # Lift up or down
                if state == 2:
                    new_cur, new_d = self.up(cur, d)
                else:
                    new_cur, new_d = self.down(cur, d)

                tmp_list = msgQueue[:]
                for m in msgQueue:
                    if m.type == 0:
                        tmp_list.remove(m)
                update_msgQueue("=", tmp_list)

                new_state = 1
                m = Msg(0, 1)
                update_msgQueue("append", m)

    def closed(self, state, cur, d):
        """
        When the door is closed, respond
         : param state: elevator state
         : param cur: current floor
         : param d: running direction
         : return: the updated three input values
        """

        if d == 1:  # up
            if self.startup(cur, d):
                state = 2
            else:
                d = 0
                if self.startup(cur, d):
                    state = 3
                else:
                    d = 1
        else:
            if self.startup(cur, d):
                state = 3
            else:
                d = 1
                if self.startup(cur, d):
                    state = 2
                else:
                    d = 0
        return state, cur, d

    def up(self, cur, d):
        while not self.stop(cur, d):
            cur += 1
            print("Going to level% d..." % cur)
            time.sleep(2)
        print("Reached the level {}".format(cur))
        return cur, d

    def down(self, cur, d):
        while not self.stop(cur, d):
            cur -= 1
            print("Going to level% d..." % cur)
            time.sleep(2)
        print("Reached the level {}".format(cur))
        return cur, d

    def startup(self, cur, d):
        """
        Whether to start
         : param cur: current floor
         : param d: running direction
         : return: whether the bool value is activated
        """
        global msgQueue
        is_start = False
        has_same_d = False
        tmp_list = msgQueue[:]
        for m in msgQueue:
            if m.type != 0:
                if d == 1 and m.value > cur:  # Upward, non-zero type message, the floor is larger than the current floor
                    has_same_d = True
                    is_start = True
                if d == 0 and m.value < cur:
                    has_same_d = True
                    is_start = True
        if not has_same_d:
            for m in msgQueue:
                if m.type and m.value == cur:
                    tmp_list.remove(m)
        update_msgQueue("=", tmp_list)
        return is_start

    def stop(self, cur, d):
        """
       Whether to stop
         : param cur: current floor
         : param d: running direction
         : return: Whether the bool value stops
        """
        global msgQueue
        is_stop = False
        has_same_d = False
        tmp_list = msgQueue[:]
        if d == 1:
            if cur == TOP:
                is_stop = True
            for m in msgQueue:
                if m.type == 1 or m.type == 2:
                    has_same_d = True
                    if m.value == cur:
                        is_stop = True
                        tmp_list.remove(m)
        else:
            if cur == BOTTOM:
                is_stop = True
            for m in msgQueue:
                if m.type == 1 or m.type == 3:
                    has_same_d = True
                    if m.value == cur:
                        is_stop = True
                        tmp_list.remove(m)
        if not has_same_d:
            for m in msgQueue:
                if m.type and m.value == cur:
                    is_stop = True
                    tmp_list.remove(m)
        update_msgQueue("=", tmp_list)
        return is_stop

    def closeDoor(self):
        global exitFlag
        if exitFlag.value == 0:
            return
        t = threading.Thread(target=closeThread)
        t.start()

    def openDoor(self):
        global exitFlag
        if exitFlag.value == 1 or exitFlag.value == 2:
            return
        t = threading.Thread(target=openThread)
        t.start()


def openThread():
    """
   Open the door thread
    """
    global exitFlag, exitTime
    print("Opening door...")
    update_exitFlag(1)
    counter = exitTime
    while counter > 0:
        if exitFlag.value != 1 and exitFlag.value != 2:
            print("Door open termination")
            exitTime = counter
            return
        if exitLock.acquire():
            time.sleep(responseInterval)
            exitLock.release()
        counter -= responseInterval
    print("Door opened...")
    update_exitFlag(3)
    exitTime = 1.5


def closeThread():
    """
    Close child thread
    """
    global exitFlag, exitTime
    print("Closing...")
    update_exitFlag(0)
    counter = exitTime
    while counter > 0:
        if exitFlag.value != 0:
            print("Closed")
            exitTime = counter
            return
        if exitLock.acquire():
            time.sleep(responseInterval)
            exitLock.release()
        counter -= responseInterval

    print("closed")

    update_exitFlag(3)
    exitTime = 1.5


if __name__ == "__main__":

    thread1 = threading.Thread(target=msgFunction)
    thread2 = StateThreed()
    thread1.start()
    thread2.start()
