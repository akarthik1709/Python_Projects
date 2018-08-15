*** Settings ***
Resource    ${CURDIR}/../../steps/velocity/velo_udp_characterization_precondition_steps.robot

Suite Setup  Set Test Requirement
Suite Teardown  Cleanup all config

*** Variables ***
${iPlatform}=  test_network

*** Test Cases ***
Validate the Preconditions for DLG_UDP script
    Validate Terminal stability 
    Validate Downstream and Upstream MIR on Traffic passing VR 
    Validate Downstream symbol rate
    Validate Downstream MODCOD
    Validate Downstream roll-off factor
    Validate Upstream symbol rate and MODCOD
    Validate Rx SNR of the Terminal
