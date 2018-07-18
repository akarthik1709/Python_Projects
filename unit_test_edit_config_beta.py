#!/usr/bin/env python3
__author__ = "Karthik"
"""
    Netconf python example by yang-explorer (https://github.com/CiscoDevNet/yang-explorer)

    Installing python dependencies::$
    > pip install lxml ncclient

    Running script: (save as example.py)
    > python example.py -a 172.30.5.2 -u admin -p iDirect! --port 830
"""

import lxml.etree as ET
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError
import datetime
import sys

def function_to_invoke_get_and_edit_config():

    while(1):
        print("=================================================")
        server_type_input = input("Please input the type of device(NMS_Upstream,PP_Upstream,PP_Tunnel, LineCard, Router, No_Device\n1)For NMS_Upstream\n2)For PP_Upstream\n3)For PP_Tunnel\n4)For LineCard\n5)For Router\n6)Basic_config\n7)Create a YANG bridge\n8)Create a YANG bridge Interface\n9)Create a loopback YANG bridge\n10) VXLAN demo\n11)For no device\n")

        if server_type_input == "11":
            sys.exit(0)

        list_of_devices = ["nms-us", "pp-us", "pp-tunnel", "linecard", "router", "basic_vpp",
        "yang_bridge_create", "yang_bridge_create_interface", "yang_bridge_loopback", "vxlan_demo", "no"]    
        
        string_input1 = ""
        while(list_of_devices): 
             if server_type_input == "1":
                 print("================================================")
                 string_input2 = input("Enter the interface number\n")
                 print("=================================================")
                 print("I am here", string_input2)
                 print("=================================================")
                 string_input3 = input("Enter the interface description\n")
                 payload = func_payload(server_type_input, string_input1,string_input2, string_input3)
                 print("the payload string is\n",payload)
                 response = func_to_use_edit_config(payload, server_type_input)
                 print("Do you want to configure any other device...??")
                 break
             elif server_type_input == "2":
                 print("================================================")
                 string_input2 = input("Enter the interface number\n")
                 print("=================================================")
                 print("I am here", string_input2)
                 print("=================================================")
                 string_input3 = input("Enter the interface description\n")
                 payload = func_payload(server_type_input, string_input1,string_input2, string_input3)
                 response_PP = func_to_use_edit_config(payload, server_type_input)
                 print("Do you want to configure any other device...??")
                 break 
             elif server_type_input == "3":
                 print("================================================")
                 string_input2 = input("Enter the interface number\n")
                 print("=================================================")
                 print("I am here", string_input2)
                 print("=================================================")
                 string_input3 = input("Enter the interface description\n")
                 payload = func_payload(server_type_input, string_input1,string_input2, string_input3)
                 print(type(payload))
                 response_PP_tunnel = func_to_use_edit_config(payload, server_type_input)
                 print("Do you want to configure any other device...??")
                 break
             elif server_type_input == "4":
                 print("================================================")
                 string_input2 = input("Enter the interface number\n")
                 print("=================================================")
                 print("I am here", string_input2)
                 print("=================================================")
                 string_input3 = input("Enter the interface description\n")
                 payload = func_payload(server_type_input, string_input1,string_input2, string_input3)
                 response_PP_tunnel = func_to_use_edit_config(payload, server_type_input)
                 print("Do you want to configure any other device...??")
                 break
             elif server_type_input == "5":
                 print("================================================")
                 string_input2 = input("Enter the interface number\n")
                 print("=================================================")
                 print("I am here", string_input2)
                 print("=================================================")
                 string_input3 = input("Enter the interface description\n")
                 payload = func_payload(server_type_input, string_input1,string_input2, string_input3)
                 response_PP_tunnel = func_to_use_edit_config(payload, server_type_input)
                 print("Do you want to configure any other device...??")
                 break
             elif server_type_input == "6":
                 print("================================================")
                 string_input1 = input("Please enter the host name for the switch\n")
                 string_input2 = ""
                 string_input3 = ""
                 payload = func_payload(server_type_input, string_input1,string_input2, string_input3)
                 response_PP_tunnel = func_to_use_edit_config(payload, server_type_input)
                 print("Do you want to configure any other device...??")
                 break
             elif server_type_input == "7":
                 print("================================================")
                 string_input1 = input("Please enter the name for the bridge domain\n")
                 string_input2 = ""
                 string_input3 = ""
                 payload = func_payload(server_type_input, string_input1,string_input2, string_input3)
                 response_PP_tunnel = func_to_use_edit_config(payload, server_type_input)
                 print("Do you want to configure any other device...??")
                 break
             elif server_type_input == "8":
                 print("================================================")
                 string_input1 = input("Please enter the name of the bridge domain interface\n")
                 string_input2 = ""
                 string_input3 = ""
                 payload = func_payload(server_type_input, string_input1,string_input2, string_input3)
                 response_PP_tunnel = func_to_use_edit_config(payload, server_type_input)
                 print("Do you want to configure any other device...??")
                 break
             elif server_type_input == "9":
                 print("================================================")
                 string_input1 = input("Please enter the name of the loopback interface\n")
                 string_input2 = input("Please enter the IP address of the Loopback\n")
                 string_input3 = ""
                 payload = func_payload(server_type_input, string_input1,string_input2, string_input3)
                 response_PP_tunnel = func_to_use_edit_config(payload, server_type_input)
                 print("Do you want to configure any other device...??")
                 break
             elif server_type_input == "10":
                 print("================================================")
                 string_input1 = input("Please enter the name of the interface for VXLAN\n")
                 string_input2 = input("Please enter the destination IP\n")
                 string_input3 = input("Please enter the source IP\n")
                 payload = func_payload(server_type_input, string_input1,string_input2, string_input3)
                 response_PP_tunnel = func_to_use_edit_config(payload, server_type_input)
                 print("Do you want to configure any other device...??")
                 break
    
             elif server_type_input == "11":
                 sys.exit(0)
	     
             else:
                 raise Exception("======Please enter the correct server type=====")

    return (string_input1, string_input2, string_input3)

