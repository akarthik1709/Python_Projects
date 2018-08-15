
testsetupLayout.cells("b").attachObject("form1");

//****************************************************************************************************************************************
//createFormLayout - function that creates a Form with configuration parameters
//****************************************************************************************************************************************
	function createFormLayout(scriptName)
	{
		//Form Setting initialization
		formInput = "{\"type\": \"settings\", \"position\": \"label-left\",	\"labelWidth\": \"90\", \"inputWidth\": \"160\", \"labelAlign\": \"center\"}~";
		//Clearing existing form, if any
		document.getElementById("myForm").innerHTML="";
		
		if(scriptName.match("Traffic")!=null) //Create config part for Traffic
		{
			designFrame("fieldset","General Login Password",350);
			designForm("input","PASSWORD","pwd","iDirect",true);
			designFrame("fieldclose","",""); //fieldset ends here

			designFrame("fieldset","Traffic Config",300); 
			designForm("checkbox","TCP","tcp","TCP",true);
			designForm("checkbox","UDP","udp","UDP",true);
			designForm("checkbox","SIP","sip","SIP",true);
			designForm("checkbox","MULTICAST","mcast","MULTICAST",true);
			designForm("input","REMOTE IP","rmt_ip","x.x.x.x",true);
			designFrame("fieldclose","",""); //fieldset ends here			
			designFrame("fieldset","MULTICAST Config",300); 			
			formInput += "{\"type\": \"combo\",\"label\": \"CFGMCAST\",\"name\": \"cfgmcast\", \"options\": [{ \"text\": \"YES\", \"value\": \"YES\" },{ \"text\": \"NO\", \"value\": \"NO\",\"selected\": \"true\"}]},";					formInput += "{\"type\": \"combo\",\"label\": \"CLEAN_MCAST_CONFIG\",\"name\": \"cleanmcast\", \"options\": [{ \"text\": \"YES\", \"value\": \"YES\" },{ \"text\": \"NO\", \"value\": \"NO\",\"selected\": \"true\"}]},";	
			designForm("input","REMOTE NAME","rmt_name","",true);
			designForm("input","PP SERVER BLADE SVN IP","pp_ip","",true);
			designFrame("fieldclose","",""); //fieldset ends here
			
			designFrame("fieldset","Selenium Config",350);
			formInput += "{\"type\": \"combo\",\"label\": \"CONFIG_SELENIUM\",\"name\": \"CONFIG_SELENIUM\", \"options\": [{ \"text\": \"YES\", \"value\": \"YES\" },{ \"text\": \"NO\", \"value\": \"NO\",\"selected\": \"true\"}]},";
			designForm("input","PC IP","PC_IP","",true);
			designForm("input","USERNAME","USERNAME","",true);
			designForm("input","PASSWORD","PASSWORD","",true);
			designFrame("fieldclose","",""); //fieldset ends here
		}		
		formData1 = formInput.split("~");
		//parsing inputs to create form
		for(var count=0;count<formData1.length-1;count++)
		{
			formData1[count]=JSON.parse(formData1[count]);
		}
		//add form to GUI
		myForm = new dhtmlXForm("myForm", formData1);			
			
	}

