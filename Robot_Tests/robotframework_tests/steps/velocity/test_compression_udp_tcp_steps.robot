*** Settings ***
Library      irobot.libraries.iSpirent  WITH NAME  iSpirent
Library      irobot.libraries.iSpirent._stcapi  WITH NAME  _stcapi
Library      irobot.libraries.iDirect.iNMS  WITH NAME  iNMS
Library      irobot.libraries.iDirect.iRemote  WITH NAME  iRemote
Library      irobot.libraries.iDirect.iPP  WITH NAME  iPP
Library      irobot.libraries.iSSH  WITH NAME  iSSH
Library      irobot.libraries.iUtilities  WITH NAME  iUtilities 


*** Keywords ***
Enable Compression and Validate
	Compress Traffic Depending on Type
	Validate Compression is enabled

Run Traffic and Find Compression Efficiency
	Run Traffic Depending on Type
	Find Compression Efficiency Depending on Type
	Stop Traffic Depending on Type

Set Test Requirement
	Log to console  \n Setting up test for Velocity ${Traffic_type} Compression\n
	Set Suite Variable  ${Traffic_type}  ${Traffic.Traffic_type}	
	log to console  Traffic Type=${Traffic_type}
	log to console  Traffic Direction=${Traffic.DIR}
	Set Suite Variable  ${iPlatform}  Velocity
    Set Suite Variable  ${NMS_Rest_Alias}  MyNMSAPI
    iNMS.Open NMS Api Session  ${NMS_Rest_Alias}  ${NMS.ip}  ${NMS.RestUserName}  ${NMS.RestPassword}
    log to console  NMS Rest Alias is MyNMSAPI

    Set Suite Variable  ${Remote_Rest_Alias}  MyRemoteAPI
    iRemote.Open Remote Api Session  ${NMS_Rest_Alias}  Remote_Rest_Alias  ${Remote.Name}  ${Remote.API.Username}  ${Remote.API.Password}  
	...  proxy_host_ip=${ProxyServer.ip}  
	Log to console  Created Remote API Session -> Remote_Rest_Alias
    ${remote_DID}=  iRemote.Get DID  Remote_Rest_Alias
	Set Suite Variable  ${remote_DID}
	Log to console  Remote DID -> ${remote_DID}

Compress Traffic Depending on Type
    Run Keyword if  '''TCP''' in '''${Traffic_type}''' or '''BOTH''' in '''${Traffic_type}'''
	...   iNMS.set mode tcp compression  ${NMS_Rest_Alias}  ${Remote.Name}  ${Remote.svn_id}  portrange=10-50000
	Run Keyword if  '''UDP''' in '''${Traffic_type}''' or '''BOTH''' in '''${Traffic_type}'''
	...   iNMS.set mode udp compression  ${NMS_Rest_Alias}  ${Remote.Name}  ${Remote.svn_id}  portrange=10-50000

Validate Compression is enabled
	Run Keyword if  '''TCP''' in '''${Traffic_type}''' or '''BOTH''' in '''${Traffic_type}'''
	...   Validate TCP Compression
	Run Keyword if  '''UDP''' in '''${Traffic_type}''' or '''BOTH''' in '''${Traffic_type}'''
	...   Validate UDP Compression	

Validate TCP Compression
	iRemote.Log in to Remote  ${NMS_Rest_Alias}  Test1  ${Remote.Name}  proxy_host_ip=${ProxyServer.ip}  proxy_username=${ProxyServer.UserName}
	Sleep  40s
	${TCP_UP}=  iRemote.execute application command  Test1  ${Command.tcp_upstream}
	log to console  ${TCP_UP}
	${result}=  Run Keyword if  '''hdr_compression_on: 1''' in '''${TCP_UP}'''
	...     Set Variable  ${True}
    ...     ELSE
    ...     Set Variable  ${False}
	Should Be True  ${result}  TCP COMPRESSION NOT ENABLED
	log to console  TCP COMPRESSION ENABLED

	iPP.log into pp  Test2  ${PP.ip}
	${login_pp_tpa}=  iPP.log into pp_process  Test2  process_name=pp_tpa
	${entire_val0}=  iSSH.execute_command  Test2  rmt ${remote_DID}
	${entire_val}=  iSSH.execute_command  Test2  ${Command.tcp_pp_val}
	log to console  ${entire_val}

