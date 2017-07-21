"""
I'm a docstring
"""
KEEP_GOING = True

CURR_INPUT = 

def follow_the_line():
    """
    :)
    """
    # initiate pid
    pid=pid(
        P=1.2,
        I=1,
        D=0.001
    )
    pid.set_sample_time(0.2)
    # set desired path
    desired = 0
    while KEEP_GOING and not BOOM_IS_HO:
        curr_dev = desired + curr_input
        # get pid-output
        pid_out = pid.update(curr_dev)
        # get powersettings from pidoutput

        # set powersettings

def get_power_setting(deviation):
    """
    :)
    """
    

