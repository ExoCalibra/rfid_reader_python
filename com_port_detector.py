#!python
# -*- coding: utf-8 -*-
"""
COM Port Detection Utility
Helps identify available COM ports for RFID reader connection
"""

import serial
import serial.tools.list_ports

def list_available_ports():
    """List all available COM ports"""
    print("Available COM Ports:")
    print("=" * 40)
    
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("No COM ports found!")
        return []
    
    for i, port in enumerate(ports, 1):
        print(f"{i}. {port.device}")
        print(f"   Description: {port.description}")
        print(f"   Manufacturer: {port.manufacturer}")
        print(f"   Hardware ID: {port.hwid}")
        print()
    
    return [port.device for port in ports]

def test_port_connection(port_name):
    """Test if a specific port can be opened"""
    print(f"Testing connection to {port_name}...")
    
    try:
        # Try to open the port
        ser = serial.Serial(port=port_name, baudrate=9600, timeout=1)
        
        if ser.is_open:
            print(f"✓ Successfully opened {port_name}")
            ser.close()
            return True
        else:
            print(f"✗ Failed to open {port_name}")
            return False
            
    except serial.SerialException as e:
        print(f"✗ Error opening {port_name}: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error with {port_name}: {e}")
        return False

def main():
    """Main function to detect and test COM ports"""
    print("COM Port Detection Utility")
    print("=" * 40)
    print()
    
    # List available ports
    available_ports = list_available_ports()
    
    if not available_ports:
        print("No COM ports detected. Please check your hardware connections.")
        return
    
    print("Testing port connections...")
    print("-" * 40)
    
    working_ports = []
    for port in available_ports:
        if test_port_connection(port):
            working_ports.append(port)
        print()
    
    print("Summary:")
    print("-" * 40)
    if working_ports:
        print(f"✓ Working ports: {', '.join(working_ports)}")
        print(f"   Recommended: Use {working_ports[0]} for your RFID reader")
    else:
        print("✗ No working ports found")
        print("   Check your hardware connections and drivers")
    
    print("\nTo use a different port, edit rfid_reader_test.py and change:")
    print("   port='COM4' to port='COM[X]' where X is your preferred port")

if __name__ == "__main__":
    main()

