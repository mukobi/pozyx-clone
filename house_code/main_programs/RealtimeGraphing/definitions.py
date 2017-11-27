# data collection type definitions
DATA_TYPE_POSITIONING = 0
DATA_TYPE_RANGING = 1
DATA_TYPE_MOTION_DATA = 2

# osc message indices relative to tag
OSC_TIME_INDEX_ABSOLUTE = 1
OSC_1D_RANGE_INDEX = 1
OSC_1D_VELOCITY_INDEX = 2

OSC_INDEX_DICT = {
    "time": OSC_TIME_INDEX_ABSOLUTE,
    "1D_range": OSC_1D_RANGE_INDEX,
    "1D_velocity": OSC_1D_VELOCITY_INDEX
}
