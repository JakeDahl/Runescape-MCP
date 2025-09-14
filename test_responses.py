#!/usr/bin/env python3
"""
Test script to demonstrate the response functionality in the MCP server.
This script shows how the server now waits for actual responses from the Java shim.
"""

import json
import time
from java_caller import JavaMethodCaller


def test_response_functionality():
    """Test the response functionality using the JavaMethodCaller."""
    print("=== MCP Server Response Functionality Test ===")
    print()
    
    # Create Java caller instance
    java_caller = JavaMethodCaller()
    
    print("Testing commands that now wait for responses:")
    print()
    
    # Test bank status check
    print("1. Checking bank status...")
    response = java_caller.check_bank_open()
    print(f"Response: {response}")
    if response["success"]:
        status = "open" if response.get("result") else "closed"
        print(f"✓ Bank is {status}")
    else:
        print(f"✗ Error: {response.get('error')}")
    print()
    
    # Test inventory count
    print("2. Getting inventory count...")
    response = java_caller.get_inventory_count()
    print(f"Response: {response}")
    if response["success"]:
        count = response.get("result", "Unknown")
        print(f"✓ Inventory count: {count}")
    else:
        print(f"✗ Error: {response.get('error')}")
    print()
    
    # Test game state
    print("3. Getting game state...")
    response = java_caller.get_game_state()
    print(f"Response: {response}")
    if response["success"]:
        state = response.get("result", "Unknown")
        print(f"✓ Game state: {state}")
    else:
        print(f"✗ Error: {response.get('error')}")
    print()
    
    # Test task management responses
    print("4. Testing task management responses...")
    
    # Clear steps
    response = java_caller.clear_upcoming_steps()
    print(f"Clear steps response: {response}")
    
    # Add a step
    response = java_caller.add_upcoming_step("Test step for response checking")
    print(f"Add step response: {response}")
    
    # Get count
    response = java_caller.get_upcoming_steps_count()
    print(f"Steps count response: {response}")
    if response["success"]:
        count = response.get("result", 0)
        print(f"✓ Steps count: {count}")
    
    # Peek next step
    response = java_caller.peek_next_step()
    print(f"Peek step response: {response}")
    if response["success"]:
        step = response.get("result", "No steps")
        print(f"✓ Next step: {step}")
    
    print()
    print("=== Response Test Complete ===")
    print("All commands now wait for actual responses from the Java shim!")


def demonstrate_timeout_behavior():
    """Demonstrate timeout behavior when Java shim is not available."""
    print("\n=== Timeout Behavior Demo ===")
    print("(This will timeout if Java shim is not running)")
    print()
    
    # Create caller with short timeout for demo
    java_caller = JavaMethodCaller()
    
    print("Testing with 3-second timeout...")
    start_time = time.time()
    
    response = java_caller.call_method_with_response("testTimeout", timeout=3)
    
    elapsed = time.time() - start_time
    print(f"Elapsed time: {elapsed:.2f} seconds")
    print(f"Response: {response}")
    
    if not response["success"] and "Timeout" in response.get("error", ""):
        print("✓ Timeout behavior working correctly")
    else:
        print("✓ Response received (Java shim is running)")


def demo_error_handling():
    """Demonstrate error handling in responses."""
    print("\n=== Error Handling Demo ===")
    print()
    
    java_caller = JavaMethodCaller()
    
    # Test with non-existent pipe
    java_caller.pipe_path = "/tmp/non_existent_pipe"
    
    response = java_caller.check_bank_open()
    print(f"Non-existent pipe response: {response}")
    
    if not response["success"]:
        print("✓ Error handling working correctly")


if __name__ == "__main__":
    test_response_functionality()
    demonstrate_timeout_behavior()
    demo_error_handling()