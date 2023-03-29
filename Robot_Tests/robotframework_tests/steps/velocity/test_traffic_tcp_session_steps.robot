*** Settings ***
Library      irobot.libraries.iSSH  WITH NAME  iSSH
Library      irobot.libraries.iUtilities  WITH NAME  iUtilities
Library      irobot.libraries.iSpirent  WITH NAME  iSpirent
Library      irobot.libraries.iIPAddress  WITH NAME  iIPAddress
Library      irobot.libraries.iREST  WITH NAME  iREST
Library      irobot.libraries.iDirect.iPP  WITH NAME  iPP
Library      irobot.libraries.iDirect.iNMS  WITH NAME  iNMS
Library      irobot.libraries.iDirect.iRemote  WITH NAME  iRemote


*** Keywords ***
Set Test Requirement
    Set Suite Variable  ${iPlatform}  Velocity
    Set Suite Variable  ${NMS_Rest_Alias}  MyNMSAPI
    Set Suite Variable  ${dump_check}  List
    Set Suite Variable  ${dump}  dump
    iNMS.Open NMS Api Session  ${NMS_Rest_Alias}  ${NMS.ip}  ${NMS.RestUserName}  ${NMS.RestPassword}
    log to console  NMS Rest Alias is MyNMSAPI
   
Log Into Remote
    log to console  logging in to remote  ${Remote.Name}
    iRemote.Open Remote Api Session  ${NMS_Rest_Alias}  test_rmt_alias  ${Remote.Name}  rest_username=${Remote.Username}  rest_password=${Remote.Password}  proxy_host_ip=${Jump.Ip}     
    ${Remote_login}=  iRemote.Log in to Remote  ${NMS_Rest_Alias}  Test1  ${Remote.Name}  proxy_host_ip=${Jump.Ip}  connect_using_tunnel=${True}
    log to console  \nlogging in to remote  Test1
           
Get Rx and Tx CID
    ${Session_Map}=  Create List
    ${dump_check}=  Create List
    ${session1}=  Create Dictionary
    Set Suite Variable  ${dump_check1}  ${EMPTY}
    ${dump_check1}=  iRemote.execute_application_command  Test1  spoof dump ${Remote.svn_id}  prompt_string=End of sessions
    ${result}=  Run Keyword if  '''End of sessions''' in '''${dump_check1}'''
    ...     Set Variable  ${True}
    ...     ELSE
    ...     Set Variable  ${False}
    Should Be True  ${result}
    ${dump_check}=  iUtilities.split_to_lines  ${dump_check1}
    ${l}=  Get Length  ${dump_check}
    :FOR  ${dump}  in  @{dump_check}
        \   ${Tx_ID1}=  Fetch From Left  ${dump}  Rx
        \   ${Tx_ID}=  Fetch From Right   ${Tx_ID1}  :
        \   ${Rx_ID1}=  Fetch From Left  ${dump}  VID
        \   ${Rx_ID}=  Fetch From Right  ${Rx_ID1}  :
        \   Set Suite Variable  ${Tx_Rx}  ${Tx_ID}:${Rx_ID}
        \   ${VID1}=  Fetch From Left  ${dump}  IP
        \   ${VID}=  Fetch From Right  ${VID1}  :       

        \   ${Source_IP1}=  Fetch From Left  ${dump}  ->
        \   ${Source_IP2}=  Fetch From Right  ${Source_IP1}  IP:
        \   ${Source_IP}=  Fetch From Left  ${Source_IP2}  :

        \   ${Source_Port}=  Fetch From Right  ${Source_IP1}  :

        \   ${Dest_IP1}=  Fetch From Right  ${dump}  ->
        \   ${Dest_IP}=  Fetch From Left  ${Dest_IP1}  :

        \   ${Dest_port}=  Fetch From Right  ${dump}  : 

        \   ${Dest_port_session}=  Create Dictionary  dest_port  ${Dest_port}
        \   ${VID_session}=  Create Dictionary  vlan_id  ${VID}
        \   ${Source_session}=  Create Dictionary  src_ip  ${Source_IP}
        \   ${Source_port_session}=  Create Dictionary  src_port  ${Source_Port}
        \   ${Dest_IP_session}=  Create Dictionary  dest_ip  ${Dest_IP}
        \   Append To List  ${Session_Map}  ${Tx_Rx},${VID_session},${Source_session},${Source_port_session},${Dest_IP_session},${Dest_port_session} 
    [Return]  ${Session_Map}

Wait for a few seconds
    Sleep  80s
    log to console  Waited for 80 seconds

Validate the two set of sessions
    ${T1}=  Get Rx and Tx CID
    log to console  The first set of sessions:${T1}
    Wait for a few seconds
    ${T2}=  Get Rx and Tx CID
    log to console  The second set of sessions:${T2}
    ${Killed_list}=  iUtilities.difference_in_two_list  ${T1}  ${T2}
    log to console  The Killed sessions are:${Killed_list}
    ${Newly_Created_list}=  iUtilities.difference_in_two_list  ${T2}  ${T1}
    log to console  The Newly created sessions are:${Newly_Created_list}


Check TCP session and get Fade and Reap timers
    ${spoof_session_init}=  iRemote.execute_application_command  Test1  spoof params ${Remote.svn_id}
    log to console  ${spoof_session_init}
    ${fade_timer}=  iUtilities.find_value_from_output  ${spoof_session_init}  fade_timeout_ms:
    ${reap_timer}=  iUtilities.find_value_from_output  ${spoof_session_init}  reap_timeout_ms:
    log to console  The Fade timer value is: ${fade_timer}
    log to console  The Reap timer value is: ${reap_timer}

Cleanup all config
    log to console  closing all open sessions
    iNMS.close_nms_api  NMS_Rest_Alias
    iSSH.Close all ssh session
    iREST.Disconnect All 
 
    