//****************************************************************************************************************************************
//saveFormLayout - function that saves a Form with configuration parameters
//****************************************************************************************************************************************
	function saveFormLayout(scriptName)
	{
		var flag=false;
		//functionality defined in iDXweb/js/configInterface.js
		saveFileAndPath();		
		
		//Config file creation start here
		
		//global variables
		trafficlist = '';
		cfgValues = '';
		cfgValues += "%0Aglobal NMSIPADDR MAIL_LIST MAIL_RESULTS i_DEST%0A";
		if(scriptName.match("Traffic")!=null)
		{
			
			var TCPChecked = false,UDPChecked = false,MCASTChecked = false;
			cfgValues += "%0Aglobal idirect_pwd REMOTEIP REMOTES CFGMCAST CLEANMCAST PPIPADDR TRAFFIC_GROUP%0A";
			cfgValues += "%0Aglobal HUBPORT REMOTEPORT stc_ChassisAddr TESTTIME STREAMNAME SRCIP SRCGW SRCMASK DSTIP DSTGW DSTMASK FPS PS VLANID REMOTES";
			cfgValues += "%0Aglobal DIR FRAMELENGTHMODE WEIGHTS NOOFCONNECTIONS FILESIZE TRAFFIC_TYPE NOOFSIPCALLS";
			cfgValues += "%0Aglobal RMTHOSTIPLIST RMTHOSTGWLIST MCASTGROUPIP CONFIG_SELENIUM pc USERNAME PASSWORD%0A";				
		}
		//COMMON LIST ******************
		cfgValues += "%0Aset idirect_pwd \""+myForm.getItemValue("pwd")+"\"";
		cfgValues += "%0A%0Aset NMSIPADDR \""+window.nwtreeTb.getValue("nmsip")+"\"";
		cfgValues += "%0Aset MAIL_LIST \""+suiteToolbar.getValue("Email")+"\"%0Aset MAIL_RESULTS NO%0Aset i_DEST \""+configTb.getValue("Path")+"\"";
		if(scriptName.match("Traffic")!=null)
		{
			
			TCPChecked = myForm.isItemChecked("tcp");
			UDPChecked = myForm.isItemChecked("udp");		
			MCASTChecked = myForm.isItemChecked("mcast");	
			SIPChecked = myForm.isItemChecked("sip");	
			traffictype = "SIMULTANEOUS";		
			if (UDPChecked && !TCPChecked && !MCASTChecked && !SIPChecked) {
				traffictype = "UDP";				
			}
			if (!UDPChecked && TCPChecked && !MCASTChecked && !SIPChecked) {
				traffictype = "TCP";				
			}
			if (!UDPChecked && !TCPChecked && MCASTChecked&& !SIPChecked) {
				traffictype = "MULTICAST";				
			}
			if (!UDPChecked && !TCPChecked && MCASTChecked&& SIPChecked) {
				traffictype = "SIP";				
			}
			if (UDPChecked) {
				trafficlist = trafficlist + "udp" + " ";
			}
			if (TCPChecked) {
				trafficlist = trafficlist + "tcp" + " ";
			}
			if (MCASTChecked) {
				trafficlist = trafficlist + "mcast" + " ";
			}	
			if (SIPChecked) {
				trafficlist = trafficlist + "sip" + " ";
			}		
			cfgValues += "%0Aset TRAFFIC_TYPE \""+traffictype+"\"";
			cfgValues += "%0Aset TRAFFIC_GROUP \{"+trafficlist+"}";
			cfgValues += "%0Aset CFGMCAST \""+myForm.getItemValue("cfgmcast")+"\"";
			cfgValues += "%0Aset CLEANMCAST \""+myForm.getItemValue("cleanmcast")+"\"";
			cfgValues += "%0Aset REMOTEIP  \""+myForm.getItemValue("rmt_ip")+"\"";
			cfgValues += "%0Aset REMOTES  \""+myForm.getItemValue("rmt_name")+"\"";
			cfgValues += "%0Aset PPIPADDR  \""+myForm.getItemValue("pp_ip")+"\"";
			cfgValues += "%0Aset CONFIG_SELENIUM  \""+myForm.getItemValue("CONFIG_SELENIUM")+"\"";
			cfgValues += "%0Aset pc  \""+myForm.getItemValue("PC_IP")+"\"";
			cfgValues += "%0Aset USERNAME  \""+myForm.getItemValue("USERNAME")+"\"";
			cfgValues += "%0Aset PASSWORD  \""+myForm.getItemValue("PASSWORD")+"\"";
			//Saving Spirentinputs  
			cfgValues += "%0A%0A";
			if(saveSpirentInputs(TCPChecked,UDPChecked,MCASTChecked,SIPChecked) == 1) {
				alert("Spirent inputs are not present, Please navigate to \"spirent test centre\" tab");
				return
			}	
			cfgValues += "%0A%0Aif 0 {selectMethod Traffic Traffic_GUI.js VELOLIBPATH+"/Traffic/}%0A";
			
		}
		if(!flag)
		{
			var out = dhtmlxAjax.getSync("FilesManager/php/saveFile.php?filename="+filename+"&location="+path+"&arr="+cfgValues+"&ext=cfg");
		}
	}	
	
