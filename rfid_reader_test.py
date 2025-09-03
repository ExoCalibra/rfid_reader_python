#!python
# -*- coding: utf-8 -*-
"""
Enhanced RFID Reader Test Application
Supports Turkish ID Cards and provides detailed card information
Python Path: C:/Users/dissc/AppData/Local/Programs/Python/Python313/python.exe
"""

# type: ignore
import serial
import time
import sys
import re
from datetime import datetime
from typing import Optional, Dict, Any

class CardInfo:
    """Class to store and analyze card information"""
    
    def __init__(self, raw_data: str, hex_data: str):
        self.raw_data = raw_data
        self.hex_data = hex_data
        self.card_type = self._detect_card_type()
        self.parsed_data = self._parse_card_data()
    
    def _detect_card_type(self) -> str:
        """Detect the type of card based on data patterns"""
        data = self.raw_data.upper()
        
        # Turkish ID Card patterns
        if len(data) == 11 and data.isdigit():
            return "Turkish ID Card (TC Kimlik)"
        
        # Check for common RFID patterns
        if len(data) == 10 and data.isalnum():
            return "Standard RFID Card"
        
        # Check for longer numeric sequences
        if len(data) >= 16 and data.isdigit():
            return "Long Format RFID Card"
        
        # Check for hex-like patterns
        if re.match(r'^[0-9A-F]+$', data) and len(data) >= 8:
            return "Hexadecimal RFID Card"
        
        return "Unknown Card Type"
    
    def _parse_card_data(self) -> Dict[str, Any]:
        """Parse card data based on detected type"""
        data = self.raw_data.upper()
        parsed = {
            "card_type": self.card_type,
            "raw_data": self.raw_data,
            "hex_data": self.hex_data,
            "length": len(self.raw_data),
            "timestamp": datetime.now().isoformat()
        }
        
        if self.card_type == "Turkish ID Card (TC Kimlik)":
            parsed.update(self._parse_turkish_id(data))
        elif "RFID" in self.card_type:
            parsed.update(self._parse_rfid_card(data))
        
        return parsed
    
    def _parse_turkish_id(self, data: str) -> Dict[str, Any]:
        """Parse Turkish ID card data"""
        if len(data) != 11 or not data.isdigit():
            return {"error": "Invalid Turkish ID format"}
        
        # Turkish ID validation algorithm
        digits = [int(d) for d in data]
        
        # Calculate check digits
        odd_sum = sum(digits[i] for i in range(0, 9, 2))
        even_sum = sum(digits[i] for i in range(1, 8, 2))
        
        # 10th digit validation
        digit_10 = (odd_sum * 7 - even_sum) % 10
        
        # 11th digit validation
        first_10_sum = sum(digits[:10])
        digit_11 = first_10_sum % 10
        
        is_valid = (digits[9] == digit_10 and digits[10] == digit_11)
        
        return {
            "turkish_id": {
                "full_number": data,
                "is_valid": is_valid,
                "check_digit_10": digit_10,
                "check_digit_11": digit_11,
                "actual_digit_10": digits[9],
                "actual_digit_11": digits[10],
                "validation_passed": is_valid
            }
        }
    
    def _parse_rfid_card(self, data: str) -> Dict[str, Any]:
        """Parse standard RFID card data"""
        parsed = {
            "rfid_data": {
                "card_number": data,
                "numeric_only": ''.join(filter(str.isdigit, data)),
                "alpha_numeric": ''.join(filter(str.isalnum, data)),
                "hex_representation": self.hex_data
            }
        }
        
        # Try to extract meaningful patterns
        if len(data) >= 8:
            # Common RFID formats
            if len(data) == 10:
                parsed["rfid_data"]["format"] = "Standard 10-digit"
            elif len(data) == 16:
                parsed["rfid_data"]["format"] = "Extended 16-digit"
            elif len(data) == 8:
                parsed["rfid_data"]["format"] = "Short 8-digit"
            else:
                parsed["rfid_data"]["format"] = f"Custom {len(data)}-digit"
        
        return parsed
    
    def get_detailed_info(self) -> str:
        """Get formatted detailed information about the card"""
        info_lines = [
            f"Card Type: {self.card_type}",
            f"Raw Data: {self.raw_data}",
            f"Hex Data: {self.hex_data}",
            f"Decimal Data: {self._get_decimal_data()}",
            f"Data Length: {len(self.raw_data)} characters",
            f"Timestamp: {self.parsed_data['timestamp']}",
            ""
        ]
        
        if self.card_type == "Turkish ID Card (TC Kimlik)":
            turkish_data = self.parsed_data.get("turkish_id", {})
            if turkish_data:
                info_lines.extend([
                    "Turkish ID Card Details:",
                    f"  Full Number: {turkish_data.get('full_number', 'N/A')}",
                    f"  Valid: {'✓ Yes' if turkish_data.get('is_valid') else '✗ No'}",
                    f"  Check Digit 10: {turkish_data.get('check_digit_10')} (Expected: {turkish_data.get('actual_digit_10')})",
                    f"  Check Digit 11: {turkish_data.get('check_digit_11')} (Expected: {turkish_data.get('actual_digit_11')})",
                    ""
                ])
        
        elif "RFID" in self.card_type:
            rfid_data = self.parsed_data.get("rfid_data", {})
            if rfid_data:
                info_lines.extend([
                    "RFID Card Details:",
                    f"  Card Number: {rfid_data.get('card_number', 'N/A')}",
                    f"  Format: {rfid_data.get('format', 'Unknown')}",
                    f"  Numeric Only: {rfid_data.get('numeric_only', 'N/A')}",
                    f"  Alpha-Numeric: {rfid_data.get('alpha_numeric', 'N/A')}",
                    ""
                ])
        
        return "\n".join(info_lines)
    
    def _get_decimal_data(self) -> str:
        """Convert hex data to decimal representation"""
        try:
            # For RFID cards, convert the raw data directly to decimal
            if self.card_type == "Hexadecimal RFID Card":
                # Convert the raw RFID data (like CAB9EAF2) to decimal
                decimal_number = int(self.raw_data, 16)
                return str(decimal_number)
            else:
                # For other cards, convert hex string to decimal
                hex_chars = self.hex_data.replace(' ', '')
                if len(hex_chars) % 2 == 0:
                    # Convert entire hex string to decimal
                    decimal_number = int(hex_chars, 16)
                    return str(decimal_number)
                else:
                    return "Invalid hex format"
        except ValueError:
            return "Conversion error"

