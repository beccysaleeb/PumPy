import time
global data_manager
global instrument
global acquisition
global profiles

# Connect to instriument if not already
def connect():
    global instrument
    instrument.SelectInstrument('WBA23LBV')
    if not instrument.IsConnected:
        print("Instrument unconnected connecting....")
        instrument.Connect()
    print("instrument connected")
    return

# Disconnect from instriument if not already
def disconnect():
    global instrument
    instrument.SelectInstrument('WBA23LBV')
    if instrument.IsConnected:
        print("Instrument connected disconnecting....")
        instrument.Disconnect()
    print("instrument disconnected")
    return

# Capture snapshot
def snap(exposure, folder, file, inst = instrument, laser405 = 0, laser488 = 0, laser561 = 0, laser638 = 0):
    # Set camera parameters
    camera = inst.CameraControl
    camera.SetTargetExposureMilliseconds(exposure)

    # Set acquisition parameters
    acquisition.SaveTiffFiles = True
    acquisition.RealTimeLocalization = False

    # Set laser powers
    lasers = inst.LightControl
    lasers[0].PercentPower = laser405
    lasers[1].PercentPower = laser488
    lasers[2].PercentPower = laser561
    lasers[3].PercentPower = laser638

    # Switch on required lasers
    laser = 0
    while laser < 4:
        if lasers[laser].PercentPower == 0:
            lasers[laser].Enabled = False
        else:
            lasers[laser].Enabled = True
        laser += 1

    # Activate lasers
    lasers.GlobalOnState = True

    # Start acquisition (arguments: folder name, file name, frames)
    acquisition.Start(folder, file, 1)

    # Wait until the acquisition has stopped
    while acquisition.IsActiveOrCompleting:
        time.sleep(0.1)

    # Disable lasers
    lasers.GlobalOnState = False

    # Wait for data_manager to finish
    while data_manager.IsBusy:
        time.sleep(0.1)

    # Check the status
    if data_manager.CurrentStatus == data_manager.Status.EMPTY:
        print("No data. Acquisition failed!")

    # Print the filenames
    files = data_manager.Files
    print('Files saved:')
    for f in files:
        print(f)
    return

# Capture series
def series(exposure, frames, folder, file, laser405 = 0, laser488 = 0, laser561 = 0, laser638 = 0):
    # Set camera parameters
    camera = instrument.CameraControl
    camera.SetTargetExposureMilliseconds(exposure)

    # Set acquisition parameters
    acquisition.SaveTiffFiles = True
    acquisition.RealTimeLocalization = False

    # Set laser powers
    lasers = instrument.LightControl
    lasers[0].PercentPower = laser405
    lasers[1].PercentPower = laser488
    lasers[2].PercentPower = laser561
    lasers[3].PercentPower = laser638

    # Switch on required lasers
    laser = 0
    while laser < 4:
        if lasers[laser].PercentPower == 0:
            lasers[laser].Enabled = False
        else:
            lasers[laser].Enabled = True
        laser += 1

    # Activate lasers
    lasers.GlobalOnState = True

    # Start acquisition (arguments: folder name, file name, frames)
    acquisition.Start(folder, file, frames)

    # Wait until the acquisition has stopped
    while acquisition.IsActiveOrCompleting:
        time.sleep(0.1)

    # Disable lasers
    lasers.GlobalOnState = False

    # Wait for data_manager to finish
    while data_manager.IsBusy:
        time.sleep(0.1)

    # Check the status
    if data_manager.CurrentStatus == data_manager.Status.EMPTY:
        print("No data. Acquisition failed!")

    # Print the filenames
    files = data_manager.Files
    print('Files saved:')
    for f in files:
        print(f)
    return
