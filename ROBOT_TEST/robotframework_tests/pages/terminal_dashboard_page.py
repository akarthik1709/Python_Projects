"""
Every page should contain following sections

1) all the locators
2) function to verify the current page is right one
3) function to make sure page is loaded
4) all the actions can be done in this page as functions
"""
from irobot.libraries.iSelenium import iSelenium
from robot.libraries.BuiltIn import BuiltIn
from terminal_commissioning_wizard_page import terminal_commissioning_wizard_page

class terminal_dashboard_page(object):
    def __init__(self):

        # all the locators will be defined under init    
        self.lnk_admin = "link:Administration"
        self.lnk_commissioning = "link:Commissioning"        
        self.lnk_commissioning_wizard = "link:Commissioning Wizard"
        
        
    def wait_for_page_to_load(self):
        try:
            iSelenium().wait_until_element_is_visible(self.lnk_commissioning, timeout=20)
            return True
        except:
            return False
    
    def goto_commissioning_wizard_page(self):
        BuiltIn().sleep(10)
        iSelenium().wait_until_element_is_enabled(self.lnk_commissioning)
        iSelenium().click_link(self.lnk_commissioning)
        iSelenium().wait_until_element_is_enabled(self.lnk_commissioning_wizard)
        iSelenium().click_link(self.lnk_commissioning_wizard)
        return self.wait_for_page_to_load()