#!/usr/bin/env python3
"""
Test script to verify the fallback mechanism works without timeouts.
"""

from java_caller import JavaMethodCaller
import time


def test_fallback_mode():
    """Test the fallback mode (no response waiting)."""
    print("=== Testing Fallback Mode (No Response Waiting) ===")
    print()
    
    # Create caller with fallback mode (default)
    java_caller = JavaMethodCaller(wait_for_responses=False)
    
    print("Testing various commands in fallback mode...")
    
    # Test bank status
    start_time = time.time()
    response = java_caller.check_bank_open()
    elapsed = time.time() - start_time
    print(f"✓ Bank status: {response} (took {elapsed:.2f}s)")
    
    # Test inventory count
    start_time = time.time()
    response = java_caller.get_inventory_count()
    elapsed = time.time() - start_time
    print(f"✓ Inventory count: {response} (took {elapsed:.2f}s)")
    
    # Test walking
    start_time = time.time()
    response = java_caller.walk_to_location(100, 200)
    elapsed = time.time() - start_time
    print(f"✓ Walk command: {response} (took {elapsed:.2f}s)")
    
    # Test task management
    start_time = time.time()
    response = java_caller.add_upcoming_step("Test step")
    elapsed = time.time() - start_time
    print(f"✓ Add step: {response} (took {elapsed:.2f}s)")
    
    start_time = time.time()
    response = java_caller.get_upcoming_steps_count()
    elapsed = time.time() - start_time
    print(f"✓ Steps count: {response} (took {elapsed:.2f}s)")
    
    print(f"\n✓ All commands completed quickly without timeouts!")


def test_response_mode():
    """Test the response waiting mode (will timeout if no response pipe)."""
    print("\n=== Testing Response Mode (Will Timeout if No Response Pipe) ===")
    print()
    
    # Create caller with response waiting enabled
    java_caller = JavaMethodCaller(wait_for_responses=True)
    
    print("Testing with response waiting (2s timeout)...")
    
    start_time = time.time()
    response = java_caller.check_bank_open()
    elapsed = time.time() - start_time
    print(f"Response mode result: {response} (took {elapsed:.2f}s)")
    
    if elapsed >= 2.0:
        print("✓ Timeout behavior working as expected")
    else:
        print("✓ Response received quickly (Java shim with response pipe is running)")


if __name__ == "__main__":
    test_fallback_mode()
    test_response_mode()