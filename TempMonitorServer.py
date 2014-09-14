#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Modbus TestKit: Implementation of Modbus protocol in python

 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr

 This is distributed under GNU LGPL license, see license.txt

 This example shows how to create a modbus server in charge of monitoring 
 cpu consumption the machine

"""

from modbus_tk.simulator import *
from modbus_tk.simulator_rpc_client import SimulatorRpcClient
from modbus_tk.utils import WorkerThread
from modbus_tk.defines import *
from modbus_tk.modbus_tcp import TcpServer
from modbus_tk.hooks import install_hook
import time


def queryTemperature():
    from pysnmp.entity.rfc3413.oneliner import cmdgen

    temp = 0

    #myoid = "1.3.6.1.4.1.2620.1.6.7.8.1.1.3.2.0" # mb temp
    myoid = "1.3.6.1.4.1.2620.1.6.7.2.4.0" # cpu usage in perct
    
    myagent = '10.0.0.208'
    mycommunity = 'vpn123'


    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(mycommunity),
        cmdgen.UdpTransportTarget((myagent, 161)),
        myoid
    )

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?'
                )
            )
        else:
            for name, val in varBinds:
                print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                temp = int(str(val)) if val else 0
                
    return temp

class SystemDataCollector:        
    """The class in charge of getting the CPU load"""
    def __init__(self, refresh_rate_in_sec):
        """Constructor"""
        self._simu = SimulatorRpcClient()
        self._max_count = refresh_rate_in_sec * 10    
        self._count = self._max_count-1
        
    def collect(self):
        """get the CPU load thanks to WMI"""
        try:
            self._count += 1
            if self._count >= self._max_count:
                self._count = 0
                #WMI get the load percentage of the machine
                #from win32com.client import GetObject
                #wmi = GetObject('winmgmts:')
                #cpu = wmi.InstancesOf('Win32_Processor')
                #for (_cpu, i) in zip(cpu, xrange(10)):
                    #value = _cpu.Properties_('LoadPercentage').Value
                    #cpu_usage = int(str(value)) if value else 0
                    
                    #execute a RPC command for changing the value
                    #self._simu.set_values(1, "Cpu", i, (cpu_usage, ))
                temp = queryTemperature()
                self._simu.set_values(1, "Temp", 1, (temp, ))
        except Exception, excpt:
            LOGGER.debug("SystemDataCollector error: %s", str(excpt))
        time.sleep(0.1)
   

def print_me(args):
    """hook function example"""
    (server, request) = args
    print "print_me: len = ", len(request)
    return None
    
def setblock_hook(args):
    (block, slice, values) = args
    print block
    if id(block) == id(switch_block):
        print "setting switch block"
    print slice
    print values
    return None
        
if __name__ == "__main__":
    
    print "temp is %d" % queryTemperature()
    
    #create the object for getting CPU data
    data_collector = SystemDataCollector(5) 
    #create the thread in charge of calling the data collector
    system_monitor = WorkerThread(data_collector.collect)
    
    #create the modbus TCP simulator and one slave 
    #and one block of analog inputs
    simu = Simulator(TcpServer())
    slave = simu.server.add_slave(1)
    slave.add_block("Temp", ANALOG_INPUTS, 0, 10)
    
    slave.add_block("switch", modbus_tk.defines.COILS, 100, 10)
    switch_block = slave._get_block("switch")
    print "switch block"
    print switch_block
    
    install_hook('modbus.ModbusBlock.setitem', setblock_hook)
    # modbus.Slave.handle_read_coils_request
    # modbus.Slave.handle_read_discrete_inputs_request
    # modbus.Slave.handle_read_holding_registers_request
    # modbus.Slave.handle_read_input_registers_request
    
    try:
        LOGGER.info("'quit' for closing the server")
        
        #start the data collect
        system_monitor.start()
        
        #start the simulator! will block until quit command is received
        simu.start()
            
    except Exception, excpt:
        print excpt
            
    finally:
        #close the simulator
        simu.close()
        #stop the data collect
        system_monitor.stop()
        
        