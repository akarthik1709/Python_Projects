import json
import ast

from irobot.libraries.logger import logger
from robot.libraries.BuiltIn import BuiltIn
from irobot.libraries.iTavern import iTavern
from irobot.libraries.iUtilities import iUtilities

class velo_terminal_ws_api_steps():

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        logger.set_system_library_log(True)

    def setup_test(self):
        self.terminal_ip = iUtilities().get_variable_from_robot("terminal_ip")
        self.username = iUtilities().get_variable_from_robot("username")
        self.password = iUtilities().get_variable_from_robot("password")
        self.tests = ast.literal_eval(json.loads(json.dumps(str(iUtilities().get_variable_from_robot("tests")))))

    def run_tx_test(self):
        session_name = iTavern().create_session("test_tx", self.terminal_ip, "GET")
        test_status = iTavern().run_test(session_name, self.tests['test_tx'])
        BuiltIn().should_be_true(test_status, "Status -> " + str(test_status))

