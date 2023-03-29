
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
    Run Keyword  Login to NMS Here

Login to NMS Here
    Set Suite Variable  ${iPlatform}  Velocity
    Set Suite Variable  ${NMS_Rest_Alias}  MyNMSAPI
    iNMS.Open NMS Api Session  ${NMS_Rest_Alias}  ${NMS.ip}  ${NMS.RestUserName}  ${NMS.RestPassword} 
    log to console  NMS Rest Alias is ${NMS_Rest_Alias}
    log to console  setup complete        

Enable Terminal Authentication
    
    #Enable Terminal Authentication  
    ${Remote_Names}=  Create List
    log to console  In enable terminal authentication block
    :FOR  ${rmt}  in  @{Remote.Name}
        \   ${patch_remote}=  iNMS.Modify Remote  ${NMS_Rest_Alias}  ${rmt}  ${terminal_data}
        \   log to console  ${terminal_data}
        \   log to console  ${patch_remote}

    # Apply changes to terminal
        \   ${apply_remote}=  iNMS.Apply Remote  ${NMS_Rest_Alias}  ${rmt}  Both
        \   log to console  ${apply_remote}


Generate Token
   # Get Satellite router object id
    ${sat_ID}=  iNMS.Get ID  ${NMS_Rest_Alias}  ${satrouter.Name}  satelliterouter
    log to console  ${satrouter.Name}
    log to console  ${sat_ID}
      
    # Generate one time token
    ${get_token}=  iNMS.Generate Token  ${NMS_Rest_Alias}  
    log to console  ${get_token}
    Set Test Variable  ${get_token}  ${get_token}


    # Patch satellite router with generated one time token
    ${satrouter_data}=  set Variable  {"provisioning_auth_token": "${get_token}"}
    log to console  ${satrouter_data}
    ${patch_satrouter}=  iNMS.Modify Component  ${NMS_Rest_Alias}  ${satrouter.Name}  satelliterouter  ${satrouter_data}
    log to console  patch response is ${patch_satrouter}

    # Apply changes to satellite router    
    ${apply_satrouter}=  iNMS.Apply Component  ${NMS_Rest_Alias}  ${satrouter.Name}  satelliterouter  Both
    log to console  apply satrouter response ${apply_satrouter}
    log to console  ${get_token}
    [Return]  ${get_token}

 
Validate PP Options

    # Validate the options reached the PP
    log to console  Validating PP options push
    iPP.Log into PP  PP_SSH_Alias  ${PP["ip"]}  ${PP["UserName"]}  ${PP["Password"]}  ${PP["SUPassword"]}
    ${pp_options_push}=  iPP.Read Auth Option File  PP_SSH_Alias
    ${Remote_Ips}=  Create List
    :FOR  ${rmt}  in  @{Remote.Name}
        \  ${Result}=  iRemote.Open Remote Api Session  ${NMS_Rest_Alias}  Test_${rmt}  ${rmt}  rest_username=${Remote.Username}  rest_password=${Remote.Password}  proxy_host_ip=${Jump.Ip}  proxy_username=${Jump.Username}   connect_using_tunnel=True                     
        \  ${get_did}=  Get DID  Test_${rmt}
    log to console  printing pp_options_push ${pp_options_push}
    log to console  printing TOKEN
    Should be True  ${pp_options_push['TERMINAL_AUTH']['${get_did}']['ATMEL']['TOKEN']}
    log to console  Token updated in AUTH.opt
    iSSH.Close ssh session  PP_SSH_Alias

Set Token Using Terminal API

    # Enter generated token via Terminal API
    log to console  Generated token is ${get_token}

    ${Remote_Ips}=  Create List
    :FOR  ${rmt}  in  @{Remote.Name}
        \   log to console  \nlogging in to remote  ${rmt}
        \   log to console  ${Jump.Ip}    
        \   ${Result}=  iRemote.Open Remote Api Session  ${NMS_Rest_Alias}  Test_${rmt}  ${rmt}  rest_username=${Remote.Username}  rest_password=${Remote.Password}  proxy_host_ip=${Jump.Ip}  proxy_username=${Jump.Username}   connect_using_tunnel=True                     
        \   ${Passcode.token}=  set Variable  {"one_time_key":"${get_token}"}
        \   ${Set_token}=  iRemote.Post Passcode  Test_${rmt}  ${Passcode.token}
        \   iRemote.Close Remote Api  Test_${rmt}
        \   log to console  ${Set_token}

Get Terminal Status
    # Get Terminal LED status using terminal API and validate Terminal in network on terminal console  
    
    ${Remote_Ip}=  Create List
    :FOR  ${rmt}  in  @{Remote.Name}
    \   log to console  \nlogging in to remote  ${rmt}
    \   log to console  ${Jump.Ip}
    \   ${Result}=  iRemote.Open Remote Api Session  ${NMS_Rest_Alias}  Test_${rmt}  ${rmt}  rest_username=${Remote.Username}  rest_password=${Remote.Password}  proxy_host_ip=${Jump.Ip}  proxy_username=${Jump.Username}   connect_using_tunnel=True                     
    \   ${Led_status}=  Get Led Status  Test_${rmt}
    \   log to console  ${Led_status}
    \   Should be Equal  ${Led_status}  green    
    \   iRemote.Close Remote Api  Test_${rmt}
    \   ${Remote_Ip}=  Set Suite Variable  ${Remote_Ip}
    
    \  log to console  Validated terminal LED NET is ${Led_status}
            
        # Verify terminal is in network
        # Setting the remote console Alias as Test1_${rmt}

    \  ${Remote_login}=  iRemote.Log in to Remote  ${NMS_Rest_Alias}  Test1_${rmt}  ${rmt}  username=${Remote.SSHUsername}  password=${Remote.SSHPassword}  proxy_host_ip=${Jump.Ip}  proxy_username=${Jump.Username}  proxy_password=${Jump.Password}  connect_using_tunnel=${True}
    \  log to console  Checking Remote state
    \  ${remote_state}=  iRemote.Check Remote State  remote_ssh_alias=Test1_${rmt}   status=Succeeded  Duration=60  username=${Remote.Username}  password=${Remote.Password}
    \  iRemote.Close Remote Api  Test_${rmt}
    \  Should be True  ${remote_state}
    \  log to console  Validated that Remote is in Network
   

Cleanup all config
    log to console  closing all open ssh sessions
    iSSH.Close all ssh session
    iREST.Disconnect All 
    log to console  closed all ssh sessions
