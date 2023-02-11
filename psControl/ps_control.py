from inputs import get_gamepad
import time

# Assumes that the controller is connected via USB

class Controller():
    def __init__(self):
        # Initialize a controller state
        self.state = {
            # Direction buttons X: Left(-1), Rest(0), Right(1)
            #                   Y: Up(-1), Rest(0), Down(1)
            "dir_X"     : 0,
            "dir_Y"     : 0,
            # Action buttons (L)eft, (R)ight, (U)p, (D)own
            "act_L"     : 0,
            "act_R"     : 0,
            "act_U"     : 0,
            "act_D"     : 0,
            # L1 R1 buttons
            "L1"        : 0,
            "R1"        : 0,
            # L2 R2 analog sticks
            "L2"        : 0,
            "R2"        : 0,
            # Select and Start
            "SEL"       : 0,
            "STR"       : 0,
            # L3 R3 buttons
            "L3_btn"    : 0,
            "R3_btn"    : 0,
            # L3 stick  : [X position, Y position]; X,Y = [-32768, 32767]
            "L3"        : [0, 0],
            # R3 stick  : [X position, Y position]; X,Y = [-32768, 32767]
            "R3"        : [0, 0],
        }

        # Store a default value for the L3 and R3 sticks because these analog values deviate quite a bit
        self.l3_def = [0,0]
        self.r3_def = [0,0]
    
    def parseCode(self, eventCode, eventState):
        if eventCode == "BTN_HAT0X":
            self.state["dir_X"] = eventState

        elif eventCode == "BTN_HAT0Y":
            self.state["dir_Y"] = eventState

        elif eventCode == "BTN_WEST":
            self.state["act_L"] = eventState

        elif eventCode == "BTN_EAST":
            self.state["act_R"] = eventState

        elif eventCode == "BTN_NORTH":
            self.state["act_U"] = eventState

        elif eventCode == "BTN_SOUTH":
            self.state["act_D"] = eventState

        elif eventCode == "BTN_TL":
            self.state["L1"] = eventState

        elif eventCode == "BTN_TR":
            self.state["R1"] = eventState

        elif eventCode == "ABS_Z":
            self.state["L2"] = eventState

        elif eventCode == "ABS_RZ":
            self.state["R2"] = eventState

        # The controls are inverted for select and start
        elif eventCode == "BTN_START":
            self.state["SEL"] = eventState

        elif eventCode == "BTN_SELECT":
            self.state["STR"] = eventState
        
        elif eventCode == "BTN_THUMBL":
            self.state["L3_btn"] = eventState
        
        elif eventCode == "BTN_THUMBR":
            self.state["R3_btn"] = eventState

        elif eventCode == "ABS_X":
            if abs(eventState) > 1000:
                self.state["L3"][0] = eventState #- self.l3_def[0]
            else:
                self.state["L3"][0] = 0

        elif eventCode == "ABS_Y":
            if abs(eventState) > 1000:
                self.state["L3"][1] = eventState #- self.l3_def[1]
            else:
                self.state["L3"][1] = 0

        elif eventCode == "ABS_RX":
            if abs(eventState) > 1000:
                self.state["R3"][0] = eventState #- self.r3_def[0]
            else:
                self.state["R3"][0] = 0

        elif eventCode == "ABS_RY":
            if abs(eventState) > 1000:
                self.state["R3"][1] = eventState #- self.r3_def[1]
            else:
                self.state["R3"][1] = 0

    # Usually implemented in a thread because it has be constantly read
    def read(self):
        for event in get_gamepad():
            # Ignore sync events
            if(event.ev_type == "Sync"):
                continue

            self.parseCode(event.code, event.state)

    # Get current state of buttons
    def getState(self, input):
        try:
            return self.state[input]
        except:
            print("Incorrect button ID")
    
    # Get current state of all parameters
    def getStateF(self):
        return self.state

    # Caliberate default values for L3 and R3 sticks
    # Do not touch the controller in this stage
    # A default state is not currently reliable
    # Instead, just ignore values < 1000
    def caliberate(self):
        return 0
        print("Performing caliberation for 5 seconds")

        t1 = time.time()
        while(time.time() - t1 < 5):
            self.read()
        self.l3_def = self.state["L3"]
        self.r3_def = self.state["R3"]

        print("Caliberation done")

    # Despite the controller having dual shock capability, the current
    # module (inputs) is unable to service this feature.
    # aproxeng is a library that can do this but is not supported for
    # windows
    def dualShock(self, input):
        pass
