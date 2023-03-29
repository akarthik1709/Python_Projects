"""
   Parse QoS statistics such as throughput and jitter from Spirent traffic measurement, 
   apply criteria, and report testing result
   
   input:  1. a list of remotes: e.g. remote_list = ['e8350', 'x1', 'x3', 'x7', 'x5-A', 'x5-B']
           2. a list of priority ("default" or "not_default"): 
              "default" -- all applications running in the remote are of equal priority
              "not_default" -- all applications running in the remote are of equal priority
              e.g. priority_list = ['default', 'not_default', 'default', 'default', 'default', 'not_default']
           3. statistics file: a csv file 
           4. criteria file: a csv file
           4. criteria file: a csv file
           5. test case: an integer indicating which test case
                              
   Output: a dictionary, e.g
 
          (1) Test passes 
             {
                'Grade'             :  'Pass',
                'Num_of_VRMT_Pass'  :  18,
                'Num_of_VRMT"       :  18,
                'Info_of_Fail"      :  []
             } 
             
          (2) Test fails
             {
                'Grade'             :  'Fail',
                'Num_of_VRMT_Pass'  :  17,
                'Num_of_VRMT"       :  18,
                'Info_of_Fail"      :  [{'expected': 45000, 'actual': 65.4, 'Name':'x3_Voip_Jitter']
             }
             which means Voip application in remote x3 fails due to high jitter (65.4>45000)

   Usage:
           1. Create an object  :  obj = processQosResult()
           2. Do setup          :  obj.setup(remote_list, priority_list, "statistics.csv", "criteria.csv", 1)
           3. Parse statistics  :  obj.parseQosStats()
           4. Report test result:  report = obj.getQosReport() where the output is a dictionary
           For each test case, 2, 3, and 4 is repeated                         
"""
import os
import pandas as pd
import numpy as np
from robot.libraries.BuiltIn import BuiltIn
from robot.errors import ExecutionFailed