Validate UDP Compression
	iRemote.Log in to Remote  ${NMS_Rest_Alias}  Test1  ${Remote.Name}  proxy_host_ip=${ProxyServer.ip}  proxy_username=${ProxyServer.UserName}
	Sleep  40s
	log to console  ${Command.udp_upstream}
	${UDP_UP}=  iRemote.execute application command  Test1  ${Command.udp_upstream}
	log to console  ${UDP_UP}
	${result}=  Run Keyword if  '''hdr_comp.compression_method = 1''' in '''${UDP_UP}'''
	...     Set Variable  ${True}  
    ...     ELSE
    ...     Set Variable  ${False}
	Should Be True  ${result}  UDP COMPRESSION NOT ENABLED
	log to console  UDP COMPRESSION ENABLED

	iPP.log into pp  Test2  ${PP.ip}
	${login_pp_tpa}=  iPP.log into pp_process  Test2  process_name=pp_tpa
	${entire_val0}=  iSSH.execute_command  Test2  rmt ${remote_DID}
	${entire_val}=  iSSH.execute_command  Test2  ${Command.udp_pp_val}
	log to console  ${entire_val}

UDP Compression Efficiency
    Run Keyword if  '''UPSTREAM''' in '''${Traffic.DIR}''' or '''BIDIRECTIONAL''' in '''${Traffic.DIR}'''
	...	   UDP Compression Efficiency Upstream 
	Run Keyword if  '''DOWNSTREAM''' in '''${Traffic.DIR}''' or '''BIDIRECTIONAL''' in '''${Traffic.DIR}'''
	...	   UDP Compression Efficiency Downstream

UDP Compression Efficiency Upstream
	iPP.log into pp  Test2  ${PP.ip}  proxy_host_ip=${ProxyServer.ip}  proxy_username=${ProxyServer.UserName}
	${login_pp_tpa}=  iPP.log into pp_process  Test2  process_name=pp_tpa
	${entire_val0}=  iSSH.execute_command  Test2  rmt ${remote_DID}
	${entire_val}=  iSSH.execute_command  Test2  ${Command.udp_upstream_eff}
	log to console  ${entire_val}
	${UDP_compressed}=  iUtilities.find_value_from_output  ${entire_val}  UDP compressed:  delimiter=:
	log to console  UDP_compressed=${UDP_compressed}  
	${Total RX UDP}=  iUtilities.find_value_from_output  ${entire_val}  Total RX UDP:  delimiter=:
	log to console  Total RX UDP=${Total RX UDP}
	${result}=  Run Keyword if  ${Total RX UDP} is 0
    ...     Set Variable  ${False}
    ...     ELSE
    ...     Set Variable  ${True}
	log to console  ${result}  
    Should Be True  ${result}  TOTAL RX UDP CANNOT BE ZERO FOR CALCULATING COMPRESSION EFFICIENCY
	${Compression_Efficiency}=  Evaluate  (float(float(${UDP_compressed})/float(${Total RX UDP})))*100
	log to console  UDP Upstream Compression_Efficiency=${Compression_Efficiency}

UDP Compression Efficiency Downstream
	iPP.log into pp  Test2  ${PP.ip}  proxy_host_ip=${ProxyServer.ip}  proxy_username=${ProxyServer.UserName}
	${login_pp_tpa}=  iPP.log into pp_process  Test2  process_name=pp_tpa
	${entire_val0}=  iSSH.execute_command  Test2  rmt ${remote_DID}
	${entire_val1}=  iSSH.execute_command  Test2  ${Command.udp_downstream_eff}
	${UDP_compressed1}=  iUtilities.find_value_from_output  ${entire_val1}  UDP compressed:  delimiter=:
	log to console  UDP_compressed=${UDP_compressed1}  
	${Total TX UDP}=  iUtilities.find_value_from_output  ${entire_val1}  Total TX UDP:  delimiter=:
	log to console  Total TX UDP=${Total TX UDP}
	${result1}=  Run Keyword if  ${Total TX UDP} is 0
    ...     Set Variable  ${False}
    ...     ELSE
    ...     Set Variable  ${True}
	log to console  ${result1}
    Should Be True  ${result1}  TOTAL TX UDP CANNOT BE ZERO FOR CALCULATING COMPRESSION EFFICIENCY 
	${Compression_Efficiency}=  Evaluate  (float(${UDP_compressed1})/float(${Total TX UDP}))*100
	log to console  UDP Downstream Compression_Efficiency=${Compression_Efficiency}   
   
