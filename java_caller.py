#!/usr/bin/env python3

import json
import os
import sys
import time
from typing import Any, Optional, Dict


class JavaMethodCaller:
    def __init__(self, pipe_path: str = "/tmp/dreambot_shim_pipe", response_pipe_path: str = "/tmp/dreambot_shim_response_pipe"):
        self.pipe_path = pipe_path
        self.response_pipe_path = response_pipe_path
    
    def call_method(self, method_name: str, *args) -> bool:
        """Legacy method for backwards compatibility - just sends without waiting for response."""
        try:
            request = {
                "method": method_name,
                "args": list(args)
            }
            json_request = json.dumps(request)
            
            if not os.path.exists(self.pipe_path):
                print(f"Error: Named pipe {self.pipe_path} not available", file=sys.stderr)
                return False
            
            with open(self.pipe_path, 'w') as pipe:
                pipe.write(json_request + '\n')
                pipe.flush()
            
            return True
        except Exception as e:
            print(f"Error calling method {method_name}: {e}", file=sys.stderr)
            return False
    
    def call_method_with_response(self, method_name: str, *args, timeout: int = 300) -> Dict[str, Any]:
        """Call method and wait for response from Java shim."""
        try:
            request = {
                "method": method_name,
                "args": list(args),
                "id": f"{method_name}_{int(time.time() * 1000)}"
            }
            
            json_request = json.dumps(request)
            
            if not os.path.exists(self.pipe_path):
                return {
                    "success": False,
                    "error": f"Named pipe {self.pipe_path} not available",
                    "result": None
                }
            
            # Send request
            with open(self.pipe_path, 'w') as pipe:
                pipe.write(json_request + '\n')
                pipe.flush()
            
            # Always wait for response from Java
            return self._wait_for_response(request.get("id"), timeout)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calling method {method_name}: {e}",
                "result": None
            }
    
    def _wait_for_response(self, request_id: str, timeout: int) -> Dict[str, Any]:
        """Wait for response from the Java shim."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if os.path.exists(self.response_pipe_path):
                    with open(self.response_pipe_path, 'r') as pipe:
                        # Set non-blocking mode would be ideal, but let's try with a small timeout
                        response_line = pipe.readline().strip()
                        if response_line:
                            response = json.loads(response_line)
                            # For methods without requestId (backward compatibility)
                            # just return the first response we get
                            if not request_id or response.get("id") == request_id:
                                return {
                                    "success": True,
                                    "result": response.get("result"),
                                    "error": response.get("error")
                                }
                
                time.sleep(0.1)  # Small delay before checking again
                
            except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
                print(f"Error reading response: {e}", file=sys.stderr)
                time.sleep(0.1)
                continue
        
        return {
            "success": False,
            "error": f"Timeout waiting for response (waited {timeout}s)",
            "result": None
        }
    
    def greet(self, name: str):
        return self.call_method_with_response("greet", name)
    
    def calculate(self, a, b, operation):
        return self.call_method_with_response("calculate", a, b, operation)
    
    def walk_to_location(self, x: int, y: int):
        return self.call_method_with_response("walkToLocation", x, y)
    
    def click_object(self, object_name: str):
        return self.call_method_with_response("clickObject", object_name)
    
    def get_inventory_count(self):
        return self.call_method_with_response("getInventoryCount")
    
    def check_bank_open(self):
        return self.call_method_with_response("bankIsOpen")
    
    def close_bank(self):
        return self.call_method_with_response("closeBank")
    
    def withdraw_item(self, item_name: str, quantity: int):
        return self.call_method_with_response("withdrawItem", item_name, quantity)
    
    def deposit_item(self, item_name: str, quantity: int):
        return self.call_method_with_response("depositItem", item_name, quantity)
    
    def deposit_all(self):
        return self.call_method_with_response("depositAllExcept")
    
    def run_dreambot_action(self, action: str, *params):
        return self.call_method_with_response("runDreambotAction", action, *params)
    
    def log_message(self, level: str, message: str):
        return self.call_method_with_response("logMessage", level, message)
    
    # Task Management Methods
    def clear_upcoming_steps(self):
        return self.call_method_with_response("clearUpcomingSteps")
    
    def add_upcoming_step(self, step_description: str):
        return self.call_method_with_response("addUpcomingStep", step_description)
    
    def get_upcoming_steps_count(self):
        return self.call_method_with_response("getUpcomingStepsCount")
    
    def peek_next_step(self):
        return self.call_method_with_response("peekNextStep")
    
    def get_next_step(self):
        return self.call_method_with_response("getNextStep")
    
    def set_current_step(self, step_description: str):
        return self.call_method_with_response("setCurrentStep", step_description)
    
    def remove_upcoming_step(self, index: int):
        return self.call_method_with_response("removeUpcomingStep", index)
    
    def insert_upcoming_step(self, index: int, step_description: str):
        return self.call_method_with_response("insertUpcomingStep", index, step_description)
    
    def handle_npc_dialogue(self, npc_name: str, max_wait_time: int):
        return self.call_method_with_response("handleNPCDialogue", npc_name, max_wait_time)
    
    def use_item_on_item(self, primary_item: str, secondary_item: str, use_item_ids: bool = False):
        return self.call_method_with_response("useItemOnItem", primary_item, secondary_item, use_item_ids)

    def perform_item_action(self, action: str, item: str, target: str = None, use_item_ids: bool = False, target_type: str = "object"):
        return self.call_method_with_response("performItemAction", action, item, target, use_item_ids, target_type)
    
    # Ground Item Methods
    def pickup_ground_item(self, item_name: str):
        return self.call_method_with_response("pickupGroundItem", item_name)
    
    def pickup_ground_item_by_id(self, item_id: int):
        return self.call_method_with_response("pickupGroundItemById", item_id)
    
    def get_nearby_ground_items(self):
        return self.call_method_with_response("getNearbyGroundItems")
    
    def ground_item_exists(self, item_name: str):
        return self.call_method_with_response("groundItemExists", item_name)
    
    def get_distance_to_ground_item(self, item_name: str):
        return self.call_method_with_response("getDistanceToGroundItem", item_name)
