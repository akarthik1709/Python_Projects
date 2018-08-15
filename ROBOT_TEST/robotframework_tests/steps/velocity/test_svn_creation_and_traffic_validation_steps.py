# iRobot Framework libraries
import irobot
import time
import collections
from robot.api.deco import keyword

# Low level Layer Libraries
from irobot.libraries.iSSH import iSSH
from irobot.libraries.iREST import iREST
from irobot.libraries.logger import logger
from irobot.libraries.iUtilities import iUtilities
from robot.libraries.BuiltIn import BuiltIn

# Middle level layer libraries

from irobot.libraries.iDirect.iNMS import iNMS
from irobot.libraries.iDirect.iPrecondition import iPrecondition
from irobot.libraries.iSpirent import iSpirent
NMS_API_Alias = 'NMS_API_Alias'
class velo_svn_creation_and_traffic_validation_steps(object):
    def __init__(self):
        logger.set_system_library_log(True)
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def setup_test(self):
        logger.console("\n --Setting up the Objects... \n")
        self.nms_ip = iUtilities().get_variable_from_robot('nms_ip')
        if not self.nms_ip:
            BuiltIn().fail("\n **NMS ip is not provided in the config file... \n")

        self.remote_name = iUtilities().get_variable_from_robot('remote_name')
        if not self.remote_name:
            BuiltIn().fail("\n **Remote name is not provided in the config file... \n")  

        self.all_svns = iUtilities().get_variable_from_robot('all_svns')
        if not self.all_svns:
            BuiltIn().fail("\n **Variable 'all_svns' value is not provided in the configuration file... \n")
        
        self.svn_to_delete = iUtilities().get_variable_from_robot('svn_to_delete')
        if not self.svn_to_delete:
            BuiltIn().fail("\n **Variable 'svn_to_delete' value is not provided in the configuration file... \n")

        self.gsp_name = iUtilities().get_variable_from_robot('gsp_name')
        if not self.gsp_name:
            BuiltIn().fail("\n **Variable 'gsp_name' value is not provided in the configuration file... \n")

        self.site_name = iUtilities().get_variable_from_robot('site_name')
        if not self.site_name:
            BuiltIn().fail("\n **Variable 'site_name' value is not provided in the configuration file... \n")

        self.port_switch_name = iUtilities().get_variable_from_robot('port_switch_name')
        if not self.port_switch_name:
            BuiltIn().fail("\n **Variable 'port_switch_name' value is not provided in the configuration file... \n")
                   
        self.ds_mir = 30 if not iUtilities().get_variable_from_robot('ds_mir') else iUtilities().get_variable_from_robot('ds_mir') 
        self.ds_cir = 1 if not iUtilities().get_variable_from_robot('ds_cir') else iUtilities().get_variable_from_robot('ds_cir') 
        self.us_mir = 30 if not iUtilities().get_variable_from_robot('us_mir') else iUtilities().get_variable_from_robot('us_mir') 
        self.us_cir = 1 if not iUtilities().get_variable_from_robot('us_cir') else iUtilities().get_variable_from_robot('us_cir') 

        # Precondition
        iPrecondition().should_be_valid_ip(self.nms_ip)
        iPrecondition().should_be_reachable_from_local(self.nms_ip)

        self.nms_ssh_username, self.nms_ssh_password=  iUtilities().get_user_credentials(self.nms_ip, 'NMS_ssh')
        self.nms_rest_username, self.nms_rest_password=  iUtilities().get_user_credentials(self.nms_ip, 'NMS_client')
        logger.console("nms_ip" + str(self.nms_ip))

        # Connecting to NMS and PP - API and SSH
        ret_nms = iNMS().open_nms_api_session('NMS_API_Alias', self.nms_ip, self.nms_rest_username, self.nms_rest_password)
        if not ret_nms:
            BuiltIn().fail("\n NMS API Session cannot be established \n ")
        
        self.remote_ip = iNMS().get_remote_properties('NMS_API_Alias', self.remote_name, "LanIP")
        logger.console("The Remote IP is -> " + str(self.remote_ip))

        ret_nms_ssh = iNMS().log_into_nms('NMS_SSH_Alias', self.nms_ip, self.nms_ssh_username, self.nms_ssh_password)
        if not ret_nms_ssh:
            BuiltIn().fail("\n NMS SSH Session cannot be established \n ")
        self.reserve_spirent = False
        self.svn_created = False
        self.svns_for_traffic = [x for x in self.all_svns if x not in self.svn_to_delete]
 
        # Fetch Spirent details
        self.spirent = iUtilities().get_variable_from_robot('Spirent')
        self.stc_ip = iUtilities().get_variable_from_robot('stc_ip')
        self.stc_slot = iUtilities().get_variable_from_robot('stc_slot')
        self.stc_hub_port = iUtilities().get_variable_from_robot('stc_hub_port')
        self.stc_remote_port = iUtilities().get_variable_from_robot('stc_remote_port')
        self.spirent_config = {}

    def generate_pp_svn_details(self, svn_list):
        sitesvns = iNMS().get_components(NMS_API_Alias, 'sitesvn')
        svndata = sitesvns[0]['obj_attributes']
        _startaddress= svndata['startaddress'].split('.') 
        _endaddress= svndata['endaddress'].split('.') 
        _gateway= svndata['gateway'].split('.')
        pp_svn_details = {'loopback_subnet':'255.255.255.255','site_name':self.site_name,'loopback_ip':'128.128.128.128','vlan_subnet':'255.255.255.128', 'svn_details': {}}
        for each_svn in svn_list:
            _startaddress[0] = str(each_svn)
            _endaddress[0] = str(each_svn)
            _gateway[0] = str(each_svn)

            pp_svn_details['svn_details'].update({\
                                                    each_svn : {
                                                        'blade_svn_name': 'SERVER_SVN_' + str(each_svn),\
                                                        'site_svn_name': 'SITE_SVN_'  + str(each_svn),\
                                                        'svn_name': 'SVN_' + str(each_svn),\
                                                        'svn_id': int(each_svn), \
                                                        'vlan_start_ip': '.'.join(_startaddress),\
                                                        'vlan_end_ip': '.'.join(_endaddress),\
                                                        'vlan_gw': '.'.join(_gateway),\
                                            }
                                    })
        return pp_svn_details
    
    def generate_remote_svn_details(self, svn_list):
        remote_svn_details = {}
        remote_details = iNMS().get_component(NMS_API_Alias, self.remote_name)
        valid_terminal_type_id = remote_details['obj_attributes']["terminaltype_id"]
        terminalsvns = iNMS().get_components(NMS_API_Alias, 'terminalsvn')

        terminal_types_available = iNMS().get_components(NMS_API_Alias, 'terminaltype')
        for each_type in terminal_types_available:
                if str(each_type['obj_id']) == str(valid_terminal_type_id):
                    terminal_type = each_type['obj_name']
                    break
        else:
            BuiltIn().fail("Unable to retrieve terminal type!")

        for each_termianl_svn in terminalsvns:
            if each_termianl_svn['obj_attributes']["eth0ip"] == self.remote_ip:
                terminalsvndata = each_termianl_svn['obj_attributes']
                _sat0gateway= terminalsvndata['sat0gateway'].split('.') 
                _sat0ip= terminalsvndata['sat0ip'].split('.') 
                _eth0gateway= terminalsvndata['eth0gateway'].split('.')
                _eth0ip= terminalsvndata['eth0ip'].split('.') 
                _sat0subnet= terminalsvndata['sat0subnet']
                _eth0subnet= terminalsvndata['eth0subnet']
                for each_svn in svn_list:
                    _sat0gateway[0] = str(each_svn)
                    _sat0ip[0] = str(each_svn)
                    _eth0gateway[0] = str(each_svn)
                    _eth0ip[0] = str(each_svn)

                    remote_svn_details.update({
                        each_svn: {
                            'sspp': {
                                'gsp_name': self.gsp_name,\
                                'obj_name': 'CONFIG_SSPP_' +str(each_svn),\
                                'dn_basec_no': '16APSK-8/9',\
                                'valid_terminal': [str(terminal_type)],\
                            },
                            'traffic_service_level':  [
                                {
                                    'direction': 'Inbound',
                                    'obj_name': 'TSL_Inbound_'+ str(each_svn)
                                },
                                {
                                    'direction': 'Outbound',
                                    'obj_name': 'TSL_Outbound_' + str(each_svn)
                                }
                            ],
                            'traffic_rule': [
                                {
                                    'protocol_enable': True,
                                    'parent_service_level_name': 'TSL_Inbound_' + str(each_svn),
                                    'svn_rng_enable': True,
                                    'protocol': 'TCP',
                                    'direction': 'Inbound',
                                    'svn_rngop': '=',
                                    'optimization': 'MaxChannelEfficiency',
                                    'obj_name': 'TR_Inbound_' + str(each_svn),
                                    'scheduling': 'PriorityQueue',
                                    'svn_rng': int(each_svn),
                                    'protocolop': '<>',
                                    'type': 'Unreliable'
                                },
                                {
                                    'protocol_enable': True,
                                    'parent_service_level_name': 'TSL_Outbound_' + str(each_svn),
                                    'svn_rng_enable': True,
                                    'protocol': 'TCP',
                                    'direction': 'Outbound',
                                    'svn_rngop': '=',
                                    'optimization': 'MaxChannelEfficiency',
                                    'obj_name': 'TR_Outbound_' + str(each_svn),
                                    'scheduling': 'PriorityQueue',
                                    'svn_rng': int(each_svn),
                                    'protocolop': '<>',
                                    'type': 'Unreliable'
                                }
                            ],
                            'vr': [
                                {
                                    'parent_service_level_name': 'TSL_Inbound_' + str(each_svn),
                                    'direction': 'Inbound',
                                    'priority': 6,
                                    'cir': int(self.us_cir),
                                    'cost': 1,
                                    'mir': int(self.us_mir)
                                },
                                {
                                    'parent_service_level_name': 'TSL_Outbound_' + str(each_svn),
                                    'direction': 'Outbound',
                                    'priority': 6,
                                    'cir': int(self.ds_cir),
                                    'cost': 1,
                                    'mir': int(self.ds_mir)
                                }
                            ],
                            'terminalsvn': [
                                {
                                    'port_switch_name': self.port_switch_name,
                                    'pp_svn_name': 'SVN_' + str(each_svn),\
                                    'sat0gateway': '.'.join(_sat0gateway),\
                                    'ipaddressing': 'StaticAddressing(0)',
                                    'sat0subnet': _sat0subnet,
                                    'eth0gateway': '.'.join(_eth0gateway),\
                                    'eth0ip': '.'.join(_eth0ip),\
                                    'eth0subnet': _eth0subnet,
                                    'sat0ip': '.'.join(_sat0ip),\
                                    'vlan_id': int(each_svn)
                                }
                            ],
                        }
                    })
        return remote_svn_details

    @keyword(name='Create ${svn_to_create} SVNs in PP')            
    def create_svns_in_pp(self, svn_to_create):
        logger.console("Creating SVNs" + str(svn_to_create) + " in PP")
        pp_svn_details = self.generate_pp_svn_details(svn_to_create)
        pp_svn = iNMS().create_svn_pp(NMS_API_Alias, pp_svn_details, *svn_to_create)
        BuiltIn().should_be_true(pp_svn, "SVN creation in PP failed" )

    @keyword(name='Create ${svn_to_create} SVNs in Terminal')        
    def create_svns_in_terminal(self, svn_to_create):
        logger.console("Creating SVNs" + str(svn_to_create) + " in Terminal")
        remote_svn_details = self.generate_remote_svn_details(svn_to_create)
        terminal_svn = iNMS().create_terminal_service_plan(NMS_API_Alias, self.remote_name, remote_svn_details, *svn_to_create)
        BuiltIn().should_be_true(terminal_svn, "SVN creation in Terminal failed" )
        self.apply_terminal()
        output, timetaken = iNMS().wait_for_component('NMS_SSH_Alias', self.remote_ip, timeout= 600) 
        if not (output): BuiltIn().fail("Terminal did not come back in network after applying configurations")
        self.svn_created = True 
        self.generate_spirent_configurations_for_svn(svn_to_create)

    def apply_terminal(self):
        logger.console("Applying the Terminal")
        apply_terminal = iNMS().apply_component(NMS_API_Alias, self.remote_name, 'terminal')
        BuiltIn().should_be_true(apply_terminal, "Apply Terminal failed" )
        BuiltIn().sleep(30)

    @keyword(name = 'Delete ${svn_to_delete} SVN in PP')
    def delete_svn_pp(self, svn_ids_to_delete):
        pp_svn_details_delete = self.generate_pp_svn_details(svn_ids_to_delete)
        delete_pp_svn_result= iNMS().delete_svn_pp(NMS_API_Alias, pp_svn_details_delete, *svn_ids_to_delete)
        BuiltIn().should_be_true(delete_pp_svn_result, "SVN Deletion in PP failed!")

    @keyword(name = 'Delete ${svn_to_delete} SVN in Terminal and PP')
    def _delete(self, svn_to_delete):
        if self.svn_created:
            self.delete_svn_terminal(svn_to_delete)
            self.delete_svn_pp(svn_to_delete)
        else:
            BuiltIn().fail("SVNs were not created. Aborting!")
      
    def delete_svn_terminal(self, svn_ids_to_delete):
        remote_svn_details_delete= self.generate_remote_svn_details(svn_ids_to_delete)
        delete_terminal_svn_result= iNMS().delete_svn_terminal(NMS_API_Alias, self.remote_name, remote_svn_details_delete, *svn_ids_to_delete)
        BuiltIn().should_be_true(delete_terminal_svn_result, "SVN Deletion in Remote failed!")
        self.apply_terminal()

    @keyword(name = 'Enable DNS for created SVNs ${svn_to_create} in Terminal')
    def enable_dns_in_svns(self, svn_to_create):
        if self.svn_created:
            for each_svn in svn_to_create:
                logger.console("\n Enabling DNS...\n")
                self.primaryaddress = '100.10.10.1'
                self.secondaryaddress = '200.20.20.1'
                self.cache_size = '50'
                dns_config_status = iNMS().enable_dns(NMS_API_Alias, self.remote_name, each_svn,
                                                    self.primaryaddress,
                                                    self.secondaryaddress,
                                                    self.cache_size)
                BuiltIn().should_be_true(dns_config_status, "\n **Enabling DNS failed")
                BuiltIn().sleep(30)
                self.dns_reverse_flag = True
                output, timetaken = iNMS().wait_for_component('NMS_SSH_Alias', self.remote_ip, timeout= 600) 
                if not (output): BuiltIn().fail("Terminal did not come back in network after enabling DNS configurations")
        else:
            BuiltIn().fail("SVNs were not created. Aborting!")

    @keyword(name = 'Enable DHCP for created SVNs ${svn_to_create} in Terminal')
    def enable_dhcp_in_svns(self, svn_to_create):
        self.dhcp_details = {'leasedurationunit': "Hours", 'mode': "DHCPServer", 'serversubnetv4': "16.16.16.16", 'leaseduration': "3600", 'defaultgateway': "16.16.16.17",'servernetmaskv4': "255.255.255.0", 
                            'dhcprange': "{\"(16.16.16.19,16.16.16.22)\"}", 'dhcpbroadcastip': "16.16.16.23", 'primarydns': "17.17.17.1", 'secondarydns': "17.17.17.2"}            
        for each_svn in svn_to_create:
            logger.console("\n Enabling DHCP...\n")
            dhcp_config_status = iNMS().configure_dhcp(NMS_API_Alias, self.remote_name, each_svn, dhcp_body=self.dhcp_details)
            BuiltIn().should_be_true(dhcp_config_status, "\n **Enabling DHCP failed")
            output, timetaken = iNMS().wait_for_component('NMS_SSH_Alias', self.remote_ip, timeout= 600) 
            BuiltIn().sleep(60)
            if not (output): BuiltIn().fail("Terminal did not come back in network after enabling DHCP configurations")
    
    @keyword(name='Add new SVN ${new_svn_to_add} in PP and Terminal')  
    def add_new_svn(self, new_svn_to_add):
        if self.svn_created:
            self.create_svns_in_pp(new_svn_to_add)
            self.create_svns_in_terminal(new_svn_to_add)
            self.generate_spirent_configurations_for_svn(new_svn_to_add)
        else:
            BuiltIn().fail("SVNs were not created. Aborting!")

    @keyword(name = 'Run UDP Traffic for ${svn_to_create} SVNs')
    def run_traffic_for_created_svns(self, svn_to_create):
        self.run_udp_traffic_for_svn(svn_to_create)
    
    @keyword(name = 'Run UDP Traffic for all SVNs')
    def run_traffic_for_all_svns(self):
        self.run_udp_traffic_for_svn(self.all_svns)

    def run_udp_traffic_for_svn(self, svnlist):
        self.reserve_ports()
        self.hand = {}
        self.streams = []
        self.spirent_svn_params = {}
        for each_svn in svnlist:
            spirent = self.spirent_config['spirent_' +str(each_svn)]
            if each_svn not in self.svns_for_traffic:
                spirent['skip_arp'] = True 
            udp_stream, handlers = iSpirent().config_udp_traffic(**spirent)
            self.hand.update({each_svn : handlers})
            self.streams.append(udp_stream)
        for each_stream in self.streams:
            iSpirent().start_traffic(each_stream)
        for x in range(0, int(self.spirent["test_time"]), 5):
            logger.console("Running Traffic... ")
            time.sleep(5)
        self.stop_traffic()
    
    def generate_spirent_configurations_for_svn(self, svn_list):
        for each_svn in svn_list:
            traffic_conf = iNMS().get_traffic_host_ipconf(NMS_API_Alias, self.remote_name, each_svn, ignore_ip_list=[])
            self.spirent_config.update({
                "spirent_" + str(each_svn) : {
                    "hub_host_name" :  'hub_host_vlan_' + str(each_svn),
                    "remote_host_name" :  'remote_host_vlan_' + str(each_svn),
                    "remote_host_vlan_id" :  int(each_svn),
                    "hub_host_vlan_id" :   int(each_svn)
                }
            })
            self.spirent_config["spirent_" + str(each_svn)].update(traffic_conf[str(each_svn)])
            self.spirent_config["spirent_" + str(each_svn)].update(self.spirent)
        return self.spirent_config

    def reserve_ports(self):
        logger.console("\n Reserving the spirent ports... \n")
        self.release_ports()
        reserve_spirent_ports = iSpirent().setup_spirent(self.stc_ip,self.stc_slot,self.stc_hub_port,self.stc_remote_port)
        BuiltIn().should_be_true(reserve_spirent_ports, "Unable to reserve spirent ports... ")
        self.reserve_spirent = True
    
    def stop_traffic(self):
        logger.console("\n Stopping the UDP traffic... \n")
        for each_stream in self.streams:
            iSpirent().stop_traffic(each_stream)

    def release_ports(self):
        if self.reserve_spirent: iSpirent().teardown_spirent()
        self.reserve_spirent = False
    
    def validate_traffic_for_all_svns(self):
        for each_svn, each_handler in self.hand.iteritems():
            if "udp_condition_list" in self.spirent.keys() and iUtilities().is_list(self.spirent["udp_condition_list"]):
                udp_condition_list = self.spirent["udp_condition_list"]
            else:
                udp_condition_list = iSpirent().obj_stc_api.result_assertion["UDP_Traffic_Validation"]
            spirent_result, output = iSpirent().validate_udp_traffic(each_handler, udp_condition_list)
            BuiltIn().should_be_true(spirent_result, "SVN Traffic validation failed... ")
    
    def validate_traffic_for_remaining_svns(self):
        if "udp_condition_list" in self.spirent.keys() and iUtilities().is_list(self.spirent["udp_condition_list"]):
            udp_condition_list = self.spirent["udp_condition_list"]
        else:
            udp_condition_list = iSpirent().obj_stc_api.result_assertion["UDP_Traffic_Validation"]
        for each_svn, each_handler in self.hand.iteritems():
            if each_svn in self.svns_for_traffic:
                spirent_result, output = iSpirent().validate_udp_traffic(each_handler, udp_condition_list)
                BuiltIn().should_be_true(spirent_result, "SVN Traffic validation failed... ")
            else:
                spirent_result, output = iSpirent().validate_udp_traffic(each_handler, udp_condition_list)
                BuiltIn().should_not_be_true(spirent_result, "SVN Traffic validation failed... ")

    def revert_changes(self):
        self.delete_svn_terminal(self.all_svns)
        self.delete_svn_pp(self.all_svns)
        logger.console("\n Releasing the spirent ports... \n")
        self.release_ports()
        iSSH().close_all_ssh_session()
        iREST().disconnect_all()
        