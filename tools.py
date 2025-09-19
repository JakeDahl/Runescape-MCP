#!/usr/bin/env python3

import mcp.types as types


def get_tool_definitions() -> list[types.Tool]:
    """Get all tool definitions for the MCP server."""
    return [
        types.Tool(
            name="call_java_method",
            description="Call a Java method via named pipe with arguments",
            inputSchema={
                "type": "object",
                "properties": {
                    "method_name": {
                        "type": "string",
                        "description": "Name of the Java method to call"
                    },
                    "args": {
                        "type": "array",
                        "description": "Arguments to pass to the method",
                        "items": {
                            "oneOf": [
                                {"type": "string"},
                                {"type": "number"},
                                {"type": "boolean"}
                            ]
                        }
                    },
                    "pipe_path": {
                        "type": "string",
                        "description": "Custom named pipe path (optional)",
                        "default": "/tmp/dreambot_shim_pipe"
                    }
                },
                "required": ["method_name"]
            }
        ),
        types.Tool(
            name="greet_user",
            description="Greet a user via the Java shim",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the person to greet"
                    }
                },
                "required": ["name"]
            }
        ),
        types.Tool(
            name="calculate",
            description="Perform a calculation via the Java shim",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    },
                    "operation": {
                        "type": "string",
                        "description": "Operation to perform",
                        "enum": ["add", "subtract", "multiply", "divide"]
                    }
                },
                "required": ["a", "b", "operation"]
            }
        ),
        types.Tool(
            name="walk_to_location",
            description="Command the bot to walk to specific coordinates (x, y, z)",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "X coordinate"
                    },
                    "y": {
                        "type": "integer",
                        "description": "Y coordinate"
                    },
                    "z": {
                        "type": "integer",
                        "description": "Z coordinate (plane/level), optional, defaults to 0"
                    }
                },
                "required": ["x", "y"]
            }
        ),
        types.Tool(
            name="click_object",
            description="Command the bot to click on an object",
            inputSchema={
                "type": "object",
                "properties": {
                    "object_name": {
                        "type": "string",
                        "description": "Name of the object to click"
                    }
                },
                "required": ["object_name"]
            }
        ),
        types.Tool(
            name="get_inventory_count",
            description="Get the current inventory count from the bot and return the actual count",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="check_inventory_for_item",
            description="Check if inventory contains a specific item and return count. Returns -1 if item not found, 0+ for actual count",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name or ID of the item to check for"
                    },
                    "use_item_id": {
                        "type": "boolean",
                        "description": "Whether to treat item_name as an ID (true) or name (false). Default is false (names)."
                    }
                },
                "required": ["item_name"]
            }
        ),
        types.Tool(
            name="inventory_contains_item",
            description="Check if inventory contains a specific item (boolean result). Simple true/false check without count",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name or ID of the item to check for"
                    },
                    "use_item_id": {
                        "type": "boolean",
                        "description": "Whether to treat item_name as an ID (true) or name (false). Default is false (names)."
                    }
                },
                "required": ["item_name"]
            }
        ),
        types.Tool(
            name="check_bank_open",
            description="Check if the bank is currently open and return true/false status",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="close_bank",
            description="Close the bank if it is currently open",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="withdraw_item",
            description="Withdraw a specific item from the bank with quantity",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name of the item to withdraw"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Quantity to withdraw (use -1 for all)"
                    }
                },
                "required": ["item_name", "quantity"]
            }
        ),
        types.Tool(
            name="deposit_item",
            description="Deposit a specific item to the bank with quantity",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name of the item to deposit"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Quantity to deposit (use -1 for all)"
                    }
                },
                "required": ["item_name", "quantity"]
            }
        ),
        types.Tool(
            name="deposit_all",
            description="Deposit all items from inventory to the bank",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="run_dreambot_action",
            description="Run a DreamBot action with parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The action to perform"
                    },
                    "params": {
                        "type": "array",
                        "description": "Parameters for the action",
                        "items": {"type": "string"}
                    }
                },
                "required": ["action"]
            }
        ),
        types.Tool(
            name="log_message",
            description="Log a message with specified level",
            inputSchema={
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "description": "Log level",
                        "enum": ["INFO", "DEBUG", "ERROR", "WARN"]
                    },
                    "message": {
                        "type": "string",
                        "description": "Message to log"
                    }
                },
                "required": ["level", "message"]
            }
        ),
        # Task Management Tools
        types.Tool(
            name="clear_upcoming_steps",
            description="Clear all upcoming steps from the task list",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="add_upcoming_step",
            description="Add a new step to the upcoming task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "step_description": {
                        "type": "string",
                        "description": "Description of the step to add"
                    }
                },
                "required": ["step_description"]
            }
        ),
        types.Tool(
            name="get_upcoming_steps_count",
            description="Get the actual number of upcoming steps in the task list",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="peek_next_step",
            description="Preview the next step without removing it from the list and return step details",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_next_step",
            description="Get and remove the next step from the task list, returning the step description",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="set_current_step",
            description="Set the current step being executed",
            inputSchema={
                "type": "object",
                "properties": {
                    "step_description": {
                        "type": "string",
                        "description": "Description of the current step"
                    }
                },
                "required": ["step_description"]
            }
        ),
        types.Tool(
            name="remove_upcoming_step",
            description="Remove a specific step from the upcoming task list by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "Index of the step to remove (0-based)"
                    }
                },
                "required": ["index"]
            }
        ),
        types.Tool(
            name="insert_upcoming_step",
            description="Insert a step at a specific position in the upcoming task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "Index where to insert the step (0-based)"
                    },
                    "step_description": {
                        "type": "string",
                        "description": "Description of the step to insert"
                    }
                },
                "required": ["index", "step_description"]
            }
        ),
        types.Tool(
            name="handle_npc_dialogue",
            description="Handle NPC dialogue interactions, waiting for all dialogue to complete. Uses the Tutorial Island dialogue handling pattern.",
            inputSchema={
                "type": "object",
                "properties": {
                    "npc_name": {
                        "type": "string",
                        "description": "Name of the NPC to interact with (optional, can be empty for any dialogue)"
                    },
                    "max_wait_time": {
                        "type": "integer",
                        "description": "Maximum time to wait for dialogue completion in seconds (default: 30)"
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="use_item_on_item",
            description="Use one item on another item in the inventory (combine items)",
            inputSchema={
                "type": "object",
                "properties": {
                    "primary_item": {
                        "type": "string", 
                        "description": "Name or ID of the primary item to use"
                    },
                    "secondary_item": {
                        "type": "string",
                        "description": "Name or ID of the secondary item to use the primary item on"
                    },
                    "use_item_ids": {
                        "type": "boolean",
                        "description": "Whether to treat the item parameters as IDs (true) or names (false). Default is false (names)."
                    }
                },
                "required": ["primary_item", "secondary_item"]
            }
        ),
        types.Tool(
            name="perform_item_action",
            description="Perform a custom action on an item, or use an item on a game object. Examples: 'Eat' on 'Lobster', use 'Bread' on 'Oven', 'Drop' an item, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The action to perform (e.g., 'Eat', 'Use', 'Drop', 'Drink', 'Wield', etc.)"
                    },
                    "item": {
                        "type": "string",
                        "description": "Name or ID of the item to perform the action on"
                    },
                    "target": {
                        "type": "string",
                        "description": "Optional target for the action. Can be another item name (for inventory actions) or game object name (for world interactions)"
                    },
                    "use_item_ids": {
                        "type": "boolean",
                        "description": "Whether to treat the item parameter as an ID (true) or name (false). Default is false (names)."
                    },
                    "target_type": {
                        "type": "string",
                        "description": "Type of target: 'item' for inventory items, 'object' for game objects. Default is 'object' if target is provided.",
                        "enum": ["item", "object"]
                    }
                },
                "required": ["action", "item"]
            }
        ),
        # Ground Item Tools
        types.Tool(
            name="pickup_ground_item",
            description="Pick up a ground item by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name of the ground item to pick up"
                    }
                },
                "required": ["item_name"]
            }
        ),
        types.Tool(
            name="pickup_ground_item_by_id",
            description="Pick up a ground item by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "integer",
                        "description": "ID of the ground item to pick up"
                    }
                },
                "required": ["item_id"]
            }
        ),
        types.Tool(
            name="get_nearby_ground_items",
            description="Get information about nearby ground items",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="ground_item_exists",
            description="Check if a specific ground item exists nearby",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name of the ground item to check for"
                    }
                },
                "required": ["item_name"]
            }
        ),
        types.Tool(
            name="get_distance_to_ground_item",
            description="Get the distance to the closest ground item by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name of the ground item to get distance to"
                    }
                },
                "required": ["item_name"]
            }
        ),
        types.Tool(
            name="get_current_tile",
            description="Get the player's current tile coordinates (x, y, z)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]
