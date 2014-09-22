


#simple Modbus client
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

from modbus_tk.utils import WorkerThread

import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
from PyQt4 import QtGui
from PyQt4.QtCore import QTimer

master = modbus_tcp.TcpMaster(host="127.0.0.1", port=502)


def collect_data():
	print "collecting data"
	coils = master.execute(1, cst.READ_COILS , 100, 10)
	reg = master.execute(1, cst.READ_INPUT_REGISTERS , 0, 10)
	#print coils
	#print reg
	global app
	#print app.allWidgets()
	print "monitored value %d" % reg[1]
	global lcd
	lcd.display(reg[1])
	return None

class TemperatureCollector:        

    def __init__(self):
        self.master = modbus_tcp.TcpMaster(host="127.0.0.1", port=502)
		
    def collect(self):
		print "collecting data START"
		coils = self.master.execute(1, cst.READ_COILS , 100, 10)
		print coils
		time.sleep(1)
		reg = master.execute(1, cst.READ_INPUT_REGISTERS , 0, 10)
		print reg
		global lcd
		lcd.display(reg[1])
		print "collecting data DONE"

def do_modbus():
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
		print master.execute(1, cst.READ_COILS , 101, 10)

    except modbus_tk.modbus.ModbusError, e:
        print "Modbus error ", e.get_exception_code()

    except Exception, e2: print "Error ", str(e2)

def main():
	global app 
	app = QtGui.QApplication(sys.argv)

	w = QtGui.QWidget()
	w.resize(250, 150)
	w.move(300, 300)
	w.setWindowTitle('Simple')

	global lcd
	lcd = QtGui.QLCDNumber(w)
	lcd.setGeometry(5, 5, 90, 100)
	lcd.display(12345)
	
	square = QtGui.QFrame(w)
	square.setGeometry(150, 70, 100, 100)
	square.setStyleSheet("QWidget { background-color: %s }" %  "green")
	
	lbl = QtGui.QLabel(w)
	lbl.setText("Temperature")
	lbl.move(10,10)
	
	w.show()
	
	# Create a QTimer
	timer = QTimer()
	# Connect it to f
	timer.timeout.connect(collect_data)
	# Call f() every 2 seconds
	timer.start(2000)
	
	sys.exit(app.exec_())

if __name__ == "__main__":
	app = None
	main()
    
        
        
    
