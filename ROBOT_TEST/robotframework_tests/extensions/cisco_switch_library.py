from irobot.libraries.logger import logger
from irobot.libraries.iTelnet import iTelnet
import time


class cisco_switch_library(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.switchtype = "gigabitethernet"  #  fastethernet/gigabitethernet
        self.objtelnet = iTelnet()
        
    def connect_to_switch_using_lantronix(self, switch_alias, lantronix_ip, lantronix_port):
        self.objtelnet.open_connection(lantronix_ip, alias=switch_alias, prompt=">")
        self.objtelnet.set_prompt("#")
        if "enable" in self.objtelnet.execute_command("en"):
            self.objtelnet.set_prompt("is")
            if "Connected to line" in self.objtelnet.execute_command("connect line " + str(lantronix_port)):
                self.objtelnet.set_prompt(".", prompt_is_regexp=True)
                return True
            else:
                logger.error("Error - Session is already connected")
                return False    
        else:
            logger.error("Error - Unable to enable the lantronix console")
            return False
    
    def _enable_switch(self, switch_alias, password='iDirect'):
        self.objtelnet.switch_connection(switch_alias)
        self.objtelnet.write_bare('\x03')                
        self.objtelnet.read() # clean up console
        self.objtelnet.write_bare('\r\n')
        time.sleep(5)
        output = self.objtelnet.read()        

        if '#' in output:
            # Already in enabled mode
            self.objtelnet.set_prompt("#")
            return True
        elif '>' in output:
            self.objtelnet.set_prompt(":")
            if "word:" in self.objtelnet.execute_command("en"):
                self.objtelnet.set_prompt("#")
                self.objtelnet.execute_command(password)
                return True
            else:
                return False
        else:
            return False

    def _enable_config_in_switch(self, switch_alias):
        self.objtelnet.switch_connection(switch_alias)
        self._enable_switch(switch_alias)
        if "config" not in self.objtelnet.execute_command(" "):
            if "config" not in self.objtelnet.execute_command("configure terminal "):
                logger.error("Error - Unable to enable config in switch")
                return False
        elif "config-" in self.objtelnet.execute_command(" "):
            self.objtelnet.execute_command("exit ")
        time.sleep(10)
        return True
    
    def get_config(self, switch_alias, port):
        self.objtelnet.switch_connection(switch_alias)
        self._enable_switch(switch_alias)
        self.objtelnet.execute_command("")
        if "config" in self.objtelnet.execute_command(""):  
            self.objtelnet.execute_command("end ") 
        if str(self.switchtype).lower().strip() == "fastethernet":
            output = self.objtelnet.execute_command("sh run interface fastEthernet " + str(port) + " ")
        else:
            output = self.objtelnet.execute_command("sh run interface GigabitEthernet " + str(port) + " ")
        if str(port) in output:
            return output
        else:
            logger.error("Error - unable to get fastethernet/GigabitEthernet config")
            return False
    
    def remove_config(self, switch_alias, port):
        self.objtelnet.switch_connection(switch_alias)
        if self._enable_config_in_switch(switch_alias):
            if str(self.switchtype).lower().strip() == "fastethernet":
                self.objtelnet.execute_command("default interface fastEthernet " + str(port) + " ")
            else:
                self.objtelnet.execute_command("default interface GigabitEthernet " + str(port) + " ")
            return True            
        else:
            logger.error("Error - unable to remove fastethernet/GigabitEthernet config")
            return False

    def set_as_access(self, switch_alias, port, vlan):
        self.objtelnet.switch_connection(switch_alias)
        if self.remove_config(switch_alias, port):
            if str(self.switchtype).lower().strip() == "fastethernet":
                if "config-i" in self.objtelnet.execute_command("interface fastEthernet "+ str(port) + " "):
                    self.objtelnet.execute_command("switchport mode access ")
                    self.objtelnet.execute_command("switchport access vlan " + str(vlan) + " ")
                    self.objtelnet.execute_command("exit ")
                    time.sleep(5)
                    return True
                else:
                    logger.error("Error - unable to log to fastethernet config")
                    return False
            else:
                if "config-i" in self.objtelnet.execute_command("interface GigabitEthernet "+ str(port) + " "):
                    self.objtelnet.execute_command("switchport mode access ")
                    self.objtelnet.execute_command("switchport access vlan " + str(vlan) + " ")
                    self.objtelnet.execute_command("exit ")
                    time.sleep(5)
                    return True
                else:
                    logger.error("Error - unable to log to GigabitEthernet config")
                    return False
        else:
            return False
    
    def set_as_trunk(self, switch_alias, port, vlan=0):
        self.objtelnet.switch_connection(switch_alias)
        if self.remove_config(switch_alias, port):
            if str(self.switchtype).lower().strip() == "fastethernet":
                if "config-i" in self.objtelnet.execute_command("interface fastEthernet "+ str(port) + " "):
                    self.objtelnet.execute_command("switchport mode trunk ")
                    self.objtelnet.execute_command("switchport trunk encapsulation dot1q  ")
                    if vlan != 0:
                        self.objtelnet.execute_command("switchport trunk allowed vlan " + str(vlan) + " ")
                    self.objtelnet.execute_command("exit ")
                    time.sleep(10)
                    return True
                else:
                    logger.error("Error - unable to log to fastethernet config")
                    return False
            else:
                if "config-i" in self.objtelnet.execute_command("interface GigabitEthernet "+ str(port) + " "):
                    self.objtelnet.execute_command("switchport mode trunk ")
                    self.objtelnet.execute_command("switchport trunk encapsulation dot1q  ")
                    if vlan != 0:
                        self.objtelnet.execute_command("switchport trunk allowed vlan " + str(vlan) + " ")
                    self.objtelnet.execute_command("exit ")
                    time.sleep(10)
                    return True
                else:
                    logger.error("Error - unable to log to gigabitethernet config")
                    return False
        else:
            return False
    
    def set_switchtype(self,value):
        self.switchtype =value

    def disconnect_switch_using_lantronix(self, switch_alias):
        self.objtelnet.switch_connection(switch_alias)
        self.objtelnet.close_connection()
        return True

#c = cisco_switch_library()
#print c.connect_to_switch_using_lantronix("myswitch", "172.16.1.114", "26")
# print c.get_config("myswitch", "1/0/1")
# print c.set_as_access("myswitch", "1/0/1", 10)
# print c.get_config("myswitch", "1/0/1")
# print c.set_as_trunk("myswitch", "1/0/1")
# print c.get_config("myswitch", "1/0/1")
# print c.set_as_trunk("myswitch", "1/0/1", "1,2-5")
# print c.get_config("myswitch", "1/0/1")
# print c.remove_config("myswitch", "1/0/1")
# print c.get_config("myswitch", "1/0/1")
# print c.disconnect_switch_using_lantronix("myswitch")