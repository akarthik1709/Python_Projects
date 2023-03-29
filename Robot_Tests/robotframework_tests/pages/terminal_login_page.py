"""
Every page should contain following sections

1) all the locators
2) function to verify the current page is right one
3) function to make sure page is loaded
4) all the actions can be done in this page as functions
"""
from irobot.libraries.iSelenium import iSelenium
from terminal_dashboard_page import terminal_dashboard_page

class terminal_login_page(object):
    def __init__(self):
        # all the locators will be defined under init         
        self.txt_username = '//*[@id="n-input-9ka41_DC0Tdx"]' # lets try to use xpath as much as possible. and while nameing the locators use the format locator type in 3 character_ locator name. 
        self.txt_password = '//*[@id="n-input-pLsUQbOmUJx0"]'
        self.btn_login = '//*[@id="login"]/fieldset/div[2]/div/form/div[4]/button'
    
    def wait_for_page_to_load(self):
        try:
            iSelenium().wait_until_element_is_visible(self.btn_login, timeout=240)  # I say here, if login button appears, it means page is loaded. my assumption and mostly true in this case
            return True
        except:
            return False
    
    def login(self, username, password):
        iSelenium().input_text(self.txt_username, username)
        iSelenium().input_text(self.txt_password, password)
        iSelenium().click_button(self.btn_login)        
        return terminal_dashboard_page().wait_for_page_to_load()