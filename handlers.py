#!/usr/bin/env python3

import logging
from typing import Any, Dict, Optional

import mcp.types as types
from java_caller import JavaMethodCaller


logger = logging.getLogger(__name__)


async def handle_call_tool(
    java_caller: JavaMethodCaller,
    name: str, 
    arguments: Optional[Dict[str, Any]]
) -> list[types.TextContent]:
    """Handle tool calls."""
    args = arguments or {}
    
    try:
        if name == "call_java_method":
            return await _handle_call_java_method(args)
        elif name == "greet_user":
            return await _handle_greet_user(java_caller, args)
        elif name == "calculate":
            return await _handle_calculate(java_caller, args)
        elif name == "walk_to_location":
            return await _handle_walk_to_location(java_caller, args)
        elif name == "click_object":
            return await _handle_click_object(java_caller, args)
        elif name == "get_inventory_count":
            return await _handle_get_inventory_count(java_caller, args)
        elif name == "check_inventory_for_item":
            return await _handle_check_inventory_for_item(java_caller, args)
        elif name == "inventory_contains_item":
            return await _handle_inventory_contains_item(java_caller, args)
        elif name == "check_bank_open":
            return await _handle_check_bank_open(java_caller, args)
        elif name == "close_bank":
            return await _handle_close_bank(java_caller, args)
        elif name == "withdraw_item":
            return await _handle_withdraw_item(java_caller, args)
        elif name == "deposit_item":
            return await _handle_deposit_item(java_caller, args)
        elif name == "deposit_all":
            return await _handle_deposit_all(java_caller, args)
        elif name == "run_dreambot_action":
            return await _handle_run_dreambot_action(java_caller, args)
        elif name == "log_message":
            return await _handle_log_message(java_caller, args)
        # Task Management Tools
        elif name == "clear_upcoming_steps":
            return await _handle_clear_upcoming_steps(java_caller, args)
        elif name == "add_upcoming_step":
            return await _handle_add_upcoming_step(java_caller, args)
        elif name == "get_upcoming_steps_count":
            return await _handle_get_upcoming_steps_count(java_caller, args)
        elif name == "peek_next_step":
            return await _handle_peek_next_step(java_caller, args)
        elif name == "get_next_step":
            return await _handle_get_next_step(java_caller, args)
        elif name == "set_current_step":
            return await _handle_set_current_step(java_caller, args)
        elif name == "remove_upcoming_step":
            return await _handle_remove_upcoming_step(java_caller, args)
        elif name == "insert_upcoming_step":
            return await _handle_insert_upcoming_step(java_caller, args)
        elif name == "handle_npc_dialogue":
            return await _handle_npc_dialogue(java_caller, args)
        elif name == "use_item_on_item":
            return await _handle_use_item_on_item(java_caller, args)
        elif name == "perform_item_action":
            return await _handle_perform_item_action(java_caller, args)
        # Ground Item Tools
        elif name == "pickup_ground_item":
            return await _handle_pickup_ground_item(java_caller, args)
        elif name == "pickup_ground_item_by_id":
            return await _handle_pickup_ground_item_by_id(java_caller, args)
        elif name == "get_nearby_ground_items":
            return await _handle_get_nearby_ground_items(java_caller, args)
        elif name == "ground_item_exists":
            return await _handle_ground_item_exists(java_caller, args)
        elif name == "get_distance_to_ground_item":
            return await _handle_get_distance_to_ground_item(java_caller, args)
        elif name == "get_current_tile":
            return await _handle_get_current_tile(java_caller, args)
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def _handle_call_java_method(args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle call_java_method tool."""
    method_name = args.get("method_name")
    method_args = args.get("args", [])
    pipe_path = args.get("pipe_path", "/tmp/dreambot_shim_pipe")
    
    if not method_name:
        return [types.TextContent(type="text", text="Error: method_name is required")]
    
    caller = JavaMethodCaller(pipe_path)
    response = caller.call_method_with_response(method_name, *method_args)
    
    if response["success"]:
        result = response.get("result", "Method executed successfully")
        return [types.TextContent(
            type="text", 
            text=f"Java method '{method_name}' result: {result}"
        )]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(
            type="text", 
            text=f"Failed to call Java method '{method_name}': {error}"
        )]


async def _handle_greet_user(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle greet_user tool."""
    name_arg = args.get("name")
    if not name_arg:
        return [types.TextContent(type="text", text="Error: name is required")]
    
    response = java_caller.greet(name_arg)
    if response["success"]:
        result = response.get("result", "Greeting completed")
        return [types.TextContent(type="text", text=f"Greeting result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to greet user: {error}")]


async def _handle_calculate(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle calculate tool."""
    a = args.get("a")
    b = args.get("b")
    operation = args.get("operation")
    
    if a is None or b is None or not operation:
        return [types.TextContent(type="text", text="Error: a, b, and operation are required")]
    
    response = java_caller.calculate(a, b, operation)
    if response["success"]:
        result = response.get("result", f"{a} {operation} {b}")
        return [types.TextContent(
            type="text", 
            text=f"Calculation result: {result}"
        )]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to calculate: {error}")]


async def _handle_walk_to_location(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle walk_to_location tool."""
    x = args.get("x")
    y = args.get("y")
    z = args.get("z", 0)  # Default z to 0 if not provided
    
    if x is None or y is None:
        return [types.TextContent(type="text", text="Error: x and y coordinates are required")]
    
    response = java_caller.walk_to_location(x, y, z)
    if response["success"]:
        result = response.get("result", f"Walking to ({x}, {y}, {z})")
        return [types.TextContent(type="text", text=f"Walk result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to walk: {error}")]


async def _handle_click_object(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle click_object tool."""
    object_name = args.get("object_name")
    
    if not object_name:
        return [types.TextContent(type="text", text="Error: object_name is required")]
    
    response = java_caller.click_object(object_name)
    if response["success"]:
        result = response.get("result", f"Clicked {object_name}")
        return [types.TextContent(type="text", text=f"Click result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to click object: {error}")]


async def _handle_get_inventory_count(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle get_inventory_count tool."""
    response = java_caller.get_inventory_count()
    if response["success"]:
        result = response.get("result", "Unknown")
        
        # Handle different response types
        if result == "count_unknown":
            return [types.TextContent(type="text", text="Inventory count request sent successfully (actual count unknown - enable response waiting for real count)")]
        else:
            return [types.TextContent(type="text", text=f"Inventory count: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to get inventory count: {error}")]


async def _handle_check_inventory_for_item(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle check_inventory_for_item tool."""
    item_name = args.get("item_name")
    use_item_id = args.get("use_item_id", False)
    
    if not item_name:
        return [types.TextContent(type="text", text="Error: item_name is required")]
    
    response = java_caller.check_inventory_for_item(item_name, use_item_id)
    if response["success"]:
        count = response.get("result", -1)
        
        if count == -1:
            item_type = "ID" if use_item_id else "name"
            return [types.TextContent(type="text", text=f"Item {item_type} '{item_name}' not found in inventory")]
        else:
            item_type = "ID" if use_item_id else "name"
            return [types.TextContent(type="text", text=f"Inventory contains {count} of item {item_type} '{item_name}'")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to check inventory for item: {error}")]


async def _handle_inventory_contains_item(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle inventory_contains_item tool."""
    item_name = args.get("item_name")
    use_item_id = args.get("use_item_id", False)
    
    if not item_name:
        return [types.TextContent(type="text", text="Error: item_name is required")]
    
    response = java_caller.inventory_contains_item(item_name, use_item_id)
    if response["success"]:
        contains = response.get("result", False)
        item_type = "ID" if use_item_id else "name"
        status = "contains" if contains else "does not contain"
        return [types.TextContent(type="text", text=f"Inventory {status} item {item_type} '{item_name}'")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to check if inventory contains item: {error}")]


async def _handle_check_bank_open(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle check_bank_open tool."""
    response = java_caller.check_bank_open()
    if response["success"]:
        result = response.get("result", False)
        
        # Handle different response types
        if result == "status_unknown":
            return [types.TextContent(type="text", text="Bank status check sent successfully (actual status unknown - enable response waiting for real status)")]
        elif isinstance(result, bool):
            status = "open" if result else "closed"
            return [types.TextContent(type="text", text=f"Bank is {status}")]
        elif isinstance(result, str) and result.lower() in ["true", "open", "yes"]:
            return [types.TextContent(type="text", text="Bank is open")]
        elif isinstance(result, str) and result.lower() in ["false", "closed", "no"]:
            return [types.TextContent(type="text", text="Bank is closed")]
        else:
            return [types.TextContent(type="text", text=f"Bank status: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to check bank status: {error}")]


async def _handle_close_bank(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle close_bank tool."""
    response = java_caller.close_bank()
    if response["success"]:
        result = response.get("result", "Bank close attempted")
        return [types.TextContent(type="text", text=f"Close bank result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to close bank: {error}")]


async def _handle_withdraw_item(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle withdraw_item tool."""
    item_name = args.get("item_name")
    quantity = args.get("quantity")
    
    if not item_name or quantity is None:
        return [types.TextContent(type="text", text="Error: item_name and quantity are required")]
    
    response = java_caller.withdraw_item(item_name, quantity)
    if response["success"]:
        result = response.get("result", f"Withdraw {quantity} {item_name} attempted")
        return [types.TextContent(type="text", text=f"Withdraw item result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to withdraw item: {error}")]


async def _handle_deposit_item(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle deposit_item tool."""
    item_name = args.get("item_name")
    quantity = args.get("quantity")
    
    if not item_name or quantity is None:
        return [types.TextContent(type="text", text="Error: item_name and quantity are required")]
    
    response = java_caller.deposit_item(item_name, quantity)
    if response["success"]:
        result = response.get("result", f"Deposit {quantity} {item_name} attempted")
        return [types.TextContent(type="text", text=f"Deposit item result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to deposit item: {error}")]


async def _handle_deposit_all(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle deposit_all tool."""
    response = java_caller.deposit_all()
    if response["success"]:
        result = response.get("result", "Deposit all attempted")
        return [types.TextContent(type="text", text=f"Deposit all result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to deposit all: {error}")]


async def _handle_run_dreambot_action(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle run_dreambot_action tool."""
    action = args.get("action")
    params = args.get("params", [])
    
    if not action:
        return [types.TextContent(type="text", text="Error: action is required")]
    
    response = java_caller.run_dreambot_action(action, *params)
    if response["success"]:
        result = response.get("result", f"Action '{action}' executed")
        return [types.TextContent(
            type="text", 
            text=f"DreamBot action result: {result}"
        )]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to execute DreamBot action: {error}")]


async def _handle_log_message(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle log_message tool."""
    level = args.get("level")
    message = args.get("message")
    
    if not level or not message:
        return [types.TextContent(type="text", text="Error: level and message are required")]
    
    response = java_caller.log_message(level, message)
    if response["success"]:
        result = response.get("result", f"[{level}] {message}")
        return [types.TextContent(type="text", text=f"Log message result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to log message: {error}")]


# Task Management Handlers
async def _handle_clear_upcoming_steps(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle clear_upcoming_steps tool."""
    response = java_caller.clear_upcoming_steps()
    if response["success"]:
        result = response.get("result", "Steps cleared")
        return [types.TextContent(type="text", text=f"Cleared upcoming steps: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to clear upcoming steps: {error}")]


async def _handle_add_upcoming_step(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle add_upcoming_step tool."""
    step_description = args.get("step_description")
    
    if not step_description:
        return [types.TextContent(type="text", text="Error: step_description is required")]
    
    response = java_caller.add_upcoming_step(step_description)
    if response["success"]:
        result = response.get("result", f"Added: {step_description}")
        return [types.TextContent(type="text", text=f"Step added: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to add step: {error}")]


async def _handle_get_upcoming_steps_count(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle get_upcoming_steps_count tool."""
    response = java_caller.get_upcoming_steps_count()
    if response["success"]:
        count = response.get("result", 0)
        return [types.TextContent(type="text", text=f"Upcoming steps count: {count}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to get steps count: {error}")]


async def _handle_peek_next_step(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle peek_next_step tool."""
    response = java_caller.peek_next_step()
    if response["success"]:
        result = response.get("result", "No upcoming steps")
        return [types.TextContent(type="text", text=f"Next step: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to peek next step: {error}")]


async def _handle_get_next_step(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle get_next_step tool."""
    response = java_caller.get_next_step()
    if response["success"]:
        result = response.get("result", "No steps available")
        return [types.TextContent(type="text", text=f"Retrieved next step: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to get next step: {error}")]


async def _handle_set_current_step(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle set_current_step tool."""
    step_description = args.get("step_description")
    
    if not step_description:
        return [types.TextContent(type="text", text="Error: step_description is required")]
    
    response = java_caller.set_current_step(step_description)
    if response["success"]:
        result = response.get("result", f"Current step: {step_description}")
        return [types.TextContent(type="text", text=f"Set current step: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to set current step: {error}")]


async def _handle_remove_upcoming_step(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle remove_upcoming_step tool."""
    index = args.get("index")
    
    if index is None:
        return [types.TextContent(type="text", text="Error: index is required")]
    
    response = java_caller.remove_upcoming_step(index)
    if response["success"]:
        result = response.get("result", f"Removed step at index {index}")
        return [types.TextContent(type="text", text=f"Remove step result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to remove step: {error}")]


async def _handle_insert_upcoming_step(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle insert_upcoming_step tool."""
    index = args.get("index")
    step_description = args.get("step_description")
    
    if index is None or not step_description:
        return [types.TextContent(type="text", text="Error: index and step_description are required")]
    
    response = java_caller.insert_upcoming_step(index, step_description)
    if response["success"]:
        result = response.get("result", f"Inserted '{step_description}' at index {index}")
        return [types.TextContent(type="text", text=f"Insert step result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to insert step: {error}")]


async def _handle_npc_dialogue(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle NPC dialogue interactions, waiting for all dialogue to complete."""
    npc_name = args.get("npc_name", "")
    max_wait_time = args.get("max_wait_time", 120)  # Default 120 seconds max wait for long dialogues
    
    response = java_caller.handle_npc_dialogue(npc_name, max_wait_time)
    if response["success"]:
        result = response.get("result", f"Successfully handled dialogue with {npc_name if npc_name else 'NPC'}")
        return [types.TextContent(type="text", text=f"NPC dialogue result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to handle NPC dialogue: {error}")]


async def _handle_use_item_on_item(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle use_item_on_item tool."""
    primary_item = args.get("primary_item")
    secondary_item = args.get("secondary_item")
    use_item_ids = args.get("use_item_ids", False)
    
    if not primary_item or not secondary_item:
        return [types.TextContent(type="text", text="Error: primary_item and secondary_item are required")]
    
    response = java_caller.use_item_on_item(primary_item, secondary_item, use_item_ids)
    if response["success"]:
        result = response.get("result", f"Used {primary_item} on {secondary_item}")
        return [types.TextContent(type="text", text=f"Use item on item result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to use item on item: {error}")]


async def _handle_perform_item_action(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle perform_item_action tool."""
    action = args.get("action")
    item = args.get("item")
    target = args.get("target")
    use_item_ids = args.get("use_item_ids", False)
    target_type = args.get("target_type", "object")  # Default to object if target is provided
    
    if not action or not item:
        return [types.TextContent(type="text", text="Error: action and item are required")]
    
    response = java_caller.perform_item_action(action, item, target, use_item_ids, target_type)
    if response["success"]:
        result = response.get("result", f"Performed {action} on {item}")
        return [types.TextContent(type="text", text=f"Item action result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to perform item action: {error}")]


# Ground Item Handlers
async def _handle_pickup_ground_item(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle pickup_ground_item tool."""
    item_name = args.get("item_name")
    
    if not item_name:
        return [types.TextContent(type="text", text="Error: item_name is required")]
    
    response = java_caller.pickup_ground_item(item_name)
    if response["success"]:
        result = response.get("result", f"Attempted to pick up ground item: {item_name}")
        return [types.TextContent(type="text", text=f"Pickup ground item result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to pick up ground item: {error}")]


async def _handle_pickup_ground_item_by_id(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle pickup_ground_item_by_id tool."""
    item_id = args.get("item_id")
    
    if item_id is None:
        return [types.TextContent(type="text", text="Error: item_id is required")]
    
    response = java_caller.pickup_ground_item_by_id(item_id)
    if response["success"]:
        result = response.get("result", f"Attempted to pick up ground item ID: {item_id}")
        return [types.TextContent(type="text", text=f"Pickup ground item by ID result: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to pick up ground item by ID: {error}")]


async def _handle_get_nearby_ground_items(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle get_nearby_ground_items tool."""
    response = java_caller.get_nearby_ground_items()
    if response["success"]:
        result = response.get("result", "No ground items information available")
        return [types.TextContent(type="text", text=f"Nearby ground items: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to get nearby ground items: {error}")]


async def _handle_ground_item_exists(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle ground_item_exists tool."""
    item_name = args.get("item_name")
    
    if not item_name:
        return [types.TextContent(type="text", text="Error: item_name is required")]
    
    response = java_caller.ground_item_exists(item_name)
    if response["success"]:
        result = response.get("result", False)
        exists_text = "exists" if result else "does not exist"
        return [types.TextContent(type="text", text=f"Ground item '{item_name}' {exists_text}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to check if ground item exists: {error}")]


async def _handle_get_distance_to_ground_item(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle get_distance_to_ground_item tool."""
    item_name = args.get("item_name")
    
    if not item_name:
        return [types.TextContent(type="text", text="Error: item_name is required")]
    
    response = java_caller.get_distance_to_ground_item(item_name)
    if response["success"]:
        distance = response.get("result", -1)
        if distance == -1:
            return [types.TextContent(type="text", text=f"Ground item '{item_name}' not found")]
        else:
            return [types.TextContent(type="text", text=f"Distance to '{item_name}': {distance:.1f}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to get distance to ground item: {error}")]


async def _handle_get_current_tile(java_caller: JavaMethodCaller, args: Dict[str, Any]) -> list[types.TextContent]:
    """Handle get_current_tile tool."""
    response = java_caller.get_current_tile()
    if response["success"]:
        result = response.get("result", "Current tile unknown")
        return [types.TextContent(type="text", text=f"Current tile: {result}")]
    else:
        error = response.get("error", "Unknown error")
        return [types.TextContent(type="text", text=f"Failed to get current tile: {error}")]
