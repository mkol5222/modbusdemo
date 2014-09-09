import modbus_tk
import modbus_tk.modbus_tcp as modbus_tcp
import threading
import modbus_tk.defines as mdef

logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

# Modbus server
server = modbus_tcp.TcpServer(address="127.0.0.1", port=502)

#creates a slave with id 1
slave1 = server.add_slave(1)
#add 2 blocks of holding registers
slave1.add_block("a", mdef.HOLDING_REGISTERS, 0, 100)#address 0, length 100
slave1.add_block("b", mdef.HOLDING_REGISTERS, 200, 20)#address 200, length 20
# registers used by demo client
slave1.add_block("z", mdef.HOLDING_REGISTERS, 100, 100)#address 100, length 100

#creates another slave with id 5
slave5 = server.add_slave(5)
slave5.add_block("c", mdef.COILS, 0, 100)
slave5.add_block("d", mdef.HOLDING_REGISTERS, 0, 100)

#set the values of registers at address 0
slave1.set_values("a", 0, range(100))
#set the values of registers at address 0
slave1.set_values("z", 102, range(10))

server.start()