class QoS_Spirent_Parse:
    """
    Configure testing parameters:
        - Arguments
            - remote_list           : list of remotes
            - priority_list         : list of settings ("default" or "not_default") regarding priority equality
            - qos_stats_file_name   : file of Spirent traffic statistics 
            - qoa_criteria_file_name: file of pass/fail criteria
            - test_case             : integer number starting with 1 to indicate which test case
        - Return
            None  
    """
    def setup(self, remote_list, priority_list, qos_stats_file_name, qos_criteria_file_name, test_case):

        self.remote_list = remote_list
        self.priority_list = priority_list
        self.qos_stats_file_name = qos_stats_file_name
        self.qos_criteria_file_name = qos_criteria_file_name
        self.test_case = int(test_case)
        self.objerr = None
        self.grade = dict()
        self.stat_list = ["AvgLatency", "AvgJitter", "BitRate", "DroppedFramePercentRate"]

    """
    Calculate total throughput in one remote
        - Arguments
           - remote     : remote
           - application: list of applications running in one remote
        - Return
          Throughput
    """    
    def sumThroughput(self, remote, applications):
        total = 0
        for app in applications:
            column_heading = remote + "_" + app + "_" + "BitRate"
            org = self.df_stat[column_heading].tolist()
            data = ['0' if x == 'N/A' else x for x in org]
            total += np.mean([float(i) for i in data])
        return total        
    
    """
    Apply pass/fail criteria to QoS statistics
        - Arguments
           - measurement: QoS statistics value
           - criteria: pass/fail criteria
           - app: application
           - stat: QoS statistics name
           - test_case: test case integer
           - priority: "default" or "not_default"
        - Return
           True : if the criteria is met
           Fasle: otherwise 
    """ 
    def applyCriteria(self, measurement, criteria, app, stat, test_case, priority,column_heading):
       passCriteria = False; 
       test_case = int(test_case)
       if test_case == 1 or test_case == 2:
           if stat == "BitRate":
              self.verify_should_be_true(str(measurement) + ">=" + str(criteria), str(column_heading) + " value "+ str(measurement) + " is not greater than or equal to criteria " + str(criteria))
              if measurement >= criteria:      
                  passCriteria = True
           elif stat == "AvgJitter":
              if self.MIR_is_capped:           # capped with MIR
                  if app != "VOIP":
                      passCriteria = True
                  else:
                      self.verify_should_be_true(str(measurement) + "<=" + str(criteria), str(column_heading) + " value " +
                                                 str(measurement) + " is not lesser than or equal to criteria "
                                                 + str(criteria) + " when VOIP MIR is capped")
                      if measurement <= criteria:
                          passCriteria = True
              else:  
                  # not capped with MIR                          
                  self.verify_should_be_true(str(measurement) + "<=" + str(criteria), str(column_heading) + " value " + str(measurement) + " is not lesser than or equal to criteria " + str(criteria) + " when VOIP MIR is not capped")
                  if measurement <= criteria:
                      passCriteria = True               
           elif stat == "AvgLatency":
                  passCriteria = True
           elif stat == "DroppedFramePercentRate":
              if self.MIR_is_capped:
                  passCriteria = True 
              else:
                  criteria = 0
                  self.verify_should_be_true(str(measurement) + "==" + str(criteria), str(column_heading) + " value " +
                                             str(measurement) + " is not equal to criteria " + str(criteria))
                  if measurement == criteria:           # no packet loss
                      passCriteria = True
       elif test_case == 3 or test_case == 4:
           if stat == "BitRate":
              self.verify_should_be_true(str(measurement) + ">=" + str(criteria), str(column_heading) + " value " +
                                         str(measurement) + " is not greater than or equal to criteria" +
                                         str(criteria))
              if measurement >= criteria:
                  passCriteria = True
           elif stat == "AvgJitter":
                if priority == "default":              # each appliction has the same priority
                    if self.MIR_is_capped:             # remote capped with MIR
                        if app != "VOIP":              # application: Data or Default
                            passCriteria = True
                        else:                          # application: Voip
                           self.verify_should_be_true(str(measurement) + "<=" + str(criteria), str(column_heading) + " value " + str(measurement)
                                                      + " is not lesser than or equal to criteria " + str(criteria)
                                                      + " when VOIP MIR is capped for " + str(priority) + " priority")
                           if measurement <= criteria:
                               passCriteria = True
                    else:                              # remote not capped with MIR
                        self.verify_should_be_true(str(measurement) + "<=" + str(criteria), str(column_heading) + " value " + str(measurement)
                                                   + " is not lesser than or equal to criteria " + str(criteria)
                                                   + " when VOIP MIR is not capped for " + str(priority) + " priority")
                        if measurement <= criteria:
                            passCriteria = True
                else:
                    self.verify_should_be_true(str(measurement) + "<=" + str(criteria), str(column_heading) + " value " + str(measurement)
                                               + " is not lesser than or equal to criteria " + str(criteria)
                                               + " for " + str(priority) + " priority")
                    if measurement <= criteria:
                        if app == "VOIP":             # Voip with the highest priority
                            condition = np.allclose(measurement, np.amin(self.priority_dict))
                            self.verify_should_be_true(condition, "Voip with the highest priority")
                            if condition:
                                passCriteria = True
                        elif app == "DEFAULT":         # Default with the lowest priority
                            condition = np.allclose(measurement, np.amax(self.priority_dict))
                            self.verify_should_be_true(condition, "Default with the lowest priority")
                            if condition:
                                passCriteria = True
                        elif app == "DATA": 
                            # Data with the middel priority
                            condition = measurement >= np.amin(self.priority_dict) and measurement <= np.amax(self.priority_dict)
                            self.verify_should_be_true(condition, " Data with the middel priority")
                            if condition:
                                passCriteria = True
           else:                                       #     == "AvgLatency" or "DroppedFramePercentRate"
               passCriteria = True
       return passCriteria
    
    """
    Parse Qos statistics
        - Arguments
          None 
        - Return
          True : if parsing is successful
          False: otherwise
    """
    def parseQosStats(self):
        # read qos statistics, and qos pass/fail criteria
        BuiltIn().should_be_true(os.path.isfile(self.qos_stats_file_name) , "File not Found")
        BuiltIn().should_be_true(os.path.isfile(self.qos_criteria_file_name) , "criteria File not found")

        if len(self.remote_list) != len(self.priority_list):
            BuiltIn().log("list is not matching",level="ERROR",html=True,console=True)
            return False

        self.df_stat = pd.read_csv(self.qos_stats_file_name)
        self.df_criteria = pd.read_csv(self.qos_criteria_file_name)

        app_list = list(["VOIP", "DATA", "DEFAULT"])
        stat_list = list(["AvgLatency", "AvgJitter", "BitRate", "DroppedFramePercentRate"])
        
        result_lst = list()
        app_lst = list()        
        # iterate through remote 	
        for i in range(len(self.remote_list)):
            remote = self.remote_list[i]
            priority = self.priority_list[i]
            column_heading = remote + "_" + "MIR"
            MIR = self.df_criteria[column_heading].tolist()[self.test_case-1]
            MIR_tolerance = self.df_criteria[column_heading+"_"+"Tolerance"].tolist()[self.test_case-1] 
            self.MIR_is_capped = False
            if MIR != "infinite":
                self.MIR_is_capped = True
                throughput_sum = self.sumThroughput(remote, app_list)

            self.priority_dict = list()
            if priority == "not_default":
                for app in app_list:
                    index = remote + "_" + app + "_" + "AvgJitter"
                    org = self.df_stat[index].tolist()
                    data = ['0' if x == 'N/A' else x for x in org]
                    self.priority_dict.append(np.mean([float(i) for i in data]))
            
            # iterate through application per remote
            for app in app_list:       #iterate through qos stats per application per remote
                for stat in stat_list:
                    column_heading = remote + "_" + app + "_" + stat
                    if stat == "BitRate" and MIR != "infinite":
                        measure = throughput_sum
                        criteria = MIR - MIR_tolerance
                    else:
                        org = self.df_stat[column_heading].tolist()
                        data = ['0' if x == 'N/A' else x for x in org]
                        measure = np.mean([float(i) for i in data])
                        if stat == "AvgJitter":
                            criteria = 47000   # tolerance = 2000
                        elif stat == "DroppedFramePercentRate" or stat == "AvgLatency":
                            criteria = 0
                        else:
                            CIR = self.df_criteria[column_heading].tolist()[self.test_case-1]
                            CIR_tolerance = self.df_criteria[column_heading+"_"+"Tolerance"].tolist()[self.test_case-1]
                            criteria = CIR - CIR_tolerance
                    ret = self.applyCriteria(measure, criteria, app, stat, self.test_case, priority,column_heading)
                    result_lst.append(ret)
                    app_lst.append(column_heading)
        self.grade["data"] = result_lst
        self.grade["apps"] = app_lst
        if self.objerr:
            err = self.objerr
            self.objerr = None
            raise err
        return True

    """
    Report QoS test result as "Pass" or "Fail"
        - Arguments
          None
    """
    def getQosResult(self):
        data = self.grade["data"]
        stat_number = len(self.stat_list)
        apps_number = len(data)/stat_number
        pass_number = 0
        for i in range(apps_number):
            true_number = 0
            for j in range(stat_number):
                true_number += data[i * stat_number + j]
            if int(true_number) == int(stat_number):
                pass_number += 1
        report = dict()
        report["Num_of_VRMT_Pass"] = pass_number
        report["Num_of_VRMT"] = apps_number
        report["Info_of_Fail"] = list()
        indice = [i for i, x in enumerate(self.grade['data']) if x == False]
        fail_detail = dict()
        for idx in indice:
            #report["Info_of_Fail"].append(self.grade['apps'][idx])            
            #report["Info_of_Fail"].append(self.grade['apps'][idx])
            column_heading = self.grade['apps'][idx]
            org = self.df_stat[column_heading].tolist()
            data = ['0' if x == 'N/A' else x for x in org]    
            actual_value = np.mean([float(i) for i in data])
            if column_heading.find("Jitter") != -1:
                expected_value = 47000
            elif column_heading.find("Dropped") != -1:
                expected_value = 0
            else:
                expected_value = self.df_criteria[column_heading].tolist()[self.test_case - 1]
            fail_detail = { "Expected" : expected_value, "Actual" : actual_value, "Name" : column_heading}
            report["Info_of_Fail"].append(fail_detail)
        s = ""
        if pass_number == apps_number:
            report["Grade"] = "Pass"
        else:
            report["Grade"] = "Fail"
            for key in report['Info_of_Fail']:
                s+=str(key)+"\n"
                # s+=("Expected criteria value :" + str(key['Expected'])+",\tActual value: " +str(key['Actual']) + ",\tRemote :" + str(key['Name']) + "\n" )        
        BuiltIn().should_be_true(report["Grade"] == "Pass","Consolidated failed - Output stats : \n" + str(s))
        return report

    def verify_should_be_true(self, condition, msg):
        try:
            BuiltIn().run_keyword_and_continue_on_failure("should_be_true", condition, "Mismatch Stats Found")
        except ExecutionFailed as err:
            self.objerr=err
            BuiltIn().log(str(msg), level="ERROR", html=True)
