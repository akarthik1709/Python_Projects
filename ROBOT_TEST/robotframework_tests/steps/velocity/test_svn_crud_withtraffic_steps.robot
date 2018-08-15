*** Settings ***
Library      irobot.libraries.iSSH  WITH NAME  iSSH
Library      irobot.libraries.iREST  WITH NAME  iREST
Library      irobot.libraries.iSpirent  WITH NAME  iSpirent
Library      irobot.libraries.iDirect.iNMS  WITH NAME  iNMS
Library      Collections

*** Keywords ***
Set Test Requirement
    Run Keyword  Login to NMS Here

Login to NMS Here
    Set Suite Variable  ${iPlatform}  Velocity
    Set Suite Variable  ${NMS_Rest_Alias}  NMS_API_Alias
    iNMS.Open NMS Api Session  ${NMS_Rest_Alias}  ${NMS.ip}  ${NMS.RestUserName}  ${NMS.RestPassword}
    ${Reserve_Flag}=  Set Variable  0
    Set Suite Variable  ${Reserve_Flag}

Create ${svn} SVN in Terminal
    ${create_terminal_svn_result}=  iNMS.create_terminal_service_plan  ${NMS_Rest_Alias}  ${Remote_name}  ${Remote_SVN_Details}  @{svn}
    Should be True  ${create_terminal_svn_result} != 0

Create ${svn} SVN in PP
    log to console  Creating SVN in PP
    ${create_pp_svn_result}=  iNMS.create_svn_pp  ${NMS_Rest_Alias}  ${PP_SVN_Details}  @{svn}
    Should be True  ${create_pp_svn_result} != 0

Delete ${svn} SVN in PP
    ${delete_pp_svn_result}=  iNMS.delete_svn_pp  ${NMS_Rest_Alias}  ${PP_SVN_Details}  @{svn}
    Should be True  ${delete_pp_svn_result} != 0

Delete ${svn} SVN in Terminal
    ${delete_terminal_svn_result}=  iNMS.delete_svn_terminal   ${NMS_Rest_Alias}  ${Remote_name}  ${Remote_SVN_Details}  @{svn}
    Should be True  ${delete_terminal_svn_result} != 0

Apply Terminal ${when}
    Log to console  Applying Terminal ${when}
    ${apply_result}=  iNMS.apply_component  ${NMS_Rest_Alias}  ${Remote_name}  terminal
    Should be true  ${apply_result}

Revert Changes
    Release Ports  ${Reserve_Flag}
    Log to console  Reverting Changes - If the SVN's were already deleted, warnings will be displayed!
    Delete ${All_SVNS} SVN in Terminal
    Apply Terminal after deleting SVN
    Log to console  Sucessfully Reverted Changes in Terminal!
    Delete ${All_SVNS} SVN in PP
    Log to console  Sucessfully Reverted Changes in PP!

Start UDP traffic for SVN - ${svn}
    ${Reserve_Flag}=  Reserve Ports  ${stc_ip}  ${stc_slot}  ${stc_hub_port}  ${stc_remote_port}
    Set Suite Variable  ${Reserve_Flag}
    @{hand}=  Create List
    @{stream}=  Create List
    @{cond}=  Create List
    :FOR  ${each_detail}  in  @{svn}
    \  Log to console  e-${each_detail}
    \  Log to console  g - &{Spirent_${each_detail}}
    \  ${udp_stream}  ${handlers}=  iSpirent.Config UDP Traffic  &{Spirent_${each_detail}}
    \  ${udp_condition}=  Get Variable value  ${Spirent_${each_detail}.UDP_Traffic_Validation}  0
    \  Log to console  udp-con-${udp_condition}
    \  Append to List  ${cond}  ${udp_condition}
    \  Log to console  udp_stream- ${udp_stream}
    \  Log to console  handlers-${handlers}
    \  Should be True  ${udp_stream} != False
    \  Append to List  ${hand}  ${handlers}
    \  Append to List  ${stream}  ${udp_stream}
    Log to console  h-${hand}\n s-${stream}
    Log to console  start-@{stream}
    :For  ${streams}  in  @{stream}
    \  Log to console  streaaa-${streams}
    \  iSpirent.Start Traffic  ${streams}
    Set Suite Variable  @{stream}
    Set Suite Variable  @{hand}
    Set Suite Variable  @{cond}

Stop traffic
    : FOR    ${INDEX}    IN RANGE    1    ${testtime}
    \  Log to console  Traffic Running .... ${INDEX}
    \  Sleep  1s
    :For  ${streams}  in  @{stream}
    \  iSpirent.Stop Traffic  ${streams}

Validate if traffic fails only in third SVN
    ${spirent_result}=  iSpirent.assert_udp_traffic  ${hand[2]}  @{traffic_must_fail}
    Should be True  ${spirent_result} 
    ${spirent_result}=  iSpirent.assert_udp_traffic  ${hand[0]}
    Should be True  ${spirent_result} 
    ${spirent_result}=  iSpirent.assert_udp_traffic  ${hand[1]}  
    Should be True  ${spirent_result} 
    Release Ports  ${Reserve_Flag}    

Validate if traffic fails only in second SVN
    ${spirent_result}=  iSpirent.assert_udp_traffic  ${hand[1]}  @{traffic_must_fail}
    Should be True  ${spirent_result} 
    ${spirent_result}=  iSpirent.assert_udp_traffic  ${hand[0]}
    Should be True  ${spirent_result} 
    ${spirent_result}=  iSpirent.assert_udp_traffic  ${hand[2]}
    Should be True  ${spirent_result} 
    Release Ports  ${Reserve_Flag}    

Validate if traffic flows in all SVNS created
    :For  ${handler}  in  @{hand}
    \  ${spirent_result}=  iSpirent.assert_udp_traffic  ${handler}
    \  Should be True  ${spirent_result} 
    Release Ports  ${Reserve_Flag}    

Validate if traffic fails in all SVNS
    ${spirent_result}=  iSpirent.assert_udp_traffic  ${hand[0]}  @{traffic_must_fail}
    Should be True  ${spirent_result} 
    ${spirent_result}=  iSpirent.assert_udp_traffic  ${hand[1]}  @{traffic_must_fail}
    Should be True  ${spirent_result} 
    ${spirent_result}=  iSpirent.assert_udp_traffic  ${hand[2]}  @{traffic_must_fail}
    Should be True  ${spirent_result} 
    Release Ports  ${Reserve_Flag}    

Reserve Ports
    [Arguments]  ${stc_ip}  ${stc_slot}  ${stc_hub_port}  ${stc_remote_port}
    ${reserve_spirent}=  iSpirent.Setup Spirent  ${stc_ip}  ${stc_slot}  ${stc_hub_port}  ${stc_remote_port}    
    Should be true  ${reserve_spirent}
    [RETURN]  1

Release Ports
    [Arguments]  ${Reserve_Flag}
    Run Keyword IF  '${Reserve_Flag}'=='1'
    ...     iSpirent.TearDown Spirent
