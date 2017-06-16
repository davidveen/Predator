import math


TIME_FORWARD_1M = 5.7


def _limit_rel_speed(rel_speed):
    # Limit the relative speed:
    #   0 < relative speed <= 1
    rel_speed = max(min(rel_speed, 1.0), 0.0)
    if rel_speed == 0:
        raise ValueError
    return rel_speed


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
    print(num_seconds, drive_left, drive_right, meters)
    # Perform the motion
    # move(drive_left, drive_right, num_seconds)


corner_forward(90, 1)
