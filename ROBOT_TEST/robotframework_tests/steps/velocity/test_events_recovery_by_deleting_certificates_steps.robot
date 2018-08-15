
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
    Run Keyword  Preconditions

Preconditions
    Set Suite Variable  ${iPlatform}  Velocity
    Set Suite Variable  ${NMS_Rest_Alias}  MyNMSAPI
    iNMS.Open NMS Api Session  ${NMS_Rest_Alias}  ${NMS.ip}  ${NMS.RestUserName}  ${NMS.RestPassword}
    log to console  NMS Rest Alias is MyNMSAPI

Log Into Remote
    ${Remote_Ips}=  Create List
    :FOR  ${rmt}  in  @{Remote.Name}
        \   log to console   Inside for loop
        \   log to console  \nlogging in to remote  ${rmt}
        \   iRemote.Open Remote Api Session  ${NMS_Rest_Alias}  test_rmt_alias  ${rmt}  rest_username=${Remote.Username}  rest_password=${Remote.Password}  proxy_host_ip=${Jump.Ip}     
	    \   ${Remote_login}=  iRemote.Log in to Remote  ${NMS_Rest_Alias}  Test1  ${rmt}  proxy_host_ip=${Jump.Ip}  connect_using_tunnel=${True}
        \   ${remote_state}=  iRemote.Check Remote State  Test1  status=Succeeded  Duration=60  username=${Remote.Username}  password=${Remote.Password}
        \   log to console  ${remote_state}
   

Go to the Path of the Certificates 
    ${path_change1}=  iRemote.execute linux command  Test1  ${Command.path_change}
    log to console  ${path_change1}
    ${Path_Return}=  iRemote.execute linux command  Test1  ls
    log to console  ${Path_Return}

Backup X509 Certificate
     ${Make_Directory}=  iRemote.execute linux command  Test1  ${Command.make_dir} 
     log to console  ${Make_Directory}
     ${Bckup_Return}=  iRemote.execute linux command  Test1  ${Command.copy_cert} 
     log to console  ${Bckup_Return}
     ${Backup_path}=  iRemote.execute linux command  Test1  ${Command.path_backup}     
     ${ls.command}=  iRemote.execute linux command  Test1  ${Command.ls_cmd} 
     log to console  ${ls.command}
     ${result}=  Run Keyword if  '''x509_global.bin''' in '''${ls.command}'''
     ...     Set Variable  ${True}
     ...     ELSE
     ...     Set Variable  ${False}
     Should Be True  ${result}

Delete the Certificates
    Go to the Path of the Certificates
    ${Rm_Return}=  iRemote.execute linux command  Test1  ${Command.del_cert}
    log to console  ${Rm_Return}
    ${ls.command}=  iRemote.execute linux command  Test1  ${Command.ls_cmd} 
    log to console  ${ls.command}

Restart Falcon
    ${Res_Return}=  iRemote.execute linux command  Test1  ${Command.res_fal} 
    log to console  ${Res_Return}
    Sleep  40s
    ${result}=  Run Keyword if  '''Starting''' in '''${Res_Return}'''
    ...     Set Variable  ${True}
    ...     ELSE
    ...     Set Variable  ${False}
    Should Be True  ${result}

Check Recovery Mode of the Remote 
    ${Remote_Ips}=  Create List
    Log Into Remote
    ${tel_Return}=  iRemote.execute_application_command  Test1  ${Command.rem_cons}
    log to console  ${tel_Return}
    ${recovery_mode}=  check_remote_state  Test1  status=Yes  timeout=60  username=${Remote.Username}  password=${Remote.Password}
    log to console  ${recovery_mode}
    Run keyword If    "${recovery_mode}"== "True"
    ...   log to console  The Remote has gone to Recovery Mode
    ...   ELSE 
    ...   log to console  The Remote is not in Recovery Mode

Check Events through API
    :FOR  ${rmt}  in  @{Remote.Name}
        \   log to console  \nlogging in to remote  ${rmt}
        \   log to console  ${Jump.Ip}
        \   iRemote.Open Remote Api Session  ${NMS_Rest_Alias}  test_rmt_alias  ${rmt}  rest_username=${Remote.Username}  rest_password=${Remote.Password}  proxy_host_ip=${Jump.Ip}  proxy_username=${Jump.Username}   connect_using_tunnel=True                     
        \   ${event_result}=  get_events  test_rmt_alias
        \   log to console  ${event_result}
    Run keyword If    "MODEM_RECOVERY_MODE" in "${event_result}"
    ...   log to console  Event Modem Recovery mode found
    ...   ELSE 
    ...   log to console  Event Modem Recovery mode not found  

Go to the Path of the Backup Folder
    ${path_bckp}=  iRemote.execute linux command  Test1  ${Command.path_backup}
    log to console  ${path_bckp}
    ${Path_Return}=  iRemote.execute linux command  Test1  pwd
    log to console  ${Path_Return}
    ${ls.command}=  iRemote.execute linux command  Test1  ${Command.ls_cmd} 
    log to console  ${ls.command}

Restore the Deleted Certificates
    ${Bckup_Ret}=  iRemote.execute linux command  Test1  ${Command.copy_bckp} 
    log to console  ${Bckup_Ret}
    Restart Falcon
    Check Recovery Mode of the Remote

Cleanup all config
    log to console  closing all open ssh sessions
    iSSH.Close all ssh session
    iREST.Disconnect All 
    log to console  closed all ssh sessions
  