def func_payload(server_type_input, string_input1,string_input2, string_input3 ):

    if server_type_input == "1":
        payload = ("""
    <config>
      <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <intf-items>
          <phys-items>
            <PhysIf-list>
              <id>eth1/%s</id>
              <descr>%s</descr>
              <adminSt>up</adminSt>
              <mtu>9216</mtu>
              <mode>access</mode>
              <layer>Layer2</layer>
              <accessVlan>vlan-50</accessVlan>
            </PhysIf-list
          </phys-items>
        </intf-items>
      </System>
    </config>
   """) %(string_input2, string_input3 )


    elif server_type_input == "2":
        payload = ("""
    <config>
      <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
         <intf-items>
          <phys-items>
            <PhysIf-list>
              <id>eth1/%s</id>
              <descr>%s</descr>
              <adminSt>up</adminSt>
              <mtu>9216</mtu>
              <mode>access</mode>
              <layer>Layer2</layer>
              <accessVlan>vlan-4048</accessVlan>
            </PhysIf-list>
          </phys-items>
        </intf-items>
      </System>
    </config>
    """) %(string_input2, string_input3 )

    elif server_type_input == "3":
        payload = ("""
    <config>
      <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <intf-items>
          <phys-items>
            <PhysIf-list>
              <id>eth1/%s</id>
              <descr>%s</descr>
              <adminSt>up</adminSt>
              <mtu>9216</mtu>
              <mode>trunk</mode>
              <layer>Layer2</layer>
              <nativeVlan>vlan-50</nativeVlan>
            </PhysIf-list>
          </phys-items>
        </intf-items>
      </System>
    </config>
   """) %(string_input2, string_input3 )

    elif server_type_input == "4":
        payload = ("""
    <config>
      <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"> 
        <intf-items>
          <phys-items>
            <PhysIf-list>
              <id>eth1/%s</id>
              <descr>%s</descr>
              <adminSt>up</adminSt>
              <mtu>9216</mtu>
              <mode>trunk</mode>
              <layer>Layer2</layer>
              <nativeVlan>vlan-50</nativeVlan>
            </PhysIf-list>
          </phys-items>
        </intf-items>
      </System>
    </config>
   """) %(string_input2, string_input3 )

    elif server_type_input == "5":
        payload = ("""
    <config>
      <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <intf-items>
          <phys-items>
            <PhysIf-list>
              <id>eth1/%s</id>
              <descr>%s</descr>
              <adminSt>up</adminSt>
              <mtu>9216</mtu>
              <mode>trunk</mode>
              <layer>Layer2</layer>
            </PhysIf-list>
          </phys-items>
        </intf-items>
      </System>
    </config>
   """) %(string_input2, string_input3 )
    elif server_type_input == "6":
        payload = ("""
      <config>
      <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <name>%s</name>
	<fm-items>
          <ifvlan-items>
            <adminSt>enabled</adminSt>
          </ifvlan-items>
          <bashshell-items>
            <adminSt>enabled</adminSt>
          </bashshell-items>
          <lldp-items>
            <adminSt>enabled</adminSt>
          </lldp-items>
          <vpc-items>
            <adminSt>enabled</adminSt>
          </vpc-items>
        </fm-items>
      </System>
    </config>
   """) %(string_input1)
    
    elif server_type_input == "7":
        payload = ("""
     <config>
     <bridge-domains xmlns="urn:opendaylight:params:xml:ns:yang:v3po">
      <bridge-domain>	
        <name>%s</name>
	    <learn>true</learn>
	      <forward>true</forward>
   	      <unknown-unicast-flood>true</unknown-unicast-flood>
        <arp-termination>false</arp-termination> 
        <flood>true</flood>
	 </bridge-domain>
	 </bridge-domains>	
     </config>
    """) %(string_input1)

    elif server_type_input == "8":
        payload = ("""
     <config>
     <bridge-domains xmlns="urn:opendaylight:params:xml:ns:yang:v3po">
       <bridge-domain>
       <name>%s</name>
         <learn>true</learn>
         <forward>true</forward>
           <unknown-unicast-flood>true</unknown-unicast-flood>
           <arp-termination>false</arp-termination>
         <flood>true</flood>
        </bridge-domain>
        </bridge-domains>
     </config>
   """) %(string_input1)

    elif server_type_input == "9":
        payload = ("""
     <config>
     <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
     <interface>
       <name>%s</name>
	    <enabled>true</enabled>
	    <type xmlns:x="urn:opendaylight:params:xml:ns:yang:v3po">x:loopback</type>
	      <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
	      <address>
	        <ip>%s</ip>
 	        <prefix-length>24</prefix-length>
	      </address>
	      </ipv4>
	        <ethernet xmlns="urn:opendaylight:params:xml:ns:yang:v3po"> 
              <mtu>9216</mtu>
            </ethernet>
     </interface>
     </interfaces>
     </config>
   """) %(string_input1, string_input2)

    elif server_type_input == "10":
        payload = ("""
     <config>
     <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
     <interface>
        <name>%s</name>
        <enabled>false</enabled>
          <type xmlns:x="urn:ietf:params:xml:ns:yang:iana-if-type">x:ethernetCsmacd</type>
            <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
            <address>
            <ip>192.168.0.1</ip>
              <prefix-length>24</prefix-length>
            </address>
            </ipv4>
            <ethernet xmlns="urn:opendaylight:params:xml:ns:yang:v3po">
              <mtu>9216</mtu>
            </ethernet>
            </interface>
            <interface>
            <name>vxlan_tunnel0</name>
              <enabled>true</enabled>
              <type xmlns:x="urn:opendaylight:params:xml:ns:yang:v3po">x:vxlan-tunnel</type>
            <vxlan xmlns="urn:opendaylight:params:xml:ns:yang:v3po">
              <dst>%s</dst>
            <decap-next>l2-input</decap-next>
            <vni>14</vni>
            <encap-vrf-id>0</encap-vrf-id>
            <src>%s</src>
            </vxlan>
            <l2 xmlns="urn:opendaylight:params:xml:ns:yang:v3po">
            <bridge-domain>bridge-domain-14</bridge-domain>
            <split-horizon-group>1</split-horizon-group>
        <bridged-virtual-interface>false</bridged-virtual-interface>
        </l2>
     </interface>
     </interfaces>
     </config>
   """) %(string_input1, string_input2, string_input3)


    return payload