//*************************************************************************************************************************************************************************
//reloadFormLayout - function that reloads a Form with configuration parameters. Function called automatically from selectFeatureReload() in "iDXweb/js/configInterface.js"
//*************************************************************************************************************************************************************************
	function reloadFormLayout(scriptName)
	{
		//Checks if Spirent is required for this script while reloading
		spirentRequirementCheck();	
		spirentPreReload();	
		//creates form first - function defined at the top of the file
		createFormLayout(scriptName);		
		passPath = scriptName;		
		if(typeof String.prototype.trim !== 'function') {
		  String.prototype.trim = function() {
			return this.replace(/^\s+|\s+$/g, ''); 
		  }
		}	
		myForm.setItemValue("udp",false);
		myForm.setItemValue("tcp",false);
		myForm.setItemValue("mcast",false);
		myForm.setItemValue("sip",false);
		var flagUDP1 = false,flagTCP1 = false,flagSIP1 = false,flagMC1 = false;
		var filteredResponse = new Array();
		for(var count=0; count<storeResponse.length;count++)
		{
			compareString = storeResponse[count];							
			if(scriptName.match("Traffic")!=null) //config reload part for Traffic
			{							
				if(compareString.match("TRAFFIC_GROUP {")!=null)
				{					
					filteredResponse = storeResponse[count].split("TRAFFIC_GROUP ");
					compareString = filteredResponse[1];										
					if(compareString.match("tcp") !=null) {
						myForm.setItemValue("tcp",true);
						flagTCP1 = true;
					}
					if(compareString.match("udp") !=null) {
						myForm.setItemValue("udp",true);
						flagUDP1 = true;
					}
					if(compareString.match("mcast") !=null) {
						myForm.setItemValue("mcast",true);
						flagMC1 = true;
					}
					if(compareString.match("sip") !=null) {
						myForm.setItemValue("sip",true);
						flagSIP1 = true;
					}
				}
				else if(compareString.match(/TRAFFIC_TYPE "/g)!=null)
				{
					filteredResponse = storeResponse[count].split("TRAFFIC_TYPE ");
					compareString = filteredResponse[1];					
					if(compareString.match(/TCP/) !=null) {
						myForm.setItemValue("tcp",true);
						myForm.setItemValue("udp",false);
						myForm.setItemValue("mcast",false);
						myForm.setItemValue("sip",false);
						flagTCP1 = true;
					}
					if(compareString.match(/UDP/) !=null) {
						myForm.setItemValue("udp",true);
						myForm.setItemValue("tcp",false);
						myForm.setItemValue("mcast",false);
						myForm.setItemValue("sip",false);
						flagUDP1 = true;
					}
					if(compareString.match(/MULTICAST/) !=null) {
						myForm.setItemValue("mcast",true);
						myForm.setItemValue("udp",false);
						myForm.setItemValue("tcp",false);
						myForm.setItemValue("sip",false);
						flagMC1 = true;
					}
					if(compareString.match(/SIP/) !=null) {
						myForm.setItemValue("mcast",false);
						myForm.setItemValue("udp",false);
						myForm.setItemValue("tcp",false);
						myForm.setItemValue("sip",true);
						flagSIP1 = true;
					}
				
				}
				else if(compareString.match(/CFGMCAST "/g)!=null)
				{
					filteredResponse = storeResponse[count].split("CFGMCAST ");
					compareString = filteredResponse[1];					
					if (compareString.match(/YES/)) 
						myForm.setItemValue("cfgmcast","YES");
					if (compareString.match(/NO/)) 
						myForm.setItemValue("cfgmcast","NO");
				}
				else if(compareString.match(/CONFIG_SELENIUM "/g)!=null)
				{
					filteredResponse = storeResponse[count].split("CONFIG_SELENIUM ");
					compareString = filteredResponse[1];					
					if (compareString.match(/YES/)) 
						myForm.setItemValue("CONFIG_SELENIUM","YES");
					if (compareString.match(/NO/)) 
						myForm.setItemValue("CONFIG_SELENIUM","NO");
				}
				else if(compareString.match(/CLEANMCAST "/g)!=null)
                                {
                                        filteredResponse = storeResponse[count].split("CLEANMCAST ");
                                        compareString = filteredResponse[1];
                                        if (compareString.match(/YES/))
                                                myForm.setItemValue("cleanmcast","YES");
                                        if (compareString.match(/NO/))
                                                myForm.setItemValue("cleanmcast","NO");
                                }
				else if(compareString.match(/NMSIPADDR /g)!=null)
				{
					filteredResponse = storeResponse[count].split("NMSIPADDR ");	
					compareString = filteredResponse[1].trim();
					window.nwtreeTb.setValue("nmsip",compareString.replace(/"/g,""));
					var ipaddr = nwtreeTb.getValue("nmsip");
									
				}
				else if(compareString.match(/idirect_pwd/g)!=null)
				{	
				filteredResponse = storeResponse[count].split("idirect_pwd ");					
				compareString = filteredResponse[1].trim();										
				myForm.setItemValue("pwd",compareString.replace(/"/g,""));
				}
				else if(compareString.match(/MAIL_LIST/g)!=null)
				{
					filteredResponse = storeResponse[count].split("MAIL_LIST ");
					compareString = filteredResponse[1].trim();
					suiteToolbar.setValue("Email",compareString.replace(/"/g,""));
				}
				else if(compareString.match(/i_DEST/g)!=null)
				{
					filteredResponse = storeResponse[count].split("i_DEST");
					compareString = filteredResponse[1].trim();
					configTb.setValue("Path",compareString.replace(/"/g,""));
				}
				else if(compareString.match(/REMOTEIP /g)!=null)
				{
					filteredResponse = storeResponse[count].split("REMOTEIP ");					
					compareString = filteredResponse[1].trim();										
					myForm.setItemValue("rmt_ip",compareString.replace(/"/g,""));											
				}
				else if(compareString.match(/REMOTES /g)!=null)
				{
					filteredResponse = storeResponse[count].split("REMOTES ");					
					compareString = filteredResponse[1].trim();						
					myForm.setItemValue("rmt_name",compareString.replace(/"/g,""));											
				}
				else if(compareString.match(/pc /g)!=null)
				{
					filteredResponse = storeResponse[count].split("pc ");					
					compareString = filteredResponse[1].trim();						
					myForm.setItemValue("PC_IP",compareString.replace(/"/g,""));											
				}
				else if(compareString.match(/USERNAME /g)!=null)
				{
					filteredResponse = storeResponse[count].split("USERNAME ");					
					compareString = filteredResponse[1].trim();						
					myForm.setItemValue("USERNAME",compareString.replace(/"/g,""));											
				}
				else if(compareString.match(/PASSWORD /g)!=null)
				{
					filteredResponse = storeResponse[count].split("PASSWORD ");					
					compareString = filteredResponse[1].trim();						
					myForm.setItemValue("PASSWORD",compareString.replace(/"/g,""));											
				}
				else if(compareString.match(/PPIPADDR /g)!=null)
				{
					filteredResponse = storeResponse[count].split("PPIPADDR ");					
					compareString = filteredResponse[1].trim();						
					myForm.setItemValue("pp_ip",compareString.replace(/"/g,""));											
				}
				//functionality defined in iDXweb/js/spirentInterface.js			
				reloadSpirentInputs(count,flagUDP1,flagTCP1,flagMC1,flagSIP1);				
			}
			if(!flagUDP1) {
				for (var i=0;i<mygrid1.getRowsNum();i++) {
					mygrid1.deleteRow(mygrid1.getRowId(i));
				}
			}
			if(!flagTCP1) {
				for (var i=0;i<mygrid2.getRowsNum();i++) {
					mygrid2.deleteRow(mygrid2.getRowId(i));
				}
			}
			if(!flagMC1) {
				for (var i=0;i<mygrid3.getRowsNum();i++) {
					mygrid3.deleteRow(mygrid3.getRowId(i));
				}
			}
			if(!flagSIP1) {
				for (var i=0;i<mygrid4.getRowsNum();i++) {
					mygrid3.deleteRow(mygrid4.getRowId(i));
				}
			}				
		}
	}
