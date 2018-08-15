"""
This script finds out the amount of UDP traffic that can possibly pass via a VLAN in a single direction,
calculating throughput for both upstream and downstream
"""

# Python specific libraries
import os
import sys
import argparse

# TestAutomation specific libraries
STA_PATH = os.environ['STA_PATH']
sys.path.append(os.path.join(STA_PATH, 'testtool', 'lib'))

from Common_library_set import ReturnValue, NetworkEnvironment, CommonLib
from logger_checkpointer import init_logger, chkpt_pass, chkpt_fail, close_logger, log, logger, chkpt_info
from PP_library_set import PP
from RMT_library_set import Remote
from LC_library_set import LC
from ws_api_pulse import WsApiPulse
from SpirentAPI import SpirentVelocityAPI, GetSpirentVelocityIps
SpirentVelocityAPI_obj = SpirentVelocityAPI()
commonLib = CommonLib()

class UDPPerformance:

    def __init__(self, network_info, terminal_ip, vlan_id, jumpserver_ip, throughput_expected_threshold=90):
        self.network_info = network_info
        self.terminal_ip = terminal_ip
        self.vlan_id = vlan_id
        self.jumpserver_ip = jumpserver_ip
        self.modulation_map = {'BPSK':1, 'QPSK':2, '8PSK':3, '16PSK':3}
        self.throughput_expected_threshold = throughput_expected_threshold
        self.pulse = WsApiPulse(network_info['nms_api_ip'][0], network_info['nms_api_username'][0], network_info['nms_api_password'][0], logger=logger)
        self.remote = Remote(self.terminal_ip, via_jump='yes', jump_ip=self.jumpserver_ip)

        #Initial setting below - will be overridden by output from findPPWithRemoteIP, get_operating_linecard_with_terminal
        self.pp = PP(network_info['pp_ip_set'][0], password=network_info['pp_password'][0], root_password=network_info['pp_password'][0])
        self.lc = LC(network_info['lc_ip_set'][1], linux_passwd=network_info['lc_password'][1])

    def findPPWithRemoteIP(self):
        '''
        This procedure helps in finding out the PP which handles that remote with the remote IP as input.
        :return: If return_code = 0, its a PASS. return_value contains pp_ip
        '''
        ret = ReturnValue('findPPWithRemoteIP')
        response = self.pulse.getDIDWithEth0IP(self.terminal_ip)

        if response.return_code > 2:
            ret = response
            ret.return_msg = 'Unable to fetch serial number with terminal ip '+str(self.terminal_ip)+' because of the following error: '+response.return_msg
            return ret

        serial_number = response.return_value

        response = self.pp.getPPWithRemoteDID(serial_number, self.network_info['pp_ip_set'], pp_password=self.network_info['pp_password'])

        if response.return_code > 2:
            ret = response
            ret.return_msg = 'Unable to fetch PP IP with serial number '+str(serial_number)+' because of the following error: '+response.return_msg
            return ret

        pp_ip = response.return_value[0]

        ret.return_code = 0
        ret.return_value = pp_ip
        ret.return_msg = 'PP which handles remote '+str(self.terminal_ip)+' is '+str(pp_ip)

        return ret

    def calculate_downstream_throughput(self):
        '''
        Procedure that calculates the downstream throughput taking modcod from PP_TPA and symbolrate from remote
        :return: If return_code = 0, its a PASS. Return value contains throughput
        '''

        ret = ReturnValue('calculate_downstream_throughput')

        #Fetch downstream modcod from PP_TPA
        response = self.pp.getCmdOutputFromPPProcess('pp_tpa', 'premote dvbs2_stats')

        if response.return_code > 2:
            ret = response
            ret.return_msg = 'Unable to fetch downstream modcod from PP because of the following error: '+response.return_msg
            return ret

        response = commonLib.splitByLineValue(response.return_value, 'cur_modcod_name','= "','"')

        if response.return_value == []:
            ret = response
            ret.return_msg = 'Unable to fetch downstream modcod from "premote dvbs2_stats" because of the following error: '+response.return_msg
            return ret

        down_modulation = self.modulation_map[response.return_value[0].split('_')[0]]
        down_fecrate = response.return_value[0].split('_')[1]

        #Fetch downstream symbolrate from remote falcon
        response = self.remote.getCmdOutputFromFalcon('rx symrate')

        if response.return_code > 2:
            ret = response
            ret.return_msg = 'Unable to fetch downstream symrate from Remote because of the following error: '+response.return_msg
            return ret

        response = commonLib.splitByLineValue(response.return_value, 'Rx Symrate','=','sym')

        if response.return_value == []:
            ret = response
            ret.return_msg = 'Unable to fetch downstream modcod from "Rx Symrate" because of the following error: '+response.return_msg
            return ret

        down_symrate = response.return_value[0]

        log('DEBUG', down_symrate)
        log('DEBUG', down_modulation)
        log('DEBUG', down_fecrate)

        #Calculate downstream throughput
        down_throughput = int(int(down_symrate)*int(down_modulation)*(float(down_fecrate.split("/")[0])/int(down_fecrate.split("/")[1])))/1000000

        ret.return_value = down_throughput
        ret.return_msg = 'Downstream throughput calculated successfully. Throughput is '+str(down_throughput)+' Mbps'
        ret.return_code = 0

        return ret

    def calculate_upstream_throughput(self):
        '''
        Procedure that calculates the upstream throughput taking modcod and symbolrate from linecard
        :return: If return_code = 0, its a PASS. Return value contains throughput
        '''

        ret = ReturnValue('calculate_upstream_throughput')

        #Fetch upstream modcod and symbol rate from LC
        response = self.lc.getCmdOutputFromLCProcess('mcd channel show')

        if response.return_code > 2:
            ret = response
            ret.return_msg = 'Unable to fetch upstream modcod and symrate from Linecard because of the following error: '+response.return_msg
            return ret

        lc_output = response.return_value

        response = commonLib.splitByLineValue(lc_output, 'Symbol Rate',':','sym')

        if response.return_value == []:
            ret = response
            ret.return_msg = 'Unable to fetch Symbol Rate from "mcd channel show" because of the following error: '+response.return_msg
            return ret

        up_symrate = response.return_value[0]

        response = commonLib.splitByLineValue(lc_output, 'Modulation',':','')

        if response.return_value == []:
            ret = response
            ret.return_msg = 'Unable to fetch upstream Modulation from "mcd channel show" because of the following error: '+response.return_msg

            return ret

        up_modulation = self.modulation_map[response.return_value[0]]

        response = commonLib.splitByLineValue(lc_output, 'FEC','(',')')

        if response.return_value == []:
            ret = response
            ret.return_msg = 'Unable to fetch upstream FEC from "mcd channel show" because of the following error: '+response.return_msg
            return ret

        up_fecrate = response.return_value[0]

        log('DEBUG',up_symrate)
        log('DEBUG',up_modulation)
        log('DEBUG',int(up_fecrate.split("/")[0]))
        log('DEBUG',int(up_fecrate.split("/")[1]))

        #Calculate upstream throughput based on modulation, fecrate and symbolrate for upstream
        up_throughput = int((int(up_symrate)*int(up_modulation))/(1/(float(up_fecrate.split("/")[0])/int(up_fecrate.split("/")[1]))))/1000000

        ret.return_value = up_throughput
        ret.return_msg = 'Upstream throughput calculated successfully. Throughput is '+str(up_throughput)+' Mbps'
        ret.return_code = 0

        return ret

    def update_ip_information(self, traffic_type, ip_info, vlan_id, direction, spirent_cfg_file_path, **kwargs):
        '''
        Procedure that updates unidirectional/bidirectional information to tcl configuration file
        :param traffic_type: UDP/TCP/MULTICAST
        :param ip_info: List that contains hub/remote information
        :param vlan_id: VLAN id information for traffic
        :param direction: upstream/downstream/bidirectional
        :param spirent_cfg_file_path: Spirent configuration path
        :return: If return_code = 0, its a PASS else FAIL
        '''
        ret = ReturnValue('update_ip_information')
        SRCIP = SRCMASK = SRCGW = DSTIP = DSTMASK = DSTGW = VLANID = DIR = STREAMNAME = FRAMELENGTHMODE = PS = FPS = NOOFCONNECTIONS = FILESIZE = ''

        #Decide if its unidirectional or bidirectional
        if 'bidirectional' in direction:
            for index in xrange(0, len(ip_info[0])):
                SRCIP += '\\"'+ip_info[0][index][0]+'\\" \\"'+ip_info[0][index][1]+'\\" '
                SRCMASK += '\\"'+ip_info[1][index][0]+'\\" \\"'+ip_info[1][index][1]+'\\" '
                SRCGW += '\\"'+ip_info[2][index][0]+'\\" \\"'+ip_info[2][index][1]+'\\" '
                DSTIP += '\\"'+ip_info[3][index][0]+'\\" \\"'+ip_info[3][index][1]+'\\" '
                DSTMASK += '\\"'+ip_info[4][index][0]+'\\" \\"'+ip_info[4][index][1]+'\\" '
                DSTGW += '\\"'+ip_info[5][index][0]+'\\" \\"'+ip_info[5][index][1]+'\\" '
                VLANID += '\\"'+str(vlan_id)+'\\" \\"'+str(vlan_id)+'\\" '
                DIR += '\\"DOWNSTREAM\\" \\"UPSTREAM\\" '
                STREAMNAME += '\\"DS\\" \\"US\\" '
                FRAMELENGTHMODE += '\\"FIXED\\" \\"FIXED\\" '
                if 'PS' in kwargs:
                    PS += '\\"'+kwargs['PS']+'\\" \\"'+kwargs['PS']+'\\" '
                if 'FPS' in kwargs:
                    FPS += '\\"'+kwargs['FPS']+'\\" \\"'+kwargs['FPS']+'\\" '
                if 'NOOFCONNECTIONS' in kwargs:
                    NOOFCONNECTIONS += '\\"'+kwargs['NOOFCONNECTIONS']+'\\" \\"'+kwargs['NOOFCONNECTIONS']+'\\" '
                if 'FILESIZE' in kwargs:
                    FILESIZE += '\\"'+kwargs['FILESIZE']+'\\" \\"'+kwargs['FILESIZE']+'\\" '
        elif direction == "downstream":
            for index in xrange(0, len(ip_info[0])):
                SRCIP += '\\"'+ip_info[0][index][0]+'\\" '
                SRCMASK += '\\"'+ip_info[1][index][0]+'\\" '
                SRCGW += '\\"'+ip_info[2][index][0]+'\\" '
                DSTIP += '\\"'+ip_info[3][index][0]+'\\" '
                DSTMASK += '\\"'+ip_info[4][index][0]+'\\" '
                DSTGW += '\\"'+ip_info[5][index][0]+'\\" '
                VLANID += '\\"'+str(vlan_id)+'\\" '
                DIR += '\\"DOWNSTREAM\\" '
                STREAMNAME += '\\"DS\\" '
                FRAMELENGTHMODE += '\\"FIXED\\" '
        elif direction == "upstream":
            for index in xrange(0, len(ip_info[0])):
                SRCIP += '\\"'+ip_info[3][index][0]+'\\" '
                SRCMASK += '\\"'+ip_info[4][index][0]+'\\" '
                SRCGW += '\\"'+ip_info[5][index][0]+'\\" '
                DSTIP += '\\"'+ip_info[0][index][0]+'\\" '
                DSTMASK += '\\"'+ip_info[1][index][0]+'\\" '
                DSTGW += '\\"'+ip_info[2][index][0]+'\\" '
                VLANID += '\\"'+str(vlan_id)+'\\" '
                DIR += '\\"UPSTREAM\\" '
                STREAMNAME += '\\"US\\" '
                FRAMELENGTHMODE += '\\"FIXED\\" '

        if direction != "bidirectional":
            if 'PS' in kwargs:
                PS += '\\"'+kwargs['PS']+'\\" '
            if 'FPS' in kwargs:
                FPS += '\\"'+kwargs['FPS']+'\\" '
            if 'NOOFCONNECTIONS' in kwargs:
                NOOFCONNECTIONS += '\\"'+kwargs['NOOFCONNECTIONS']+'\\" '
            if 'FILESIZE' in kwargs:
                FILESIZE += '\\"'+kwargs['FILESIZE']+'\\" '

        #Patch all Traffic_Type, IP addresses, vlan id in config file
        command_list = {'TRAFFIC_TYPE': 'sed -i "s/set TRAFFIC_TYPE .*/set TRAFFIC_TYPE \\"'+traffic_type+'\\"/g" '+spirent_cfg_file_path,
                        'SRCIP': 'sed -i "s/set SRCIP .*/set SRCIP {'+SRCIP+'}/g" '+spirent_cfg_file_path,
                        'SRCMASK': 'sed -i "s/set SRCMASK .*/set SRCMASK {'+SRCMASK+'}/g" '+spirent_cfg_file_path,
                        'SRCGW': 'sed -i "s/set SRCGW .*/set SRCGW {'+SRCGW+'}/g" '+spirent_cfg_file_path,
                        'DSTIP': 'sed -i "s/set DSTIP .*/set DSTIP {'+DSTIP+'}/g" '+spirent_cfg_file_path,
                        'DSTMASK': 'sed -i "s/set DSTMASK .*/set DSTMASK {'+DSTMASK+'}/g" '+spirent_cfg_file_path,
                        'DSTGW': 'sed -i "s/set DSTGW .*/set DSTGW {'+DSTGW+'}/g" '+spirent_cfg_file_path,
                        'VLANID': 'sed -i "s/set VLANID .*/set VLANID {'+VLANID+'}/g" '+spirent_cfg_file_path,
                        'DIR': 'sed -i "s/set DIR .*/set DIR {'+DIR+'}/g" '+spirent_cfg_file_path,
                        'STREAMNAME': 'sed -i "s/set STREAMNAME .*/set STREAMNAME {'+STREAMNAME+'}/g" '+spirent_cfg_file_path,
                        'FRAMELENGTHMODE': 'sed -i "s/set FRAMELENGTHMODE .*/set FRAMELENGTHMODE {'+FRAMELENGTHMODE+'}/g" '+spirent_cfg_file_path
                        }

        if PS != '':
            command_list['PS'] = 'sed -i "s/set PS .*/set PS {'+PS+'}/g" '+spirent_cfg_file_path
        if FPS != '':
            command_list['FPS'] = 'sed -i "s/set FPS .*/set FPS {'+FPS+'}/g" '+spirent_cfg_file_path
        if NOOFCONNECTIONS != '':
            command_list['NOOFCONNECTIONS'] = 'sed -i "s/set NOOFCONNECTIONS .*/set NOOFCONNECTIONS {'+NOOFCONNECTIONS+'}/g" '+spirent_cfg_file_path
        if FILESIZE != '':
            command_list['FILESIZE'] = 'sed -i "s/set FILESIZE .*/set FILESIZE {'+PS+'}/g" '+spirent_cfg_file_path

        for key in command_list:
            pre_ret3 = commonLib.execCommand(str(command_list[key]))

            if pre_ret3.return_value != '':
                ret = pre_ret3
                ret.return_msg = 'Failed to set '+str(key)+' for UDP traffic VLAN '+str(vlan_id)+': '+pre_ret3.return_msg
                return ret

        ret.return_code = 0
        ret.return_msg = 'Updated hub/remote info successfully'

        return ret

    def coarse_tuning(self, optimized_throughput, spirent_cfg, tuning=500000, threshold_limit=20):
        '''
        The procedure does coarse tuning, finds the optimized threshold and passes on the value for another round of fine tuning
        :param optimized_throughput: Throughput which needs to be optimized
        :param spirent_cfg: Config file with port information
        :param tuning: Change the value by so many Kbps if it fails Eg: 500000
        :param threshold_limit: A failure limit beyond which it is no longer expected to PASS
        :return: Returns the optimized threshold
        '''

        threshold_flag = 0
        while 1:
            response = SpirentVelocityAPI_obj.send_spirent_traffic_cir(
                            spirent_config=str(spirent_cfg),
                            cir=optimized_throughput)

            if response.return_code > 0:
                optimized_throughput -= tuning
            else:
                break

            threshold_flag += 1

            if threshold_flag == threshold_limit:
                optimized_throughput = 0
                break

        return optimized_throughput


    def find_right_throughput(self, throughput, spirent_cfg):
        '''
        Procedure that finds out the optimized throughput after passing through course and fine way of tuning it
        :param throughput: Initial throughput from network
        :param spirent_cfg: Spirent configuration file for traffic
        :return: If return_code = 0, its a PASS else FAIL, return_value contains optimized throughput
        '''
        ret = ReturnValue('find_right_throughput')

        optimized_throughput = throughput*int(self.throughput_expected_threshold)/100

        initial_throughput = optimized_throughput

        chkpt_info('Iteration 1 - Coarse tuning FPS.Small test time','Coarse tuning with FPS variations in steps of 0.5 Mbps with a test time of 30 seconds to find out an approximate throughput')

        #First test the setup with a smaller test time - which is 30 seconds
        commonLib.execCommand('sed -i "s/set TESTTIME .*/set TESTTIME \\"30\\"/g" '+spirent_cfg)

        #This loop below does coarse tuning, where decrements are done in steps of 0.5 Mbps. If it fails it decreases and iterates, if its PASSes it breaks the loop
        optimized_throughput = self.coarse_tuning(optimized_throughput, spirent_cfg)

        if optimized_throughput == 0:
            ret.return_msg = "Failed to get pass throughput threshold even after reducing the throughput by 10 Mbps from the expected throughput: "+str(initial_throughput)
            ret.return_value = 500
            return ret

        optimized_throughput += 100000

        chkpt_info('Iteration 2 - Coarse tuning FPS.Larger test time','Coarse tuning with FPS variations in steps of 0.5 Mbps with a test time of 300 seconds to find out an approximate throughput')

        #Above loop does coarse tuning until it passes, This loop below does fine tuning to check if it still passes - until we fail and break.
        while 1:
            #Now that we found the threshold, now test the setup with a bigger test time - which is 300 seconds or 5 minutes
            commonLib.execCommand('sed -i "s/set TESTTIME .*/set TESTTIME \\"300\\"/g" '+spirent_cfg)
            response = SpirentVelocityAPI_obj.send_spirent_traffic_cir(
                            spirent_config=str(spirent_cfg),
                            cir=optimized_throughput)

            if response.return_code > 0:
                optimized_throughput -= 100000

                #This loop below does fine tuning for larger testtime, where decrements are done in steps of 0.5 Mbps. If it fails it decreases and iterates, if its PASSes it breaks the loop
                optimized_throughput = self.coarse_tuning(optimized_throughput, spirent_cfg, tuning=500000)

                if optimized_throughput == 0:
                    ret.return_msg = "Failed to get pass throughput threshold even after reducing the throughput by 10 Mbps from the expected throughput: "+str(initial_throughput)
                    ret.return_value = 501
                    return ret

                break

            else:
                optimized_throughput += 100000

        chkpt_info('Iteration 3 - Fine tuning FPS.Larger test time','Fine tuning with minute FPS variations in steps of 0.1 Mbps with a test time of 300 seconds to find out an approximate throughput')

        #Fine tuning round 2
        while 1:

            response = SpirentVelocityAPI_obj.send_spirent_traffic_cir(
                            spirent_config=str(spirent_cfg),
                            cir=optimized_throughput)

            if response.return_code > 0:
                optimized_throughput -= 100000

                #This loop below does fine tuning for larger testtime, where decrements are done in steps of 0.1 Mbps. If it fails it decreases and iterates, if its PASSes it breaks the loop
                optimized_throughput = self.coarse_tuning(optimized_throughput, spirent_cfg, tuning=100000)

                if optimized_throughput == 0:
                    ret.return_msg = "Failed to get pass throughput threshold even after reducing the throughput by 2 Mbps from the expected throughput: "+str(initial_throughput)
                    ret.return_value = 501
                    return ret

                break

            else:
                optimized_throughput += 100000

        if optimized_throughput < initial_throughput:
            ret.return_value = optimized_throughput
            ret.return_msg = "Calculated throughput threshold for successful traffic is "+str(float(optimized_throughput)/1000000)+" Mbps which is not inline with the expected throughput "+str(float(initial_throughput)/1000000)+" Mbps ("+str(self.throughput_expected_threshold)+" percent of "+str(float(throughput)/1000000)+")"
            ret.return_code = 500
        else:
            ret.return_value = optimized_throughput
            ret.return_msg = "Calculated throughput threshold for successful traffic is "+str(float(optimized_throughput)/1000000)+" Mbps which is inline with the expected throughput "+str(float(initial_throughput)/1000000)+" Mbps ("+str(self.throughput_expected_threshold)+" percent of "+str(float(throughput)/1000000)+")"
            ret.return_code = 0

        return ret

