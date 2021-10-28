import subprocess, sys
import time
import tkinter.messagebox
import tkinter as tk
import datetime

BATTERY_START_CHARGING_PERCENTAGE = 25.0
BATTERY_STOP_CHARGING_PERCENTAGE = 90.0
SLEEP_TIME_S = 60.0*1

# Note windows commands, so file can only be used with windows os
CMD_GET_BATTERY_PERGENTAGE = "WMIC PATH Win32_Battery Get EstimatedChargeRemaining"
CMD_GET_BATTERY_IS_CHARGING = "WMIC Path Win32_Battery Get BatteryStatus"


class MsgBoxBatteryEvent(object):
    """
    Create a message box which is either destroyed when a battery charging state change occurred,
    or when the user closes the message box manually

    Parameters
    ----------
    wait_time_ms : int (optional)
        Time to wait before a battery charging state change is polled
        in milliseconds (default=100 ms)
    """

    def __init__(self, wait_time_ms: int=100) -> None:
        # root and top used to A have option to hide root window
        # But B have msg box added to task bar
        self.__root = tk.Tk()
        self.__root.withdraw()
        self.__top = tk.Toplevel(self.__root)
        self.__top.iconify()
        self.__is_root_alive = True
        self.__battery_charging_state_init = get_battery_charging_state()
        self.__wait_time_ms = wait_time_ms
        
    def is_root_alive(self) -> bool:
        """
        Returns boolean True when root window of message box exist
        """
        return self.__is_root_alive

    def destory_root(self) -> None:
        """
        Destory the root msg box window
        """
        if self.is_root_alive():
            self.__is_root_alive = False
            self.__root.destroy()

    def __close_msg_box_state_change_fnc(self) -> None:
        """
        Function to close message box automatically when a battery charging
        state change has occurred
        """
        # Battery state changed, then close message box, otherwise poll again after
        # self.__wait_time_ms ms
        # No worries about recursion depth, function self.__root.after returns without blocking
        if self.__battery_charging_state_init != get_battery_charging_state():
            self.destory_root()
        elif self.is_root_alive():
            # only continue when root of msg box is still alive, 
            # otherwise the polling process should end
            self.__root.after(self.__wait_time_ms, self.__close_msg_box_state_change_fnc)

    def create_msg_box(self, *args, **kwargs) -> None:
        """
        Create message box with battery notification, which ends when either user
        closes the message box, or when the battery charging state changes (i.e from charging
        to discharging or vice versa)
        """
        self.__battery_charging_state_init = get_battery_charging_state()
        self.__close_msg_box_state_change_fnc()
        tkinter.messagebox.showinfo(*args, **kwargs, master=self.__root, parent=self.__top)
        self.destory_root()

    def __call__(self, *args, **kwards) -> None:
        """
        Runs the method create_msg_box
        """
        self.create_msg_box(*args, **kwards)


def print_time(msg: str) -> None:
    """
    Print a message with a time stamp
    """
    time_now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(time_now, msg, sep=" ")

def get_battery_charging_state() -> bool:
    """
    Returns the battery charging state

    True when battery is charging
    """
    process_battery_charing = subprocess.run(CMD_GET_BATTERY_IS_CHARGING, capture_output=True)
    is_charinging = (process_battery_charing.stdout.decode().replace("\r","").rsplit("\n"))
    if len(is_charinging[1].strip()) == 0:
        # Rare condition when a change occurs from charging to not charging or vise versa
        # String is then empty or filled with whitespace 
        is_charinging[1] = "-1"
    return int(is_charinging[1].strip()) == 2

def get_battery_percentage() -> float:
    """
    Returns the battery charge percentage 
    """
    process_battery_charge = subprocess.run(CMD_GET_BATTERY_PERGENTAGE, capture_output=True)
    percentage = (process_battery_charge.stdout.decode().replace("\r","").rsplit("\n"))
    return float(percentage[1].strip())

def main() -> None:
    while True:
        # Get battery percentage 
        percentage = get_battery_percentage()

        # Get battery charging state
        is_charinging = get_battery_charging_state()
        
        # Open notification if required
        if is_charinging:
            if percentage >= BATTERY_STOP_CHARGING_PERCENTAGE:
                print_time("Battery is sufficiently charged. Percentage: %2.1f %s" % (percentage, "%"))
                MsgBoxBatteryEvent()(title="Battery notification", message="Battery is done charging\nPrecentage: %2.1f" % percentage)
                is_charinging = get_battery_charging_state()
        else:
            if percentage <= BATTERY_START_CHARGING_PERCENTAGE:
                print_time("Battery needs charging. Percentage: %2.1f %s" % (percentage, "%"))
                MsgBoxBatteryEvent()(title="Battery notification", message="Battery is near empty\nPrecentage: %2.1f" % percentage)
                is_charinging = get_battery_charging_state()
        # Print status and wait 
        status = "charging" if is_charinging else "discharging"
        print_time("Status: %s, Percantage battery: %2.1f %s" % (status, percentage, "%"))
        time.sleep(SLEEP_TIME_S)

if __name__ == "__main__":
    if sys.platform != "win32":
        print("ERROR: Battery percentage notifier can only be used with a windows os")
        raise Exception("ERROR: Battery percentage notifier can only be used with a windows os")
    main()