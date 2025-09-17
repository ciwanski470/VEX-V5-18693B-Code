# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       charlieiwanski                                               #
# 	Created:      8/17/2025, 8:47:21 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()
controller = Controller()

motorL1 = Motor(Ports.PORT1, True)
motorL2 = Motor(Ports.PORT2, True)
motorR1 = Motor(Ports.PORT10, False)
motorR2 = Motor(Ports.PORT9, False)

intakeMotor = Motor(Ports.PORT11, True)

intakeMotor.set_velocity(60, PERCENT)
intakeMotor.set_max_torque(100, PERCENT)

vision__RED_BALL = Signature(1, 10333, 15491, 12912,-1401, -947, -1174,3.9, 0)
vision__BLUE_BALL = Signature(2, -4779, -4069, -4424,6677, 7949, 7313,7, 0)
vision = Vision(Ports.PORT12, 50, vision__RED_BALL, vision__BLUE_BALL)

filterMotor = Motor(Ports.PORT13, True)
filterMotor.set_velocity(100, PERCENT)

conveyorMotor = Motor(Ports.PORT14)
conveyorMotor.set_velocity(50, PERCENT)

MODE_RED = 0
MODE_BLUE = 1

def dampPercent(percent):
    return 10 * math.sqrt(percent)

def leftStickChanged():
    vel = dampPercent(controller.axis3.position())
    motorL1.set_velocity(vel, PERCENT)
    motorL2.set_velocity(vel, PERCENT)
    
    motorL1.spin(FORWARD)
    motorL2.spin(FORWARD)

    print("Left torque: " + str(motorL1.torque()) + " NM")

def rightStickChanged():
    vel = dampPercent(controller.axis2.position())
    motorR1.set_velocity(vel, PERCENT)
    motorR2.set_velocity(vel, PERCENT)

    motorR1.spin(FORWARD)
    motorR2.spin(FORWARD)

    print("Right torque: " + str(motorR1.torque()) + " NM")

intakeState = 0

def buttonL1Down():
    global intakeState

    if intakeState != 1:
        intakeMotor.spin(FORWARD)
        conveyorMotor.spin(FORWARD)
        intakeState = 1
    else:
        intakeMotor.stop()
        conveyorMotor.stop()
        intakeState = 0
    
def buttonL2Down():
    global intakeState

    if intakeState != 2:
        intakeMotor.spin(REVERSE)
        conveyorMotor.spin(REVERSE)
        intakeState = 2
    else:
        intakeMotor.stop()
        conveyorMotor.stop()
        intakeState = 0

filterState = 0

def buttonR1Down():
    global filterState

    if filterState != 1:
        filterMotor.spin(FORWARD)
        filterState = 1
    else:
        filterMotor.stop()
        filterState = 0

def buttonR2Down():
    global filterState

    if filterState != 2:
        filterMotor.spin(REVERSE)
        filterState = 2
    else:
        filterMotor.stop()
        filterState = 0

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")

    # place driver control in this while loop

    controller.axis3.changed(leftStickChanged)
    controller.axis2.changed(rightStickChanged)
    
    controller.buttonL1.pressed(buttonL1Down)
    controller.buttonL2.pressed(buttonL2Down)

    controller.buttonR1.pressed(buttonR1Down)
    controller.buttonR2.pressed(buttonR2Down)
    

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()