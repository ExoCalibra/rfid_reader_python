# Enhanced RFID Reader Test Application

A comprehensive RFID reader application that supports Turkish ID cards and provides detailed card information analysis.

## Features

### 🆔 Turkish ID Card Support
- **Automatic Detection**: Automatically detects Turkish ID cards (TC Kimlik) based on 11-digit format
- **Validation Algorithm**: Implements the official Turkish ID validation algorithm
- **Check Digit Verification**: Validates the 10th and 11th check digits
- **Detailed Analysis**: Shows validation results and expected vs actual check digits

### 📊 Enhanced Card Information
- **Multiple Card Types**: Supports various RFID card formats
  - Turkish ID Cards (TC Kimlik)
  - Standard RFID Cards (10-digit)
  - Long Format RFID Cards (16+ digits)
  - Hexadecimal RFID Cards
  - Custom format cards
- **Detailed Data Analysis**: 
  - Raw data and hexadecimal representation
  - Single decimal number representation of card data
  - Card format detection
  - Numeric and alphanumeric data extraction
  - Timestamp tracking
  - Read count statistics

### 🔧 Technical Features
- **Serial Communication**: COM4 port with 9600 baud rate
- **Real-time Monitoring**: Continuous or timed monitoring options
- **Data Filtering**: Filters out incomplete reads and duplicates
- **Error Handling**: Comprehensive error handling and status indicators
- **User-friendly Interface**: Clear status messages and progress indicators

## Installation

1. Ensure Python 3.13 is installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
Run the batch file for easy execution:
```bash
run_rfid_test.bat
```

### Manual Execution
```bash
python rfid_reader_test.py
```

### Test Turkish ID Validation
```bash
python test_turkish_id.py
```

### Detect Available COM Ports
```bash
python com_port_detector.py
```

## Menu Options

1. **Monitor RFID reads (continuous) - Detailed**: Shows comprehensive card information
2. **Monitor RFID reads (continuous) - Simple**: Shows basic card type and data
3. **Monitor RFID reads (30 seconds) - Detailed**: Timed monitoring with detailed info
4. **Monitor RFID reads (30 seconds) - Simple**: Timed monitoring with basic info
5. **Exit**: Close the application

## Turkish ID Card Validation

The application uses the official Turkish ID validation algorithm:

1. **Length Check**: Must be exactly 11 digits
2. **First Digit**: Cannot be 0
3. **10th Digit**: Calculated as `(odd_sum * 7 - even_sum) % 10`
4. **11th Digit**: Calculated as `sum(first_10_digits) % 10`

### Example Output for Turkish ID Card
```
Card Type: Turkish ID Card (TC Kimlik)
Raw Data: 10000000146
Hex Data: 31 30 30 30 30 30 30 30 31 34 36
Decimal Data: 3401181938
Data Length: 11 characters
Timestamp: 2024-01-15T10:30:45.123456

Turkish ID Card Details:
  Full Number: 10000000146
  Valid: ✓ Yes
  Check Digit 10: 4 (Expected: 4)
  Check Digit 11: 6 (Expected: 6)
```

## Supported Card Types

### Turkish ID Cards (TC Kimlik)
- **Format**: 11 digits
- **Validation**: Official Turkish algorithm
- **Example**: `10000000146`

### Standard RFID Cards
- **Format**: 10 alphanumeric characters
- **Example**: `1234567890`

### Long Format RFID Cards
- **Format**: 16+ digits
- **Example**: `1234567890123456`

### Hexadecimal RFID Cards
- **Format**: 8+ hex characters
- **Example**: `A1B2C3D4`

## Configuration

### Serial Port Settings
- **Port**: COM4 (configurable in code)
- **Baud Rate**: 9600
- **Data Bits**: 8
- **Parity**: None
- **Stop Bits**: 1
- **Flow Control**: None

### Customization
Edit `rfid_reader_test.py` to modify:
- Serial port settings
- Card type detection patterns
- Output format
- Monitoring duration

## Troubleshooting

### Connection Issues
1. Check if COM4 is the correct port
2. Ensure RFID reader is properly connected
3. Verify device drivers are installed
4. Try different baud rates if needed
5. **Permission Errors**: If you get "Access denied" errors:
   - Close other applications that might be using the COM port
   - Try running the application as Administrator
   - Use `python com_port_detector.py` to find available ports

### No Card Detection
1. Ensure cards are properly positioned
2. Check RFID reader power and connections
3. Verify card compatibility
4. Try different card types

### Invalid Turkish ID
1. Check if the card is a genuine Turkish ID
2. Verify the 11-digit format
3. Ensure proper card positioning
4. Check for card damage

## Dependencies

- `pyserial==3.5`: Serial communication
- `typing-extensions==4.8.0`: Type hints support

## File Structure

```
FitnessDesktop/
├── rfid_reader_test.py      # Main RFID reader application
├── test_turkish_id.py       # Turkish ID validation test
├── com_port_detector.py      # COM port detection utility
├── run_rfid_test.bat        # Windows batch file for easy execution
├── requirements.txt         # Python dependencies
└── README.md               # This documentation
```

## License

This project is open source and available under the MIT License.
