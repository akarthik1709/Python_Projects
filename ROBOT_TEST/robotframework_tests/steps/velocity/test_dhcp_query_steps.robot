*** Settings ***
Library     irobot.libraries.iUtilities  WITH NAME  iUtilities
Library     irobot.libraries.iDirect.iNMS  WITH NAME  iNMS
Library     irobot.libraries.iDirect.iRemote  WITH NAME  iRemote
Library     irobot.libraries.iSpirent  WITH NAME  iSpirent
Library     irobot.libraries.iIPAddress  WITH NAME  iIPAddress

*** Variable***
${iPlatform}=  velocity
${nms_ip}=  ${NMS.IP}
${remote_name}=  ${DHCP.Remote}
${start_ip}=  ${DHCP.Start_IP}
${end_ip}=  ${DHCP.End_IP}
${device_count}=  ${DHCP.device_count}
${DHCP_Flag}=  0
${Reserve_Flag}=  0
${Bind_Flag}=  0
${dhcp_relay_ip}=  ${dhcp_relay.relaytov4}

*** Keywords ***
Prepare Setup Environment
    # Get the vlan id from the Spirent details , to set vlan id for the remote
    Log to console  hub_host_vlan_id-${Spirent.hub_host_vlan_id}
    Run Keyword if  '${Spirent.hub_host_vlan_id}' == ''
    ...     Set Suite Variable  ${vlan_id}  1
    ...     ELSE
    ...     Set Suite Variable  ${vlan_id}  ${Spirent.hub_host_vlan_id}
    Log to console  vlan is -${vlan_id}

    # login to nms as root using ssh
    ${NMS_SSH_Alias}=  Set Variable  nmslog
    ${credentials}=  iUtilities.Get Credentials  ${nms_ip}  NMS_ssh
    ${NMSUserName}=  Get Dictionary Keys  ${credentials}
    ${NMSUserName}=  Set Variable  @{NMSUserName}[0]
    ${NMSPassword}=  Set Variable  &{credentials}[${NMSUserName}]

    ${credentials}=  iUtilities.Get Credentials  ${nms_ip}  NMS_su
    ${NMSSUUsername}=  Get Dictionary Keys  ${credentials}
    ${NMSSUUsername}=  Set Variable  @{NMSSUUsername}[0]
    ${NMSSUPassword}=  Set Variable  &{credentials}[${NMSSUUsername}]

    iNMS.Log in to NMS  ${NMS_SSH_Alias}  ${nms_ip}  ${NMSUserName}  ${NMSPassword}  ${NMSSUPassword}
    Set Suite Variable  ${NMS_SSH_Alias}

    # login to nms as admin using REST api
    ${credentials}=  iUtilities.Get Credentials  ${nms_ip}  NMS_client
    ${NMSRestUserName}=  Get Dictionary Keys  ${credentials}
    ${NMSRestUserName}=  Set Variable  @{NMSRestUserName}[0]
    ${NMSRestPassword}=  Set Variable  &{credentials}[${NMSRestUserName}]

    ${NMSAPI_Alias}=  Set Variable  rest_log
    iNMS.Open NMS API Session  ${NMSAPI_Alias}  ${nms_ip}  ${NMSRestUserName}  ${NMSRestPassword}
    Set Suite Variable  ${NMSAPI_Alias}
    Run Keyword  Get Remote IP
    Run Keyword  Validate Remote LAN IP  True

    # Get Remote Application credentials
    ${remote_App_credentials}=  iUtilities.Get Credentials  ${remote_ip}  Modem_app
    Log to console  remt-${remote_App_credentials}
    ${RMTAppUserName}=  Get Dictionary Keys  ${remote_App_credentials}
    ${RMTAppUserName}=  Set Variable  @{RMTAppUserName}[0]
    ${RMTAppPassword}=  Set Variable  &{remote_App_credentials}[${RMTAppUserName}]
    Log to console  remote_App_credentials-${RMTAppUserName},${RMTAppPassword}
    iRemote.Open Remote Api Session  ${NMSAPI_Alias}  rmt_api_session  ${remote_name}  ${RMTAppUserName}  ${RMTAppPassword}
    ${RMTAPI_Alias}=  Set Variable  rmt_api_session
    Set Suite Variable  ${RMTAppUserName}
    Set Suite Variable  ${RMTAppPassword}
    Set Suite Variable  ${RMTAPI_Alias}

    Run keyword  Reserve Ports 

Get Remote IP
    ${remote_id}=  iNMS.Get ID  ${NMSAPI_Alias}  ${remote_name}  Remote
    ${terminalsvn}=  iNMS.Get Components  ${NMSAPI_Alias}  terminalsvn  vlan_id=${vlan_id}&obj_parentid=${remote_id}
    ${rmt_vlan_sat_ip}=  iUtilities.Get Param With Name Dictionary  ${terminalsvn}  obj_parentid  ${remote_id}  sat0ip
    Set Suite Variable  ${rmt_vlan_sat_ip}
    ${terminalsvn}=  iNMS.Get Components  ${NMSAPI_Alias}  terminalsvn  vlan_id=1&obj_parentid=${remote_id}
    ${remote_sat_ip}=  iUtilities.Get Param With Name Dictionary  ${terminalsvn}  obj_parentid  ${remote_id}  sat0ip
    Set Suite Variable  ${remote_sat_ip}
    ${remote_ip}=  iNMS.Get Remote Properties  ${NMSAPI_Alias}  ${remote_name}  lanip
    Set Suite Variable  ${remote_ip}

