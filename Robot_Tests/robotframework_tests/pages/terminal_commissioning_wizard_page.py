"""
Every page should contain following sections

1) all the locators
2) function to verify the current page is right one
3) function to make sure page is loaded
4) all the actions can be done in this page as functions
"""
from irobot.libraries.iSelenium import iSelenium
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
import time

class terminal_commissioning_wizard_page(object):
    def __init__(self):
        # all the locators will be defined under init
        self.btn_enter_commission_mode = '//*[@id="commissioning_wizard"]/div[3]/div/button'        
        self.btn_continue_without_changes = '//*[@id="commissioning_wizard"]/div[3]/div/button[1]'
        self.btn_skip_to_next_step = "//div[@id='commissioning_wizard']/div[3]/div/button"
        self.xpath_remote_latitude = '//*[@id="angle-calculator-remote-latitude-container"]/span/span/input[1]'
        self.xpath_remote_longitude = '//*[@id="angle-calculator-remote-longitude-container"]/span/span/input[1]'
        self.id_remote_latitude = '#angle-calculator-remote-latitude'
        self.id_remote_longitude = '#angle-calculator-remote-longitude'
        self.btn_continue_to_next_step = '//*[@id="commissioning_wizard"]/div[3]/div/button'
        self.xpath_rf_frequency = '//*[@id="antenna-pointing-rf-frequency-container"]/span/span/input[1]'
        self.id_rf_frequency = '#antenna-pointing-rf-frequency'
        self.xpath_symrate = '//*[@id="antenna-pointing-symbol-rate-container"]/span/span/input[1]'
        self.id_symrate = '#antenna-pointing-symbol-rate'
        self.xpath_rolloff = '//*[@id="antenna-pointing-rolloff-container"]/span/span/input[1]'
        self.id_rolloff = '#antenna-pointing-rolloff'
        self.btn_antenna_pointing = '//*[@id="commissioning_wizard"]/div[2]/div/div/strong/div[2]/div[1]/span[1]/button'
        self.btn_continue_to_point_antenna = '//div[3]/button'
        self.txt_lock_status = "//*[@id='commissioning_wizard']/div[2]/div/div/strong/p/span[2]"
        self.xpath_uplink_frequency = '//*[@id="cross-polarization-rf-uplink-frequency-container"]/span/span/input[1]'
        self.id_uplink_frequency = '#cross-polarization-rf-uplink-frequency'
        self.btn_turn_on_signal = "//button[@type='submit']"
        self.btn_turn_off_signal_and_complete = "//button[@type='submit'][2]"
        self.btn_apply_changes = "//button[@type='submit']"
        self.btn_return_to_dashboard = '//*[@id="commissioning_wizard"]/div[2]/div/div[2]/button'
        
    def wait_for_page_to_load(self, element):
        try:
            iSelenium().wait_until_element_is_visible(element, timeout=25)
            return True
        except Exception as e:
            print ("\nElement is not visible, error message is: "+str(e)+".\n")
            return False

    def wait_and_click_btn(self, btn_locator):
        try:
            iSelenium().wait_until_element_is_enabled(btn_locator, timeout=25)
            time.sleep(3)
            iSelenium().click_button(btn_locator)
            time.sleep(1)
            return True
        except Exception as e:
            print ("\nButton is not enabled to click on it, error message is: "+str(e)+".\n")
            return False

    # step 1
    def enter_commission_mode(self):
        status = self.wait_and_click_btn(self.btn_enter_commission_mode)
        return status

    # step 2
    def continue_without_changes(self):
        status = self.wait_and_click_btn(self.btn_continue_without_changes)
        if status != True:
            status = self.wait_and_click_btn(self.btn_skip_to_next_step)
        return status

    # step 3
    def input_antenna_pointing_details(self, latitude, longitude):
        locator_lst = [self.id_remote_latitude, self.id_remote_longitude]
        value_lst = [latitude, longitude]
        try:
            for each_locator, each_value in zip(locator_lst, value_lst):
                iSelenium().set_kendo_ui_numeric_box(each_locator, each_value)
            status = self.enable_continue_btn()
            if not status:
                return status
            return True
        except:
            False

    # step 4
    def configure_downstream(self, frequency, symrate, rolloff):
        locator_lst = [self.id_rf_frequency, self.id_symrate, self.id_rolloff]
        value_lst = [frequency, symrate, rolloff]
        try:
            for each_locator, each_value in zip(locator_lst, value_lst):
                iSelenium().set_kendo_ui_numeric_box(each_locator, each_value)
            status = self.enable_continue_btn()
            if not status:
                return status
            return True
        except:
            return False
    # step 5
    def fine_antenna_pointing(self):
        try:
            btn_list = [self.btn_antenna_pointing, self.btn_continue_to_point_antenna]
            for each_btn in btn_list:
                status = self.wait_and_click_btn(each_btn)
                if not status:
                    return status
            for i in range(0, 60):
                output = iSelenium().get_text(self.txt_lock_status)
                time.sleep(1)
                if "locked" in output.lower():
                    break
            self.wait_and_click_btn(self.btn_antenna_pointing)
            status = self.enable_continue_btn()
            if not status:
                return status
            return True
        except:
            return False

    # step 6
    def enable_continue_btn(self):
        status = self.wait_and_click_btn(self.btn_skip_to_next_step)
        return status

    # step 7
    def cross_polarization_test(self):
        iSelenium().wait_for_spinner_to_complete()
        time.sleep(5)
        status = self.wait_and_click_btn(self.btn_skip_to_next_step)
        return status

    # step 8
    def p1db_test(self, frequency):
        try:
            btn_list = [self.btn_turn_on_signal, self.btn_apply_changes, self.btn_turn_off_signal_and_complete]
            iSelenium().set_kendo_ui_numeric_box(self.id_uplink_frequency, frequency)
            for each_btn in btn_list:
                status = self.wait_and_click_btn(each_btn)
                time.sleep(2)
                if not status:
                    return False
            status = self.enable_continue_btn()
            if not status:
                return status
            return True
        except:
            return False

    # step 9
    def enter_transmit_parameters(self):
        status = self.continue_without_changes()
        return status

    # step 10
    def save_and_exit_commissioning_mode(self):
        status = self.enable_continue_btn()
        return status

    # step 11
    def finish_and_return_to_dashboard(self):
        status = self.wait_and_click_btn(self.btn_return_to_dashboard)
        return status
