def main():
    # Initialize logger
    init_logger(module_str='UDPPerformance', chkpt_str='UDPPerformance_chk')

    #User inputs explained
    parser = argparse.ArgumentParser()
    parser.add_argument("network_name", help="Name of the network under test")
    parser.add_argument("terminal_ip", help="For which terminal is traffic being tested")
    parser.add_argument("jumpserver_ip", help="Jumpserver IP where the remote is connected to")
    parser.add_argument("vlan_id", help="Vlan id under test")
    parser.add_argument("site_name", help="Name of the site under test")
    parser.add_argument("spirent_cfg", help="Name of the spirent config file for hub/remote port information")
    parser.add_argument("throughput_expected_threshold", nargs='?', help="Threshold of throughput that is expected to PASS, usually set at 90 percent")

    cl_args = parser.parse_args()
    network_name = cl_args.network_name
    terminal_ip = cl_args.terminal_ip
    vlan_id = cl_args.vlan_id
    site_name = cl_args.site_name
    jumpserver_ip = cl_args.jumpserver_ip
    spirent_cfg = os.environ['STA_PATH']+'/Velocity/config/'+cl_args.spirent_cfg
    throughput_expected_threshold = cl_args.throughput_expected_threshold

    #Collect network information
    network_environment_obj = NetworkEnvironment(network_name)
    network_info = network_environment_obj.getNetworkInfo('obj')
    network_info = network_info.return_value

    traffic_obj = UDPPerformance(network_info, terminal_ip, vlan_id, jumpserver_ip, throughput_expected_threshold)

    chkpt_info('Test criteria and User input information','Test to find out the maximum passing downstream and upstream throughput comparing it with expected throughput. User wants to '\
                                        'test with network:'+str(network_name)+' remote:'+str(terminal_ip)+' vlan:'+str(vlan_id)+' with Spirent port information under '+str(spirent_cfg)+' \
                                         User expects '+str(throughput_expected_threshold)+' percent of the throughput to flow to pass this test')

    response = traffic_obj.findPPWithRemoteIP()

    if response.return_code > 0:
        chkpt_fail('Find PP with Remote info',response.return_msg)
        close_logger()
    else:
        chkpt_pass('Find PP with Remote info',response.return_msg)
        #Overridding PP with new PP IP
        traffic_obj.pp = PP(response.return_value)

    response = traffic_obj.pulse.get_operating_linecard_with_terminal(terminal_ip)

    if response.return_code > 0:
        chkpt_fail('Find RX LC with Remote info',response.return_msg)
        close_logger()
    else:
        chkpt_pass('Find RX LC with Remote info',response.return_msg)
        #Overridding RX LC Info with new RX LC IP
        traffic_obj.lc = LC(response.return_value[0]['rx'])

    #Calculate downstream throughput
    response = traffic_obj.calculate_downstream_throughput()

    if response.return_code > 0:
        chkpt_fail('Calculate downstream throughput',response.return_msg)
        close_logger()
    else:
        chkpt_pass('Calculate downstream throughput',response.return_msg)
        down_throughput = response.return_value

    #Calculate upstream throughput
    response = traffic_obj.calculate_upstream_throughput()

    if response.return_code > 0:
        chkpt_fail('Calculate upstream throughput',response.return_msg)
        close_logger()
    else:
        chkpt_pass('Calculate upstream throughput',response.return_msg)
        up_throughput = response.return_value


    vlan_list = []
    vlan_list.append(str(vlan_id))
    terminal_ip_list = []
    terminal_ip_list.append(terminal_ip)
    #Get hub and remote information automatically via VLAN ID
    spirent_ip_info = GetSpirentVelocityIps(network_name, vlan_list, site_name, spirent_cfg, terminal_ip_list)
    response = spirent_ip_info.get_all_ips(str(vlan_id),return_dict = 'no')

    if response.return_code > 0:
        chkpt_fail('Collect Hub/Remote information',response.return_msg)
        close_logger()
    else:
        chkpt_pass('Collect Hub/Remote information',response.return_msg)
        ip_info = response.return_value[terminal_ip]
        print ip_info

    #Update hub and remote information in tcl configuration file - Downstream
    response = traffic_obj.update_ip_information('UDP', ip_info, vlan_id, "downstream", spirent_cfg, PS='1500', FPS='411')

    if response.return_code > 0:
        chkpt_fail('Update Hub/Remote information in config - downstream',response.return_msg)
        close_logger()
    else:
        chkpt_pass('Update Hub/Remote information in config - downstream',response.return_msg)

    chkpt_info('Find Optimized throughput - Downstream','Iterations start to find optimized downstream throughput')

    #Find out the right throughput for downstream
    response = traffic_obj.find_right_throughput(int(down_throughput)*1000000, spirent_cfg)

    if response.return_code == 501:
        chkpt_fail('Optimized throughput - Downstream',response.return_msg)
    else:
        chkpt_info('Optimized throughput - Downstream',response.return_msg)

    #Update hub and remote information in tcl configuration file - Upstream
    response = traffic_obj.update_ip_information('UDP', ip_info, vlan_id, "upstream", spirent_cfg)

    if response.return_code > 0:
        chkpt_fail('Update Hub/Remote information in config - upstream',response.return_msg)
        close_logger()
    else:
        chkpt_pass('Update Hub/Remote information in config - upstream',response.return_msg)

    chkpt_info('Find Optimized throughput - Upstream','Iterations start to find optimized upstream throughput')

    #Find out thr right throughput for upstream
    response = traffic_obj.find_right_throughput(int(up_throughput)*1000000, spirent_cfg)

    if response.return_code == 501:
        chkpt_fail('Optimized throughput - Upstream',response.return_msg)
    else:
        chkpt_info('Optimized throughput - Upstream',response.return_msg)

    close_logger()

if __name__ == '__main__':
    main()
