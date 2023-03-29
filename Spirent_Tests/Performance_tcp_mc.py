# Python imports#
import json
import sys
import argparse
import os
import time

sys.path.append(os.environ['STA_PATH'] + "testtool/lib")
# Local imports#
from ws_api import WsApi
from Common_library_set import CommonLib
from Common_library_set import ReturnValue
from NMS_library_set import NMS
from LC_library_set import LC
from RMT_library_set import RmtCommandValidation
from PP_library_set import PPCommandValidation
from Common_library_set import NetworkEnvironment
from SpirentAPI import SpirentVelocityAPI
from logger_checkpointer import init_logger, log, chkpt_pass, chkpt_fail, chkpt_info, log_json, close_logger

common_library = CommonLib()
spirent_API_obj = SpirentVelocityAPI()

class performance_test:
    def __init__(self, api_ip):
        ws_api = WsApi(ip_addr = api_ip)
        self.ws_api = ws_api

    def configure_mir_api(self, element_name, sspp_name, unconfig = "no"):
        ret = ReturnValue("configure_mir_api")
        if unconfig == "no":
            ret1 = nms_api.getParameterOnMatch('query?obj_name=' + str(element_name), ['obj_name'], [str(element_name)], 'obj_id')
            if ret1.return_code != 0:
                ret = ret1
                chkpt_fail('API call', ret.return_msg)
                return ret
            self.terminal_id = ret1.return_value
            sspp_name = sspp_name[0]
            ret2 = nms_api.getParameterOnMatch('query?obj_name="' + str(sspp_name)+'"', ['obj_name'], [str(sspp_name)], 'obj_id')
            if ret2.return_code != 0:
                ret = ret2
                chkpt_fail('API call', ret.return_msg)
                return ret
            self.sspp_id = ret2.return_value
            component = 'terminalserviceplan'
            tsp_id = nms_api.getParameterOnMatch(str(component),['obj_parentid'],[str(self.terminal_id)], 'obj_id')
            input_url = 'sspc/query?obj_parent_id='+str(tsp_id.return_value)+'&profile_id='+str(self.sspp_id)
            print input_url
            ret3 = self.ws_api.get(str(input_url))
            if ret3.return_code != 0:
                ret = ret3
                chkpt_fail('API call', ret.return_msg)
                return ret
            sspc_id = ret3.return_value['data']['obj_id']
            component = 'terminalqosapplication'
            ret2 = self.ws_api.get(input_url=str(component))
            if ret2.return_code != 0:
                ret = ret2
                chkpt_fail('API call', ret.return_msg)
                return ret
            output = ret2.return_value
            count = output['meta']['count']
            self.ibound_id = []
            self.obound_id = []
            for x in range(0,count):
                if output['data'][x]['obj_parent_id'] == int(sspc_id):
                    if output['data'][x]['obj_attributes']['direction'] == "Inbound":
                        self.ibound_id.append(output['data'][x]['obj_id'])
                        continue
                    if output['data'][x]['obj_attributes']['direction'] == "Outbound":
                        self.obound_id.append(output['data'][x]['obj_id'])
            input_url = str(component)+'/'+str(self.ibound_id[0])
            ret3 = self.ws_api.get(input_url)
            if ret3.return_code != 0:
                ret = ret3
                chkpt_fail('API call', ret.return_msg)
                return ret
            print "output of inbound id is,"+str(ret3.return_value)
            output = ret3.return_value
            self.original_mir_ib = output['data']['obj_attributes']['mir']
            input_mir = {"mir":"4"}
            ret4 = self.ws_api.patch(input_url, input_data_dict = input_mir)
            if ret4.return_code != 0:
                ret = ret4
                chkpt_fail('Patching component', ret.return_msg)
                return ret
            input_url = str(component)+'/'+str(self.obound_id[0])
            ret5 = self.ws_api.get(input_url)
            if ret5.return_code != 0:
                ret = ret5
                chkpt_fail('API call', ret.return_msg)
                return ret
            output = ret5.return_value
            self.original_mir_ob = output['data']['obj_attributes']['mir']
            input_mir = {"mir":"30"}
            ret6 = self.ws_api.patch(input_url, input_data_dict = input_mir)
            if ret6.return_code != 0:
                ret = ret6
                chkpt_fail('Patching component', ret.return_msg)
                return ret
            ret8 = self.ws_api.apply(str(self.terminal_id), input_data_dict = input_mir)
            if ret8.return_code != 0:
                ret = ret8
                chkpt_fail('API call', ret.return_msg)
                return ret
            ret = ret8
            return ret
        if unconfig == "yes":
            component = 'terminalqosapplication'
            input_url = str(component)+'/'+str(self.ibound_id[0])
            input_mir = {"mir":str(self.original_mir_ib)}
            ret4 = self.ws_api.patch(input_url, input_data_dict = input_mir)
            if ret4.return_code != 0:
                ret = ret4
                chkpt_fail('Patching component', ret.return_msg)
                return ret
            input_mir = {"mir":str(self.original_mir_ob)}
            input_url = str(component)+'/'+str(self.obound_id[0])
            ret6 = self.ws_api.patch(input_url, input_data_dict = input_mir)
            if ret6.return_code != 0:
                ret = ret6
                chkpt_fail('Patching component', ret.return_msg)
                return ret
            ret8 = self.ws_api.apply(str(self.terminal_id), input_data_dict = input_mir)
            if ret8.return_code != 0:
                ret = ret8
                chkpt_fail('API call', ret.return_msg)
                return ret
            ret = ret8
            return ret

    def validate_qos_status(self, sl_name):
        ret = ReturnValue("validate_qos_status")
        ret9 = rmt_obj.get_did('DID', 'CX751')
        if ret9.return_code != 0:
            ret = ret9
            return ret
        did = ret9.return_value
        if 'DOWN' in str(sl_name):
            ret10 = pp_obj.check_qos_status('Bps', row_key= sl_name, min_expected_val=28000000, max_expected_val=34000000, velo='yes', did=did)
            if ret10.return_code != 0:
                ret = ret10
                chkpt_fail('validate_qos_status', ret.return_msg)
                return ret
            else:
                ret.return_code = 0
                ret.return_value = None
                ret.return_msg = "Traffic rate is in range for DOWNSTREAM"
        if 'UP' in str(sl_name):
            ret11 = rmt_obj.check_qos_status('Out_bps', min_expected_val=3800000, max_expected_val=4300000, velo='yes', row_key=sl_name)
            if ret11.return_code != 0:
                ret = ret11
                chkpt_fail('validate_qos_status', ret.return_msg)
                return ret
            else:
                ret.return_code = 0
                ret.return_value = None
                ret.return_msg = "Traffic rate is in range for UPSTREAM"
        return ret

