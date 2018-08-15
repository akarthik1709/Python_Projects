from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from irobot.libraries.logger import logger
from irobot.libraries.iUtilities import iUtilities
from irobot.libraries.iSpirent import iSpirent

from irobot.libraries.iDirect.iNMS import iNMS
from irobot.libraries.iDirect.iRemote import iRemote
from irobot.libraries.iSSH import iSSH
from irobot.libraries.iSpirent import iSpirent 

import time
import json

class velo_multicast_overlay_steps(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        logger.set_system_library_log(True)

    # Keywords are defined
    def prepare_environment(self):
        # Reading NMS details and conneting to API interface
        self.flag_create_beam = False
        nms_ip = iUtilities().get_variable_from_robot('nms_ip')
        if not nms_ip:
            BuiltIn().fail("\n NMS IP is not provided in the config file \n")

        nms_rest_username, nms_rest_password = iUtilities().get_user_credentials(nms_ip, 'NMS_client')
        iNMS().open_nms_api_session("nms_api_alias", nms_ip, nms_rest_username, nms_rest_password)
        
        #Reading Terminal Details and connecting to SSH and API interface
        self.remote_name = iUtilities().get_variable_from_robot('remote_name')
        proxy_host_ip = iUtilities().get_variable_from_robot('proxy_host_ip')
        self.remote_ip = iNMS().get_remote_properties("nms_api_alias", self.remote_name, "lanip")
        remote_username, remote_password = iUtilities().get_user_credentials(self.remote_ip, "Modem_ssh" )
        remote_rest_username, remote_rest_password = iUtilities().get_user_credentials(self.remote_ip, "Modem_rest")
        proxy_username = iUtilities().get_variable_from_robot('proxy_username') or "root"
        proxy_password = iUtilities().get_variable_from_robot('proxy_password') or "iDirect"
        iRemote().log_into_remote("nms_api_alias", "remote_ssh_alias", self.remote_name, remote_username, remote_password, proxy_host_ip=proxy_host_ip, proxy_username=proxy_username, proxy_password=proxy_password, connect_using_tunnel=True)
        iRemote().open_remote_api_session("nms_api_alias", "remote_rest_alias", self.remote_name, remote_rest_username, remote_rest_password, proxy_host_ip=proxy_host_ip, proxy_username=proxy_username, proxy_password=proxy_password)
        
        self.wide_beam_lat_long = iUtilities().get_variable_from_robot('wide_beam_lat_long')
        self.spot_wide_beam_lat_long = iUtilities().get_variable_from_robot('spot_wide_beam_lat_long')

        #reading network related parameter
        self.msspp_parameters = iUtilities().get_variable_from_robot('msspp_parameters')
        self.sspp_name = iUtilities().get_variable_from_robot('sspp_name')

        self.mgsp_name = "TEST_MGSP_" + str(iUtilities().get_current_epoch_time()) #To make sure name is unique
        self.msspp_name = "TEST_MSSPP_" + str(iUtilities().get_current_epoch_time()) #To make sure name is unique
        self.msspc_name = self.remote_name + "_" + self.msspp_name

        # reading network domain related info
        self.inetprofile = iUtilities().get_variable_from_robot('inetprofile')
        self.inroutegroupprofile = iUtilities().get_variable_from_robot('inroutegroupprofile')

        # reading beam related information
        self.satellite_name = iUtilities().get_variable_from_robot('satellite_name')
        self.beam = iUtilities().get_variable_from_robot('beam')
             
        # reading channel realted information
        self.channel = iUtilities().get_variable_from_robot('channel')
  
        # reading spirent related information and creating connection
        self.spirent=iUtilities().get_variable_from_robot("Spirent")
        stc_ip = iUtilities().get_variable_from_robot("stc_ip")
        stc_slot = iUtilities().get_variable_from_robot("stc_slot")
        stc_hub_port = iUtilities().get_variable_from_robot("stc_hub_port")
        stc_remote_port = iUtilities().get_variable_from_robot("stc_remote_port")

        status = iSpirent().setup_spirent(stc_ip,stc_slot,stc_hub_port,stc_remote_port)
        BuiltIn().should_be_true(status, "Suite Setup Failed - Spirent setup was unsuccessful!")
        self.setup_spirent = True
        # reading output folder 
        self.output_folder = iUtilities().get_variable_from_robot("OUTPUT_DIR")
        self.channel_map = dict()
        logger.console("prepare setup")
    
    def teardown_environment(self):
        if self.setup_spirent: iSpirent().teardown_spirent()
        if self.flag_create_beam:
            #delete channel
            iNMS().delete_component("nms_api_alias", "auto_ds_only_channel" ,"channel")

            #delete inet
            iNMS().delete_component("nms_api_alias", "auto_overlay_inet", "inet")

            #Remove created beam from the inet and inroute group profile
            beam_id_json = dict()
            beam_id_json["obj_id"] = self.inetprofile_obj_id
            beam_id_json["obj_parentid"] = self.inetprofile_obj_parentid
            beam_id_json["beamid_list"] = self.inet_orig_beamid_list
            iNMS().modify_component("nms_api_alias", self.inetprofile, "inetprofile", beam_id_json)
            iNMS().apply_component("nms_api_alias", self.inetprofile, "inetprofile")
            beam_id_json.clear()

            beam_id_json["obj_id"] = self.inroutegroupprofile_obj_id
            beam_id_json["obj_parentid"] = self.inroutegroupprofile_obj_parentid
            beam_id_json["beamid_list"] = self.inroute_orig_beamid_list
            iNMS().modify_component("nms_api_alias", self.inroutegroupprofile, "inroutegroupprofile", beam_id_json)
            iNMS().apply_component("nms_api_alias", self.inroutegroupprofile, "inroutegroupprofile")

            #delete beam
            iNMS().delete_component("nms_api_alias", "auto_wide_beam" ,"beam")

        try:
            #delete msspc
            iNMS().delete_component("nms_api_alias", self.msspc_name ,"sspc")
            iNMS().apply_remote("nms_api_alias", self.remote_name)
        except: pass

        try:
            #delete msspp
            iNMS().delete_component("nms_api_alias", self.msspp_name ,"msspp")
        except: pass
   
        try:
            #delete mgsp
            iNMS().delete_component("nms_api_alias", self.mgsp_name ,"mgsp")
        except: pass

        iNMS().close_nms_api("nms_api_alias")
        iRemote().close_remote_api("remote_rest_alias")
        iRemote().close_remote_shell("remote_ssh_alias")
        logger.console("Suite TearDown Completed!")

    @keyword(name="Verify if channel exists with downstream only property, otherwise create a new beam, inet and channel")
    def create_one_way_inet(self):   
        '''
        This function validate one-way INET.
        It validates the downstream only channel, beam and inet. If these doesn't exist, it creates a new one.
        '''
        self.channel_id_ds = self.is_downstream_only_channel_available()
        if not(self.channel_id_ds):
            self.create_wide_beam()
            self.create_inet()
            self.channel_id_ds = self.create_ds_only_channel()
            time.sleep(240) #maxtimum time for lab network for option push to happen, as if existing action plan is there it takes 120 secs + new one 120 secs
            self.flag_create_beam = True
            logger.info("New Downstream only channel has been created and will be used for this test", also_console = True)
        else:
            logger.info("Existing Downstream only channel is found and will be used for this test", also_console = True)
        if not iUtilities().is_list(self.channel_id_ds):
            self.channel_id_ds=[self.channel_id_ds]
        
        self.channel_map = dict.fromkeys(self.channel_id_ds, dict())
     
    @keyword(name="Validate satellite options file for one way iNet")
    def validate_satellite_option_file(self):
        '''
        This function Validate the one-way INET options file under satellite options file
        '''
        active_optionfile_satellite = iNMS().get_optionfiles("nms_api_alias", self.satellite_name, "satellite")
        self.inet_id = list()
        self.ds_freq_channel = list()
        for channel_options in active_optionfile_satellite[0]["PP_INETS_OPT"]["CHANNEL"]:
            if int(str(channel_options["channel_obj_id"]).strip()) in self.channel_id_ds:#Finding the ds only channel obj_id in satellite options
                if "INBOUND_CHANNEL" in channel_options:
                    BuiltIn().fail("INET is available as 2-way instead of 1-way")                    
                else:
                    self.ds_freq_channel.append(float(str(channel_options["OUTBOUND_CHANNEL"]["gateway_frequency"]).strip()))
                    self.inet_id.append(int(str(channel_options["inet_id"]).strip()))#Getting the inet id from the satellite options where it matches the channel obj_id 
                    self.channel_map[int(str(channel_options["channel_obj_id"]).strip())]=dict()
                    self.channel_map[int(str(channel_options["channel_obj_id"]).strip())][int(str(channel_options["inet_id"]).strip())]="" 
                     
                              
        if len(self.inet_id) == 0:
            BuiltIn().fail("INET ID is not found in channel options")
        else:
            logger.info("One way INET is available in channel options", also_console = True)

    @keyword(name="Validate status report for one way iNet for TX linecard using NMS API")
    def validate_lc_status_report(self):
        '''
        This function Validate the status report of line card assigned to 1-way INET.
        '''
        all_linecard_list = iNMS().get_components("nms_api_alias", "linecard")
        all_tx_lc_id = [lc["obj_id"] for lc in all_linecard_list if lc["obj_attributes"]["model_type"] == "Marconi"]
        all_rx_lc_id = [lc["obj_id"] for lc in all_linecard_list if lc["obj_attributes"]["model_type"] == "Tesla"]
        for rx_lc_id in all_rx_lc_id:
            inet_id_rx = iNMS().get_current_status_by_id("nms_api_alias", rx_lc_id, "lc_net")
            if int(inet_id_rx[0]["value"][-1]) in self.inet_id:
                BuiltIn().fail("No 1-way Inet available in Network")
        
        flagfound = False
        for tx_lc_id in all_tx_lc_id:
            inet_id_tx = iNMS().get_current_status_by_id("nms_api_alias", tx_lc_id, "lc_net")
            for ch in self.channel_map:
                if int(inet_id_tx[0]["value"][-1]) in self.channel_map[ch].keys():
                    self.channel_map[ch][int(inet_id_tx[0]["value"][-1])]=tx_lc_id
                    flagfound = True

        if flagfound:
            logger.info("TX Assigned to INET", also_console = True)            
        else:
           BuiltIn().fail("No LC is assigned to inet")
            

    @keyword(name="Enable Multicast Overlay in Terminal using NMS API")
    def enable_multicat_overlay(self):
        rmt_configuration = iNMS().get_component("nms_api_alias", self.remote_name,"termianl_new")
        if "usemulticastreceiver" in rmt_configuration["obj_attributes"]:
            # If multcast receiver is not enabled, enable it
            if str(rmt_configuration["obj_attributes"]["usemulticastreceiver"]).strip().lower() == "true":
                logger.info("Multicast Reciever is enabled for terminal")
            else:
                remote_json = dict()
                remote_json["obj_id"] = rmt_configuration["obj_id"]
                remote_json["obj_parentid"] = rmt_configuration["obj_parentid"]
                remote_json["usemulticastreceiver"] = "true"
                iNMS().modify_component("nms_api_alias", self.remote_name, "termianl_new", remote_json)
                

            # If mobile type is not fixed, set it to fixed
            terminal_type = iNMS().get_component_by_id("nms_api_alias", rmt_configuration["obj_attributes"]["terminaltype_id"], "terminaltype" )
            if terminal_type["obj_attributes"]["mobilitytype"] != "Fixed":
                terminal_type_json = dict()
                terminal_type_json["obj_id"] = terminal_type["obj_id"]
                terminal_type_json["obj_parentid"] = terminal_type["obj_parentid"]
                terminal_type_json["mobilitytype"] = "Fixed"
                iNMS().modify_component_by_id("nms_api_alias", rmt_configuration["obj_attributes"]["terminaltype_id"], "terminaltype", terminal_type_json)
                iNMS().apply_component_by_id("nms_api_alias", rmt_configuration["obj_attributes"]["terminaltype_id"], "terminaltype")

            #Modifying the geolocation to keep terminal in wide beam

            query_geolocation = iNMS().get_components("nms_api_alias", "nmsquery", query="obj_type=413")
            self.obj_id_geolocation = iUtilities().get_values_from_listdictionary(query_geolocation, True, False, "obj_id", obj_parentid=rmt_configuration["obj_id"])
            self.terminal_geo_location = iNMS().get_component_by_id("nms_api_alias", self.obj_id_geolocation["obj_id"], "geolocation")
            geolocation_json = dict()
            geolocation_json["obj_parentid"] = self.terminal_geo_location["obj_parentid"]
            geolocation_json["obj_id"] = self.terminal_geo_location["obj_id"]
            geolocation_json["latdegrees"] = self.wide_beam_lat_long[0]
            geolocation_json["longdegrees"] = self.wide_beam_lat_long[1]
            iNMS().modify_component_by_id("nms_api_alias", self.obj_id_geolocation["obj_id"], "geolocation", geolocation_json)
            iNMS().apply_component("nms_api_alias", self.remote_name, "termianl_new")
            logger.info("Multicast Overlay is enabled in NMS WUI for Terminal", also_console=True)   
        else:
            BuiltIn().fail("Multicast reciever Key is not present in NMS")
        
    @keyword(name="Copy falcon.json from NMS in Terminal and restart falcon")
    def copy_falcon(self):
        active_optionfile_terminal = iNMS().get_optionfiles("nms_api_alias", self.remote_name, "termianl_new")
        falcon_json = json.dumps(active_optionfile_terminal[0]["TERMINAL_OPT"],sort_keys=True, indent=4, separators=(',', ': '))        
        outputfalconfile = self.output_folder + "/falcon.json"
        iUtilities().write_to_json_file(falcon_json, outputfalconfile)
        iSSH().send_file_via_scp("remote_ssh_alias", outputfalconfile, "/sysopt/config/sat_router/")
        iRemote().restart_application("remote_ssh_alias")
        time.sleep(30) #Time to sleep for terminal to initaite the connection
        if iRemote().login_to_application("remote_ssh_alias"):
            logger.info("Terminal falcon restarted successfully", also_console=True)
            time.sleep(120) #Time to sleep for terminal to start falcon and come in network
        else:
            BuiltIn().fail("Falcon restart of Terminal is not successful")

    @keyword(name="Validate Remotestate in Terminal API as ${remote_state} for ${reciever_type} receiver")
    def check_remote_state(self, remote_state, reciever_type):
        remote_state = remote_state.replace('"','').strip()
        rx_output = iRemote().get_properties("remote_rest_alias", "rx")
        if reciever_type == "primary":
            terminal_rx_info = iUtilities().get_values_from_listdictionary(rx_output, True, True, "id", "state", "if_frequency", beam_type="PRIMARY")
        else:
            terminal_rx_info = iUtilities().get_values_from_listdictionary(rx_output, True, True, "id", "state", "if_frequency", beam_type="RECEIVE-ONLY")

        logger.info("RX ID of " + str(reciever_type) + " reciever : " + str(terminal_rx_info["id"][0]), also_console= True)
        if str(terminal_rx_info["state"][0]).lower() == remote_state.lower():
            if remote_state.lower() == "locked":
                inet_freq_terminal = (float(terminal_rx_info["if_frequency"][0]/1000.0))  #Converting frequency from MHZ to GHz
                if (inet_freq_terminal in self.ds_freq_channel and reciever_type == "primary") or (inet_freq_terminal not in self.ds_freq_channel and reciever_type == "secondary"):                    
                    BuiltIn().fail(str(reciever_type) + " receiver of terminal is locked to 1-way INET in the unexpected frequency")
                logger.info("Terminal is locked to " + str(reciever_type) + " receicer of frequency : " + str(inet_freq_terminal) + " GHz", also_console=True)
            else:
                logger.info("Terminal is not locked to 2-way INET as expected", also_console=True)
        else:
            BuiltIn().fail("Terminal is in " +str(remote_state) + " state. which is not expected")
    

    @keyword(name="Create MSSPP with persistent enabled using NMS API")
    def create_msspp(self):
        logger.warn("Modifying MSSPP does not show the saved regional-beam scope configuration-PULSE-14903")
        self.msspp_parameters['mgsp'].update({
            'obj_name' : self.mgsp_name,
            'cost' : "0.1",
            'priority' : "1",
            'scope' : "Global",
        })
        
        self.msspp_parameters.update({
            'fap': {
                'direction' : "Aggregate"
            }
        })
        self.msspp_parameters['msspp'].update({
            'obj_name' : self.msspp_name,
        })
        self.msspp_parameters['geoscopeqos'].update({
            'dn_cost' : "0.1",
            'dn_priority' : "1"
        })
        self.msspp_id= iNMS().create_msspp("nms_api_alias", self.remote_name , \
                                                     self.msspp_parameters['mgsp'], \
                                                     self.msspp_parameters['fap'], \
                                                     self.msspp_parameters['msspp'], \
                                                     self.msspp_parameters['multicast_group_address'], \
                                                     self.msspp_parameters['geoscopeqos'])

    @keyword(name="Validate events for multicast group created using NMS API")
    def multicast_events(self):
        multicast_events, _, _ = iNMS().get_current_events("nms_api_alias", time_interval=3600)
        is_event_occured = False
        for events in multicast_events:
            if events["condition_type"] == "MULTICAST_GROUP_CREATED":
                if "multicast_group_address" in events["parameters"] and self.msspp_parameters["multicast_group_address"]["dest_ipaddr"] in events["parameters"]:
                    logger.info("Events get generated for multicast address: " + str(self.msspp_parameters["multicast_group_address"]["dest_ipaddr"]), also_console=True)
                    is_event_occured = True
                    break
        if not is_event_occured:
            BuiltIn().fail("Events do not get created as 'MULTICAST_GROUP_CREATED' for multicast group address")


    @keyword(name="Associate MSSPP to Terminal using NMS API")
    def map_msspp_to_terminal(self):
        sspc_params = {
            "remote_name": self.remote_name,
            "obj_name": self.msspc_name
        }
        iNMS().create_msspc("nms_api_alias", self.msspp_id, sspc_params)

    @keyword(name="Config and Run persistent multicast traffic using Spirent")
    def run_mcast_traffic(self):
        mcast_status=  iSpirent().config_run_multicast_traffic(**self.spirent)
        BuiltIn().should_be_true(mcast_status, "Test failed - Spirent validation of Persistent MCAST traffic is failed")

    @keyword(name="Validate multicast remote Rx traffic stats from NMS API for MSSPP against Spirent's TX stats")
    def validate_traffic_results(self):
        logger.warn("Multicast SSPP is not present under elements to retrieve the stats for multicast DATA-PULSE-12957")

        multicast_sspp_bytes= iNMS().get_current_stats_by_id('nms_api_alias',  str(self.msspp_id), "multicast_sspp_bytes")
        
        #calculate stats in real Ip data rate 22 bytes is ethernet overhead,2 bytes is SVN overhead,30 is resolution.
        spirent_tx_rate = round(float((((int(self.spirent["str_frame_size"]) - 22) + 2) * int(self.spirent["str_fps"]) * 30)))

        if spirent_tx_rate == multicast_sspp_bytes:
            logger.info("Spirent TX and Remote RX stats are equal!",also_console=True)
        else:
            BuiltIn().fail("Stats validation fails!")

    @keyword(name='Validate Remotestate in events using NMS API as "In Network" for primary receiver')    
    def term_primary_remotestate(self):
        spotbeam_geolocation_json = dict()
        spotbeam_geolocation_json["obj_parentid"] = self.terminal_geo_location["obj_parentid"]
        spotbeam_geolocation_json["obj_id"] = self.terminal_geo_location["obj_id"]
        spotbeam_geolocation_json["latdegrees"] = self.spot_wide_beam_lat_long[0]
        spotbeam_geolocation_json["longdegrees"] = self.spot_wide_beam_lat_long[1]
        iNMS().modify_component_by_id("nms_api_alias", self.obj_id_geolocation["obj_id"], "geolocation", spotbeam_geolocation_json)
        iNMS().apply_component("nms_api_alias", self.remote_name, "termianl_new")
        self.copy_falcon()
        self.check_remote_state(remote_state="Locked", reciever_type="secondary")
        time.sleep(30)#Status page to get updated in terminal
        remote_online_status = iNMS().get_current_status("nms_api_alias", self.remote_name,"remote", "term_state" )
        if (int(remote_online_status[0]["value"][-1])) == 1:
            logger.info("Terminal is network for primary Receiver", also_console=True)
        else:
            BuiltIn().fail("Terminal is not in network")

    @keyword(name="Config and Run Simultaneous Bi-directional unicast and dynamic multicast Traffic")
    def run_simultaneous_traffic(self):
        iSpirent().config_run_simultaneous_traffic(**self.spirent)

    @keyword(name="Validate unicast traffic from NMS API under SSPP stats")
    def sspp_stats_ucast(self):
        #sspc stats throughput from NMS and converting that in mbps
        us_sspc_stats = iNMS().get_current_stats("nms_api_alias", self.remote_name + " : " + self.sspp_name , "sspc" ,"sspc_us_allocated_bw_bytes")
        us_throughput_nms_udp = round(float(((int(us_sspc_stats[-1])*8)/30)/1000000.0),2)      

        ds_sspc_stats = iNMS().get_current_stats("nms_api_alias", self.remote_name + " : " + self.sspp_name , "sspc", "sspc_ds_allocated_bw_bytes")
        ds_throughput_nms_udp = round(float(((int(ds_sspc_stats[-1])*8)/30)/1000000.0),2)

        #calculating the throughput from spirent traffic being sent
        ds_throughput_spirent_udp = round(float(((self.spirent["str_frame_size"] - 22)  * self.spirent["str_fps"] * 8)/1000000.0),2)
        us_throughput_spirent_udp = round(float(((self.spirent["str_frame_size"] - 22)  * self.spirent["str_fps"] * 8)/1000000.0),2)

        #percentage difference between traffic sent and received from NMS API.
        ds_loss_percentage = float(abs(ds_throughput_nms_udp - ds_throughput_spirent_udp))/float(max(ds_throughput_nms_udp,ds_throughput_spirent_udp))*100
        us_loss_percentage = float(abs(us_throughput_nms_udp - us_throughput_spirent_udp))/float(max(us_throughput_nms_udp,us_throughput_spirent_udp))*100

        if (ds_loss_percentage and us_loss_percentage) <= 1:
            logger.info("There is no loss in traffic", also_console= True)
        else:
            BuiltIn().fail("There is a loss of trafic in DS by : " + str(us_loss_percentage) + " and of US by : " + str(us_loss_percentage))
        time.sleep(2)

    # Supportive functions are below
    def is_downstream_only_channel_available(self):
        '''
        Validates whether downstream channel is present in the network
        '''
        channel_details = iNMS().get_components("nms_api_alias", "channel")
        channel_obj_id = iUtilities().get_values_from_listdictionary(channel_details, True, True, "obj_id", isoutboundonly="true", state="Up")
        if channel_obj_id and channel_obj_id["obj_id"] != []:
            return channel_obj_id["obj_id"]
        else:
            return False            
  
    def create_wide_beam(self):
        '''
        Creates wide beam or overlay beam in the network
        '''   
        self.sat_id = iNMS().get_component("nms_api_alias", self.satellite_name, "satellite")
        beam_json = dict()
        beam_json["obj_parentid"] = self.sat_id["obj_id"] 
        beam_json["obj_name"] = "auto_wide_beam"
        beam_json["beam_index"] = self.beam["beam_index"]

        if self.beam["beam_type"] == "Circular":
            beam_json["azimuth"] = self.beam["azimuth"]
            beam_json["elevation"] = self.beam["elevation"]
            beam_json["radius"] = self.beam["radius"]
            beam_json["beam_type"] = "Circular"   
        else:
            beam_json["beam_type"] = "Non-Circular"
            beam_json["beamcontour"] = self.beam["beamcontour"]

        iNMS().create_component("nms_api_alias", 'beam', beam_json)
        iNMS().apply_component("nms_api_alias", "auto_wide_beam", "beam")
        self.wide_beam_obj_id = iNMS().get_id("nms_api_alias", "auto_wide_beam", "beam")
        if self.wide_beam_obj_id:
            self.associate_beam_inet_inroute() #to add the created beams under inet and inroutegroupprofile
        else:
            BuiltIn().fail("Beam Creations fail")

    def associate_beam_inet_inroute(self):
        '''
        This function adds the created wide beam or overlay beam in the inetprofile and inroutgroupprofile
        '''      
        beam_id_json = dict()        
        
        inroutegroupprofile = iNMS().get_component("nms_api_alias", self.inroutegroupprofile, "inroutegroupprofile")
        self.inroute_orig_beamid_list = inroutegroupprofile["obj_attributes"]["beamid_list"]
        self.inroutegroupprofile_obj_id = inroutegroupprofile["obj_id"]
        self.inroutegroupprofile_obj_parentid = inroutegroupprofile["obj_parentid"]
        beam_id_json["obj_id"]= self.inroutegroupprofile_obj_id
        beam_id_json["obj_parentid"]= self.inroutegroupprofile_obj_parentid
        beam_id_json["beamid_list"]=str(self.inroute_orig_beamid_list).replace('}', ',' + str(self.wide_beam_obj_id).strip() + '}')
        iNMS().modify_component("nms_api_alias", self.inroutegroupprofile, "inroutegroupprofile", beam_id_json)
        iNMS().apply_component("nms_api_alias", self.inroutegroupprofile, "inroutegroupprofile")        
        beam_id_json.clear()

        inetprofile = iNMS().get_component("nms_api_alias", self.inetprofile, "inetprofile")
        self.inet_orig_beamid_list = inetprofile["obj_attributes"]["beamid_list"]
        self.inetprofile_obj_id = inetprofile["obj_id"]
        self.inetprofile_obj_parentid = inetprofile["obj_parentid"]
        beam_id_json["obj_id"]= self.inetprofile_obj_id
        beam_id_json["obj_parentid"]=self.inetprofile_obj_parentid
        beam_id_json["beamid_list"]=str(self.inet_orig_beamid_list).replace('}', ',' + str(self.wide_beam_obj_id).strip() + '}')
        iNMS().modify_component("nms_api_alias", self.inetprofile, "inetprofile", beam_id_json)
        iNMS().apply_component("nms_api_alias", self.inetprofile, "inetprofile")

    
    def create_inet(self):
        '''
        Creates an inet for wide beam or overlay beam in the network
        '''  
        inet_json = dict()
        inet_json["obj_parentid"] = self.wide_beam_obj_id           
        inet_json["obj_name"] = "auto_overlay_inet"
        inet_json["channelindex"] = 1
        
        iNMS().create_component("nms_api_alias", 'inet', inet_json)
        iNMS().apply_component("nms_api_alias", "auto_overlay_inet", "inet")
        inet_for_wide_beam_obj_id = iNMS().get_id("nms_api_alias", "auto_overlay_inet", "inet")
        return inet_for_wide_beam_obj_id
    
    def create_ds_only_channel(self):
        '''
        Creates downstream only channel for 1-way iNet in the network
        ''' 

        channel_json = dict()
        channel_json["obj_parentid"] = self.sat_id["obj_parentid"]
        channel_json["priority"] = 1
        channel_json["obj_name"] = "auto_ds_only_channel"
        channel_json["fwdpsdlimit"] = 100
        channel_json["channelindex"] = 1
        channel_json["state"] = "Up"
        channel_json["fwduserpolarization"] = self.channel["fwduserpolarization"]
        channel_json["fwdtwta_id"] = 1
        channel_json["beam_id"] = self.wide_beam_obj_id
        channel_json["fwdbandwidth"] = self.channel["fwd_bandwidth"]
        channel_json["channel_id"] = 15
        channel_json["isoutboundonly"] = "true"
        channel_json["pairedchannel"] = 1
        channel_json["fwduserfrequency"] = self.channel["user_frequency"]
        channel_json["fwdgatewaypolarization"] = self.channel["fwdgatewaypolarization"]
        channel_json["fwdgatewayfrequency"] = self.channel["gateway_frequency"]
        channel_json["fwdbackoff"] = 1

        iNMS().create_component("nms_api_alias", "channel", channel_json)
        iNMS().apply_component("nms_api_alias", "auto_ds_only_channel", "channel")
        iNMS().apply_component("nms_api_alias", self.satellite_name, "satellite")
        ds_only_channel = iNMS().get_id("nms_api_alias", "auto_ds_only_channel", "channel")
        return ds_only_channel

    # To be implemented
    @keyword(name="Start OpenAMIP to terminal to travel across ${polarization_type} beams")
    def start_open_amip(self, polarization_type):
        logger.warn("Start OpenAMIP to terminal to travel across " + polarization_type + " beams - Yet to implement")
    
    @keyword(name="Configure and Run background persistent multicast traffic using Spirent")
    def run_background_mcast_traffic(self):
        logger.warn("Configure and Run background persistent multicast traffic using Spirent - Yet to implement")   
    
    @keyword(name='Validate Remotestate in events using NMS API as "In Network" for primary receiver in spot beam')
    def term_primary_remotestate_spot(self):
        logger.warn('Validate Remotestate in events using NMS API as "In Network" for primary receiver in spot beam - yet to implement') 
    
    @keyword(name="Configure and Run background unicast traffic using Spirent")
    def run_background_ucast_traffic(self):
        logger.warn("Configure and Run background unicast traffic using Spirent - Yet to implement")  
    
    @keyword(name="Validate spot Beam switch using NMS API events")
    def beam_switch_events(self):
        logger.warn("Validate spot Beam switch using NMS API events - Yet to implement") 

    @keyword(name="Validate Overlay Beam switch using Terminal API events")
    def overlay_beam_switch_events(self):
        logger.warn("Validate Overlay Beam switch using Terminal API events - Yet to implement") 
    
    @keyword(name="Stop all the traffic and validate the loss in Traffic")
    def stop_all_traffic(self):
        logger.warn("Stop all the traffic and validate the loss in Traffic - Yet to implement")  