class EnhancedRFIDReader:
    def __init__(self, port='COM4', baudrate=9600, timeout=1):
        """
        Initialize enhanced RFID reader with serial connection parameters
        
        Args:
            port (str): Serial port (default: COM4)
            baudrate (int): Baud rate (default: 9600)
            timeout (int): Read timeout in seconds (default: 1)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self.read_count = 0
        self.last_card_info = None
        
    def connect(self):
        """Establish connection to the RFID reader"""
        try:
            # Try to close any existing connection first
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
                time.sleep(0.5)  # Give time for port to be released
            
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout
            )
            
            if self.serial_connection.is_open:
                print(f"✓ Successfully connected to {self.port}")
                print(f"   Baudrate: {self.baudrate}")
                print(f"   Data bits: 8")
                print(f"   Parity: None")
                print(f"   Stop bits: 1")
                print(f"   Flow control: None")
                return True
            else:
                print(f"✗ Failed to open {self.port}")
                return False
                
        except serial.SerialException as e:
            print(f"✗ Serial connection error: {e}")
            if "PermissionError" in str(e) or "Access denied" in str(e):
                print(f"   This usually means {self.port} is being used by another application")
                print(f"   Try closing other applications that might be using {self.port}")
                print(f"   Or try running the application as Administrator")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False
    
    def disconnect(self):
        """Close the serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"✓ Disconnected from {self.port}")
    
    def read_rfid(self):
        """Read RFID data from the serial port"""
        if not self.serial_connection or not self.serial_connection.is_open:
            print("✗ No active connection")
            return None
        
        try:
            # Read available data
            if self.serial_connection.in_waiting > 0:
                data = self.serial_connection.read(self.serial_connection.in_waiting)
                return data
            return None
            
        except serial.SerialException as e:
            print(f"✗ Read error: {e}")
            return None
    
    def read_complete_rfid(self):
        """Read complete RFID data with proper buffering"""
        if not self.serial_connection or not self.serial_connection.is_open:
            return None
        
        try:
            # Wait for data to be available
            if self.serial_connection.in_waiting == 0:
                return None
            
            # Read all available data
            data = b""
            while self.serial_connection.in_waiting > 0:
                chunk = self.serial_connection.read(self.serial_connection.in_waiting)
                data += chunk
                time.sleep(0.01)  # Small delay to ensure complete transmission
            
            return data if data else None
            
        except serial.SerialException as e:
            # Don't spam error messages for common read issues
            if "ClearCommError" not in str(e) and "PermissionError" not in str(e):
                print(f"✗ Read error: {e}")
            return None
        except Exception as e:
            print(f"✗ Unexpected read error: {e}")
            return None
    
    def process_card_data(self, data: bytes) -> Optional[CardInfo]:
        """Process raw card data and create CardInfo object"""
        if not data:
            return None
        
        # Convert bytes to string and clean up
        rfid_data = data.decode('utf-8', errors='ignore').strip()
        
        # Remove common prefixes/suffixes and clean the data
        rfid_data = rfid_data.replace('\r', '').replace('\n', '').replace('\x00', '')
        
        # Filter out very short reads (likely incomplete)
        if len(rfid_data) < 8:
            return None
        
        # Convert to hex for analysis
        hex_data = ' '.join([f'{b:02X}' for b in data])
        
        return CardInfo(rfid_data, hex_data)
    
    def monitor_rfid(self, duration=None, show_detailed=True):
        """
        Monitor for RFID reads continuously with enhanced information
        
        Args:
            duration (int): Duration to monitor in seconds (None for infinite)
            show_detailed (bool): Whether to show detailed card information
        """
        if not self.connect():
            return
        
        print("\n" + "="*60)
        print("Enhanced RFID Monitoring Started")
        print("="*60)
        print("Supported Card Types:")
        print("  • Turkish ID Cards (TC Kimlik)")
        print("  • Standard RFID Cards")
        print("  • Long Format RFID Cards")
        print("  • Hexadecimal RFID Cards")
        print("="*60)
        print("Please scan an RFID card/tag")
        print("Press Ctrl+C to stop\n")
        
        start_time = time.time()
        last_read = ""
        
        try:
            while True:
                # Check if duration limit reached
                if duration and (time.time() - start_time) > duration:
                    print(f"\nMonitoring stopped after {duration} seconds")
                    break
                
                # Read RFID data with better buffering
                data = self.read_complete_rfid()
                
                if data:
                    card_info = self.process_card_data(data)
                    
                    if card_info and card_info.raw_data != last_read:
                        self.read_count += 1
                        last_read = card_info.raw_data
                        self.last_card_info = card_info
                        
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"\n[{timestamp}] Read #{self.read_count}")
                        print("-" * 50)
                        
                        if show_detailed:
                            print(card_info.get_detailed_info())
                        else:
                            print(f"Card Type: {card_info.card_type}")
                            print(f"Data: {card_info.raw_data}")
                            print(f"Hex: {card_info.hex_data}")
                            print(f"Decimal: {card_info._get_decimal_data()}")
                        
                        print("-" * 50)
                
                # Small delay to prevent high CPU usage
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n✓ Monitoring stopped by user")
            if self.read_count > 0:
                print(f"Total reads: {self.read_count}")
        finally:
            self.disconnect()