def main():
    global nms_api, pp_obj, rmt_obj
    init_logger(module_str='Performance_test', chkpt_str='Performance_test_tcp', log_str='Performance_test_tcp_mcast')

    parser = argparse.ArgumentParser()
    parser.add_argument("script_config_file", help="json file containing the configuration info about the test")
    cl_args = parser.parse_args()
    script_config_file = cl_args.script_config_file

    file_input = open(script_config_file, 'r')
    json_data = json.loads(file_input.read())
    network_file = json_data["network_file"]
    component = json_data["terminal_name"]
    sspp_name = json_data["sspp_name"]
    sl_name = json_data["sl_name"]
    vlan_name = json_data["vlan_name"]


    spirent_cfg_tcp_file_path = json_data["spirent_cfg_tcp_file_path"]
    spirent_cfg_mc_file_path = json_data["spirent_cfg_mc_file_path"]

    network_environment_obj = NetworkEnvironment(network_file)
    network_info = network_environment_obj.getNetworkInfo("obj")
    network_info =  network_info.return_value

    nms_api = NMS(network_info["nms_api_ip"][0], server_username= network_info["nms_username"][1], server_password=network_info["nms_password"][0], api_username=network_info["nms_api_username"][0],
                  api_password=network_info["nms_api_password"][0], restclient_path= os.environ["VELOTOOLPATH"])


    pp_obj = PPCommandValidation(network_info["pp_ip_set"][0])

    rmt_ip = network_info["rmt_ip_set"][0]
    rmt_port = network_info["rmt_port_set"][0]

    rmt_obj = RmtCommandValidation(rmt_ip, rmt_port, linux_passwd = network_info["nms_password"][0], console_passwd = network_info["nms_password"][0])

    performance_test_obj = performance_test(network_info["nms_api_ip"][0])
    ret12 = performance_test_obj.configure_mir_api(component, sspp_name)
    if ret12.return_code != 0:
        chkpt_fail('configure_mir_api', ret12.return_msg)
    else:
        chkpt_pass('configure_mir_api', ret12.return_msg)
    #start tcp background traffic
    spirent_API_obj.send_spirent_traffic_cir(spirent_config=str(os.environ['VELOCONFPATH']) + '' + str(spirent_cfg_tcp_file_path), start_or_stop='start')
    time.sleep(65)
    for x in sl_name:
        ret13 = performance_test_obj.validate_qos_status(x)
        if ret13.return_code != 0:
            chkpt_fail('validate_qos_status', ret13.return_msg)
        else:
            chkpt_pass('validate_qos_status', ret13.return_msg)

    #Stop the background traffic running
    spirent_API_obj.send_spirent_traffic_cir(spirent_config=str(os.environ['VELOCONFPATH']) + '' + str(spirent_cfg_tcp_file_path),start_or_stop='stop')

    #starting multicast traffic
    spirent_API_obj.send_spirent_traffic_cir(spirent_config=str(os.environ['VELOCONFPATH']) + '' + str(spirent_cfg_mc_file_path))
    ret14 = performance_test_obj.configure_mir_api(component, sspp_name, unconfig="yes")
    if ret14.return_code != 0:
        chkpt_fail('unconfigure_mir_api', ret12.return_msg)
    else:
        chkpt_pass('unconfigure_mir_api', ret12.return_msg)
    close_logger()

if __name__ == '__main__':
    main()

