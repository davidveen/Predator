#!/usr/bin/env python
# coding: Latin-1
#
# Based on:
# https://www.piborg.org/diddyborg/install
#
# Import library functions we need
import time
import sys
import math
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
def _chip_present():
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

_chip_present()
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


def corner_forward(angle, radius, rel_speed=1.0):
    """
    EXPERIMENTAL

    Make a corner
    """
    rel_speed = _limit_rel_speed(rel_speed)
    pi = math.pi
    angle_rad = angle / 180.0 * pi

    if angle < 0.0:
        drive_left = 1.0 * rel_speed
        drive_right = math.cos(angle_rad) * rel_speed
    else:
        drive_left = 1.0 * rel_speed
        drive_right = -math.cos(angle_rad) * rel_speed

    # Calculate the required time delay
    meters = 2 * pi * radius * math.sin(angle/720.0 * pi)
    num_seconds = meters * TIME_FORWARD_1M / rel_speed

    # Perform the motion
    move(drive_left, drive_right, num_seconds)


def spin(angle, rel_speed=1.0):
    """
    Function to spin an angle in degrees
    """
    rel_speed = _limit_rel_speed(rel_speed)

    if angle < 0.0:
        # Left turn
        drive_left = -rel_speed
        drive_right = rel_speed
        angle *= -1
    else:
        # Right turn
        drive_left = rel_speed
        drive_right = -rel_speed
    # Calculate the required time delay
    num_seconds = (angle / 360.0) * TIME_SPIN_360 / rel_speed
    # Perform the motion
    move(drive_left, drive_right, num_seconds)


def drive(meters, rel_speed=1.0):
    """
    Function to drive a distance in meters
    """
    rel_speed = _limit_rel_speed(rel_speed)

    if meters < 0.0:
        # Reverse drive
        drive_left = -rel_speed
        drive_right = -rel_speed
        meters *= -1
    else:
        # Forward drive
        drive_left = rel_speed
        drive_right = rel_speed

    # Calculate the required time delay
    num_seconds = meters * TIME_FORWARD_1M / rel_speed

    # Perform the motion
    move(drive_left, drive_right, num_seconds)


def _limit_rel_speed(rel_speed):
    # Limit the relative speed:
    #   0 < relative speed <= 1
    rel_speed = max(min(rel_speed, 1.0), 0.0)
    if rel_speed == 0:
        raise ValueError
    return rel_speed