def test_connection():
    """Test basic connection without monitoring"""
    reader = EnhancedRFIDReader()
    
    if reader.connect():
        print("✓ Connection test successful!")
        reader.disconnect()
        return True
    else:
        print("✗ Connection test failed!")
        return False

def show_last_card_info():
    """Show information about the last read card"""
    reader = EnhancedRFIDReader()
    if reader.last_card_info:
        print("\nLast Card Information:")
        print("=" * 50)
        print(reader.last_card_info.get_detailed_info())
    else:
        print("No card has been read yet.")

def main():
    """Main function to run the enhanced RFID reader test"""
    print("=" * 60)
    print("Enhanced RFID Reader Test Application")
    print("Supports Turkish ID Cards and Detailed Analysis")
    print("=" * 60)
    print(f"Port: COM4")
    print(f"Baudrate: 9600")
    print(f"Data bits: 8")
    print(f"Parity: None")
    print(f"Stop bits: 1")
    print(f"Flow control: None")
    print("=" * 60)
    
    # Test connection first
    print("\nTesting connection...")
    if not test_connection():
        print("\nCannot proceed without connection")
        return
    
    # Ask user what to do
    print("\nChoose an option:")
    print("1. Monitor RFID reads (continuous) - Detailed")
    print("2. Monitor RFID reads (continuous) - Simple")
    print("3. Monitor RFID reads (30 seconds) - Detailed")
    print("4. Monitor RFID reads (30 seconds) - Simple")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            reader = EnhancedRFIDReader()
            
            if choice == '1':
                reader.monitor_rfid(show_detailed=True)
                break
            elif choice == '2':
                reader.monitor_rfid(show_detailed=False)
                break
            elif choice == '3':
                reader.monitor_rfid(duration=30, show_detailed=True)
                break
            elif choice == '4':
                reader.monitor_rfid(duration=30, show_detailed=False)
                break
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
