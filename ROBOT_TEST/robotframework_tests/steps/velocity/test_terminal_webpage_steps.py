import sys
import os
import time

from irobot.libraries.iSelenium import iSelenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "..","..", "pages"))

from terminal_login_page import terminal_login_page
from terminal_dashboard_page import terminal_dashboard_page
from terminal_commissioning_wizard_page import terminal_commissioning_wizard_page


class velo_terminal_webpage_steps(object):
    def __init__(self):
        self.login_page = terminal_login_page() 
        self.dashboard_page = terminal_dashboard_page()
        self.commissioning_wizard_page = terminal_commissioning_wizard_page()
                
        iSelenium().open_browser_with_tunnel("remote_wui", "172.18.214.12", "gc")
        iSelenium().maximize_browser_window()


    def commissioning_test(self):
        # login and pass credentials
        if self.login_page.wait_for_page_to_load():
            self.login_page.login("admin", "iDirect")
        else:
            print("\nTest failed - Login page didn't get load\n")

        # from dashboard go to commissioning page
        if self.dashboard_page.wait_for_page_to_load():
            self.dashboard_page.goto_commissioning_wizard_page()            
        else:
            print("\nTest failed - Dashboard page didn't load\n")

        # execute wizard steps 1-11
        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.btn_enter_commission_mode):
            status = self.commissioning_wizard_page.enter_commission_mode()
            if status:
                print "\nStep 1 is Passed\n"
            else:
                return status
        else:
            print("\nStep 1 Failed: 'Enter Commissioning Mode' did not load\n")

        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.btn_continue_without_changes):
            status = self.commissioning_wizard_page.continue_without_changes()
            if status:
                print "\nStep 2 is Passed\n"
        else:
            print("\nStep 2 Failed: 'Continue Without Changes' btn was not found\n")

        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.xpath_remote_latitude) and \
        self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.xpath_remote_longitude):
            status = self.commissioning_wizard_page.input_antenna_pointing_details(latitude=0.01, longitude=5.01)
            if status:
                print "\nStep 3 is Passed\n"
            else: 
                return status
        else:
            print("\nStep 3 Failed: 'Remote Latitude' txt box was not found\n")

        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.xpath_rf_frequency):
            status = self.commissioning_wizard_page.configure_downstream(frequency=19900, symrate=45000, rolloff=20)
            if status:
                print "\nStep 4 is Passed\n"
            else:
                return status
        else:
            print("\nStep 4 Failed: 'RF Frequency' txt did not load\n")

        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.btn_antenna_pointing):
            status = self.commissioning_wizard_page.fine_antenna_pointing()
            if status:
                print "\nStep 5 is Passed\n"
            else:
                return status
        else:
            print("\nStep 5 Failed: 'Start Antenna Pointing' btn did not load\n")

        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.btn_skip_to_next_step):
            status = self.commissioning_wizard_page.enable_continue_btn()
            if status:
                print "\nStep 6 is Passed\n"
            else:
                return status
        else:
            print("\nStep 6 Failed: Continue btn did not load\n")

        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.btn_skip_to_next_step):
            status = self.commissioning_wizard_page.cross_polarization_test()
            if status:
                print "\nStep 7 is Passed\n"
            else:
                return status
        else:
            print("\nStep 7 Failed: Continue btn box did not load\n")

        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.xpath_uplink_frequency):
            status = self.commissioning_wizard_page.p1db_test(frequency=20000)
            if status:
                print "\nStep 8 is Passed\n"
            else:
                return status
        else:
            print("\nStep 8 Failed: 'Turn on Signal' did not load\n")

        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.btn_continue_without_changes):
            status = self.commissioning_wizard_page.enter_transmit_parameters()
            if status:
                print "\nStep 9 is Passed\n"
            else:
                return status
        else:
            print("\nStep 9 Failed: 'p1B1' txt box did not load\n")

        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.btn_continue_to_next_step):
            status = self.commissioning_wizard_page.save_and_exit_commissioning_mode()
            if status:
                print "\nStep 10 is Passed\n"
            else:
                return status
        else:
            print("\nStep 10 Failed: Continue btn did not load\n")

        if self.commissioning_wizard_page.wait_for_page_to_load(self.commissioning_wizard_page.btn_return_to_dashboard):
            status = self.commissioning_wizard_page.finish_and_return_to_dashboard()
            if status:
                print "\nStep 11 is Passed. Wizard Test is Complete\n"
            else:
                return status
        else:
            print("\nStep 11 Failed: 'Return to Dashboard' btn did not load\n")

    def __del__(self):
        iSelenium().close_browser("remote_wui")


z = velo_terminal_webpage_steps()
z.commissioning_test()