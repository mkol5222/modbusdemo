
#simple Modbus client
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

if __name__ == "__main__":
    try:
		#Connect to the slave
		master = modbus_tcp.TcpMaster(host="127.0.0.1", port=502)
		# read registers
		#print master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 6)
		# write 0-11 to registers
		#master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12))
		
		print master.execute(1, cst.READ_INPUT_REGISTERS , 0, 10)
		print master.execute(1, cst.WRITE_SINGLE_COIL , 100, output_value=1)
		print master.execute(1, cst.READ_COILS , 100, 10)
		print master.execute(1, cst.WRITE_SINGLE_COIL , 101, output_value=1)
		print master.execute(1, cst.READ_COILS , 100, 10)

    except modbus_tk.modbus.ModbusError, e:
        print "Modbus error ", e.get_exception_code()

    except Exception, e2:
        print "Error ", str(e2)
