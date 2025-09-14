#!/usr/bin/env python3
"""
Test script to demonstrate the task management functionality in the MCP server.
This script shows how the new task management tools work with the DreamBot shim.
"""

import json
import time
from java_caller import JavaMethodCaller


def test_task_management():
    """Test the task management functionality using the JavaMethodCaller directly."""
    print("=== MCP Server Task Management Test ===")
    print()
    
    # Create Java caller instance
    java_caller = JavaMethodCaller()
    
    # Clear any existing steps
    print("1. Clearing existing upcoming steps...")
    success = java_caller.clear_upcoming_steps()
    print(f"✓ Clear steps: {success}")
    time.sleep(1)
    
    # Add some upcoming steps
    print("\n2. Adding upcoming steps...")
    steps = [
        "Walk to bank area",
        "Open bank booth", 
        "Deposit all items except pickaxe",
        "Withdraw 28 iron ore",
        "Close bank",
        "Walk to furnace"
    ]
    
    for step in steps:
        success = java_caller.add_upcoming_step(step)
        print(f"✓ Added step: {step} - {success}")
        time.sleep(0.5)
    
    # Check how many steps we have
    print("\n3. Checking upcoming steps count...")
    success = java_caller.get_upcoming_steps_count()
    print(f"✓ Steps count request: {success}")
    time.sleep(1)
    
    # Peek at the next step
    print("\n4. Peeking at next step...")
    success = java_caller.peek_next_step()
    print(f"✓ Peek next step: {success}")
    time.sleep(1)
    
    # Set current step and simulate some work
    print("\n5. Simulating task execution...")
    success = java_caller.set_current_step("Preparing to start mining run...")
    print(f"✓ Set current step: {success}")
    time.sleep(2)
    
    # Remove and execute the first step
    print("\n6. Getting and executing next step...")
    success = java_caller.get_next_step()
    print(f"✓ Get next step: {success}")
    time.sleep(1)
    
    # Simulate walking to bank
    success = java_caller.set_current_step("Walking to bank area...")
    print(f"✓ Set current step (walking): {success}")
    time.sleep(3)
    
    # Get the next step and execute it
    success = java_caller.get_next_step()
    print(f"✓ Get next step (bank): {success}")
    time.sleep(1)
    
    # Test inserting a step at the beginning
    print("\n7. Inserting priority step...")
    success = java_caller.insert_upcoming_step(0, "Check inventory space before banking")
    print(f"✓ Insert priority step: {success}")
    time.sleep(1)
    
    # Test removing a specific step
    print("\n8. Removing a specific step...")
    success = java_caller.remove_upcoming_step(2)  # Remove the 3rd step
    print(f"✓ Remove step at index 2: {success}")
    time.sleep(1)
    
    # Check remaining steps
    print("\n9. Checking remaining steps...")
    success = java_caller.get_upcoming_steps_count()
    print(f"✓ Final steps count: {success}")
    time.sleep(1)
    
    print("\n=== Test Complete ===")
    print("Check the DreamBot UI to see the upcoming steps displayed!")
    print("You should see the remaining steps in the 'Upcoming Steps' section.")


def demo_mining_scenario():
    """Demonstrate a realistic mining scenario using task management."""
    print("\n=== Mining Scenario Demo ===")
    print()
    
    java_caller = JavaMethodCaller()
    
    # Clear existing steps
    java_caller.clear_upcoming_steps()
    
    # Set up a complete mining scenario
    mining_steps = [
        "Check current inventory for pickaxe",
        "Walk to mining location (iron rocks)",
        "Start mining iron ore",
        "Monitor inventory until full",
        "Walk back to bank",
        "Open bank interface",
        "Deposit all iron ore",
        "Check if more mining cycles needed",
        "Close bank and return to mining"
    ]
    
    print("Setting up mining scenario steps...")
    for i, step in enumerate(mining_steps):
        java_caller.add_upcoming_step(step)
        print(f"{i+1}. {step}")
        time.sleep(0.3)
    
    print(f"\n✓ Added {len(mining_steps)} steps to the task queue")
    
    # Simulate executing the first few steps
    print("\nSimulating task execution...")
    
    java_caller.set_current_step("Starting mining session...")
    time.sleep(2)
    
    # Execute first 3 steps
    for i in range(3):
        java_caller.get_next_step()
        time.sleep(1)
        if i == 0:
            java_caller.set_current_step("Checking inventory for pickaxe...")
        elif i == 1:
            java_caller.set_current_step("Walking to iron rock location...")
        elif i == 2:
            java_caller.set_current_step("Beginning to mine iron ore...")
        time.sleep(2)
    
    print("\n✓ Mining scenario demonstration complete!")


if __name__ == "__main__":
    test_task_management()
    demo_mining_scenario()