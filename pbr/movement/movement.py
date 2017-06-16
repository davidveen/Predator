#!/usr/bin/env python
# coding: Latin-1
#
# Based on:
# https://www.piborg.org/diddyborg/install
#
# Import library functions we need
import time
import sys
import pbr.PicoBorgRev.PicoBorgRev3 as PicoBorgRev

#############
# Constants #
#############

# Setup the PicoBorg Reverse
PBR = PicoBorgRev.PicoBorgRev()
# Uncomment and change the value if you have changed the board address
# PBR.i2cAddress = 0x44
PBR.Init()

# Movement settings (worked out from our DiddyBorg on a smooth surface)
TIME_FORWARD_1M = 5.7  # Number of seconds needed to move about 1 meter
TIME_SPIN_360 = 4.8  # Number of seconds needed to make a full left / right spin

# Power settings
VOLTAGE_IN = 12.0  # Total battery voltage to the PicoBorg Reverse
VOLTAGE_OUT = 6.0  # Maximum motor voltage

# Setup the power limits
if VOLTAGE_OUT > VOLTAGE_IN:
    MAX_POWER = 1.0
else:
    MAX_POWER = VOLTAGE_OUT / float(VOLTAGE_IN)


######################
# Check chip present #
######################
def chip_present():
    if not PBR.foundChip:
        boards = PicoBorgRev.ScanForPicoBorgReverse()
        if len(boards) == 0:
            print 'No PicoBorg Reverse found, check you are attached :)'
        else:
            print 'No PicoBorg Reverse at address %02X, but we did find boards:' % (PBR.i2cAddress)
            for board in boards:
                print '    %02X (%d)' % (board, board)
            print 'If you need to change the I²C address change the setup line so it is correct, e.g.'
            print 'PBR.i2cAddress = 0x%02X' % (boards[0])
        sys.exit()

chip_present()
# Uncomment to disable EPO latch, needed if you do not have a switch / jumper
# PBR.SetEpoIgnore(True)
PBR.SetCommsFailsafe(False)  # Disable the communications failsafe
PBR.ResetEpo()


###################################
# Movement functions for Predator #
###################################

def move(drive_left, drive_right, num_seconds):
    """
    Function to perform a general movement
    """
    # Set the motors running
    PBR.SetMotor1(drive_right * MAX_POWER)
    PBR.SetMotor2(-drive_left * MAX_POWER)
    # Wait for the time
    time.sleep(num_seconds)
    # Turn the motors off
    PBR.MotorsOff()


# def corner(meters_hor, meters_ver, num_seconds):

def spin(angle):
    """
    Function to spin an angle in degrees
    """
    if angle < 0.0:
        # Left turn
        drive_left = -1.0
        drive_right = +1.0
        angle *= -1
    else:
        # Right turn
        drive_left = +1.0
        drive_right = -1.0
    # Calculate the required time delay
    num_seconds = (angle / 360.0) * TIME_SPIN_360
    # Perform the motion
    move(drive_left, drive_right, num_seconds)


def drive(meters):
    """
    Function to drive a distance in meters
    """
    if meters < 0.0:
        # Reverse drive
        drive_left = -1.0
        drive_right = -1.0
        meters *= -1
    else:
        # Forward drive
        drive_left = +1.0
        drive_right = +1.0
    # Calculate the required time delay
    num_seconds = meters * TIME_FORWARD_1M
    # Perform the motion
    move(drive_left, drive_right, num_seconds)
