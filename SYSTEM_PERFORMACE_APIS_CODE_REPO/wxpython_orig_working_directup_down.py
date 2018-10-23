
# -*- coding: utf-8 -*-

# set_size.py

import wx
import test_python_script_network
import downstream_modified_gw_user_pair
import ipaddress
import sys
import random
import time
#import notify2
#import dbus

class Example(wx.Frame):

    def __init__(self, parent, title, message=''):
        super(Example, self).__init__(parent, title=title,
            size=(1000, 1000))
        self.Centre()
        self.InitUI()
        self.parent = parent
        self.dir_array=[]
        # self.parent.Update()
        self.Refresh()
        #self.on_timer()
        #self.Bind(wx.EVT_SIZE, self.OnSize)
        #self.Centre()
        #self.SetSize(1000, 1000)
        #self.Show(True)
        
    
    
    
    def on_timer(self):
        self.InitUI()
        wx.CallLater(5000, self.on_timer)
        #self.timer = wx.Timer(self)
	#self.Bind(wx.EVT_TIMER,self.InitUI())
	#self.timer.Start(1000) #10 minutes

    def ask(self, parent=None, message='', default_value=''):
        dlg = wx.TextEntryDialog(parent, message, caption="GetTextFromUserPromptStr")
        dlg.ShowModal()
        result = dlg.GetValue()
        dlg.Destroy()
        return result
    
    def InitUI(self):
        self.pnl = wx.Panel(self)

        self.sizer = wx.GridBagSizer(20, 20)
        self.Refresh()
        self.Update()
        itm_initui = self.sizer.FindItemAtPosition((0, 0))
        if (itm_initui!=None) and itm_initui.IsWindow():
            self.sizer.Detach(itm_initui.GetWindow())
        self.rb0 = wx.RadioButton(self.pnl,11, label = 'None',pos = (10, 10), style = wx.RB_GROUP) 
        self.rb1 = wx.RadioButton(self.pnl,11, label = 'Upstream',pos = (10, 30)) 
        #self.rb1.Bind(wx.EVT_RADIOBUTTON, self.layout_panel_downstream)
        
        self.Refresh()
        self.rb2 = wx.RadioButton(self.pnl,22, label = 'Downstream',pos = (10, 50)) 
        #self.rb2.Bind(wx.EVT_RADIOBUTTON, self.layout_panel_upstream)
        itm_initui1 = self.sizer.FindItemAtPosition((0, 0))
        if (itm_initui1!=None) and itm_initui1.IsWindow():
            self.sizer.Detach(itm_initui1.GetWindow())
        self.Refresh()
        self.UpdateWindowUI(wx.UPDATE_UI_FROMIDLE)
        #self.parent.Update()
        self.Layout() 
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)
        self.Refresh()
        self.rb2.Refresh()
        self.rb2.Update() 
        self.pnl.SetSizerAndFit(self.sizer) 
		
         
        
        lblList = ['Upstream', 'Downstream']
          
		  
        #self.rbox = wx.RadioBox(pnl, label = 'RadioBox', pos = (80,10), choices = lblList,
        #majorDimension = 1, style = wx.RA_SPECIFY_ROWS) 
    
        #self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
    def onChecked(self, e):
        try:
            self.cb = e.GetEventObject() 
            print self.cb.GetLabel(),' is clicked',self.cb.GetValue()
            print type(self.cb.GetLabel())

            if self.label_name == "Upstream" and self.cb.GetLabel() == "Default Downstream" and self.cb.GetValue() == True:
                raise IncorrectcomboError  
            elif self.label_name == "Downstream" and self.cb.GetLabel() == "Default Upstream" and self.cb.GetValue() == True:
                raise IncorrectcomboError

            if self.cb.GetValue() == True and self.cb.GetLabel() == "Default Upstream":
                print("I am inside if")
                self.st_up_default = wx.StaticText(self.pnl, label='# of Default Carriers')
                itmcomp124 = self.sizer.FindItemAtPosition((3, 4))
                if (itmcomp124 != None) and itmcomp124.IsWindow():
                    print("Inside if for detach 1 ")
                    self.sizer.Detach(itmcomp124.GetWindow())
                self.sizer.Add(self.st_up_default, pos=(3,4), flag=wx.ALL | wx.ALIGN_CENTER, border=15) 
                self.st_up_default_values = wx.StaticText(self.pnl, label='500, 1000, 1500, 2000, 3000, 5500, 7000, 7500')
                itmcomp125 = self.sizer.FindItemAtPosition((3, 5))
                if (itmcomp125 != None) and itmcomp125.IsWindow():
                    print("Inside if for detach 1 ")
                    self.sizer.Detach(itmcomp125.GetWindow())
                self.sizer.Add(self.st_up_default_values, pos=(3,5), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
                 
                itmcomp12 = self.sizer.FindItemAtPosition((10, 0))
                if (itmcomp12 != None) and itmcomp12.IsWindow():
                    print("Inside if for detach 1 ")
                    self.sizer.Detach(itmcomp12.GetWindow())
                    self.st8.Hide()
                itmcomp123 = self.sizer.FindItemAtPosition((10,1))
                if (itmcomp123 != None) and itmcomp123.IsWindow():
                    print("Inside if for detach 2")
                    self.sizer.Detach(itmcomp123.GetWindow())
                    self.combo1.Hide()

                itmcomp123t = self.sizer.FindItemAtPosition((10,2))
                if (itmcomp123t != None) and itmcomp123t.IsWindow():
                    print("Inside if for detach 2")
                    self.sizer.Detach(itmcomp123t.GetWindow())
                    self.st9a1.Hide()

                self.stlabel = wx.StaticText(self.pnl, label = 'These values are ommited since the default is running')
                #self.stlabel.SetValue("This section is omitted since the defaule is chosen")
                self.sizer.Add(self.stlabel, pos=(10, 0), span=(1,4), flag=wx.ALL, border=15)
                self.pnl.SetSizerAndFit(self.sizer)

            if self.cb.GetValue() == True and self.cb.GetLabel() == "Default Downstream":
                print("I am inside downstream if")
                
                itmcomp12 = self.sizer.FindItemAtPosition((3, 2))
                if (itmcomp12 != None) and itmcomp12.IsWindow():
                    print("Inside if for detach 1 ")
                    self.sizer.Detach(itmcomp12.GetWindow())
                    self.sc0a.Destroy()
                self.pnl.SetSizerAndFit(self.sizer)

                self.st_up_default2 = wx.StaticText(self.pnl, label='# of Default Carriers')
                itmcomp124 = self.sizer.FindItemAtPosition((3, 4))
                if (itmcomp124 != None) and itmcomp124.IsWindow():
                    print("Inside if for detach 1 ")
                    self.sizer.Detach(itmcomp124.GetWindow())
                self.sizer.Add(self.st_up_default2, pos=(3,4), flag=wx.ALL | wx.ALIGN_CENTER, border=15) 
                self.pnl.SetSizerAndFit(self.sizer)

                self.st_up_default_values = wx.StaticText(self.pnl, label='1000, 5000, 10000, 20000, 30000, 45000')
                itmcomp125 = self.sizer.FindItemAtPosition((3, 5))
                if (itmcomp125 != None) and itmcomp125.IsWindow():
                    print("Inside if for detach 1 ")
                    self.sizer.Detach(itmcomp125.GetWindow())
                self.sizer.Add(self.st_up_default_values, pos=(3,5), flag=wx.ALL | wx.ALIGN_CENTER, border=15) 
                self.pnl.SetSizerAndFit(self.sizer)

                itmcomp12 = self.sizer.FindItemAtPosition((10, 0))
                if (itmcomp12 != None) and itmcomp12.IsWindow():
                    print("Inside if for detach 1 ")
                    self.sizer.Detach(itmcomp12.GetWindow())
                    self.st8.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

                itmcomp123 = self.sizer.FindItemAtPosition((10,1))
                if (itmcomp123 != None) and itmcomp123.IsWindow():
                    print("Inside if for detach 2")
                    self.sizer.Detach(itmcomp123.GetWindow())
                    self.combo.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

                itmcomp123t = self.sizer.FindItemAtPosition((10,2))
                if (itmcomp123t != None) and itmcomp123t.IsWindow():
                    print("Inside if for detach 2")
                    self.sizer.Detach(itmcomp123t.GetWindow())
                    self.st9a.Hide()
                self.stlabel = wx.StaticText(self.pnl, label = 'These values are ommited since the default is running')
                #self.stlabel.SetValue("This section is omitted since the defaule is chosen")
                self.sizer.Add(self.stlabel, pos=(10, 0), span=(1,4), flag=wx.ALL, border=15)  
                
                self.pnl.SetSizerAndFit(self.sizer)
            if self.cb.GetValue() == False and self.cb.GetLabel() == "Default Downstream":
                print("INSIDE FROM DEFAULT RESTORATION>>>")
                self.stlabel.Hide()
                self.st_up_default2.Hide()
                self.st_up_default_values.Hide()
                #self.sc.Hide()
                #self.sc0.Hide()
                #self.sc0a.Hide()
                #self.sc1.Hide()
                #self.sc2.Hide()
                #self.sc3.Hide()
                #self.sc4.Hide()
                #self.sc5.Hide()
                #self.st8.Hide()
                #self.st9.Hide()
                #self.st9a.Hide()
                #self.combo.Hide()
                self.layout_panel_downstream()
            
            if self.cb.GetValue() == False and self.cb.GetLabel() == "Default Upstream":
                print("INSIDE FROM DEFAULT RESTORATION>>>")
                self.stlabel.Hide()
                self.st_up_default.Hide()
                self.st_up_default_values.Hide()
                #self.sc.Hide()
                #self.sc0.Hide()
                #self.sc0a.Hide()
                #self.sc1.Hide()
                #self.sc2.Hide()
                #self.sc3.Hide()
                #self.sc4.Hide()
                #self.sc5.Hide()
                #self.st8.Hide()
#                self.st9.Hide()
                #self.st9a.Hide()
                self.layout_panel_upstream()

        except IncorrectcomboError:
            wx.MessageBox("Please Enter the Correct Combination of the traffic direction and the default option. Please Re-open the console")
            sys.exit(-1)  
        #except:
        #    import sys, traceback
        #    #xc = traceback.format_exception(*sys.exc_info()
        #    wx.MessageBox("Please enter the correct option")
        return self.cb 

    def OnSize(self, event):
        hsize = event.GetSize()[0] * 0.75
        self.SetSizeHints(minW=-1, minH=hsize, maxH=hsize)
        #self.SetTitle(str(event.GetSize())) 

    
    def layout_panel_upstream(self):
        self.st1 = wx.StaticText(self.pnl, label='Upstream Automation Parameters')
        self.st0 = wx.StaticText(self.pnl, label='Timer for Symbol rate run')
        self.st2 = wx.StaticText(self.pnl, label='NMS IP:')
        self.st3 = wx.StaticText(self.pnl, label='NMS Username:')
        self.st4 = wx.StaticText(self.pnl, label='NMS Password:')
        self.st5 = wx.StaticText(self.pnl, label='       PP IP:')
        self.st6 = wx.StaticText(self.pnl, label=' PP Username:')
        self.st7 = wx.StaticText(self.pnl, label=' PP Password:')
        self.st8 = wx.StaticText(self.pnl, label='# of Carriers:')
        self.st9a1 = wx.StaticText(self.pnl, label='KSps (128 to 7500)')
        self.dir_array.append("upstream")
        
        print("THE DIR ARRAY IS >>>", self.dir_array)
        """
        if self.label_name == "downstream":
            self.sizer.Delete(self.st1, pos=(2, 0), span=(1, 2), flag=wx.ALL, border=15)
            self.sizer.Delete(self.st2, pos=(4, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Delete(self.st3, pos=(5, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Delete(self.st4, pos=(6, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Delete(self.st5, pos=(7, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Delete(self.st6, pos=(8, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Delete(self.st7, pos=(9, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Delete(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
        """
        if not (self.cb2.GetLabel() == "Default Upstream" and self.cb2.GetValue() == False and self.label_name == "Upstream"):
            print("These parameters are not modified")
        elif not (self.cb2.GetLabel() == "Default Upstream" and self.cb2.GetValue() == False and len(self.dir_array) == 2):
            print("I AM IN UPSTREAM DEFAULT>>>>")
            itma  = self.sizer.FindItemAtPosition((2,0))
            if (itma!= None) and itma.IsWindow():
                self.sizer.Detach(itma.GetWindow())
                #self.st1.Hide()
            itmab  = self.sizer.FindItemAtPosition((3,0))
            if (itmab!= None) and itmab.IsWindow():
                self.sizer.Detach(itmab.GetWindow())
                self.st0.Hide()

            itm1a = self.sizer.FindItemAtPosition((4,0))
            if (itm1a!= None) and itm1a.IsWindow():
                self.sizer.Detach(itm1a.GetWindow())
                self.st2.Hide()

            itm2a = self.sizer.FindItemAtPosition((5,0))
            if (itm2a!= None) and itm2a.IsWindow():
                self.sizer.Detach(itm2a.GetWindow())
                self.st2.Hide()

            itm3a = self.sizer.FindItemAtPosition((6,0))
            if (itm3a!= None) and itm3a.IsWindow():
                self.sizer.Detach(itm3a.GetWindow())
                self.st3.Hide()

            itm4a = self.sizer.FindItemAtPosition((7,0))
            if (itm4a!= None) and itm4a.IsWindow():
                self.sizer.Detach(itm4a.GetWindow())
                self.st5.Hide()

            itm5a = self.sizer.FindItemAtPosition((8,0))
            if (itm5a!= None) and itm5a.IsWindow():
                self.sizer.Detach(itm5a.GetWindow())
                self.st6.Hide()

            itm6a = self.sizer.FindItemAtPosition((9,0))
            if (itm6a!= None) and itm6a.IsWindow():
                self.sizer.Detach(itm6a.GetWindow())
                self.st7.Hide()

            itm7a = self.sizer.FindItemAtPosition((10,0))
            if (itm7a!= None) and itm7a.IsWindow():
                print("Adding the symbol static text")
                self.sizer.Detach(itm7a.GetWindow())
                self.st8.Hide()

            itm7b = self.sizer.FindItemAtPosition((10,2))
            if (itm7b!= None) and itm7b.IsWindow():
                print("Adding the symbol static text")
                self.sizer.Detach(itm7b.GetWindow()) 

                self.st9a.Hide()
        
        
            self.sizer.Add(self.st1, pos=(2, 0), span=(1, 2), flag=wx.ALL, border=15)
            self.sizer.Add(self.st0, pos=(3, 0), flag=wx.ALL, border=15)

            self.sizer.Add(self.st2, pos=(4, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)

            self.sizer.Add(self.st3, pos=(5, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st4, pos=(6, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st5, pos=(7, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st6, pos=(8, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st7, pos=(9, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15) 
            self.sizer.Add(self.st9a1, pos=(10, 2), flag=wx.ALL | wx.ALIGN_CENTER, border=15) 
       
        if self.label_name == "Upstream":
            print("PRINTING TO CHECK IN IF>>>><<")
            itm  = self.sizer.FindItemAtPosition((2,0))
            if (itm != None) and itm.IsWindow():
                self.sizer.Detach(itm.GetWindow())

            itm0  = self.sizer.FindItemAtPosition((3,0))
            if (itm0 != None) and itm0.IsWindow():
                self.sizer.Detach(itm0.GetWindow())
            itm1 = self.sizer.FindItemAtPosition((4,0))
            if (itm1 != None) and itm1.IsWindow():
                self.sizer.Detach(itm1.GetWindow())
                self.st2.Hide()
            itm2 = self.sizer.FindItemAtPosition((5,0))
            if (itm2 != None) and itm2.IsWindow():
                self.sizer.Detach(itm2.GetWindow())
                self.st3.Hide()
            itm3 = self.sizer.FindItemAtPosition((6,0))
            if (itm3 != None) and itm3.IsWindow():
                self.sizer.Detach(itm3.GetWindow())
                self.st4.Hide()

            itm4 = self.sizer.FindItemAtPosition((7,0))
            if (itm4 != None) and itm4.IsWindow():
                self.sizer.Detach(itm4.GetWindow())
                self.st5.Hide()

            itm5 = self.sizer.FindItemAtPosition((8,0))
            if (itm5 != None) and itm5.IsWindow():
                self.sizer.Detach(itm5.GetWindow())
                self.st6.Hide()

            itm6 = self.sizer.FindItemAtPosition((9,0))
            if (itm6 != None) and itm6.IsWindow():
                self.sizer.Detach(itm6.GetWindow())
                self.st7.Hide()

            itm7 = self.sizer.FindItemAtPosition((10,0))
            if (itm7 != None) and itm7.IsWindow():
                self.sizer.Detach(itm7.GetWindow())
                self.st8.Hide()

            itm71 = self.sizer.FindItemAtPosition((10,2))
            if (itm71 != None) and itm71.IsWindow():
                self.sizer.Detach(itm71.GetWindow())
                self.st9a1.Hide()

            self.sizer.Add(self.st1, pos=(2, 0), span=(1, 2), flag=wx.ALL, border=15)
            self.sizer.Add(self.st0, pos=(3, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st2, pos=(4, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st3, pos=(5, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st4, pos=(6, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st5, pos=(7, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st6, pos=(8, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st7, pos=(9, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st9a1, pos=(10, 2), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
        else:
            print("PRINTING TO CHECK IF IN ELSE??>>")
            self.sizer.Add(self.st1, pos=(2, 0), span=(1, 2), flag=wx.ALL, border=15)
            self.sizer.Add(self.st0, pos=(3, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st2, pos=(4, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st3, pos=(5, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st4, pos=(6, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st5, pos=(7, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st6, pos=(8, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st7, pos=(9, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st9a1, pos=(10, 2), flag=wx.ALL | wx.ALIGN_CENTER, border=15)

        

        if self.dir_array[0] == "downstream" and self.dir_array[1] == "upstream":
            print("PRINTING TO CHECK IN IF>>>><<")
            itm  = self.sizer.FindItemAtPosition((2,0))
            if (itm != None) and itm.IsWindow():
                self.sizer.Detach(itm.GetWindow())

            itm0  = self.sizer.FindItemAtPosition((3,0))
            if (itm0 != None) and itm0.IsWindow():
                self.sizer.Detach(itm0.GetWindow())
            itm1 = self.sizer.FindItemAtPosition((4,0))
            if (itm1 != None) and itm1.IsWindow():
                self.sizer.Detach(itm1.GetWindow())
                self.st2.Hide()
            itm2 = self.sizer.FindItemAtPosition((5,0))
            if (itm2 != None) and itm2.IsWindow():
                self.sizer.Detach(itm2.GetWindow())
                self.st3.Hide()
            itm3 = self.sizer.FindItemAtPosition((6,0))
            if (itm3 != None) and itm3.IsWindow():
                self.sizer.Detach(itm3.GetWindow())
                self.st4.Hide()

            itm4 = self.sizer.FindItemAtPosition((7,0))
            if (itm4 != None) and itm4.IsWindow():
                self.sizer.Detach(itm4.GetWindow())
                self.st5.Hide()

            itm5 = self.sizer.FindItemAtPosition((8,0))
            if (itm5 != None) and itm5.IsWindow():
                self.sizer.Detach(itm5.GetWindow())
                self.st6.Hide()

            itm6 = self.sizer.FindItemAtPosition((9,0))
            if (itm6 != None) and itm6.IsWindow():
                self.sizer.Detach(itm6.GetWindow())
                self.st7.Hide()

            itm7 = self.sizer.FindItemAtPosition((10,0))
            if (itm7 != None) and itm7.IsWindow():
                self.sizer.Detach(itm7.GetWindow())
                self.st8.Hide()

            itm71 = self.sizer.FindItemAtPosition((10,2))
            if (itm71 != None) and itm71.IsWindow():
                self.sizer.Detach(itm71.GetWindow())
                self.st9a.Hide()

            self.sizer.Add(self.st1, pos=(2, 0), span=(1, 2), flag=wx.ALL, border=15)
            self.sizer.Add(self.st0, pos=(3, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st2, pos=(4, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st3, pos=(5, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st4, pos=(6, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st5, pos=(7, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st6, pos=(8, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st7, pos=(9, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st9a1, pos=(10, 2), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
        
        
        symbol_selection = ["1 Carrier", "2 Carriers", "3 Carriers", "4 Carriers", "5 Carriers", "6 Carriers", "7 Carriers", "8 Carriers", "9 Carriers", "10 Carriers"]      
        self.combo1 = wx.ComboBox(self.pnl,choices = symbol_selection)
#        print self.combo1 + "KSps (1000 to 45000)"
        #self.choice = wx.Choice(self.pnl, choices= symbol_selection )
        if self.dir_array[0] == "downstream" and self.dir_array[1] == "upstream":
            print("PRINTING TO CHECK IF IN DOWNSTREAM OR UPSTREAM>><<")
            itmcom = self.sizer.FindItemAtPosition((10,1))
            if (itmcom!= None) and itmcom.IsWindow():
                print("I am in Combo1")
                self.sizer.Detach(itmcom.GetWindow())
                #self.combo.Destroy()
            self.sizer.Add(self.combo1, pos=(10,1), flag=wx.ALL, border=15)
            self.combo1.Bind(wx.EVT_COMBOBOX, self.OnCombo_upstream)
            self.pnl.SetSizerAndFit(self.sizer)

        #else:
        #    itmcom12 = self.sizer.FindItemAtPosition((10,1))
        #    if (itmcom12!= None) and itmcom12.IsWindow():
        #        print("I am in Combo1")
        #        self.sizer.Detach(itmcom12.GetWindow())
        #        self.combo1.Hide() 
            
        #itmcom1 = self.sizer.FindItemAtPosition((10,1))
        #if itmcom1 == None:
        #    self.sizer.Add(self.combo1, pos=(10,1), flag=wx.ALL, border=15)
        if self.label_name == "Upstream" and self.cb2.GetValue() == False and len(self.dir_array) == 2 and self.cb2.GetLabel() == "Default Upstream":
            print("I AM IN COMBO SELECTION UPSTREASM")
            itmcom1e = self.sizer.FindItemAtPosition((10,1))
            if (itmcom1e!= None) and itmcom1e.IsWindow():
                self.sizer.Detach(itmcom1e.GetWindow())
                #self.combo1.Hide()

            itm7a = self.sizer.FindItemAtPosition((10,0))
            if (itm7a!= None) and itm7a.IsWindow():
                print("Adding the symbol static text")
                self.sizer.Detach(itm7a.GetWindow())
                self.st8.Hide()
            self.sizer.Add(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            #self.pnl.SetSizerAndFit(self.sizer) 

            itm7b = self.sizer.FindItemAtPosition((10,2))
            if (itm7b!= None) and itm7b.IsWindow():
                print("Adding the symbol static text")
                self.sizer.Detach(itm7b.GetWindow())
                self.st9a1.Hide()
            #self.pnl.SetSizerAndFit(self.sizer)
            
            self.sizer.Add(self.combo1, pos=(10,1), flag=wx.ALL, border=15)
            self.combo1.Bind(wx.EVT_COMBOBOX, self.OnCombo_upstream)

            self.sizer.Add(self.st9a, pos=(10, 2), flag=wx.ALL | wx.ALIGN_CENTER, border=15) 
            self.pnl.SetSizerAndFit(self.sizer)

            self.itmcom1a = self.sizer.FindItemAtPosition((3,4))
            if (self.itmcom1a!= None) and self.itmcom1a.IsWindow() and self.itmcom1a.IsShown():
                self.sizer.Detach(self.itmcom1a.GetWindow())
                self.st_up_default.Hide()

            self.itmcom1b = self.sizer.FindItemAtPosition((3,5))
            if (self.itmcom1b!= None) and self.itmcom1b.IsWindow():
                self.sizer.Detach(self.itmcom1b.GetWindow())
                self.st_up_default_values.Hide() 
        """
        if not(self.cb2.GetLabel() == "Default Upstream" and self.cb2.GetValue() == False and self.label_name == "Upstream"):
            print("I AM IN DEFAULT UPSTREAM FALSE>>>")
            
            self.itmcom1a = self.sizer.FindItemAtPosition((3,4))
            if (self.itmcom1a!= None) and self.itmcom1a.IsWindow() and self.itmcom1a.IsShown():
                self.sizer.Detach(self.itmcom1a.GetWindow())
                self.st_up_default.Hide()

            self.itmcom1b = self.sizer.FindItemAtPosition((3,5))
            if (self.itmcom1b!= None) and self.itmcom1b.IsWindow():
                self.sizer.Detach(self.itmcom1b.GetWindow())
                self.st_up_default_values.Hide()
            
            self.itmcom1c = self.sizer.FindItemAtPosition((10,1))
            if (self.itmcom1c!= None) and self.itmcom1c.IsWindow():
                self.sizer.Detach(self.itmcom1c.GetWindow())
                self.combo.Hide()
            #self.sizer.Add(self.combo1, pos=(10,1), flag=wx.ALL, border=15)

            self.itmcom1bc = self.sizer.FindItemAtPosition((10,2))
            if (self.itmcom1bc!= None) and self.itmcom1bc.IsWindow():
                self.sizer.Detach(self.itmcom1bc.GetWindow())
                self.st9a.Hide()

        #self.sizer.Add(self.choice, pos=(8,1), flag=wx.ALL, border=15)

#        text_output = self.OnCombo1(wx.EVT_COMBOBOX)
#        print("TEXT OUTPUT", text_output)
         """
        """
        if not (self.cb2.GetLabel() == "Default Upstream" and self.cb2.GetValue() == False and self.label_name == "Upstream"):
            print("DEFAULT")
        else:
            print("IN ELSE FOR ADDING COMBO>>")
            itmcom1 = self.sizer.FindItemAtPosition((10,1))
            if (itmcom1!= None) and itmcom1.IsWindow():
                self.sizer.Detach(itmcom1.GetWindow())
                self.combo.Hide()
            self.sizer.Add(self.combo1, pos=(10,1), flag=wx.ALL, border=15)

            text = self.combo1.Bind(wx.EVT_COMBOBOX, self.OnCombo_upstream)  
            print("TEXT", text)
        """
        #self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)
        self.sc0 = wx.TextCtrl(self.pnl)
        self.sc0.SetMaxLength(15)
        self.sc0.SetValue("600")
        self.Refresh()
        result = self.sc0.Bind(wx.EVT_TEXT,self.OnKeyTyped_Timer)
        #self.sc.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        self.sc0a = wx.StaticText(self.pnl, label='(in secs)')
        self.Refresh()

        self.sc = wx.TextCtrl(self.pnl)
        self.sc.SetMaxLength(15)
        self.sc.SetValue("172.17.224.11")
        result = self.sc.Bind(wx.EVT_TEXT,self.OnKeyTyped_NMSIP)
        #self.sc.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        self.sc1 = wx.TextCtrl(self.pnl)
        self.sc1.SetMaxLength(7)
        self.sc1.SetValue("admin")
        result = self.sc1.Bind(wx.EVT_TEXT,self.OnKeyTyped_NMSUSER)
        #self.sc1.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        self.sc2 = wx.TextCtrl(self.pnl)
        self.sc2.SetMaxLength(7)
        self.sc2.SetValue("admin")
        result = self.sc2.Bind(wx.EVT_TEXT,self.OnKeyTyped_NMSPASS)
        #self.sc2.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        self.sc3 = wx.TextCtrl(self.pnl)
        self.sc3.SetMaxLength(15)
        self.sc3.SetValue("172.17.224.20")
        result = self.sc3.Bind(wx.EVT_TEXT,self.OnKeyTyped_PPIP)
        #self.sc3.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        self.sc4 = wx.TextCtrl(self.pnl)
        self.sc4.SetMaxLength(7)
        self.sc4.SetValue("idirect")
        #self.sc4.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        result = self.sc4.Bind(wx.EVT_TEXT,self.OnKeyTyped_PPUSER)

        print("THE KEY TYPED", result)

        self.sc5 = wx.TextCtrl(self.pnl)
        self.sc5.SetMaxLength(7)
        self.sc5.SetValue("iDirect")
        result = self.sc5.Bind(wx.EVT_TEXT,self.OnKeyTyped_PPPASS)
        #self.sc5.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        """
        self.sc1 = wx.SpinCtrl(self.pnl, value='0')
        self.sc.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        self.sc1.SetRange(-459, 1000)

        self.sc2 = wx.SpinCtrl(self.pnl, value='0')
        self.sc2.SetRange(-459, 1000)

        self.sc3 = wx.SpinCtrl(self.pnl, value='0')
        self.sc3.SetRange(-459, 1000)

        self.sc4 = wx.SpinCtrl(self.pnl, value='0')
        self.sc4.SetRange(-459, 1000)

        self.sc5 = wx.SpinCtrl(self.pnl, value='0')
        self.sc5.SetRange(-459, 1000)
        """
        

        #self.sc6 = wx.SpinCtrl(pnl, value='0')
        #self.sc6.SetRange(-459, 1000)
        
        """
        if self.label_name == "downstream": 
            self.sizer.Delete(self.sc, pos=(4, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Delete(self.sc1, pos=(5, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Delete(self.sc2, pos=(6, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Delete(self.sc3, pos=(7, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Delete(self.sc4, pos=(8, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Delete(self.sc5, pos=(9, 1), flag=wx.ALIGN_CENTER)
        """
        if self.label_name == "Upstream":
            itm11b = self.sizer.FindItemAtPosition((3,1))
            if (itm11b!= None) and itm11b.IsWindow():
                self.sizer.Detach(itm11b.GetWindow())
                self.sc0.Hide()
            itm11asec = self.sizer.FindItemAtPosition((3,2))
            if (itm11asec!= None) and itm11asec.IsWindow():
                self.sizer.Detach(itm11asec.GetWindow())
                self.sc0a.Hide()
            itm11a = self.sizer.FindItemAtPosition((4,1))
            if (itm11a!= None) and itm11a.IsWindow():
                self.sizer.Detach(itm11a.GetWindow())
                self.sc.Hide()
            itm12a = self.sizer.FindItemAtPosition((5,1))
            if (itm12a!= None) and itm12a.IsWindow():
                self.sizer.Detach(itm12a.GetWindow())
                self.sc1.Hide()
            itm13a = self.sizer.FindItemAtPosition((6,1))
            if (itm13a!= None) and itm13a.IsWindow():
                self.sizer.Detach(itm13a.GetWindow())
                self.sc2.Hide()

            itm14a = self.sizer.FindItemAtPosition((7,1))
            if (itm14a!= None) and itm14a.IsWindow():
                self.sizer.Detach(itm14a.GetWindow())
                self.sc3.Hide()

            itm15a = self.sizer.FindItemAtPosition((8,1))
            if (itm15a!= None) and itm15a.IsWindow():
                self.sizer.Detach(itm15a.GetWindow())
                self.sc4.Hide()

            itm16a = self.sizer.FindItemAtPosition((9,1))
            if (itm16a!= None) and itm16a.IsWindow():
                self.sizer.Detach(itm16a.GetWindow())
                self.sc5.Hide()

            self.sizer.Add(self.sc0, pos=(3, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc0a, pos=(3, 2), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc, pos=(4, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc1, pos=(5, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc2, pos=(6, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc3, pos=(7, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc4, pos=(8, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc5, pos=(9, 1), flag=wx.ALIGN_CENTER)
        
        if self.dir_array[0] == "downstream" and self.dir_array[1] == "upstream":
            print("PRINITNG TOI CHECK IS DOWNSTREAM AND UP")
            itm11a = self.sizer.FindItemAtPosition((3,1))
            if (itm11a!= None) and itm11a.IsWindow():
                self.sizer.Detach(itm11a.GetWindow())
                self.sc0.Hide()
                self.pnl.SetSizerAndFit(self.sizer) 

            itm11b = self.sizer.FindItemAtPosition((3,2))
            if (itm11b!= None) and itm11b.IsWindow():
                self.sizer.Detach(itm11b.GetWindow())
                self.sc0a.Hide()

            itm11 = self.sizer.FindItemAtPosition((4,1))
            if (itm11!= None) and itm11.IsWindow():
                self.sizer.Detach(itm11.GetWindow())
                self.sc.Hide()

            itm12 = self.sizer.FindItemAtPosition((5,1))
            if (itm12 != None) and itm12.IsWindow():
                self.sizer.Detach(itm12.GetWindow())
                self.sc1.Hide()

            itm13 = self.sizer.FindItemAtPosition((6,1))
            if (itm13 != None) and itm13.IsWindow():
                self.sizer.Detach(itm13.GetWindow())
                self.sc2.Hide()

            itm14 = self.sizer.FindItemAtPosition((7,1))
            if (itm14!= None) and itm14.IsWindow():
                self.sizer.Detach(itm14.GetWindow())
                self.sc3.Hide()


            itm15 = self.sizer.FindItemAtPosition((8,1))
            if (itm15!= None) and itm15.IsWindow():

                self.sizer.Detach(itm15.GetWindow())
                self.sc4.Hide()

            itm16 = self.sizer.FindItemAtPosition((9,1))
            if (itm16!= None) and itm16.IsWindow():
                self.sizer.Detach(itm16.GetWindow())
                self.sc5.Hide()


            self.sizer.Add(self.sc0, pos=(3, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc0a, pos=(3, 2), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc, pos=(4, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc1, pos=(5, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc2, pos=(6, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc3, pos=(7, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc4, pos=(8, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc5, pos=(9, 1), flag=wx.ALIGN_CENTER)
            self.pnl.SetSizerAndFit(self.sizer)

        """
        else:
            print("PRINTING TO CHECK IN SAME DOWN AND UP")
            self.sizer.Add(self.sc0, pos=(3, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc0a, pos=(3, 2), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc, pos=(4, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc1, pos=(5, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc2, pos=(6, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc3, pos=(7, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc4, pos=(8, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc5, pos=(9, 1), flag=wx.ALIGN_CENTER) 
        """
        #self.sizer.Add(self.sc6, pos=(7, 1), flag=wx.ALIGN_CENTER)

        #self.st3 = wx.StaticText(pnl, label='')
        #self.sizer.Add(self.st3, pos=(7, 0), flag=wx.ALL|wx.ALIGN_RIGHT, border=15)

        #self.celsius = wx.StaticText(pnl, label='')
        #self.sizer.Add(self.celsius, pos=(2, 1), flag=wx.ALL, border=15)

        computeButton = wx.Button(self.pnl, label='Compute')
        #computeButton.SetFocus()
        closeButton = wx.Button(self.pnl, label='Close')
        computeButton.Bind(wx.EVT_BUTTON, self.OnCompute)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        
        if self.label_name == "Upstream"  and self.cb2.GetValue() == False and len(self.dir_array) == 2:
            print("WHEN BOTH ARE IN UPSTREAM>>>>>?")

            itmcom1e = self.sizer.FindItemAtPosition((10,1))
            if (itmcom1e!= None) and itmcom1e.IsWindow():
                self.sizer.Detach(itmcom1e.GetWindow())
                self.combo1.Hide()
            self.sizer.Add(self.combo1, pos=(10,1), flag=wx.ALL, border=15)
            self.combo1.Bind(wx.EVT_COMBOBOX, self.OnCombo_upstream)

            itm7b = self.sizer.FindItemAtPosition((10,2))
            if (itm7b!= None) and itm7b.IsWindow():
                print("Adding the symbol static text")
                self.sizer.Detach(itm7b.GetWindow())
                self.st9a1.Hide()
            
            self.sizer.Add(self.st9a1, pos=(10, 2), flag=wx.ALL | wx.ALIGN_CENTER, border=15)

            
            itm7a = self.sizer.FindItemAtPosition((10,0))
            if (itm7a!= None) and itm7a.IsWindow():
                print("Adding the symbol static text_combo_related")
                self.sizer.Detach(itm7a.GetWindow())
                self.st8.Hide()
            self.sizer.Add(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15) 
            self.pnl.SetSizerAndFit(self.sizer)
             

            itmcomp = self.sizer.FindItemAtPosition((17,0))
            if (itmcomp != None) and itmcomp.IsWindow():
                self.sizer.Detach(itmcomp.GetWindow())
                computeButton.Hide()

            itmcomp1 = self.sizer.FindItemAtPosition((17,1))
            if (itmcomp1 != None) and itmcomp1.IsWindow():
                self.sizer.Detach(itmcomp1.GetWindow())
                closeButton.Hide()
            
            self.sizer.Add(computeButton, pos=(17, 0), flag=wx.ALIGN_RIGHT|wx.BOTTOM, border=30)

            self.sizer.Add(closeButton, pos=(17, 1), flag=wx.ALIGN_LEFT|wx.BOTTOM, border=30)
        else:
            self.sizer.Add(computeButton, pos=(17, 0), flag=wx.ALIGN_RIGHT|wx.BOTTOM, border=30)

            self.sizer.Add(closeButton, pos=(17, 1), flag=wx.ALIGN_LEFT|wx.BOTTOM, border=30)
            self.pnl.SetSizerAndFit(self.sizer)

        if self.cb2.GetLabel() == "Default Upstream" and self.cb2.GetValue() == "False":
            print("PRINTING TO CHECK IN FALSE AND DOWNSTREAM>><<>><<")
            itmcomp = self.sizer.FindItemAtPosition((17,0))
            if (itmcomp != None) and itmcomp.IsWindow():
                self.sizer.Detach(itmcomp.GetWindow())
                #computeButton.Hide()

            itmcomp1 = self.sizer.FindItemAtPosition((17,1))
            if (itmcomp1 != None) and itmcomp1.IsWindow():
                self.sizer.Detach(itmcomp1.GetWindow())
                #closeButton.Hide()
        if self.label_name == "Upstream" and self.cb2.GetValue() == False and len(self.dir_array) == 2:
            print("WHEN BOTH EL:EMENTS ARE UPSTREAM>>")
            
            itm11a = self.sizer.FindItemAtPosition((3,1))
            
            if (itm11a!= None) and itm11a.IsWindow():
                self.sizer.Detach(itm11a.GetWindow())
                self.sc0.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

            itm11asecv = self.sizer.FindItemAtPosition((3,2))
            if (itm11asecv!= None) and itm11asecv.IsWindow():
                self.sizer.Detach(itm11asecv.GetWindow())
                self.sc0a.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

            itm12ar = self.sizer.FindItemAtPosition((4,1))
            if (itm12ar!= None) and itm12ar.IsWindow():
                self.sizer.Detach(itm12ar.GetWindow())
                self.sc.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

            itm13at = self.sizer.FindItemAtPosition((5,1))
            if (itm13at!= None) and itm13at.IsWindow():
                self.sizer.Detach(itm13at.GetWindow())
                self.sc1.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

            itm14an = self.sizer.FindItemAtPosition((6,1))
            if (itm14an!= None) and itm14an.IsWindow():
                self.sizer.Detach(itm14an.GetWindow())
                self.sc2.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

            itm15aj = self.sizer.FindItemAtPosition((7,1))
            if (itm15aj!= None) and itm15aj.IsWindow():
                self.sizer.Detach(itm15aj.GetWindow())
                self.sc3.Hide()
                self.pnl.SetSizerAndFit(self.sizer)
            
            itm16ay = self.sizer.FindItemAtPosition((8,1))
            if (itm16ay!= None) and itm16ay.IsWindow():
                self.sizer.Detach(itm16ay.GetWindow())
                self.sc4.Hide()
                self.pnl.SetSizerAndFit(self.sizer)
            itm17a9 = self.sizer.FindItemAtPosition((9,1))
            if (itm17a9!= None) and itm17a9.IsWindow():
                self.sizer.Detach(itm17a9.GetWindow())
                self.sc5.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

        if not (self.cb2.GetLabel() == "Default Upstream" and self.cb2.GetValue() == False and self.label_name == "Upstream"):
            print("These parameters are not modified")
        elif not(self.label_name == "Upstream" and self.cb2.GetValue() == False and len(self.dir_array) ==2):
            itm11b = self.sizer.FindItemAtPosition((3,1))
            if (itm11b!= None) and itm11b.IsWindow():
                self.sizer.Detach(itm11b.GetWindow())
                self.sc0.Hide()
            itm11asec = self.sizer.FindItemAtPosition((3,2))
            if (itm11asec!= None) and itm11asec.IsWindow():
                self.sizer.Detach(itm11asec.GetWindow())
                self.sc0a.Hide()
            itm11a = self.sizer.FindItemAtPosition((4,1))
            if (itm11a!= None) and itm11a.IsWindow():
                self.sizer.Detach(itm11a.GetWindow())
                self.sc.Hide()
            itm12a = self.sizer.FindItemAtPosition((5,1))
            if (itm12a!= None) and itm12a.IsWindow():
                self.sizer.Detach(itm12a.GetWindow())
                self.sc1.Hide()
            itm13a = self.sizer.FindItemAtPosition((6,1))
            if (itm13a!= None) and itm13a.IsWindow():
                self.sizer.Detach(itm13a.GetWindow())
                self.sc2.Hide()

            itm14a = self.sizer.FindItemAtPosition((7,1))
            if (itm14a!= None) and itm14a.IsWindow():
                self.sizer.Detach(itm14a.GetWindow())
                self.sc3.Hide()

            itm15a = self.sizer.FindItemAtPosition((8,1))
            if (itm15a!= None) and itm15a.IsWindow():
                self.sizer.Detach(itm15a.GetWindow())
                self.sc4.Hide()

            itm16a = self.sizer.FindItemAtPosition((9,1))
            if (itm16a!= None) and itm16a.IsWindow():
                self.sizer.Detach(itm16a.GetWindow())
                self.sc5.Hide()

            self.sizer.Add(self.sc0, pos=(3, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc0a, pos=(3, 2), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc, pos=(4, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc1, pos=(5, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc2, pos=(6, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc3, pos=(7, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc4, pos=(8, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc5, pos=(9, 1), flag=wx.ALIGN_CENTER)
        #self.sizer.Add(self.sc6, pos=(7, 1), flag=wx.ALIGN_CENTER)

        #self.st3 = wx.StaticText(pnl, label='')
        #self.sizer.Add(self.st3, pos=(7, 0), flag=wx.ALL|wx.ALIGN_RIGHT, border=15)

        #self.celsius = wx.StaticText(pnl, label='')
        #self.sizer.Add(self.celsius, pos=(2, 1), flag=wx.ALL, border=15)

        computeButton = wx.Button(self.pnl, label='Compute')
        #computeButton.SetFocus()
        closeButton = wx.Button(self.pnl, label='Close')

        if not (self.cb2.GetLabel() == "Default Upstream" and self.cb2.GetValue() == False and self.label_name == "Upstream"):
            print("DEFAULT")
        else:
            print("IN ELSE FOR ADDING COMBO>>")
            itmcom1 = self.sizer.FindItemAtPosition((10,1))
            if (itmcom1!= None) and itmcom1.IsWindow():
                self.sizer.Detach(itmcom1.GetWindow())
                self.combo.Hide()
            self.sizer.Add(self.combo1, pos=(10,1), flag=wx.ALL, border=15)

            text = self.combo1.Bind(wx.EVT_COMBOBOX, self.OnCombo_upstream)  
            print("TEXT", text) 
        
        if not (self.cb2.GetLabel() == "Default Upstream" and self.cb2.GetValue() == False and self.label_name == "Upstream"):
            print("THe values are fine")
        elif not(self.label_name == "Upstream" and self.cb2.GetValue() == False and len(self.dir_array) ==2):
            itmcomp_down = self.sizer.FindItemAtPosition((17,0))
            if (itmcomp_down!=None) and itmcomp_down.IsWindow():
                self.sizer.Detach(itmcomp_down.GetWindow())
                computeButton.Hide()
            
            itmcomp1 = self.sizer.FindItemAtPosition((17,1))
            if (itmcomp1 != None) and itmcomp1.IsWindow():
                self.sizer.Detach(itmcomp1.GetWindow())
                closeButton.Hide()
            self.sizer.Add(computeButton, pos=(17, 0), flag=wx.ALIGN_RIGHT|wx.TOP, border=30) 
            self.sizer.Add(closeButton, pos=(17, 1), flag=wx.ALIGN_LEFT|wx.TOP, border=30)
        if self.label_name == "Upstream":
            itmcomp = self.sizer.FindItemAtPosition((17,0))
            if (itmcomp!=None) and itmcomp.IsWindow():
                self.sizer.Detach(itmcomp.GetWindow())
                computeButton.Hide()    
            itmcomp1 = self.sizer.FindItemAtPosition((17,1))
            if (itmcomp1 != None) and itmcomp1.IsWindow():
                self.sizer.Detach(itmcomp1.GetWindow())
                closeButton.Hide()
        
        if not (self.cb2.GetLabel() == "Default Upstream" and self.cb2.GetValue() == False and self.label_name == "Upstream"):
            print("DEFAULT")
        elif not(self.label_name == "Upstream" and self.cb2.GetValue() == False and len(self.dir_array) ==2):
            print("IN ELSE FOR ADDING COMBO>>")
            print("I AM HERE")
              

            itmcom1 = self.sizer.FindItemAtPosition((10,1))
            if (itmcom1!= None) and itmcom1.IsWindow():
                self.sizer.Detach(itmcom1.GetWindow())
                self.combo.Hide()
            self.sizer.Add(self.combo1, pos=(10,1), flag=wx.ALL, border=15)
            self.combo1.Bind(wx.EVT_COMBOBOX, self.OnCombo_upstream)

            self.pnl.SetSizerAndFit(self.sizer)
        
        if self.label_name == "Upstream":
            #itm7b = self.sizer.FindItemAtPosition((10,2))
            #if (itm7b!= None) and itm7b.IsWindow():
            #    print("Adding the symbol static text")
            #    self.sizer.Detach(itm7b.GetWindow())
            #    self.st9a.Hide()
            
           # self.sizer.Add(self.st9a, pos=(10, 2), flag=wx.ALL | wx.ALIGN_CENTER, border=15)

            """
            itm7a = self.sizer.FindItemAtPosition((10,0))
            if (itm7a!= None) and itm7a.IsWindow():
                print("Adding the symbol static text")
                self.sizer.Detach(itm7a.GetWindow())
                self.st8.Hide()
            self.sizer.Add(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15) 
            self.pnl.SetSizerAndFit(self.sizer)
            """
            print("In UPSTREAM FOR TEST???>>>")
            itmcom1 = self.sizer.FindItemAtPosition((10,1))
            if (itmcom1!= None) and itmcom1.IsWindow():
                self.sizer.Detach(itmcom1.GetWindow())
                self.combo1.Hide()
            self.sizer.Add(self.combo1, pos=(10,1), flag=wx.ALL, border=15)
            self.combo1.Bind(wx.EVT_COMBOBOX, self.OnCombo_upstream)

            self.pnl.SetSizerAndFit(self.sizer) 
            
        

        #self.pnl.SetSizer(self.sizer)
        self.pnl.SetSizerAndFit(self.sizer)
        self.SetTitle('LAYER 1 AUTOMATION CONSOLE')
        self.Centre()
        #self.text_parameters()
        #self.sizer.ForceRefresh()
        #self.Fit()


        return (self.pnl, self.dir_array)

    def layout_panel_downstream(self):
        #try:
        self.Refresh()
        self.Update()
        self.st1 = wx.StaticText(self.pnl, label='Downstream Automation Parameters')
        self.st0 = wx.StaticText(self.pnl, label='Timer Symbol Time')
        self.st2 = wx.StaticText(self.pnl, label='NMS IP:')
        self.st3 = wx.StaticText(self.pnl, label='NMS Username:')
        self.st4 = wx.StaticText(self.pnl, label='NMS Password:')
        self.st5 = wx.StaticText(self.pnl, label='       PP IP:')
        self.st6 = wx.StaticText(self.pnl, label=' PP Username:')
        self.st7 = wx.StaticText(self.pnl, label=' PP Password:')
        self.st8 = wx.StaticText(self.pnl, label='# of Carriers:')
        self.st9a = wx.StaticText(self.pnl, label='KSps (1000 to 45000)')
        self.dir_array.append("downstream")

        print("THE DIR ARRAY IS>>>>", self.dir_array) 
         
        
        if not (self.cb2.GetLabel() == "Default Downstream" and self.cb2.GetValue() == False and self.label_name == "Downstream"):
            print("These parameters are not modified")
        elif not (self.cb2.GetLabel() == "Default Downstream" and self.cb2.GetValue() == False and len(self.dir_array) == 2):
            print("THE DEFAULT AND IN FALSE>>>>>>>")
            itma  = self.sizer.FindItemAtPosition((2,0))
            if (itma!= None) and itma.IsWindow():
                self.sizer.Detach(itma.GetWindow())

                #self.st1.Hide()
            itma1  = self.sizer.FindItemAtPosition((3,0))
            if (itma1!= None) and itma1.IsWindow():
                self.sizer.Detach(itma1.GetWindow())
                self.st0.Hide()

            itm1a = self.sizer.FindItemAtPosition((4,0))
            if (itm1a!= None) and itm1a.IsWindow():
                self.sizer.Detach(itm1a.GetWindow())
                self.st2.Hide()
                #self.st2.Hide()
            itm2a = self.sizer.FindItemAtPosition((5,0))
            if (itm2a!= None) and itm2a.IsWindow():
                self.sizer.Detach(itm2a.GetWindow())
                self.st3.Hide()

                #self.st3.Hide()
            itm3a = self.sizer.FindItemAtPosition((6,0))
            if (itm3a!= None) and itm3a.IsWindow():
                self.sizer.Detach(itm3a.GetWindow())
                self.st4.Hide()

                #self.st4.Hide()
            itm4a = self.sizer.FindItemAtPosition((7,0))
            if (itm4a!= None) and itm4a.IsWindow():
                self.sizer.Detach(itm4a.GetWindow())
                self.st5.Hide()
            itm5a = self.sizer.FindItemAtPosition((8,0))
            if (itm5a!= None) and itm5a.IsWindow():
                self.sizer.Detach(itm5a.GetWindow())
                self.st6.Hide()

                #self.st6.Hide()
            itm6a = self.sizer.FindItemAtPosition((9,0))
            if (itm6a!= None) and itm6a.IsWindow():
                self.sizer.Detach(itm6a.GetWindow())
                self.st7.Hide()

                #self.st7.Hide()
            itm7a = self.sizer.FindItemAtPosition((10,0))
            if (itm7a!= None) and itm7a.IsWindow():
                print("Adding the symbol static text")
                self.sizer.Detach(itm7a.GetWindow())
                self.st8.Hide()
            #self.pnl.SetSizerAndFit(self.sizer) 

            itm7b = self.sizer.FindItemAtPosition((10,2))
            if (itm7b!= None) and itm7b.IsWindow():
                print("Adding the symbol static text")
                self.sizer.Detach(itm7b.GetWindow())
                self.st9a.Hide()
            #self.pnl.SetSizerAndFit(self.sizer) 

        
            self.sizer.Add(self.st1, pos=(2, 0), span=(1, 2), flag=wx.ALL, border=15)
            self.sizer.Add(self.st0, pos=(3, 0), flag=wx.ALL, border=15)

            self.sizer.Add(self.st2, pos=(4, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)

            self.sizer.Add(self.st3, pos=(5, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st4, pos=(6, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st5, pos=(7, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st6, pos=(8, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st7, pos=(9, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15) 
            self.sizer.Add(self.st9a, pos=(10, 2), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.pnl.SetSizerAndFit(self.sizer) 
        
        if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
            print("PRINTING TO CHECK IN IF>>>><<")
            itm  = self.sizer.FindItemAtPosition((2,0))
            if (itm != None) and itm.IsWindow():
                self.sizer.Detach(itm.GetWindow())

            itm0  = self.sizer.FindItemAtPosition((3,0))
            if (itm0 != None) and itm0.IsWindow():
                self.sizer.Detach(itm0.GetWindow())
            itm1 = self.sizer.FindItemAtPosition((4,0))
            if (itm1 != None) and itm1.IsWindow():
                self.sizer.Detach(itm1.GetWindow())
                self.st2.Hide()
            itm2 = self.sizer.FindItemAtPosition((5,0))
            if (itm2 != None) and itm2.IsWindow():
                self.sizer.Detach(itm2.GetWindow())
                self.st3.Hide()
            itm3 = self.sizer.FindItemAtPosition((6,0))
            if (itm3 != None) and itm3.IsWindow():
                self.sizer.Detach(itm3.GetWindow())
                self.st4.Hide()

            itm4 = self.sizer.FindItemAtPosition((7,0))
            if (itm4 != None) and itm4.IsWindow():
                self.sizer.Detach(itm4.GetWindow())
                self.st5.Hide()

            itm5 = self.sizer.FindItemAtPosition((8,0))
            if (itm5 != None) and itm5.IsWindow():
                self.sizer.Detach(itm5.GetWindow())
                self.st6.Hide()

            itm6 = self.sizer.FindItemAtPosition((9,0))
            if (itm6 != None) and itm6.IsWindow():
                self.sizer.Detach(itm6.GetWindow())
                self.st7.Hide()

            itm7 = self.sizer.FindItemAtPosition((10,0))
            if (itm7 != None) and itm7.IsWindow():
                self.sizer.Detach(itm7.GetWindow())
                self.st8.Hide()

            itm71 = self.sizer.FindItemAtPosition((10,2))
            if (itm71 != None) and itm71.IsWindow():
                self.sizer.Detach(itm71.GetWindow())
                self.st9a.Hide()

            self.sizer.Add(self.st1, pos=(2, 0), span=(1, 2), flag=wx.ALL, border=15)
            self.sizer.Add(self.st0, pos=(3, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st2, pos=(4, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st3, pos=(5, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st4, pos=(6, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st5, pos=(7, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st6, pos=(8, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st7, pos=(9, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st9a, pos=(10, 2), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.pnl.SetSizerAndFit(self.sizer) 


        symbol_selection = ["1 Carrier", "2 Carriers", "3 Carriers", "4 Carriers", "5 Carriers", "6 Carriers", "7 Carriers", "8 Carriers", "9 Carriers", "10 Carriers"]      
        self.combo = wx.ComboBox(self.pnl,choices = symbol_selection)
        #self.choice = wx.Choice(self.pnl, choices= symbol_selection )
        if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
            itmcom1v = self.sizer.FindItemAtPosition((10,1))
            if (itmcom1v!= None) and itmcom1v.IsWindow():
                self.sizer.Detach(itmcom1v.GetWindow())
                #self.combo.Hide()
            self.sizer.Add(self.combo, pos=(10,1), flag=wx.ALL, border=15)
            self.pnl.SetSizerAndFit(self.sizer)

        if self.cb2.GetLabel() == "Default Downstream" and self.cb2.GetValue() == False and len(self.dir_array) == 2:
            print("I AM IN COMBO SELECTTION>>")
            
            itmcom1e = self.sizer.FindItemAtPosition((10,1))
            if (itmcom1e!= None) and itmcom1e.IsWindow():
                self.sizer.Detach(itmcom1e.GetWindow())
                #self.combo.Hide()

            itm7a = self.sizer.FindItemAtPosition((10,0))
            if (itm7a!= None) and itm7a.IsWindow():
                print("Adding the symbol static text")
                self.sizer.Detach(itm7a.GetWindow())
                self.st8.Hide()
            #self.pnl.SetSizerAndFit(self.sizer) 

            itm7b = self.sizer.FindItemAtPosition((10,2))
            if (itm7b!= None) and itm7b.IsWindow():
                print("Adding the symbol static text")
                self.sizer.Detach(itm7b.GetWindow())
                self.st9a.Hide()
            #self.pnl.SetSizerAndFit(self.sizer)
            
            self.sizer.Add(self.combo, pos=(10,1), flag=wx.ALL, border=15)
            self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo_downstream)

            self.sizer.Add(self.st8, pos=(10, 0), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.sizer.Add(self.st9a, pos=(10, 2), flag=wx.ALL | wx.ALIGN_CENTER, border=15) 
            self.pnl.SetSizerAndFit(self.sizer)

            self.itmcom1a = self.sizer.FindItemAtPosition((3,4))
            if (self.itmcom1a!= None) and self.itmcom1a.IsWindow() and self.itmcom1a.IsShown():
                self.sizer.Detach(self.itmcom1a.GetWindow())
                self.st_up_default2.Hide()

            self.itmcom1b = self.sizer.FindItemAtPosition((3,5))
            if (self.itmcom1b!= None) and self.itmcom1b.IsWindow():
                self.sizer.Detach(self.itmcom1b.GetWindow())
                self.st_up_default_values.Hide()


        #if self.cb.GetLabel() == "Default Downstream" and self.cb.GetValue() == False:
        #    itmcom1234 = self.sizer.FindItemAtPosition((10,1))
        #    if itmcom1234.IsWindow():
        #        self.sizer.Detach(itmcom1234.GetWindow()) 

        
            
                #self.combo.Hide()
            
        #self.sizer.Add(self.choice, pos=(8,1), flag=wx.ALL, border=15)

        #text_output = self.OnCombo1(wx.EVT_COMBOBOX)
        #print("TEXT OUTPUT", text_output)
        
        #print("TEXT", text)
        
        #self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)

        self.sc0 = wx.TextCtrl(self.pnl)
        self.sc0.SetMaxLength(15)
        self.sc0.SetValue("600")
        self.Refresh()
        result = self.sc0.Bind(wx.EVT_TEXT,self.OnKeyTyped_Timer)
        #self.sc.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        self.sc0a = wx.StaticText(self.pnl, label='(in secs)')
        self.Refresh()

        #self.sc.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)
        self.sc = wx.TextCtrl(self.pnl)
        self.sc.SetMaxLength(15)
        self.sc.SetValue("172.17.224.11")
        self.Refresh()
        result = self.sc.Bind(wx.EVT_TEXT,self.OnKeyTyped_NMSIP)
        #self.sc.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        self.sc1 = wx.TextCtrl(self.pnl)
        self.sc1.SetMaxLength(7)
        self.sc1.SetValue("admin")
        result = self.sc1.Bind(wx.EVT_TEXT,self.OnKeyTyped_NMSUSER)
        #self.sc1.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        self.sc2 = wx.TextCtrl(self.pnl)
        self.sc2.SetMaxLength(7)
        self.sc2.SetValue("admin")
        result = self.sc2.Bind(wx.EVT_TEXT,self.OnKeyTyped_NMSPASS)
        #self.sc2.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        self.sc3 = wx.TextCtrl(self.pnl)
        self.sc3.SetMaxLength(15)
        self.sc3.SetValue("172.17.224.20")
        result = self.sc3.Bind(wx.EVT_TEXT,self.OnKeyTyped_PPIP)
        #self.sc3.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        self.sc4 = wx.TextCtrl(self.pnl)
        self.sc4.SetMaxLength(7)
        self.sc4.SetValue("idirect")
        #self.sc4.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        result = self.sc4.Bind(wx.EVT_TEXT,self.OnKeyTyped_PPUSER)

        print("THE KEY TYPED", result)

        self.sc5 = wx.TextCtrl(self.pnl)
        self.sc5.SetMaxLength(7)
        self.sc5.SetValue("iDirect")
        result = self.sc5.Bind(wx.EVT_TEXT,self.OnKeyTyped_PPPASS)
        #self.sc5.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        print("THE KEY TYPED", result)

        """
        self.sc1 = wx.SpinCtrl(self.pnl, value='0')
        self.sc.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        self.sc1.SetRange(-459, 1000)

        self.sc2 = wx.SpinCtrl(self.pnl, value='0')
        self.sc2.SetRange(-459, 1000)

        self.sc3 = wx.SpinCtrl(self.pnl, value='0')
        self.sc3.SetRange(-459, 1000)

        self.sc4 = wx.SpinCtrl(self.pnl, value='0')
        self.sc4.SetRange(-459, 1000)

        self.sc5 = wx.SpinCtrl(self.pnl, value='0')
        self.sc5.SetRange(-459, 1000)
        """
        

        #self.sc6 = wx.SpinCtrl(pnl, value='0')
        #self.sc6.SetRange(-459, 1000)
        
        """
        if self.label_name == "Upstream": 
            self.sizer.Delete(self.sc, pos=(4, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Delete(self.sc1, pos=(5, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Delete(self.sc2, pos=(6, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Delete(self.sc3, pos=(7, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Delete(self.sc4, pos=(8, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Delete(self.sc5, pos=(9, 1), flag=wx.ALIGN_CENTER)
        """
        
        if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
            print("I AM IN BLANKS CONDITION CHECK>>>")
            itm11a = self.sizer.FindItemAtPosition((3,1))
            if (itm11a!= None) or itm11a.IsWindow():
                self.sizer.Detach(itm11a.GetWindow())
                print("TEST IN WINDOW1")
                self.sc0.Hide()
                self.pnl.SetSizerAndFit(self.sizer) 
            itm11asec = self.sizer.FindItemAtPosition((3,2))
            if (itm11asec!= None) or itm11asec.IsWindow():
                self.sizer.Detach(itm11asec.GetWindow())
                print("TEST IN WINDOW2")
                self.sc0a.Hide()


            itm11 = self.sizer.FindItemAtPosition((4,1))
            if (itm11!= None) or itm11.IsWindow():
                self.sizer.Detach(itm11.GetWindow())
                print("TEST IN WINDOW3")
                self.sc.Hide()

            itm12 = self.sizer.FindItemAtPosition((5,1))
            if (itm12!= None) or itm12.IsWindow():
                self.sizer.Detach(itm12.GetWindow())
                print("TEST IN WINDOW4")
                self.sc1.Hide()

            itm13 = self.sizer.FindItemAtPosition((6,1))
            if (itm13!= None) or itm13.IsWindow():
                self.sizer.Detach(itm13.GetWindow())
                print("TEST IN WINDOW5")
                self.sc2.Hide()

            itm14 = self.sizer.FindItemAtPosition((7,1))
            if (itm14!= None) or itm14.IsWindow():
                self.sizer.Detach(itm14.GetWindow())
                print("TEST IN WINDOW6")
                self.sc3.Hide()

            itm15 = self.sizer.FindItemAtPosition((8,1))
            if (itm15!= None) or itm15.IsWindow():
                self.sizer.Detach(itm15.GetWindow())
                print("TEST IN WINDOW7")
                self.sc4.Hide()

            itm16 = self.sizer.FindItemAtPosition((9,1))
            if (itm16!= None) or itm16.IsWindow():
                self.sizer.Detach(itm16.GetWindow())
                print("TEST IN WINDOW8")
                self.sc5.Hide()
                 
            self.sizer.Add(self.sc0, pos=(3, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc0a, pos=(3, 2), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc, pos=(4, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc1, pos=(5, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc2, pos=(6, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc3, pos=(7, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc4, pos=(8, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc5, pos=(9, 1), flag=wx.ALIGN_CENTER)
            self.pnl.SetSizerAndFit(self.sizer)
            
        
         
        if self.label_name == "Downstream" and self.cb2.GetValue() == False and len(self.dir_array) == 2:
            print("WHEN BOTH EL:EMENTS ARE DOWNSTREAM>>")
            
            itm11a = self.sizer.FindItemAtPosition((3,1))
            
            if (itm11a!= None) and itm11a.IsWindow():
                self.sizer.Detach(itm11a.GetWindow())
                self.sc0.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

            itm11asecv = self.sizer.FindItemAtPosition((3,2))
            if (itm11asecv!= None) and itm11asecv.IsWindow():
                self.sizer.Detach(itm11asecv.GetWindow())
                self.sc0a.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

            itm12ar = self.sizer.FindItemAtPosition((4,1))
            if (itm12ar!= None) and itm12ar.IsWindow():
                self.sizer.Detach(itm12ar.GetWindow())
                self.sc.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

            itm13at = self.sizer.FindItemAtPosition((5,1))
            if (itm13at!= None) and itm13at.IsWindow():
                self.sizer.Detach(itm13at.GetWindow())
                self.sc1.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

            itm14an = self.sizer.FindItemAtPosition((6,1))
            if (itm14an!= None) and itm14an.IsWindow():
                self.sizer.Detach(itm14an.GetWindow())
                self.sc2.Hide()
                self.pnl.SetSizerAndFit(self.sizer)

            itm15aj = self.sizer.FindItemAtPosition((7,1))
            if (itm15aj!= None) and itm15aj.IsWindow():
                self.sizer.Detach(itm15aj.GetWindow())
                self.sc3.Hide()
                self.pnl.SetSizerAndFit(self.sizer)
            
            itm16ay = self.sizer.FindItemAtPosition((8,1))
            if (itm16ay!= None) and itm16ay.IsWindow():
                self.sizer.Detach(itm16ay.GetWindow())
                self.sc4.Hide()
                self.pnl.SetSizerAndFit(self.sizer)
            itm17a9 = self.sizer.FindItemAtPosition((9,1))
            if (itm17a9!= None) and itm17a9.IsWindow():
                self.sizer.Detach(itm17a9.GetWindow())
                self.sc5.Hide()
                self.pnl.SetSizerAndFit(self.sizer)
                
            #self.sizer.Add(self.sc0, pos=(3, 1), flag=wx.ALIGN_CENTER)
            #self.sizer.Add(self.sc0a, pos=(3, 2), flag=wx.ALIGN_CENTER)
            #self.sizer.Add(self.sc, pos=(4, 1), flag=wx.ALIGN_CENTER)
            #self.sizer.Add(self.sc1, pos=(5, 1), flag=wx.ALIGN_CENTER)
            #self.sizer.Add(self.sc2, pos=(6, 1), flag=wx.ALIGN_CENTER)
            #self.sizer.Add(self.sc3, pos=(7, 1), flag=wx.ALIGN_CENTER)
            #self.sizer.Add(self.sc4, pos=(8, 1), flag=wx.ALIGN_CENTER)
            #self.sizer.Add(self.sc5, pos=(9, 1), flag=wx.ALIGN_CENTER)

            self.pnl.SetSizerAndFit(self.sizer) 
            
        
        
        """
        print("THE VALUE OF THE CHECKBOX", self.cb2.GetValue() )
        print("THE VALUE OF THE GETLABEL", self.cb2.GetLabel() )
        print("THE VALUE OF THE LABEL NAME", self.label_name )
        """
        if not (self.cb2.GetLabel() == "Default Downstream" and self.cb2.GetValue() == False and self.label_name == "Downstream"):
            print("These parameters are not modified")
        elif not(self.label_name == "Downstream" and self.cb2.GetValue() == False and len(self.dir_array) ==2):
            print("ADDING THE BLANKS>>>")
            itm11b = self.sizer.FindItemAtPosition((3,1))
            if (itm11b!= None) and itm11b.IsWindow():
                self.sizer.Detach(itm11b.GetWindow())
                self.sc0.Hide()
            itm11asec = self.sizer.FindItemAtPosition((3,2))
            if (itm11asec!= None) and itm11asec.IsWindow():
                self.sizer.Detach(itm11asec.GetWindow())
                self.sc0a.Hide()
            itm11a = self.sizer.FindItemAtPosition((4,1))
            if (itm11a!= None) and itm11a.IsWindow():
                self.sizer.Detach(itm11a.GetWindow())
                self.sc.Hide()
            itm12a = self.sizer.FindItemAtPosition((5,1))
            if (itm12a!= None) and itm12a.IsWindow():
                self.sizer.Detach(itm12a.GetWindow())
                self.sc1.Hide()
            itm13a = self.sizer.FindItemAtPosition((6,1))
            if (itm13a!= None) and itm13a.IsWindow():
                self.sizer.Detach(itm13a.GetWindow())
                self.sc2.Hide()

            itm14a = self.sizer.FindItemAtPosition((7,1))
            if (itm14a!= None) and itm14a.IsWindow():
                self.sizer.Detach(itm14a.GetWindow())
                self.sc3.Hide()

            itm15a = self.sizer.FindItemAtPosition((8,1))
            if (itm15a!= None) and itm15a.IsWindow():
                self.sizer.Detach(itm15a.GetWindow())
                self.sc4.Hide()

            itm16a = self.sizer.FindItemAtPosition((9,1))
            if (itm16a!= None) and itm16a.IsWindow():
                self.sizer.Detach(itm16a.GetWindow())
                self.sc5.Hide()

            self.sizer.Add(self.sc0, pos=(3, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc0a, pos=(3, 2), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc, pos=(4, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc1, pos=(5, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc2, pos=(6, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc3, pos=(7, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc4, pos=(8, 1), flag=wx.ALIGN_CENTER)
            self.sizer.Add(self.sc5, pos=(9, 1), flag=wx.ALIGN_CENTER)
            self.pnl.SetSizerAndFit(self.sizer)
            
        #self.sizer.Add(self.sc6, pos=(7, 1), flag=wx.ALIGN_CENTER)

        #self.st3 = wx.StaticText(pnl, label='')
        #self.sizer.Add(self.st3, pos=(7, 0), flag=wx.ALL|wx.ALIGN_RIGHT, border=15)

        #self.celsius = wx.StaticText(pnl, label='')
        #self.sizer.Add(self.celsius, pos=(2, 1), flag=wx.ALL, border=15)
        
        if not (self.cb2.GetLabel() == "Default Downstream" and self.cb2.GetValue() == False and self.label_name == "Downstream"):
            print("DEFAULT")
        elif not(self.label_name == "Downstream" and self.cb2.GetValue() == False and len(self.dir_array) ==2):
            print("IN ELSE FOR ADDING COMBO>>")
            print("I AM HERE")
              

            itmcom1 = self.sizer.FindItemAtPosition((10,1))
            if (itmcom1!= None) and itmcom1.IsWindow():
                self.sizer.Detach(itmcom1.GetWindow())
                self.combo.Hide()
            self.sizer.Add(self.combo, pos=(10,1), flag=wx.ALL, border=15)
            self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo_downstream)

            self.pnl.SetSizerAndFit(self.sizer)
         
        #self.sizer.Add(self.st8, pos=(10,0), flag=wx.ALL, border=15)
        #self.sizer.Add(self.st9a, pos=(10,2), flag=wx.ALL, border=15)

        computeButton = wx.Button(self.pnl, label='Compute')
        #computeButton.SetFocus()
        closeButton = wx.Button(self.pnl, label='Close')
        
        if not (self.cb2.GetLabel() == "Default Downstream" and self.cb2.GetValue() == False and self.label_name == "Downstream"):
            print("THe values are fine")
        else:
            itmcomp_down = self.sizer.FindItemAtPosition((17,0))
            if (itmcomp_down!=None) and itmcomp_down.IsWindow():
                self.sizer.Detach(itmcomp_down.GetWindow())
                computeButton.Hide()
            
            itmcomp1 = self.sizer.FindItemAtPosition((17,1))
            if (itmcomp1 != None) and itmcomp1.IsWindow():
                self.sizer.Detach(itmcomp1.GetWindow())
                closeButton.Hide()
            self.sizer.Add(computeButton, pos=(17, 0), flag=wx.ALIGN_RIGHT|wx.TOP, border=30) 
            self.sizer.Add(closeButton, pos=(17, 1), flag=wx.ALIGN_LEFT|wx.TOP, border=30)

        if len(self.dir_array) == 2:
            itmcomp = self.sizer.FindItemAtPosition((17,0))
            if (itmcomp!=None) and itmcomp.IsWindow():
                self.sizer.Detach(itmcomp.GetWindow())
                computeButton.Hide()    
            itmcomp1 = self.sizer.FindItemAtPosition((17,1))
            if (itmcomp1 != None) and itmcomp1.IsWindow():
                self.sizer.Detach(itmcomp1.GetWindow())
                closeButton.Hide()
            

        #itm_compute = self.sizer.FindItemAtPosition((17,0))
        #if (itm_compute ==None):
       # self.sizer.Add(computeButton, pos=(17, 0), flag=wx.ALIGN_RIGHT|wx.TOP, border=30) 
        
        #itm_close = self.sizer.FindItemAtPosition((17,1))
        #if (itm_close == None):
        #    self.sizer.Add(closeButton, pos=(17, 1), flag=wx.ALIGN_LEFT|wx.TOP, border=30) 
            

        #self.sizer.Add(closeButton, pos=(17, 1), flag=wx.ALIGN_LEFT|wx.TOP, border=30)
        
        computeButton.Bind(wx.EVT_BUTTON, self.OnCompute)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

        self.UpdateWindowUI(wx.UPDATE_UI_FROMIDLE)
        self.Refresh()
        self.Update()
        self.pnl.SetSizerAndFit(self.sizer)
        self.SetTitle('LAYER 1 AUTOMATION CONSOLE')
        self.Centre()
        
            #self.text_parameters()
        #except:
        #wx.MessageBox("Please Enter the correct COmbination. PLease Re-open the console..:)")
            #sys.exit(-1)
        return self.pnl

    def hide_downstream(self, event):
        self.layout_panel_downstream().Hide()
        self.Layout()

    def hide_upstream(self, event):
        self.layout_panel_upstream().Hide()
        self.Layout()
    def OnKeyTyped_NMSIP(self, event): 
      self.text_nmsip = []
      self.text_nmsip.append(event.GetString())
      print("The text entered1", self.text_nmsip)

      return self.text_nmsip
    def OnKeyTyped_NMSUSER(self, event): 
      self.text_nmsuser = []
      self.text_nmsuser.append(event.GetString())
      print("The text entered2", self.text_nmsuser)
    
      return self.text_nmsuser

    def OnKeyTyped_NMSPASS(self, event): 
      self.text_nmspass = []
      self.text_nmspass.append(event.GetString())
      print("The text entered3", self.text_nmspass)
    
      return self.text_nmspass

    def OnKeyTyped_PPIP(self, event): 
      self.text_ppip = []
      self.text_ppip.append(event.GetString())
      print("The text entered4", self.text_ppip)
    
      return self.text_ppip

    def OnKeyTyped_Timer(self, event):
      self.text_timer = []
      self.text_timer.append(event.GetString())
      print("The Timer value given", self.text_timer)

      return self.text_timer

    def OnKeyTyped_PPUSER(self, event): 
      self.text_ppuser = []
      self.text_ppuser.append(event.GetString())
      print("The text entered5", self.text_ppuser)
    
      return self.text_ppuser

    def OnKeyTyped_PPPASS(self, event): 
      self.text_pppass = []
      self.text_pppass.append(event.GetString())
      print("The text entered6", self.text_pppass)

      return self.text_pppass

    def text_parameters(self):
        print("THE NMS IP", self.text_nmsip)      
        print("THE NMS USER",self.text_nmsuser)      
        print("THE NMS PASS",self.text_nmspass)      
        print("THE PP IP", self.text_ppip)      
        print("THE PP USERNAME", self.text_ppuser)      
        print("THE PP Pass", self.text_pppass)

    def OnMaxLen(self,event): 
      print "Maximum length reached"

    def OnRadiogroup(self, e): 
      
      
      rb = e.GetEventObject()
      rb.Refresh()
       
      self.label_name = rb.GetLabel().encode("utf-8")
      print("LABEL NAME", self.label_name)
    
      self.cb1 = wx.CheckBox(self.pnl, label = 'Default Upstream',pos = (150,10))
      self.cb2 = wx.CheckBox(self.pnl, label = 'Default Downstream',pos = (150,40)) 
      
      #self.dir_array = dir_array
      
       
      if self.label_name == "Upstream":
        #self.layout_panel_downstream()
        
        self.layout_panel_upstream()
        self.Bind(wx.EVT_CHECKBOX,self.onChecked) 
        self.Centre() 
        self.cb1.Show(True)
        self.cb2.Show(False)
        self.UpdateWindowUI(wx.UPDATE_UI_FROMIDLE)
        #self.parent.Update()
        self.Layout() 
        self.Refresh()
        self.item_extender =  wx.StaticText(self.pnl, label='Bears Network')
        item_bears = self.sizer.FindItemAtPosition((20,20))
        if item_bears != None and item_bears.IsWindow():
            self.sizer.Detach(item_bears.GetWindow())
            self.item_extender.Hide()
            self.sizer.Add(self.item_extender, pos=(20, 20), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.pnl.SetSizerAndFit(self.sizer) 

        else:
            self.sizer.Add(self.item_extender, pos=(20, 20), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.pnl.SetSizerAndFit(self.sizer) 

        self.pnl.SetSizerAndFit(self.sizer)
        #self.Show(False)

      elif self.label_name == "Downstream":

        self.layout_panel_downstream()
      
        self.Bind(wx.EVT_CHECKBOX,self.onChecked) 
        self.Centre() 
        self.cb2.Show(True)
        self.cb1.Show(False)
        self.UpdateWindowUI(wx.UPDATE_UI_FROMIDLE)
        #self.parent.Update()
        self.Layout() 
        self.Refresh()
        #self.sizer.Fit()
        self.item_extender =  wx.StaticText(self.pnl, label='Bears Network') 
        item_bears = self.sizer.FindItemAtPosition((20,20))
        self.item_extender.Hide()
        if item_bears != None and item_bears.IsWindow():
            self.sizer.Detach(item_bears.GetWindow())
            self.sizer.Add(self.item_extender, pos=(20, 20), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.pnl.SetSizerAndFit(self.sizer) 

        else:
            self.sizer.Add(self.item_extender, pos=(20, 20), flag=wx.ALL | wx.ALIGN_CENTER, border=15)
            self.pnl.SetSizerAndFit(self.sizer) 

        self.pnl.SetSizerAndFit(self.sizer) 
        

      print("THE RB", rb)
    

    
    def OnCombo_upstream(self, event): 
        text_field = self.combo1.GetValue().encode("utf-8")
        
        print ("The value got from on combo is", text_field)
        self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
        self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
        self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
        self.st93 = wx.StaticText(self.pnl, label='     Carrier4:')
        self.st94 = wx.StaticText(self.pnl, label='     Carrier5:')
        self.st95 = wx.StaticText(self.pnl, label='     Carrier6:')
        self.st96 = wx.StaticText(self.pnl, label='     Carrier7:')
        self.st97 = wx.StaticText(self.pnl, label='     Carrier8:')
        self.st98 = wx.StaticText(self.pnl, label='     Carrier9:')
        self.st99 = wx.StaticText(self.pnl, label='     Carrier10:')
            

        if text_field == "1 Carrier":
            #self.text_parameters()
            if self.label_name == "Upstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm40a = self.sizer.FindItemAtPosition((11,0))
                if (itm40a != None) and itm40a.IsWindow():
                    self.sizer.Detach(itm40a.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
                itm4b = self.sizer.FindItemAtPosition((12,0))
                if (itm4b!=None) and itm4b.IsWindow():
                    self.sizer.Detach(itm4b.GetWindow())

                itm4c = self.sizer.FindItemAtPosition((12,1))
                if (itm4c!=None) and itm4c.IsWindow():
                    self.sizer.Detach(itm4c.GetWindow())
                    
                itm4d = self.sizer.FindItemAtPosition((13,0))
                if (itm4d!=None) and itm4d.IsWindow():
                    self.sizer.Detach(itm4d.GetWindow())

                itm4e = self.sizer.FindItemAtPosition((13,1))
                if (itm4e!=None) and itm4e.IsWindow():
                    self.sizer.Detach(itm4e.GetWindow())

                itm4f = self.sizer.FindItemAtPosition((14,0))
                if (itm4f!=None) and itm4f.IsWindow():
                    self.sizer.Detach(itm4f.GetWindow())

                itm4z = self.sizer.FindItemAtPosition((14,1))
                if (itm4z!=None) and itm4z.IsWindow():
                    self.sizer.Detach(itm4z.GetWindow())

                itm4g = self.sizer.FindItemAtPosition((15,0))
                if (itm4g!=None) and itm4g.IsWindow():
                    self.sizer.Detach(itm4g.GetWindow())

                itm4h = self.sizer.FindItemAtPosition((15,1))
                if (itm4h!=None) and itm4h.IsWindow():
                    self.sizer.Detach(itm4h.GetWindow())

                itm4i = self.sizer.FindItemAtPosition((4,4))
                if (itm4i!=None) and itm4i.IsWindow():
                    self.sizer.Detach(itm4i.GetWindow())

                itm4j = self.sizer.FindItemAtPosition((4,5))
                if (itm4j!=None) and itm4j.IsWindow():
                    self.sizer.Detach(itm4j.GetWindow())

                itm4k = self.sizer.FindItemAtPosition((5,4))
                if (itm4k!=None) and itm4k.IsWindow():
                    self.sizer.Detach(itm4k.GetWindow())

                itm4l = self.sizer.FindItemAtPosition((5,5))
                if (itm4l!=None) and itm4l.IsWindow():
                    self.sizer.Detach(itm4l.GetWindow())

                itm4m = self.sizer.FindItemAtPosition((6,4))
                if (itm4m!=None) and itm4m.IsWindow():
                    self.sizer.Detach(itm4m.GetWindow())

                itm4n = self.sizer.FindItemAtPosition((6,5))
                if (itm4n!=None) and itm4n.IsWindow():
                    self.sizer.Detach(itm4n.GetWindow())

                itm4o = self.sizer.FindItemAtPosition((7,4))
                if (itm4o!=None) and itm4o.IsWindow():
                    self.sizer.Detach(itm4o.GetWindow())

                itm4p = self.sizer.FindItemAtPosition((7,5))
                if (itm4p!=None) and itm4p.IsWindow():
                    self.sizer.Detach(itm4p.GetWindow())
                itm4q = self.sizer.FindItemAtPosition((8,4))
                if (itm4q!=None) and itm4q.IsWindow():
                    self.sizer.Detach(itm4q.GetWindow())

                itm4r = self.sizer.FindItemAtPosition((8,5))
                if (itm4r!=None) and itm4r.IsWindow():
                    self.sizer.Detach(itm4r.GetWindow())

            itemCarrier1 = self.sizer.FindItemAtPosition((11,1))
            if itemCarrier1 == None:
                self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
            
            item_st91 = self.sizer.FindItemAtPosition((12,0))
            if item_st91 != None and item_st91.IsShown():
                print("I am in st91")
                self.sizer.Detach(item_st91.GetWindow())
                self.st91.Hide()
            item_st92 = self.sizer.FindItemAtPosition((13,0))
            if item_st92 != None and item_st92.IsShown():
                print("I am in st912")
                self.sizer.Detach(item_st92.GetWindow())

                self.st92.Hide()

            item_st93 = self.sizer.FindItemAtPosition((14,0))
            if item_st93!= None and item_st93.IsShown():
                print("I am in st93")
                self.sizer.Detach(item_st93.GetWindow())

                self.st93.Hide()

            item_st94 = self.sizer.FindItemAtPosition((15,0))
            if item_st94 != None and item_st94.IsShown():
                print("I am in st94")
                self.sizer.Detach(item_st94.GetWindow())


                self.st94.Hide()

            item_st95 = self.sizer.FindItemAtPosition((4,4))
            if item_st95 != None and item_st95.IsShown():
                print("I am in st95")
                self.sizer.Detach(item_st95.GetWindow())

                self.st95.Hide()

            item_st96 = self.sizer.FindItemAtPosition((5,4))
            if item_st96 != None and item_st96.IsShown():
                print("I am in st96")
                self.sizer.Detach(item_st96.GetWindow())


                self.st96.Hide()

            item_st97 = self.sizer.FindItemAtPosition((6,4))
            if item_st97 != None and item_st97.IsShown():
                self.sizer.Detach(item_st97.GetWindow())
                print("I am in st97")

                self.st97.Hide()

            item_st98 = self.sizer.FindItemAtPosition((7,4))
            if item_st98 != None and item_st98.IsShown():
                print("I am in st98")
                self.sizer.Detach(item_st98.GetWindow())

                self.st98.Hide()
            item_st99 = self.sizer.FindItemAtPosition((8,4))
            if item_st99 != None and item_st99.IsShown():
                print("I am in st99")
                self.sizer.Detach(item_st99.GetWindow())

                self.st99.Hide()
           
            itm41a = self.sizer.FindItemAtPosition((12,1))
            if (itm41a!=None) and itm41a.IsWindow():
                self.sizer.Detach(itm41a.GetWindow())
                self.sc91a.Hide()
            itm41s = self.sizer.FindItemAtPosition((13,1))
            if (itm41s!=None) and itm41s.IsWindow():
                self.sizer.Detach(itm41.GetWindow())
                self.sc91.Hide()
            itm41b = self.sizer.FindItemAtPosition((14,1))
            if (itm41b!=None) and itm41b.IsWindow():
                self.sizer.Detach(itm41b.GetWindow())
                self.sc92.Hide()

            itm41c = self.sizer.FindItemAtPosition((15,1))
            if (itm41c!=None) and itm41c.IsWindow():
                self.sizer.Detach(itm41c.GetWindow())
                self.sc93.Hide()

            itm41d = self.sizer.FindItemAtPosition((4,5))
            if (itm41d!=None) and itm41d.IsWindow():
                self.sizer.Detach(itm41d.GetWindow())
                self.sc94.Hide()

            itm41e = self.sizer.FindItemAtPosition((5,5))
            if (itm41e!=None) and itm41e.IsWindow():
                self.sizer.Detach(itm41e.GetWindow())
                self.sc95.Hide()
            
            itm41f = self.sizer.FindItemAtPosition((6,5))
            if (itm41f!=None) and itm41f.IsWindow():
                self.sizer.Detach(itm41f.GetWindow())
                self.sc96.Hide()

            itm41g = self.sizer.FindItemAtPosition((7,5))
            if (itm41g!=None) and itm41g.IsWindow():
                self.sizer.Detach(itm41g.GetWindow())
                self.sc97.Hide()
                
            itm41h = self.sizer.FindItemAtPosition((8,5))
            if (itm41h!=None) and itm41h.IsWindow():
                self.sizer.Detach(itm41h.GetWindow())
                self.sc98.Hide()
            self.pnl.SetSizerAndFit(self.sizer)
        if text_field == "2 Carriers":
            if self.label_name == "Upstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401a = self.sizer.FindItemAtPosition((11,0))
                if (itm401a != None) and itm401a.IsWindow():
                    self.sizer.Detach(itm401a.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401ab = self.sizer.FindItemAtPosition((11,1))
                if (itm401ab != None) and itm401ab.IsWindow():
                    self.sizer.Detach(itm401ab.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401n = self.sizer.FindItemAtPosition((12,0))
                if (itm401n != None) and itm401n.IsWindow():
                    self.sizer.Detach(itm401n.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401o = self.sizer.FindItemAtPosition((12,1))
                if (itm401o != None) and itm401o.IsWindow():
                    self.sizer.Detach(itm401o.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            self.pnl.SetSizerAndFit(self.sizer)
        if text_field == "3 Carriers":
            if self.label_name == "Upstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401v = self.sizer.FindItemAtPosition((13,1))
                if (itm401v != None) and itm401v.IsWindow():
                    self.sizer.Detach(itm401v.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            self.pnl.SetSizerAndFit(self.sizer)
        if text_field == "4 Carriers":
            if self.label_name == "Upstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            self.pnl.SetSizerAndFit(self.sizer)
        if text_field == "5 Carriers":
            if self.label_name == "Upstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            if self.label_name == "Upstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            self.pnl.SetSizerAndFit(self.sizer)
        if text_field == "6 Carriers":
            if self.label_name == "Upstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            if self.label_name == "Upstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm411 = self.sizer.FindItemAtPosition((4,4))
                if (itm411 != None) and itm411.IsWindow():
                    self.sizer.Detach(itm411.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((4,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm412 = self.sizer.FindItemAtPosition((4,5))
                if (itm412!=None) and itm412.IsWindow():
                    self.sizer.Detach(itm412.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((4,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc95, pos=(4,5), flag=wx.TOP | wx.EXPAND)
            self.pnl.SetSizerAndFit(self.sizer)
        if text_field == "7 Carriers":
            if self.label_name == "Upstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            if self.label_name == "Upstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm411 = self.sizer.FindItemAtPosition((4,4))
                if (itm411 != None) and itm411.IsWindow():
                    self.sizer.Detach(itm411.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((4,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm412 = self.sizer.FindItemAtPosition((4,5))
                if (itm412!=None) and itm412.IsWindow():
                    self.sizer.Detach(itm412.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((4,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc95, pos=(4,5), flag=wx.TOP | wx.EXPAND)
            
            self.sc96 = wx.SpinCtrl(self.pnl, value='0')
            self.sc96.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm413 = self.sizer.FindItemAtPosition((5,4))
                if (itm413!=None) and itm413.IsWindow():
                    self.sizer.Detach(itm413.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((5,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st96, pos=(5, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm414 = self.sizer.FindItemAtPosition((5,5))
                if (itm414!=None) and itm414.IsWindow():
                    self.sizer.Detach(itm414.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((5,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc96, pos=(5, 5), flag=wx.TOP | wx.EXPAND)
            self.pnl.SetSizerAndFit(self.sizer)
        if text_field == "8 Carriers":
            if self.label_name == "Upstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            if self.label_name == "Upstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm411 = self.sizer.FindItemAtPosition((4,4))
                if (itm411 != None) and itm411.IsWindow():
                    self.sizer.Detach(itm411.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((4,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm412 = self.sizer.FindItemAtPosition((4,5))
                if (itm412!=None) and itm412.IsWindow():
                    self.sizer.Detach(itm412.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((4,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc95, pos=(4,5), flag=wx.TOP | wx.EXPAND)
            
            self.sc96 = wx.SpinCtrl(self.pnl, value='0')
            self.sc96.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm413 = self.sizer.FindItemAtPosition((5,4))
                if (itm413!=None) and itm413.IsWindow():
                    self.sizer.Detach(itm413.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((5,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st96, pos=(5, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm414 = self.sizer.FindItemAtPosition((5,5))
                if (itm414!=None) and itm414.IsWindow():
                    self.sizer.Detach(itm414.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((5,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc96, pos=(5, 5), flag=wx.TOP | wx.EXPAND)
            
            self.sc97 = wx.SpinCtrl(self.pnl, value='0')
            self.sc97.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm415 = self.sizer.FindItemAtPosition((6,4))
                if (itm415!=None) and itm415.IsWindow():
                    self.sizer.Detach(itm415.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((6,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st97, pos=(6, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm416 = self.sizer.FindItemAtPosition((6,5))
                if (itm416!=None) and itm416.IsWindow():
                    self.sizer.Detach(itm416.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((6,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc97, pos=(6, 5), flag=wx.TOP | wx.EXPAND)
            self.pnl.SetSizerAndFit(self.sizer)
        if text_field == "9 Carriers":
            if self.label_name == "Upstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            if self.st9 == None:
                self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            else:
                self.st9.Hide()
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            if self.sc91a ==  None:
                self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
            else:
                self.sc91a.Hide()
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            if self.label_name == "Upstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm411 = self.sizer.FindItemAtPosition((4,4))
                if (itm411 != None) and itm411.IsWindow():
                    self.sizer.Detach(itm411.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((4,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm412 = self.sizer.FindItemAtPosition((4,5))
                if (itm412!=None) and itm412.IsWindow():
                    self.sizer.Detach(itm412.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((4,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc95, pos=(4,5), flag=wx.TOP | wx.EXPAND)
            
            self.sc96 = wx.SpinCtrl(self.pnl, value='0')
            self.sc96.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm413 = self.sizer.FindItemAtPosition((5,4))
                if (itm413!=None) and itm413.IsWindow():
                    self.sizer.Detach(itm413.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((5,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st96, pos=(5, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm414 = self.sizer.FindItemAtPosition((5,5))
                if (itm414!=None) and itm414.IsWindow():
                    self.sizer.Detach(itm414.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((5,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc96, pos=(5, 5), flag=wx.TOP | wx.EXPAND)
            
            self.sc97 = wx.SpinCtrl(self.pnl, value='0')
            self.sc97.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm415 = self.sizer.FindItemAtPosition((6,4))
                if (itm415!=None) and itm415.IsWindow():
                    self.sizer.Detach(itm415.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((6,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st97, pos=(6, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm416 = self.sizer.FindItemAtPosition((6,5))
                if (itm416!=None) and itm416.IsWindow():
                    self.sizer.Detach(itm416.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((6,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc97, pos=(6, 5), flag=wx.TOP | wx.EXPAND)
            
            self.sc98 = wx.SpinCtrl(self.pnl, value='0')
            self.sc98.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm417 = self.sizer.FindItemAtPosition((7,4))
                if (itm417!=None) and itm417.IsWindow():
                    self.sizer.Detach(itm417.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((7,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st98, pos=(7, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm436 = self.sizer.FindItemAtPosition((7,5))
                if (itm436!= None) and itm436.IsWindow():
                    self.sizer.Detach(itm436.GetWindow())
            if self.dir_array[0] == "upstream" and self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((7,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc98, pos=(7, 5), flag=wx.TOP | wx.EXPAND)
            self.pnl.SetSizerAndFit(self.sizer)
        if text_field == "10 Carriers":
            #self.text_parameters()
            if self.label_name == "Upstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((11,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(128 , 7500)
            if self.label_name == "Upstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((12,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((13,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((14,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            if self.label_name == "Upstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,0))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((15,1))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm411 = self.sizer.FindItemAtPosition((4,4))
                if (itm411 != None) and itm411.IsWindow():
                    self.sizer.Detach(itm411.GetWindow())

            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((4,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm412 = self.sizer.FindItemAtPosition((4,5))
                if (itm412!=None) and itm412.IsWindow():
                    self.sizer.Detach(itm412.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((4,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc95, pos=(4,5), flag=wx.TOP | wx.EXPAND)
            
            self.sc96 = wx.SpinCtrl(self.pnl, value='0')
            self.sc96.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm413 = self.sizer.FindItemAtPosition((5,4))
                if (itm413!=None) and itm413.IsWindow():
                    self.sizer.Detach(itm413.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((5,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st96, pos=(5, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm414 = self.sizer.FindItemAtPosition((5,5))
                if (itm414!=None) and itm414.IsWindow():
                    self.sizer.Detach(itm414.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((5,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc96, pos=(5, 5), flag=wx.TOP | wx.EXPAND)
            
            self.sc97 = wx.SpinCtrl(self.pnl, value='0')
            self.sc97.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm415 = self.sizer.FindItemAtPosition((6,4))
                if (itm415!=None) and itm415.IsWindow():
                    self.sizer.Detach(itm415.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((6,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st97, pos=(6, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm416 = self.sizer.FindItemAtPosition((6,5))
                if (itm416!=None) and itm416.IsWindow():
                    self.sizer.Detach(itm416.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((6,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc97, pos=(6, 5), flag=wx.TOP | wx.EXPAND)
            
            self.sc98 = wx.SpinCtrl(self.pnl, value='0')
            self.sc98.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm417 = self.sizer.FindItemAtPosition((7,4))
                if (itm417!=None) and itm417.IsWindow():
                    self.sizer.Detach(itm417.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((7,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st98, pos=(7, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm436 = self.sizer.FindItemAtPosition((7,5))
                if (itm436!= None) and itm436.IsWindow():
                    self.sizer.Detach(itm436.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((7,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc98, pos=(7, 5), flag=wx.TOP | wx.EXPAND)
		    
            self.sc99 = wx.SpinCtrl(self.pnl, value='0')
            self.sc99.SetRange(128,7500)
            if self.label_name == "Upstream":
                itm418 = self.sizer.FindItemAtPosition((8,4))
                if (itm418!=None) and itm418.IsWindow():
                    self.sizer.Detach(itm418.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((8,4))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.st99, pos=(8, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Upstream":
                itm437 = self.sizer.FindItemAtPosition((8,5))
                if (itm437!= None) and itm437.IsWindow():
                    self.sizer.Detach(itm437.GetWindow())
            if self.dir_array[0] == "upstream" or self.dir_array[1] == "downstream":
                itm401 = self.sizer.FindItemAtPosition((8,5))
                if (itm401 != None) and itm401.IsWindow():
                    self.sizer.Detach(itm401.GetWindow())
            self.sizer.Add(self.sc99, pos=(8, 5), flag=wx.TOP | wx.EXPAND)
            
            self.pnl.SetSizerAndFit(self.sizer)  

        return text_field

    def OnCombo_downstream(self, event): 
        #text_field = self.combo.GetValue().encode("utf-8")
        """ 
        print ("The value got from on combo is", text_field)
        if text_field == "1 Carrier":
            self.text_parameters()
            self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
        
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc9 = wx.SpinCtrl(self.pnl, value='0')
            self.sc9.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc9, pos=(11, 1), flag=wx.TOP | wx.EXPAND)

        if text_field == "2 Carriers":
            self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
            
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
        if text_field == "3 Carriers":
            self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
            
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
        if text_field == "4 Carriers":
            self.st93 = wx.StaticText(self.pnl, label='     Carrier4:')
            
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
        if text_field == "5 Carriers":
            self.st94 = wx.StaticText(self.pnl, label='     Carrier5:')
            
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
        if text_field == "6 Carriers":
            self.st95 = wx.StaticText(self.pnl, label='     Carrier6')
           
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc95, pos=(4, 5), flag=wx.TOP | wx.EXPAND)
        if text_field == "7 Carriers":
            self.st96 = wx.StaticText(self.pnl, label='     Carrier7:')
           
            self.sizer.Add(self.st96, pos=(5, 4), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc96 = wx.SpinCtrl(self.pnl, value='0')
            self.sc96.SetRange(-459, 1000)
           
            self.sizer.Add(self.sc96, pos=(5, 5), flag=wx.TOP | wx.EXPAND)
        if text_field == "8 Carriers":
            self.st97 = wx.StaticText(self.pnl, label='     Carrier8:')
           
            self.sizer.Add(self.st97, pos=(6, 4), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc97 = wx.SpinCtrl(self.pnl, value='0')
            self.sc97.SetRange(-459, 1000)
           
            self.sizer.Add(self.sc97, pos=(6, 5), flag=wx.TOP | wx.EXPAND)
        if text_field == "9 Carriers":
            self.st98 = wx.StaticText(self.pnl, label='     Carrier9:')
           
            self.sizer.Add(self.st98, pos=(7, 4), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc98 = wx.SpinCtrl(self.pnl, value='0')
            self.sc98.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc98, pos=(7, 5), flag=wx.TOP | wx.EXPAND)
        if text_field == "10 Carriers":
            #self.text_parameters()
            self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
            
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc9 = wx.SpinCtrl(self.pnl, value='0')
            self.sc9.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc9, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
            self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
            
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(-459, 1000)
           
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
            
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(-459, 1000)
           
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            self.st93 = wx.StaticText(self.pnl, label='     Carrier4:')
            
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(-459, 1000)
           
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND) 
            self.st94 = wx.StaticText(self.pnl, label='     Carrier5:')
            
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            self.st95 = wx.StaticText(self.pnl, label='     Carrier6')
           
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(-459, 1000)
           
            self.sizer.Add(self.sc95, pos=(4, 5), flag=wx.TOP | wx.EXPAND)
            self.st96 = wx.StaticText(self.pnl, label='     Carrier7:')
            
            self.sizer.Add(self.st96, pos=(5, 4), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc96 = wx.SpinCtrl(self.pnl, value='0')
            self.sc96.SetRange(-459, 1000)
           
            self.sizer.Add(self.sc96, pos=(5, 5), flag=wx.TOP | wx.EXPAND)
            self.st97 = wx.StaticText(self.pnl, label='     Carrier8:')
            
            self.sizer.Add(self.st97, pos=(6, 4), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc97 = wx.SpinCtrl(self.pnl, value='0')
            self.sc97.SetRange(-459, 1000)
           
            self.sizer.Add(self.sc97, pos=(6, 5), flag=wx.TOP | wx.EXPAND)
            self.st98 = wx.StaticText(self.pnl, label='     Carrier9:')
            
            self.sizer.Add(self.st98, pos=(7, 4), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc98 = wx.SpinCtrl(self.pnl, value='0')
            self.sc98.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc98, pos=(7, 5), flag=wx.TOP | wx.EXPAND) 
            self.st98 = wx.StaticText(self.pnl, label='     Carrier10:')
            
            self.sizer.Add(self.st98, pos=(8, 4), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc99 = wx.SpinCtrl(self.pnl, value='0')
            self.sc99.SetRange(-459, 1000)
            
            self.sizer.Add(self.sc99, pos=(8, 5), flag=wx.TOP | wx.EXPAND)
        """
        print("Added back after restoration")
        text_field = self.combo.GetValue().encode("utf-8")
        
        print ("The value got from on combo is", text_field)
        self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
        self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
        self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
        self.st93 = wx.StaticText(self.pnl, label='     Carrier4:')
        self.st94 = wx.StaticText(self.pnl, label='     Carrier5:')
        self.st95 = wx.StaticText(self.pnl, label='     Carrier6:')
        self.st96 = wx.StaticText(self.pnl, label='     Carrier7:')
        self.st97 = wx.StaticText(self.pnl, label='     Carrier8:')
        self.st98 = wx.StaticText(self.pnl, label='     Carrier9:')
        self.st99 = wx.StaticText(self.pnl, label='     Carrier10:')
        if text_field == "1 Carrier":
            print("I AM IN SYMBOL 1")
            #self.text_parameters()
            if self.label_name == "Downstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            itemCarrier1a = self.sizer.FindItemAtPosition((11,0))
            if itemCarrier1a == None: 
                self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
                self.sc91a = wx.SpinCtrl(self.pnl, value='0')
                self.sc91a.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
                itm4b = self.sizer.FindItemAtPosition((12,0))
                if (itm4b!=None) and itm4b.IsWindow():
                    self.sizer.Detach(itm4b.GetWindow())

                itm4c = self.sizer.FindItemAtPosition((12,1))
                if (itm4c!=None) and itm4c.IsWindow():
                    self.sizer.Detach(itm4c.GetWindow())
                    
                itm4d = self.sizer.FindItemAtPosition((13,0))
                if (itm4d!=None) and itm4d.IsWindow():
                    self.sizer.Detach(itm4d.GetWindow())

                itm4e = self.sizer.FindItemAtPosition((13,1))
                if (itm4e!=None) and itm4e.IsWindow():
                    self.sizer.Detach(itm4e.GetWindow())

                itm4f = self.sizer.FindItemAtPosition((14,0))
                if (itm4f!=None) and itm4f.IsWindow():
                    self.sizer.Detach(itm4f.GetWindow())

                itm4z = self.sizer.FindItemAtPosition((14,1))
                if (itm4z!=None) and itm4z.IsWindow():
                    self.sizer.Detach(itm4z.GetWindow())

                itm4g = self.sizer.FindItemAtPosition((15,0))
                if (itm4g!=None) and itm4g.IsWindow():
                    self.sizer.Detach(itm4g.GetWindow())

                itm4h = self.sizer.FindItemAtPosition((15,1))
                if (itm4h!=None) and itm4h.IsWindow():
                    self.sizer.Detach(itm4h.GetWindow())

                itm4i = self.sizer.FindItemAtPosition((4,4))
                if (itm4i!=None) and itm4i.IsWindow():
                    self.sizer.Detach(itm4i.GetWindow())

                itm4j = self.sizer.FindItemAtPosition((4,5))
                if (itm4j!=None) and itm4j.IsWindow():
                    self.sizer.Detach(itm4j.GetWindow())

                itm4k = self.sizer.FindItemAtPosition((5,4))
                if (itm4k!=None) and itm4k.IsWindow():
                    self.sizer.Detach(itm4k.GetWindow())

                itm4l = self.sizer.FindItemAtPosition((5,5))
                if (itm4l!=None) and itm4l.IsWindow():
                    self.sizer.Detach(itm4l.GetWindow())

                itm4m = self.sizer.FindItemAtPosition((6,4))
                if (itm4m!=None) and itm4m.IsWindow():
                    self.sizer.Detach(itm4m.GetWindow())

                itm4n = self.sizer.FindItemAtPosition((6,5))
                if (itm4n!=None) and itm4n.IsWindow():
                    self.sizer.Detach(itm4n.GetWindow())

                itm4o = self.sizer.FindItemAtPosition((7,4))
                if (itm4o!=None) and itm4o.IsWindow():
                    self.sizer.Detach(itm4o.GetWindow())

                itm4p = self.sizer.FindItemAtPosition((7,5))
                if (itm4p!=None) and itm4p.IsWindow():
                    self.sizer.Detach(itm4p.GetWindow())
                itm4q = self.sizer.FindItemAtPosition((8,4))
                if (itm4q!=None) and itm4q.IsWindow():
                    self.sizer.Detach(itm4q.GetWindow())

                itm4r = self.sizer.FindItemAtPosition((8,5))
                if (itm4r!=None) and itm4r.IsWindow():
                    self.sizer.Detach(itm4r.GetWindow())

            itemCarrier1 = self.sizer.FindItemAtPosition((11,1))
            if itemCarrier1 == None:
                self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
            
            item_st91 = self.sizer.FindItemAtPosition((12,0))
            if item_st91 != None and item_st91.IsShown():
                print("I am in st91")
                self.sizer.Detach(item_st91.GetWindow())
                self.st91.Hide()
            item_st92 = self.sizer.FindItemAtPosition((13,0))
            if item_st92 != None and item_st92.IsShown():
                print("I am in st912")
                self.sizer.Detach(item_st92.GetWindow())

                self.st92.Hide()

            item_st93 = self.sizer.FindItemAtPosition((14,0))
            if item_st93!= None and item_st93.IsShown():
                print("I am in st93")
                self.sizer.Detach(item_st93.GetWindow())

                self.st93.Hide()

            item_st94 = self.sizer.FindItemAtPosition((15,0))
            if item_st94 != None and item_st94.IsShown():
                print("I am in st94")
                self.sizer.Detach(item_st94.GetWindow())


                self.st94.Hide()

            item_st95 = self.sizer.FindItemAtPosition((4,4))
            if item_st95 != None and item_st95.IsShown():
                print("I am in st95")
                self.sizer.Detach(item_st95.GetWindow())

                self.st95.Hide()

            item_st96 = self.sizer.FindItemAtPosition((5,4))
            if item_st96 != None and item_st96.IsShown():
                print("I am in st96")
                self.sizer.Detach(item_st96.GetWindow())


                self.st96.Hide()

            item_st97 = self.sizer.FindItemAtPosition((6,4))
            if item_st97 != None and item_st97.IsShown():
                self.sizer.Detach(item_st97.GetWindow())
                print("I am in st97")

                self.st97.Hide()

            item_st98 = self.sizer.FindItemAtPosition((7,4))
            if item_st98 != None and item_st98.IsShown():
                print("I am in st98")
                self.sizer.Detach(item_st98.GetWindow())

                self.st98.Hide()
            item_st99 = self.sizer.FindItemAtPosition((8,4))
            if item_st99 != None and item_st99.IsShown():
                print("I am in st99")
                self.sizer.Detach(item_st99.GetWindow())

                self.st99.Hide()
           
            itm41a = self.sizer.FindItemAtPosition((12,1))
            if (itm41a!=None) and itm41a.IsWindow():
                self.sizer.Detach(itm41a.GetWindow())
                self.sc91a.Hide()
            itm41s = self.sizer.FindItemAtPosition((13,1))
            if (itm41s!=None) and itm41s.IsWindow():
                self.sizer.Detach(itm41.GetWindow())
                self.sc91.Hide()
            itm41b = self.sizer.FindItemAtPosition((14,1))
            if (itm41b!=None) and itm41b.IsWindow():
                self.sizer.Detach(itm41b.GetWindow())
                self.sc92.Hide()

            itm41c = self.sizer.FindItemAtPosition((15,1))
            if (itm41c!=None) and itm41c.IsWindow():
                self.sizer.Detach(itm41c.GetWindow())
                self.sc93.Hide()

            itm41d = self.sizer.FindItemAtPosition((4,5))
            if (itm41d!=None) and itm41d.IsWindow():
                self.sizer.Detach(itm41d.GetWindow())
                self.sc94.Hide()

            itm41e = self.sizer.FindItemAtPosition((5,5))
            if (itm41e!=None) and itm41e.IsWindow():
                self.sizer.Detach(itm41e.GetWindow())
                self.sc95.Hide()
            
            itm41f = self.sizer.FindItemAtPosition((6,5))
            if (itm41f!=None) and itm41f.IsWindow():
                self.sizer.Detach(itm41f.GetWindow())
                self.sc96.Hide()

            itm41g = self.sizer.FindItemAtPosition((7,5))
            if (itm41g!=None) and itm41g.IsWindow():
                self.sizer.Detach(itm41g.GetWindow())
                self.sc97.Hide()
                
            itm41h = self.sizer.FindItemAtPosition((8,5))
            if (itm41h!=None) and itm41h.IsWindow():
                self.sizer.Detach(itm41h.GetWindow())
                self.sc98.Hide()


        if text_field == "2 Carriers":
            if self.label_name == "Downstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)

        if text_field == "3 Carriers":
            self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
            if self.label_name == "Downstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)

        if text_field == "4 Carriers":
            self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
            if self.label_name == "Downstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st93 = wx.StaticText(self.pnl, label='     Carrier4:')
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)

        if text_field == "5 Carriers":
            self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
            if self.label_name == "Downstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st93 = wx.StaticText(self.pnl, label='     Carrier4:')
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st94 = wx.StaticText(self.pnl, label='     Carrier5:')
            if self.label_name == "Downstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)

        if text_field == "6 Carriers":
            self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
            if self.label_name == "Downstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st93 = wx.StaticText(self.pnl, label='     Carrier4:')
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st94 = wx.StaticText(self.pnl, label='     Carrier5:')
            if self.label_name == "Downstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st95 = wx.StaticText(self.pnl, label='     Carrier6:')
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm411 = self.sizer.FindItemAtPosition((4,4))
                if (itm411 != None) and itm411.IsWindow():
                    self.sizer.Detach(itm411.GetWindow())
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm412 = self.sizer.FindItemAtPosition((4,5))
                if (itm412!=None) and itm412.IsWindow():
                    self.sizer.Detach(itm412.GetWindow())
            self.sizer.Add(self.sc95, pos=(4,5), flag=wx.TOP | wx.EXPAND)

        if text_field == "7 Carriers":
            self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
            if self.label_name == "Downstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st93 = wx.StaticText(self.pnl, label='     Carrier4:')
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st94 = wx.StaticText(self.pnl, label='     Carrier5:')
            if self.label_name == "Downstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st95 = wx.StaticText(self.pnl, label='     Carrier6:')
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm411 = self.sizer.FindItemAtPosition((4,4))
                if (itm411 != None) and itm411.IsWindow():
                    self.sizer.Detach(itm411.GetWindow())
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm412 = self.sizer.FindItemAtPosition((4,5))
                if (itm412!=None) and itm412.IsWindow():
                    self.sizer.Detach(itm412.GetWindow())
            self.sizer.Add(self.sc95, pos=(4,5), flag=wx.TOP | wx.EXPAND)
            
            self.st96 = wx.StaticText(self.pnl, label='     Carrier7:')
            self.sc96 = wx.SpinCtrl(self.pnl, value='0')
            self.sc96.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm413 = self.sizer.FindItemAtPosition((5,4))
                if (itm413!=None) and itm413.IsWindow():
                    self.sizer.Detach(itm413.GetWindow())
            self.sizer.Add(self.st96, pos=(5, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm414 = self.sizer.FindItemAtPosition((5,5))
                if (itm414!=None) and itm414.IsWindow():
                    self.sizer.Detach(itm414.GetWindow())
            self.sizer.Add(self.sc96, pos=(5, 5), flag=wx.TOP | wx.EXPAND)
        if text_field == "8 Carriers":
            self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
            if self.label_name == "Downstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st93 = wx.StaticText(self.pnl, label='     Carrier4:')
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st94 = wx.StaticText(self.pnl, label='     Carrier5:')
            if self.label_name == "Downstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st95 = wx.StaticText(self.pnl, label='     Carrier6:')
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm411 = self.sizer.FindItemAtPosition((4,4))
                if (itm411 != None) and itm411.IsWindow():
                    self.sizer.Detach(itm411.GetWindow())
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm412 = self.sizer.FindItemAtPosition((4,5))
                if (itm412!=None) and itm412.IsWindow():
                    self.sizer.Detach(itm412.GetWindow())
            self.sizer.Add(self.sc95, pos=(4,5), flag=wx.TOP | wx.EXPAND)
            
            self.st96 = wx.StaticText(self.pnl, label='     Carrier7:')
            self.sc96 = wx.SpinCtrl(self.pnl, value='0')
            self.sc96.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm413 = self.sizer.FindItemAtPosition((5,4))
                if (itm413!=None) and itm413.IsWindow():
                    self.sizer.Detach(itm413.GetWindow())
            self.sizer.Add(self.st96, pos=(5, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm414 = self.sizer.FindItemAtPosition((5,5))
                if (itm414!=None) and itm414.IsWindow():
                    self.sizer.Detach(itm414.GetWindow())
            self.sizer.Add(self.sc96, pos=(5, 5), flag=wx.TOP | wx.EXPAND)
            
            self.st97 = wx.StaticText(self.pnl, label='     Carrier8:')
            self.sc97 = wx.SpinCtrl(self.pnl, value='0')
            self.sc97.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm415 = self.sizer.FindItemAtPosition((6,4))
                if (itm415!=None) and itm415.IsWindow():
                    self.sizer.Detach(itm415.GetWindow())
            self.sizer.Add(self.st97, pos=(6, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm416 = self.sizer.FindItemAtPosition((6,5))
                if (itm416!=None) and itm416.IsWindow():
                    self.sizer.Detach(itm416.GetWindow())
            self.sizer.Add(self.sc97, pos=(6, 5), flag=wx.TOP | wx.EXPAND)

        if text_field == "9 Carriers":
            self.st9 = wx.StaticText(self.pnl, label='     Carrier1:')
            if self.label_name == "Downstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.st91 = wx.StaticText(self.pnl, label='     Carrier2:')
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st92 = wx.StaticText(self.pnl, label='     Carrier3:')
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st93 = wx.StaticText(self.pnl, label='     Carrier4:')
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st94 = wx.StaticText(self.pnl, label='     Carrier5:')
            if self.label_name == "Downstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            
            self.st95 = wx.StaticText(self.pnl, label='     Carrier6:')
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm411 = self.sizer.FindItemAtPosition((4,4))
                if (itm411 != None) and itm411.IsWindow():
                    self.sizer.Detach(itm411.GetWindow())
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm412 = self.sizer.FindItemAtPosition((4,5))
                if (itm412!=None) and itm412.IsWindow():
                    self.sizer.Detach(itm412.GetWindow())
            self.sizer.Add(self.sc95, pos=(4,5), flag=wx.TOP | wx.EXPAND)
            
            self.st96 = wx.StaticText(self.pnl, label='     Carrier7:')
            self.sc96 = wx.SpinCtrl(self.pnl, value='0')
            self.sc96.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm413 = self.sizer.FindItemAtPosition((5,4))
                if (itm413!=None) and itm413.IsWindow():
                    self.sizer.Detach(itm413.GetWindow())
            self.sizer.Add(self.st96, pos=(5, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm414 = self.sizer.FindItemAtPosition((5,5))
                if (itm414!=None) and itm414.IsWindow():
                    self.sizer.Detach(itm414.GetWindow())
            self.sizer.Add(self.sc96, pos=(5, 5), flag=wx.TOP | wx.EXPAND)
            
            self.st97 = wx.StaticText(self.pnl, label='     Carrier8:')
            self.sc97 = wx.SpinCtrl(self.pnl, value='0')
            self.sc97.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm415 = self.sizer.FindItemAtPosition((6,4))
                if (itm415!=None) and itm415.IsWindow():
                    self.sizer.Detach(itm415.GetWindow())
            self.sizer.Add(self.st97, pos=(6, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm416 = self.sizer.FindItemAtPosition((6,5))
                if (itm416!=None) and itm416.IsWindow():
                    self.sizer.Detach(itm416.GetWindow())
            self.sizer.Add(self.sc97, pos=(6, 5), flag=wx.TOP | wx.EXPAND)
            
            self.st98 = wx.StaticText(self.pnl, label='     Carrier9:')
            self.sc98 = wx.SpinCtrl(self.pnl, value='0')
            self.sc98.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm417 = self.sizer.FindItemAtPosition((7,4))
                if (itm417!=None) and itm417.IsWindow():
                    self.sizer.Detach(itm417.GetWindow())
            self.sizer.Add(self.st98, pos=(7, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm436 = self.sizer.FindItemAtPosition((7,5))
                if (itm436!= None) and itm436.IsWindow():
                    self.sizer.Detach(itm436.GetWindow())
            self.sizer.Add(self.sc98, pos=(7, 5), flag=wx.TOP | wx.EXPAND)
        if text_field == "10 Carriers":
            #self.text_parameters()
            
            if self.label_name == "Downstream":
                itm40 = self.sizer.FindItemAtPosition((11,0))
                if (itm40 != None) and itm40.IsWindow():
                    self.sizer.Detach(itm40.GetWindow())
            self.sizer.Add(self.st9, pos=(11, 0), flag=wx.TOP | wx.EXPAND, border=5)
            self.sc91a = wx.SpinCtrl(self.pnl, value='0')
            self.sc91a.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm41 = self.sizer.FindItemAtPosition((11,1))
                if (itm41!=None) and itm41.IsWindow():
                    self.sizer.Detach(itm41.GetWindow())
            self.sizer.Add(self.sc91a, pos=(11, 1), flag=wx.TOP | wx.EXPAND)
             
            
            self.sc91 = wx.SpinCtrl(self.pnl, value='0')
            self.sc91.SetRange(1000 , 45000)
            if self.label_name == "Downstream":
                itm43 = self.sizer.FindItemAtPosition((12,0))
                if (itm43!= None) and itm43.IsWindow():
                    self.sizer.Detach(itm43.GetWindow())
            self.sizer.Add(self.st91, pos=(12, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm44 = self.sizer.FindItemAtPosition((12,1))
                if (itm44!= None) and itm44.IsWindow():
                    self.sizer.Detach(itm44.GetWindow())
            self.sizer.Add(self.sc91, pos=(12, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc92 = wx.SpinCtrl(self.pnl, value='0')
            self.sc92.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm45 = self.sizer.FindItemAtPosition((13,0))
                if (itm45!=None) and itm45.IsWindow():
                    self.sizer.Detach(itm45.GetWindow())
            self.sizer.Add(self.st92, pos=(13, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((13,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc92, pos=(13, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc93 = wx.SpinCtrl(self.pnl, value='0')
            self.sc93.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm47 = self.sizer.FindItemAtPosition((14,0))
                if (itm47 != None) and itm47.IsWindow():
                    self.sizer.Detach(itm47.GetWindow())
            self.sizer.Add(self.st93, pos=(14, 0), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":     
                itm46 = self.sizer.FindItemAtPosition((14,1))
                if (itm46!= None) and itm46.IsWindow():
                    self.sizer.Detach(itm46.GetWindow())
            self.sizer.Add(self.sc93, pos=(14, 1), flag=wx.TOP | wx.EXPAND)
            
            if self.label_name == "Downstream":
                itm48 = self.sizer.FindItemAtPosition((15,0))
                if (itm48 != None) and itm48.IsWindow():
                    self.sizer.Detach(itm48.GetWindow())
            self.sizer.Add(self.st94, pos=(15, 0), flag=wx.TOP | wx.EXPAND, border=15)
            self.sc94 = wx.SpinCtrl(self.pnl, value='0')
            self.sc94.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm49 = self.sizer.FindItemAtPosition((15,1))
                if (itm49 != None) and itm49.IsWindow():
                    self.sizer.Detach(itm49.GetWindow())
            self.sizer.Add(self.sc94, pos=(15, 1), flag=wx.TOP | wx.EXPAND)
            
            self.sc95 = wx.SpinCtrl(self.pnl, value='0')
            self.sc95.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm411 = self.sizer.FindItemAtPosition((4,4))
                if (itm411 != None) and itm411.IsWindow():
                    self.sizer.Detach(itm411.GetWindow())
            self.sizer.Add(self.st95, pos=(4, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm412 = self.sizer.FindItemAtPosition((4,5))
                if (itm412!=None) and itm412.IsWindow():
                    self.sizer.Detach(itm412.GetWindow())
            self.sizer.Add(self.sc95, pos=(4,5), flag=wx.TOP | wx.EXPAND)
            
            self.sc96 = wx.SpinCtrl(self.pnl, value='0')
            self.sc96.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm413 = self.sizer.FindItemAtPosition((5,4))
                if (itm413!=None) and itm413.IsWindow():
                    self.sizer.Detach(itm413.GetWindow())
            self.sizer.Add(self.st96, pos=(5, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm414 = self.sizer.FindItemAtPosition((5,5))
                if (itm414!=None) and itm414.IsWindow():
                    self.sizer.Detach(itm414.GetWindow())
            self.sizer.Add(self.sc96, pos=(5, 5), flag=wx.TOP | wx.EXPAND)
            
            self.sc97 = wx.SpinCtrl(self.pnl, value='0')
            self.sc97.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm415 = self.sizer.FindItemAtPosition((6,4))
                if (itm415!=None) and itm415.IsWindow():
                    self.sizer.Detach(itm415.GetWindow())
            self.sizer.Add(self.st97, pos=(6, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm416 = self.sizer.FindItemAtPosition((6,5))
                if (itm416!=None) and itm416.IsWindow():
                    self.sizer.Detach(itm416.GetWindow())
            self.sizer.Add(self.sc97, pos=(6, 5), flag=wx.TOP | wx.EXPAND)
            
            self.sc98 = wx.SpinCtrl(self.pnl, value='0')
            self.sc98.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm417 = self.sizer.FindItemAtPosition((7,4))
                if (itm417!=None) and itm417.IsWindow():
                    self.sizer.Detach(itm417.GetWindow())
            self.sizer.Add(self.st98, pos=(7, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm436 = self.sizer.FindItemAtPosition((7,5))
                if (itm436!= None) and itm436.IsWindow():
                    self.sizer.Detach(itm436.GetWindow())
            self.sizer.Add(self.sc98, pos=(7, 5), flag=wx.TOP | wx.EXPAND)
		    
            self.sc99 = wx.SpinCtrl(self.pnl, value='0')
            self.sc99.SetRange(1000,45000)
            if self.label_name == "Downstream":
                itm418 = self.sizer.FindItemAtPosition((8,4))
                if (itm418!=None) and itm418.IsWindow():
                    self.sizer.Detach(itm418.GetWindow())
            self.sizer.Add(self.st99, pos=(8, 4), flag=wx.TOP | wx.EXPAND, border=15)
            if self.label_name == "Downstream":
                itm437 = self.sizer.FindItemAtPosition((8,5))
                if (itm437!= None) and itm437.IsWindow():
                    self.sizer.Detach(itm437.GetWindow())
            self.sizer.Add(self.sc99, pos=(8, 5), flag=wx.TOP | wx.EXPAND) 
        self.pnl.SetSizerAndFit(self.sizer)    
        return text_field
       

    def OnChoice(self,event): 
      self.choice.GetString
      self.choice.GetSelection() 
    
    def OnClose(self, e):

        self.Close(True)

    def OnCompute(self, e):

        try:
            nms_ip = self.sc.GetValue()
        
            print ("THe fahr value", nms_ip)
            test_ip = ipaddress.ip_address(nms_ip)
            print("THe IP ADdress", test_ip)
        except:
            print("Please Enter a Valid IP ADdress")
            sys.exit(-1)

        nms_user = self.sc1.GetValue().encode("utf-8")

        print("The nms user", nms_user)

        nms_pass = self.sc2.GetValue().encode("utf-8")

        print("The pass", nms_pass)

        try:
            pp_ip = self.sc3.GetValue()

            ipaddress.ip_address(pp_ip)
            print("The pp ip", pp_ip)
        except:
            print("Please Enter a valid IP Address")
            sys.exit(-1)
            

        pp_user = self.sc4.GetValue().encode("utf-8")

        print("The pp user", pp_user)

        pp_pass = self.sc5.GetValue().encode("utf-8")

        time = self.sc0.GetValue().encode("utf-8")
        print ("The TIme set is", time)

        print("The pp pass", pp_pass)

        #try:
        if self.cb.GetValue() == True:
            if self.label_name == "Downstream" and self.cb.GetLabel() == "Default Downstream": 
                value_test = self.st_up_default_values.GetLabel()
                print("I AM IN TEST AND THIS IS THE LABEL>>>", value_test)   
                value_test_encoded = value_test.encode("utf-8")
                symbol_list = value_test_encoded.split(",")
                print("The Symbol list after the downstream check has been selected", symbol_list)
            elif self.label_name == "Upstream" and self.cb.GetLabel() == "Default Upstream":
                value_test_upstream = self.st_up_default_values.GetLabel()
                print("I AM IN TEST AND THIS IS THE LABEL UPSTREAM>>>", value_test_upstream)   
                value_test_encoded = value_test_upstream.encode("utf-8")
                symbol_list = value_test_encoded.split(",")
                print("The Symbol list after the upstream check has been selected", symbol_list)
                raw_input("WAIT FOR EXAMINATION IN UPSTREAM...")

            if self.label_name == "Upstream":
                test_python_script_network.func_include_filename(nms_ip, nms_user, nms_pass, pp_ip, pp_user, pp_pass, symbol_list, time)
                test_python_script_network.main(nms_ip, nms_user, nms_pass, pp_ip, pp_user, pp_pass, symbol_list, time)
    
            elif self.label_name == "Downstream":
                downstream_modified_gw_user_pair.main(nms_ip, nms_user, nms_pass, pp_ip, pp_user, pp_pass, symbol_list)
        #except:
        elif self.cb.GetValue() == False:    
            try: 
                Carrier1 = self.sc91a.GetValue()
            except:
                Carrier1 = ""
                print ("THE VALUE 1", Carrier1)

            try:
                Carrier2 = self.sc91.GetValue()
            except:
                Carrier2 = ""
                print("THE VALUE 2", Carrier2)
            try:
                Carrier3 = self.sc92.GetValue()
            except:
                Carrier3 = ""
                print("THE VALUE  3", Carrier3)
            
            try:
                Carrier4 = self.sc93.GetValue()
            except:
                Carrier4 = ""
                print("THE VALUE  4", Carrier4)
            
            try:
                Carrier5 = self.sc94.GetValue()
            except:
                Carrier5 = ""
                print("THE VALUE  5", Carrier5)
            
            try:
                Carrier6 = self.sc95.GetValue()
            except:
                Carrier6 = ""
                print("THE VALUE  6", Carrier6)
            
            try:
                Carrier7 = self.sc96.GetValue()
            except:
                Carrier7 = ""
                print("THE VALUE  7", Carrier7)
            
            try:
                Carrier8 = self.sc97.GetValue()
            except:
                Carrier8 = ""
                print("THE VALUE  8", Carrier8)
            
            try:
                Carrier9 = self.sc98.GetValue()
            except:
                Carrier9 = ""
                print("THE VALUE  9", Carrier9)
            
            try:
                Carrier10 = self.sc99.GetValue()
            except:
                Carrier10 = ""
                print("THE VALUE  10", Carrier10)
            
            #cels = round((fahr - 32) * 5 / 9.0, 2)
    #        self.celsius.SetLabel(str(cels))
            symbol_list = []
            symbol_list.append(Carrier1)
            symbol_list.append(Carrier2)
            symbol_list.append(Carrier3)
            symbol_list.append(Carrier4)
            symbol_list.append(Carrier5)
            symbol_list.append(Carrier6)
            symbol_list.append(Carrier7)
            symbol_list.append(Carrier8)
            symbol_list.append(Carrier9)
            symbol_list.append(Carrier10)

            print("THE LENGTH OF THE LIST", symbol_list)
            raw_input("WAIT FOR EXAMINATION...")
            
            symbol_list = filter(None, symbol_list) 
            print ("The symbol list is", symbol_list)
            raw_input("WAIT FOR EXAMINATION...")
        
            if self.label_name == "Upstream":
                test_python_script_network.func_include_filename(nms_ip, nms_user, nms_pass, pp_ip, pp_user, pp_pass, symbol_list)
                test_python_script_network.main(nms_ip, nms_user, nms_pass, pp_ip, pp_user, pp_pass, symbol_list)
        
            elif self.label_name == "Downstream":
                downstream_modified_gw_user_pair.main(nms_ip, nms_user, nms_pass, pp_ip, pp_user, pp_pass, symbol_list)


        
        return (nms_ip, nms_user, nms_pass, pp_ip, pp_user, pp_pass, symbol_list)
    
class IncorrectcomboError():
    pass


def main():
    try: 
        app = wx.App(clearSigInt=False)
        ex = Example(None, title='LAYER 1 AUTOMATION CONSOLE')
    
        ex.Show()
        app.MainLoop()
    except KeyboardInterrupt:
        print("TEST<<>?>")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ("Hello")