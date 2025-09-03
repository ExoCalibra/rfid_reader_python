e
import serial
import time
import sys
from datetime import datetime

class RFIDReader:
    def __init__(self, port='COM3', baudrate=9600, timeout=1):
        """
        Initialize RFID reader with serial connection parameters
        
        Args:
            port (str): Serial port (default: COM3)
            baudrate (int): Baud rate (default: 9600)
            timeout (int): Read timeout in seconds (default: 1)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        
    def connect(self):
        """Establish connection to the RFID reader"""
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout
            )
            
            if self.serial_connection.is_open:
                print(f"Successfully connected to {self.port}")
                print(f"   Baudrate: {self.baudrate}")
                print(f"   Data bits: 8")
                print(f"   Parity: None")
                print(f"   Stop bits: 1")
                print(f"   Flow control: None")
                return True
            else:
                print(f"Failed to open {self.port}")
                return False
                
        except serial.SerialException as e:
            print(f"Serial connection error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
    
    def disconnect(self):
        """Close the serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"Disconnected from {self.port}")
    
    def read_rfid(self):
        """Read RFID data from the serial port"""
        if not self.serial_connection or not self.serial_connection.is_open:
            print("No active connection")
            return None
        
        try:
            # Read available data