Validate Remote LAN IP
    [Arguments]  ${value}
    ${ping_status}=  iNMS.ping_ip  ${NMS_SSH_Alias}  ${remote_ip}
    Log to console  Ping value is -${value}=${ping_status}
    Should be True  ${ping_status} == ${value}  Ping from NMS to remote ip has failed!

Configure Remote as DHCP Server
    ${output}=  iNMS.Configure DHCP  ${NMSAPI_Alias}  ${remote_name}  ${vlan_id}  enable  dhcp_body=${dhcp_config}
    Set Suite Variable  ${DHCP_Flag}  1
    Run Keyword  Wait for the remote to be up

Configure Remote as DHCP Relay
    ${output}=  iNMS.Configure DHCP  ${NMSAPI_Alias}  ${remote_name}  ${vlan_id}  enable  dhcp_body=${dhcp_relay}
    Set Suite Variable  ${DHCP_Flag}  4
    Run Keyword  Wait for the remote to be up

Disable DHCP
    ${output}=  iNMS.Configure DHCP  ${NMSAPI_Alias}  ${remote_name}  ${vlan_id}  mode=disable
    Set Suite Variable  ${DHCP_Flag}  0
    Run Keyword  Wait for the remote to be up

Wait for the remote to be up
    Sleep  20
    ${status}=  iNMS.Wait for Component  ${NMS_SSH_Alias}  ${remote_sat_ip}
    Should be True  ${status[0]}  Remote did not not come back to the Network!

Validate DHCP Status on remote
    Log to console  vlan is - ${vlan_id}
    Log to console  DHCP Enabled on Remote - ${status}
    Run Keyword IF  '${DHCP_Flag}'=='0'
    ...     Should Not be True  ${status}  Remote DHCP Status Failed- Still Enabled!
    Run Keyword IF  '${DHCP_Flag}'=='1'
    ...     Should be True  ${status}  Remote DHCP-Server Status Failed- Still Disabled!
    Run Keyword IF  '${DHCP_Flag}'=='4'
    ...     Should be True  ${status}  Remote DHCP-Relay Status Failed- Still Disabled!

Validate DHCP Server Status on remote
    ${status}=  iRemote.Get DHCP Status  rmt_api_session  ${vlan_id}  ${start_ip}  ${end_ip}  SERVER
    Set Suite Variable  ${status}
    Run keyword  Validate DHCP Status on remote

Validate DHCP Relay Status on remote
    ${status}=  iRemote.Get DHCP Status  rmt_api_session  ${vlan_id}  ${dhcp_relay_ip}  ${dhcp_relay_ip}  RELAY
    Set Suite Variable  ${status}
    Run keyword  Validate DHCP Status on remote

Reserve Ports
    ${reserve_spirent}=  Setup Spirent  ${stc_ip}  ${stc_slot}  ${stc_hub_port}  ${stc_remote_port}
    Should be true  ${reserve_spirent}  Spirent setup failed, ports are not connected!
    Set Suite Variable  ${Reserve_Flag}  1

Compute DHCP Server gateway
    ${svn_out}=  iNMS.Get Components  ${NMSAPI_Alias}  svn  svnidx=${vlan_id}
    ${svn_id}=  iUtilities.Get Param With Name Dictionary  ${svn_out}  svnidx  ${vlan_id}  obj_id
    
    ${sitesvn_out}=  iNMS.Get Components  ${NMSAPI_Alias}  sitesvn  obj_parentid=${svn_id}
    ${sitesvn_id}=  iUtilities.Get Param With Name Dictionary  ${sitesvn_out}  obj_parentid  ${svn_id}  obj_id
    
    ${bladesvn_out}=  iNMS.Get Components  ${NMSAPI_Alias}  bladesvn  svn_id=${sitesvn_id}
    ${stc_svr_gtw_ip}=  iUtilities.Get Param With Name Dictionary  ${bladesvn_out}  svn_id  ${sitesvn_id}  eth0ipv4address
    ${stc_svr_mask}=  iUtilities.Get Param With Name Dictionary  ${bladesvn_out}  svn_id  ${sitesvn_id}  eth0ipv4netmask
    ${stc_svr_cidr}=  iIPAddress.Netmask to CIDR  ${stc_svr_mask}
    Set Suite Variable  ${stc_svr_gtw_ip}
    Set Suite Variable  ${stc_svr_cidr}
    

