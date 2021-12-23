
# Unsure if I can get rid of this within this file
import serial
import time

# PumPy FUNCTIONS

def initialiseBoard(port, baudrate):

    # Port auto opens upon object creation
    # NB - timeout is important to prevent blocking when using read functions etc
    board = serial.Serial(port, baudrate, timeout=10)
    msg = board.readline()
    if (msg == b'Connected!\r\n'):
        print("Connection successful")
    else:
        print("Connection FAILED")
    time.sleep(2) # wait for Arduino
    return board

# Enter pump shield/motor address as xy or variable representing this
# For mode, withdraw or infuse can be used
# Duration to be entered in seconds
def startPump(board, pump, mode, duration):

    if (mode == 'infuse'):
        direction = 1
    elif (mode == 'withdraw'):
        direction = 2
    else:
        print('ERROR: invalid mode, "infuse" or "withdraw" supported')
        return

    if (duration > 0 and duration < 10):
        duration = '0000' + str(duration)
    elif (duration > 0 and duration < 100):
        duration = '000' + str(duration)
    elif (duration > 0 and duration < 1000):
        duration = '00' + str(duration)
    elif (duration > 0 and duration < 10000):
        duration = '0' + str(duration)
    elif (duration > 10000 or duration < 0):
        print('ERROR: invalid duration, 0 - 10000 seconds supported')
        return

    command = 'r' + str(pump) + str(direction) + str(duration)
    print("Starting motor\n")
    board.write(b'' + command.encode('utf-8'))
    msg = board.readline()
    print(msg.decode('utf-8'))
    return

# I have not included correction for syringe diameter, therefore
# flow rate should be completed for each syringe type and for each pump
# Enter pump shield/motor address as xy or variable representing this
# repeats is an integer representing how many repeat measurements to average over
def calibrateFlow(board, pump, repeats):
    sum = 0
    for repeat in repeats:
        startWeight = input("Starting weight: ")
        pump = pump.encode('utf-8')
        board.write(b's' + pump + b'255')
        startPump(pump, 'infuse', 10)
        endWeight = input("Starting weight: ")
        sum = sum + (endWeight - startWeight)
    flowrate = sum / repeats
    return flowrate

# Enter pump shield/motor address as xy or variable representing this
# Enter speed as integer 0 - 255, where 255 is max. speed and 0 is stopped
def pumpSpeed(board, pump, speed):
    if (speed > 0 and speed < 10):
        speed = '00' + str(speed)
    elif (speed > 0 and speed < 100):
        speed = '0' + str(speed)
    elif (speed > 255 or speed < 0):
        print('ERROR: invalid speed, 0 - 255 seconds supported')
        return

    command = 's' + str(pump) + str(speed)
    board.write(b'' + command.encode('utf-8'))
    msg = board.readline()
    print(msg.decode('utf-8'))
    return

# NB, not yet tested
# For pre-calibrated syringes/pumps only, see calibration.py
# Unknown if the 0-255 increments flowrate linearly, assumed to here
def flowRate(board, pump, syringeLabel, csvPath, targetFlow):
    import pandas as pd
    df = pd.read_csv(csvPath)
    maxFlow = df.loc[syringeLabel, 'flowrate']

    if (targetFlow > maxFlow):
        pumpSpeed(pump, 255)
        print("Target flowrate above max., flowrate set at " + maxFlow)
    else:
        speed = (255 / maxFlow) * targetFlow
        pumpSpeed(pump, speed)
    return speed

def getNumberOfPumps(board):
    board.write(b'p')
    msg = board.readline()
    msg = msg.decode('utf-8')
    return int(msg[0]) * int(msg[2])

def getStatus(board):
    board.write(b'g')
    msg = board.readline()
    print(msg.decode('utf-8'))
    return msg

def stopAllPumps(board):
    board.write(b'a')
    msg = board.readline()
    print(msg.decode('utf-8'))
    return

def stopPump(board, pump):
    command = 'a' + str(pump)
    board.write(b'' + command.encode('utf-8'))
    msg = board.readline()
    print(msg.decode('utf-8'))
    return

