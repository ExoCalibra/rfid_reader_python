#!python
# -*- coding: utf-8 -*-
"""
Test script for Turkish ID Card validation
This script demonstrates the Turkish ID card validation algorithm
"""

def validate_turkish_id(tc_number: str) -> dict:
    """
    Validate Turkish ID number using the official algorithm
    
    Args:
        tc_number (str): 11-digit Turkish ID number
        
    Returns:
        dict: Validation results
    """
    if len(tc_number) != 11 or not tc_number.isdigit():
        return {
            "valid": False,
            "error": "Turkish ID must be exactly 11 digits"
        }
    
    digits = [int(d) for d in tc_number]
    
    # First digit cannot be 0
    if digits[0] == 0:
        return {
            "valid": False,
            "error": "First digit cannot be 0"
        }
    
    # Calculate check digits using Turkish ID algorithm
    odd_sum = sum(digits[i] for i in range(0, 9, 2))
    even_sum = sum(digits[i] for i in range(1, 8, 2))
    
    # 10th digit validation: (odd_sum * 7 - even_sum) % 10
    digit_10 = (odd_sum * 7 - even_sum) % 10
    
    # 11th digit validation: sum of first 10 digits % 10
    first_10_sum = sum(digits[:10])
    digit_11 = first_10_sum % 10
    
    # Check if calculated digits match the actual digits
    is_valid = (digits[9] == digit_10 and digits[10] == digit_11)
    
    # Convert to hex and decimal for display
    hex_data = ' '.join([f'{ord(d):02X}' for d in tc_number])
    # Convert hex to single decimal number
    hex_string = ''.join([f'{ord(d):02X}' for d in tc_number])
    decimal_data = str(int(hex_string, 16))
    
    return {
        "valid": is_valid,
        "full_number": tc_number,
        "hex_data": hex_data,
        "decimal_data": decimal_data,
        "check_digit_10": digit_10,
        "check_digit_11": digit_11,
        "actual_digit_10": digits[9],
        "actual_digit_11": digits[10],
        "odd_sum": odd_sum,
        "even_sum": even_sum,
        "first_10_sum": first_10_sum
    }

def test_turkish_ids():
    """Test various Turkish ID numbers"""
    test_cases = [
        "12345678901",  # Invalid example
        "12345678910",  # Invalid example
        "10000000146",  # Valid example
        "11111111111",  # Invalid (all same digits)
        "1234567890",   # Too short
        "123456789012", # Too long
        "00000000000",  # Invalid (starts with 0)
    ]
    
    print("Turkish ID Card Validation Test")
    print("=" * 50)
    
    for tc_number in test_cases:
        result = validate_turkish_id(tc_number)
        
        print(f"\nTesting: {tc_number}")
        print(f"Valid: {'✓ Yes' if result['valid'] else '✗ No'}")
        
        if result['valid']:
            print(f"✓ Valid Turkish ID Card")
            print(f"  Hex Data: {result.get('hex_data', 'N/A')}")
            print(f"  Decimal Data: {result.get('decimal_data', 'N/A')}")
        elif 'error' in result:
            print(f"✗ Error: {result['error']}")
        else:
            print(f"✗ Invalid - Check digits don't match")
            print(f"  Expected 10th digit: {result['check_digit_10']}, Got: {result['actual_digit_10']}")
            print(f"  Expected 11th digit: {result['check_digit_11']}, Got: {result['actual_digit_11']}")
            print(f"  Hex Data: {result.get('hex_data', 'N/A')}")
            print(f"  Decimal Data: {result.get('decimal_data', 'N/A')}")

if __name__ == "__main__":
    test_turkish_ids()