def func_to_use_edit_config(payload, server_type_input):
    try:
        response = m.edit_config(target='running', config=payload).xml
        print(type(response))
        print("response", response)
        time_now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        print("The time now is ", time_now)
        file_name = "edit_config.xml" + "_" + time_now
        print(file_name)
        text_file = open(file_name, "w")
        text_file.write(response)
        text_file.close()

    except RPCError as e:
        data = e._raw

    return response

def func_to_use_get_config(string_input1, string_input2, string_input3):
    payload = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <intf-items>
      <phys-items>
        <PhysIf-list/>
      </phys-items>
    </intf-items>
  </System>
</filter>
"""    
    try:
        response = m.get_config(target='running', config=payload).xml
        print(type(response))
        print("response", response)
        time_now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        print("The time now is ", time_now)
        file_name = "get_config.xml" + "_" + time_now
        print(file_name)
        text_file = open(file_name, "w")
        text_file.write(response)
        text_file.close()

    except RPCError as e:
        data = e._raw

if __name__ == '__main__':

    
    parser = ArgumentParser(description='Usage:')

    # script arguments
    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str, required=True,
                        help="Device Password (netconf agent password(Enter the device type in the
                        code as either nexus, junos or default))")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    args = parser.parse_args()

    # connect to netconf agent
    with manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         timeout=90,
                         hostkey_verify=False,
                         device_params={'name': 'nexus'}) as m:
    
        function_to_invoke_get_and_edit_config()
 