Find Compression Efficiency Depending on Type
	Run Keyword if  '''TCP''' in '''${Traffic_type}''' or '''BOTH''' in '''${Traffic_type}'''
	...	   TCP Compression Efficiency
	Run Keyword if  '''UDP''' in '''${Traffic_type}''' or '''BOTH''' in '''${Traffic_type}'''
	...	   UDP Compression Efficiency

TCP Compression Efficiency
    Run Keyword if  '''UPSTREAM''' in '''${Traffic.DIR}''' or '''BIDIRECTIONAL''' in '''${Traffic.DIR}'''
	...	   TCP Compression Efficiency Upstream 

TCP Compression Efficiency Upstream
	iRemote.Log in to Remote  ${NMS_Rest_Alias}  Test1  ${Remote.Name}  proxy_host_ip=${ProxyServer.ip}  proxy_username=${ProxyServer.UserName}
	${TCP_UP_STATS_HDR}=  iRemote.execute application command  Test1  ${Command.tcp_up_stats}  tx_full_hdr_packets
	${num_comp_hdr_bytes_reduced}=  iUtilities.find_value_from_output  ${TCP_UP_STATS_HDR}  num_comp_hdr_bytes_reduced  delimiter==
	log to console  Total bytes compressed=${num_comp_hdr_bytes_reduced}
	${TCP_UP_STATS_TOTAL}=  iRemote.execute application command  Test1  ${Command.tcp_up_stat_total_bytes}  
	${num_tcp_bytes_temp}=  iUtilities.Fetch From Right  ${TCP_UP_STATS_TOTAL}  =
	${num_tcp_bytes}=  iUtilities.Fetch From Left  ${num_tcp_bytes_temp}  [
	log to console  Total bytes=${num_tcp_bytes}
	${result}=  Run Keyword if  ${num_tcp_bytes.strip()} is 0
    	...     Set Variable  ${False}
    	...     ELSE
    	...     Set Variable  ${True}
	log to console  ${result}
    	Should Be True  ${result}  TOTAL BYTES CANNOT BE ZERO FOR CALCULATING COMPRESSION EFFICIENCY
	${Compression_Efficiency}=  Evaluate  (float(${num_tcp_bytes})-float(${num_comp_hdr_bytes_reduced}))/float(${num_tcp_bytes})*100
	log to console  TCP Upstream Compression Efficiency=${Compression_Efficiency} 

	
Run Traffic Depending on Type
	${spirent_status}=  iSpirent.Setup Spirent  ${stc_ip}  ${stc_slot}  ${stc_hub_port}  ${stc_remote_port}
    Should be True  ${spirent_status}
	Run Keyword if  '''TCP''' in '''${Traffic_type}''' or '''BOTH''' in '''${Traffic_type}'''
	...   Run TCP Traffic
	Run Keyword if  '''UDP''' in '''${Traffic_type}''' or '''BOTH''' in '''${Traffic_type}'''
	...   Run UDP Traffic

Run TCP Traffic
	${stream}  ${tmp_var1}  ${tmp_var2}  ${tmp_var3}  ${tmp_var4}=  iSpirent.Config TCP Traffic  &{Spirent}
	log to console  ${stream}
	iSpirent.start traffic  ${stream}
	Set Suite Variable  ${stream_block}  ${stream}

Run UDP Traffic
	${stream}  ${handlers}=  iSpirent.Config UDP Traffic  &{Spirent}
	log to console  ${stream}
	iSpirent.start traffic  ${stream}
	Set Suite Variable  ${stream_block}  ${stream}

Stop Traffic Depending on Type
	iSpirent.stop traffic  ${stream_block}

Remove Compression Depending on Type
	Run Keyword if  '''TCP''' in '''${Traffic_type}''' or '''BOTH''' in '''${Traffic_type}'''
	...   iNMS.set mode tcp compression  ${NMS_Rest_Alias}  ${Remote.Name}  ${Remote.svn_id}  mode=disable
	Run Keyword if  '''UDP''' in '''${Traffic_type}''' or '''BOTH''' in '''${Traffic_type}'''
	...   iNMS.set mode udp compression  ${NMS_Rest_Alias}  ${Remote.Name}  ${Remote.svn_id}  mode=disable
    Sleep  60s

Teardown Environment
	Remove Compression Depending on Type
	iSpirent.teardown spirent
    log to console  closing all open ssh sessions
    iSSH.Close all ssh session
    log to console  closed all ssh sessions
    