#!/usr/bin/env python
"""change_uwb_settings.py - Changes the UWB settings of all devices listed.

This assumes all listed devices are on the same UWB settings already,
otherwise you should run the set_same_settings.py script, as that one
finds all devices on all settings.
"""
import sys
from pypozyx import *
from pypozyx.definitions.registers import POZYX_UWB_CHANNEL, POZYX_UWB_RATES, POZYX_UWB_PLEN
from modules.configuration import Configuration

class ChangeUWBSettings:

    def __init__(self, pozyx, uwb_settings, devices=None, set_local=True, save_to_flash=True):
        if devices is None:
            devices = []
        self.pozyx = pozyx
        self.uwb_settings = uwb_settings
        self.devices = devices
        self.set_local = set_local
        self.save_to_flash = save_to_flash
        self.get_start_settings()

    def get_start_settings(self):
        self.start_settings = UWBSettings()
        status = self.pozyx.getUWBSettings(self.start_settings)
        if status == POZYX_SUCCESS:
            print("Old UWB settings: %s" % self.start_settings)
        else:
            print("Old UWB settings could not be retrieved, terminating")
            raise Exception
        return status

    def get_new_settings(self):
        self.start_settings = UWBSettings()
        status = self.pozyx.getUWBSettings(self.start_settings)
        if status == POZYX_SUCCESS:
            print("New UWB settings: %s" % self.start_settings)
        else:
            print("New UWB settings could not be retrieved, terminating")
            raise Exception
        return status

    def run(self):
        for tag in self.devices:
            self.set_to_settings(tag)
        if not self.set_local:
            self.pozyx.setUWBSettings(self.start_settings)
        else:
            if save_to_flash:
                self.pozyx.saveUWBSettings()
                self.get_new_settings()

    def set_to_settings(self, remote_id):
        self.pozyx.setUWBSettings(self.start_settings)
        self.pozyx.setUWBSettings(self.uwb_settings, remote_id)
        self.pozyx.setUWBSettings(self.uwb_settings)
        whoami = SingleRegister()
        status = self.pozyx.getWhoAmI(whoami, remote_id)
        if whoami[0] != 0x67 or status != POZYX_SUCCESS:
            # print("Changing UWB settings on device 0x%0.4x failed" % remote_id)
            return
        else:
            print("Settings successfully changed on device 0x%0.4x" % remote_id)
        if self.save_to_flash:
            status = self.pozyx.saveUWBSettings(remote_id)
            if status != POZYX_SUCCESS:
                print("\tAnd saving settings failed.")
            else:
                print("\tAnd saving settings succeeded")


def check_uwb_setting(uwb_settings):
    # channel
    channel = uwb_settings.channel
    if channel < 1 or channel > 6:
        sys.exit("Incorrect channel value (%i). Channel needs to be a whole number from 1 to 6." % channel)
    # bitrate
    bitrate = uwb_settings.bitrate
    if bitrate < 0 or bitrate > 2:
        sys.exit("Incorrect bitrate value. Bitrate needs to be a whole number from 0 to 2.")
    # prf
    prf = uwb_settings.prf
    if prf < 1 or prf > 2:
        sys.exit("Incorrect prf value. Prf needs to be 1 or 2.")
    # plen
    plen = uwb_settings.plen
    possible_plen = [0x0C, 0x28, 0x18, 0x08, 0x34, 0x24, 0x14, 0x04]
    if plen not in possible_plen:
        sys.exit("Incorrect plen value. Plen needs to be 0x0C, 0x28, 0x18, 0x08, 0x34, 0x24, 0x14, or 0x04.")
    # gain
    gain = uwb_settings.gain_db
    if uwb_settings.gain_db < 0 or uwb_settings.channel > 33.5:
        sys.exit("Incorrect gain value. Gain needs to be a number from 0 to 33.5.")


if __name__ == '__main__':
    # ***DEFAULTS*** #
    default_uwb_settings = UWBSettings(channel=2,
                               bitrate=1,
                               prf=2,
                               plen=0x08,
                               gain_db=15.0)
    # set to True if local tag needs to change settings as well.
    set_local = True
    # set to True if needed to save to flash
    save_to_flash = True
    # don't try to remotely change settings, it doesn't work.
    devices = [0x0000]
    # ***END DEFAULTS*** #

    uwb_settings = None

    arguments = sys.argv
    arg_length = len(arguments)

    # no arguments added on, only call was to script
    if arg_length is 1:
        uwb_settings = default_uwb_settings
        print("Setting default UWB settings:\nCh 2, BR 850 mbps, PRF 64 Mhz, PLen 1024, Gain 15 db\n")
    # all 5 UWB arguments were passed plus the call to the script
    elif arg_length is 6:
        try:
            arg_channel = int(arguments[1])
            arg_bitrate = int(arguments[2])
            arg_prf = int(arguments[3])
            arg_plen = int(arguments[4], 16)
            arg_gain = float(arguments[5])
        except ValueError:
            sys.exit(
                "\nThere was an error in your arguments, please make sure they are in the form:\n"
                "[int] channel [int] bitrate [int] prf [hex int] plen [float] gain")

        uwb_settings = UWBSettings(channel=arg_channel,
                                   bitrate=arg_bitrate,
                                   prf=arg_prf,
                                   plen=arg_plen,
                                   gain_db=arg_gain)
        # print(uwb_settings)
        # print(uwb_settings.data)




    else:
        sys.exit("\nSorry, your arguments are incorrect. Please make sure you include no arguments "
                 "after the script name to use the default settings or include 6 arguments in the form:\n"
                 "[int] channel [int] bitrate [int] prf [hex int] plen [float] gain")

    check_uwb_setting(uwb_settings)

    serial_port = Configuration.get_correct_serial_port()
    # pozyx
    pozyx = PozyxSerial(serial_port)

    # initialize the class
    c = ChangeUWBSettings(pozyx, uwb_settings, devices, set_local, save_to_flash)

    # run the functionality
    c.run()