Configure DHCP Server in Spirent
    ${DHCP_Server_name}=  Set Variable  dhcp_server
    Run keyword  Compute DHCP Server gateway
    ${dhcp_server_start_ip}=  iIPAddress.Get Next IP Address  ${dhcp_relay.relaytov4}  ${stc_svr_cidr}
    ${dhcp_svr}  ${handler}=  iSpirent.Create DHCP Server Device  ${DHCP_Server_name}  ${dhcp_relay.relaytov4}  ${stc_svr_cidr}  ${stc_svr_gtw_ip}  ${dhcp_server_start_ip}  ${start_ip}  ${dhcp_config.defaultgateway}  ${device_count}  ${vlan_id}
    Set Suite Variable  ${dhcp_svr}
    Set Suite Variable  ${handler}

Start DHCP Server
    iSpirent.Start DHCP Server  ${dhcp_svr}

Verify if DHCP server is UP
    ${svr_state}=  iSpirent.Check DHCP Server State  ${handler}
    ${state}=  Get From Dictionary  ${svr_state}  ${handler}  
    Should be true  '${state}'=='UP'  DHCP Server is Down

Stop DHCP Server and verify state
    iSpirent.Stop DHCP Server  ${dhcp_svr}
    ${svr_state}=  iSpirent.Check DHCP Server State  ${handler}
    ${state}=  Get From Dictionary  ${svr_state}  ${handler}
    Should be true  '${state}'!='UP'  DHCP Server is still Running

Bind all DHCP Clients and validate IPs
    Run keyword  Bind DHCP Clients on Spirent and validate IPs  ${device_count}
    Set Suite Variable  ${Bind_Flag}  1

Bind few DHCP Clients and validate IPs
    Run keyword  Bind DHCP Clients on Spirent and validate IPs  ${device_count}
    Set Suite Variable  ${Bind_Flag}  3

Configure DHCP Clients in Spirent
    ${clients}  ${handlers}=  iSpirent.create_DHCP_client_devices  ${device_count}  ${vlan_id}
    Set Suite Variable  ${handlers}
    Set Suite Variable  ${clients}
    ${clients_var}=  Get Length  ${clients}
    ${handlers_var}=  Get Length  ${handlers}
    Set Suite Variable  ${handlers_var}
    Should Be Equal  ${device_count}  ${clients_var}
    Should Be Equal  ${device_count}  ${handlers_var}

Bind DHCP Clients on Spirent and validate IPs
    [Arguments]  ${device_count}
    :FOR  ${each_handler}  IN  @{handlers}
    \  iSpirent.dhcp bind  ${each_handler}
    :FOR  ${each_client}  IN  @{clients}
    \  ${dict_var}=  iSpirent.get dhcp client ip address  ${each_client}
    \  Log to console  ${dict_var}
    \  Log to console  ${each_client}
    \  Run keyword  Validate Spirent IP in DHCP Range  ${dict_var}  ${each_client}

Verify DHCP Client State
    ${client_status_list}=  iSpirent.Check Dhcp Client State  @{handlers}
    ${client_list_lenght}=  Get Length  ${client_status_list}
    Should be true  '${client_list_lenght}'=='${handlers_var}'  Client-list lenght does not match number of handlers!

Validate Spirent IP in DHCP Range
    [Arguments]  ${dict_var}  ${each_client}
    ${Stc_dhcp_client_ip}=  Get From Dictionary  ${dict_var}  ${each_client}
    ${is_in_range}=  iIPAddress.Is in Range ip  ${start_ip}  ${end_ip}  ${Stc_dhcp_client_ip}
    Log to console  Allocated IP for client is in valid DHCP range - ${is_in_range}
    Should be true  ${is_in_range}  The Issued IP address is not within requested range!

Release few DHCP Clients
    ${count_all_handlers}=  Get Length  ${handlers}
    ${count_var}=  Evaluate  ${count_all_handlers}/2
    ${release_var}=  Convert To Integer  ${count_var}
    ${few_handlers}=  Get Slice From List  ${handlers}  ${release_var}
    :FOR  ${each_handler}  IN  @{few_handlers}
    \  iSpirent.dhcp_release  ${each_handler}
    Set Suite Variable  ${Bind_Flag}  2
    ${device_count}=  Get Length  ${few_handlers}
    Set Suite Variable  ${device_count}

Release All DHCP Clients
    :FOR  ${each_handler}  IN  @{handlers}
    \  iSpirent.dhcp_release  ${each_handler}
    Set Suite Variable  ${Bind_Flag}  0

TearDown Environment
    Run Keyword IF  '${Bind_Flag}'>='1'
    ...     Release All DHCP Clients

    Run Keyword IF  '${DHCP_Flag}'>='1'
    ...     Disable DHCP

    Run Keyword IF  '${Reserve_Flag}'=='1'
    ...     UnReserve Ports

    Run Keyword  Wait for the remote to be up

    iRemote.Close Remote api  ${RMTAPI_Alias}
    iNMS.Close NMS Shell  ${NMS_SSH_Alias}
    iNMS.Close NMS API  ${NMSAPI_Alias}

UnReserve Ports
    Teardown Spirent
    Set Suite Variable  ${Reserve_Flag}  0

