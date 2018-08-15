##########################################################################################################
#### Name : "Traffic.tcl"
#### Description : This script can be used to send UDP , TCP or Multicast Traffic
####
#############################################################################################################

#Sourcing of lib files
source "$::env(VELOLIBPATH)/global_lib.tcl"
source "$::env(VELOLIBPATH)/stc_lib.exp"
source "$::env(VELOLIBPATH)/nms_lib.tcl"

proc start_main {} {

global_scope

set testcase_name "Traffic.tcl"
set chkpt_file "$time_dir/Traffic_chk_[pid].txt"
#opening the file to update the check point file
set fp1 [ open $chkpt_file "w"]
close $fp1


#TEST SETUP
set timeout 30
# Dummy telnet session to update result
catch {i_sp_telnet_session $NMSIPADDR $idirect_user $idirect_pwd 23 dummytelnet} err

# Getting the build versions of all components
getbuildofallcomponents

#Pre condition Validation
global REMOTES
set REMOTES $REMOTEIP
# check for network status, can be disabled when developing test
if {![info exists DEBUG_RUN]} \
{
    foreach remoteip $REMOTEIP {
        if {[ pingipaddr $remoteip ]} {
            update_result "Remote State" PASS "Precondition:Able to ping Remote"
            pr_stdout "Precondition:Able to ping remote" GREEN
            pr_chkpt "$chkpt_file" "REMOTESTATE" "PASS" "Precondition:Able to ping remote"
        } else {
            update_result "Remote State" FAIL "Precondition Failed:Unable to ping Remote"
            pr_stdout "Precondition:Unable to ping Remote" RED
            pr_chkpt "$chkpt_file" "REMOTESTATE" "FAIL" "Precondition Failed:Unable to ping Remote"
            script_exit $chkpt_file $testcase_name
        }
    }
}
#MAIN
if {![info exists TRAFFIC_GROUP] } {
	puts "Running $TRAFFIC_TYPE Traffic"
	update_result "Traffic Test" INFO "Running $TRAFFIC_TYPE Traffic"
} else {
	update_result "Traffic Test" INFO "Running $TRAFFIC_TYPE Traffic ($TRAFFIC_GROUP)"
}


if { $TRAFFIC_TYPE == "TCP" } {
#	if {[catch {invoke_crc} err]} {
#                update_result "Validate CRC Error" FAIL "$err"
#                pr_stdout "Validate CRC Error: $err" RED
#                pr_chkpt "$chkpt_file" "Validate CRC Error" "FAIL" "$err"
#        }

	if {[catch {run_tcp_traffic "Traffic/Traffic_chk.txt"} err]} {
		update_result "Validate TRAFFIC" FAIL "$err"
		pr_stdout "Validate TRAFFIC: $err" RED
		pr_chkpt "$chkpt_file" "Validate TRAFFIC:" "FAIL" "$err"	
	}
	
	#resultFromChkpt "$::env(VELOSCRPATH)/L1Stats/L1Stats_LC_chk.txt"
	               
	update_result "TCP Traffic" "INFO" "TCP Traffic Completed"
}
if { $TRAFFIC_TYPE == "UDP" } {

#	if {[catch {invoke_crc} err]} {
#                update_result "Validate CRC Error" FAIL "$err"
#                pr_stdout "Validate CRC Error: $err" RED
#                pr_chkpt "$chkpt_file" "Validate CRC Error" "FAIL" "$err"
#        }

	if {[catch {run_traffic "Traffic/Traffic_chk.txt"} err]} {
		update_result "Validate TRAFFIC" FAIL "$err"
		pr_stdout "Validate TRAFFIC: $err" RED
		pr_chkpt "$chkpt_file" "Validate TRAFFIC:" "FAIL" "$err"	
	}                
	
	#resultFromChkpt "$::env(VELOSCRPATH)/L1Stats/L1Stats_LC_chk.txt"
	
	update_result "UDP Traffic" "INFO" "UDP Traffic Completed"
	
	if {$CONFIG_SELENIUM == "YES"} {
		puts "Start selenium script"
		set SelWindowsPC [check_if_selenium_running $pc "/tmp"]
		 

		set cfg [ open "$::env(VELOTOOLPATH)/seleniumrun.bat" "w"]
		set t [ clock seconds]
		set h [ clock format $t -format "%D%H%M%S"]
		puts $cfg "Test Started: $h"
		puts $cfg "del SYNCUP"
		puts $cfg "cd c:\\Users\\testteam-5\\Tracing\\Selenium\\Selenium"
		set h [string trim $h ":-_"]
		set h [regsub -all {/} $h ""]
		puts $cfg "mkdir -p C:\\Selenium\\rep\\UDP_Stats_$h"   
		puts $cfg "ant clean compile run -Dtest_file=StatsEvents/UDP_Stats -Drep_dir=UDP_Stats_$h"
		puts $cfg "echo \"Testing..\" >> SYNCUP"
		puts $cfg "del c:\\Selenium\\test\\seleniumrun.bat"
		close $cfg

		putfile -IPADDR $pc -USERNAME $USERNAME -PASSWD $PASSWORD -LFILENAME $::env(VELOTOOLPATH)/seleniumrun.bat -RFILENAME /cygdrive/c/Selenium/test/seleniumrun.bat

		putfile -IPADDR $pc -USERNAME $USERNAME -PASSWD $PASSWORD -LFILENAME $::env(VELOTOOLPATH)/gettime.tcl -RFILENAME /cygdrive/c/Selenium/test/gettime.tcl
		sleep 5

		i_ssh_session $pc $USERNAME $PASSWORD "Test PC"
		send "expect /cygdrive/c/Selenium/test/gettime.tcl\n"
		expect "$ "
		send "/n"

		waitforseleniumtoFinish "Demo" 60 $pc 

		getfile -IPADDR $pc -USERNAME $USERNAME -PASSWORD $PASSWORD -LFILENAME  "$i_DEST/UDP_Stats_$h" -RFILENAME /cygdrive/c/Selenium/rep/UDP_Stats_$h
		getfile -IPADDR $pc -USERNAME $USERNAME -PASSWORD $PASSWORD -LFILENAME  "$i_DEST/UDP_Stats_$h" -RFILENAME /cygdrive/c/Selenium/rep/out.txt
		getfile -IPADDR $pc -USERNAME $USERNAME -PASSWORD $PASSWORD -LFILENAME  "$i_DEST/UDP_Stats_$h" -RFILENAME /cygdrive/c/Selenium/rep/UDP_Stats_*.jpg
		
		resultFromChkpt "$i_DEST/UDP_Stats_$h/out.txt"
	}
}
if { $TRAFFIC_TYPE == "IPV6" } {
	if {[catch {run_traffic_ipv6 "Traffic/Traffic_chk.txt"} err]} {
		update_result "Validate TRAFFIC" FAIL "$err"
		pr_stdout "Validate TRAFFIC: $err" RED
		pr_chkpt "$chkpt_file" "Validate TRAFFIC:" "FAIL" "$err"	
	}                
	update_result "IPv6 Traffic" "INFO" "IPv6 Traffic Completed"
}
if { $TRAFFIC_TYPE == "SIP" } {
	#Validation for Same ip in list
	foreach val $SRCIP {
		if {[regexp $val $DSTIP]} {
			update_result "Validate SIP TRAFFIC" FAIL "Duplicate ip $val not allowed in SIP traffic. Source and destination ip for bi direction traffic should be different"
			pr_stdout "Validate SIP TRAFFIC: Duplicate ip $val not allowed in SIP traffic. Source and destination ip for bi direction traffic should be different" "RED"
			pr_chkpt "$chkpt_file" "Validate SIP TRAFFIC:" "FAIL" "Duplicate ip $val not allowed in SIP traffic. Source and destination ip for bi direction traffic should be different"	
			update_result "Validate SIP TRAFFIC" "INFO" "SIP Traffic Completed"
			script_exit $chkpt_file $testcase_name
	
		}
	}
	if {[catch {run_traffic_sip "Traffic/Traffic_chk.txt"} err]} {
		update_result "Validate SIP TRAFFIC" FAIL "$err"
		pr_stdout "Validate SIP TRAFFIC: $err" RED
		pr_chkpt "$chkpt_file" "Validate SIP TRAFFIC:" "FAIL" "$err"	
	}                
	update_result "Validate SIP TRAFFIC" "INFO" "SIP Traffic Completed"
}
if { $TRAFFIC_TYPE == "MULTICAST" } {

	for {set i 0} {$i < [llength $TERMSERVER_PORT]} {incr i;} {
		if { [catch {set connected [i_sp_telnet_session [lindex $TERMSERVER $i] $idirect_root $idirect_pwd [expr [lindex $TERMSERVER_PORT $i] + 10000] rmtlog$i]} err]} {
			update_result "Login to Term Console of RMT" FAIL "Unable to login to term port [expr [lindex $TERMSERVER_PORT $i] + 10000]"
			pr_stdout "Login to Term Console of RMT:Unable to login to term port [expr [lindex $TERMSERVER_PORT $i] + 10000]" RED
			pr_chkpt "$chkpt_file" "Login to Term Console of RMT" "FAIL" "Unable to login to term port [expr [lindex $TERMSERVER_PORT $i] + 10000]"
			script_exit $chkpt_file $testcase_name
		}
	}
	run_mcast_traffic $FPS $PS "FIXED" $REMOTES $chkpt_file $CFGMCAST $CLEANMCAST
	update_result "Multicast" "INFO" "Multicast Traffic Completed"
	
}
if { $TRAFFIC_TYPE == "SIMULTANEOUS" } {
	if {[regexp "mcast" $TRAFFIC_GROUP]}  {
		for {set i 0} {$i < [llength $TERMSERVER_PORT]} {incr i;} {
			if { [catch {set connected [i_sp_telnet_session [lindex $TERMSERVER $i] $idirect_root $idirect_pwd [expr [lindex $TERMSERVER_PORT $i] + 10000] rmtlog$i]} err]} {
				update_result "Login to Term Console of RMT" FAIL "Unable to login to term port [expr [lindex $TERMSERVER_PORT $i] + 10000]"
				pr_stdout "Login to Term Console of RMT:Unable to login to term port [expr [lindex $TERMSERVER_PORT $i] + 10000]" RED
				pr_chkpt "$chkpt_file" "Login to Term Console of RMT" "FAIL" "Unable to login to term port [expr [lindex $TERMSERVER_PORT $i] + 10000]"
				script_exit $chkpt_file $testcase_name
			}
		}
	}
	pr_stdout "Simultaneous traffic $TRAFFIC_GROUP " BLUE
	if {[catch {run_simultaneous_traffic "Traffic/Traffic_chk.txt"} err]} {
		update_result "Validate TRAFFIC" FAIL "$err"
		pr_stdout "Validate TRAFFIC: $err" RED
		pr_chkpt "$chkpt_file" "Validate TRAFFIC:" "FAIL" "$err"	
	}	
	update_result "SIMULTANEOUS" "INFO" "SIMULTANEOUS Traffic Completed"
}		

#script_exit $chkpt_file $testcase_name
}

if {[catch {start_main} err]} {
	puts $err
	update_result "Script Status " FAIL "Completed with runtime exception:$err"
	i_script_exit
} else {
	update_result "Script Status" INFO "Completed"	
	pr_stdout "Script finished..Exiting"
	exit
}

