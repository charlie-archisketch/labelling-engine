GENERATE_NAME_TOOL = [
    {
        "toolSpec": {
            "name": "generate_furniture_name",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "It must be Korean.",
                            "minLength": 1,
                            "maxLength": 150,
                        }
                    },
                    "required": ["name"]
                }
            }
        }
    }
]

GENERATE_TYPE_TOOL = [
    {
        "toolSpec": {
            "name": "generate_furniture_type",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "description": """
                            You must classify an item into exactly one of the following categories. 
                            Do  not generate any values outside of the given labels.

                            - Floor Item : products placed on the floor (e.g., carpet, mat)
                            - Standing Item : products standing on the floor (e.g., chair, desk, sofa)
                            - Wall Item : products attached to the wall (e.g., wall cabinet, frame, wall shelf)
                            - Ceiling Item : products attached to the ceiling (e.g., ceiling light, mobile)
                            - Swing Door : hinged doors (open/close by swinging)
                            - Sliding Door : sliding doors
                            - Folding Door : folding doors
                            - Garage Door : garage doors
                            - Swing Window : hinged windows (open/close by swinging)
                            - Sliding Window : sliding windows
                            - Folding Window : folding windows
                            - Standard Window : standard windows
                            - Space : a space/room itself
                            """,
                            "minLength": 1,
                            "maxLength": 20
                        }
                    },
                    "required": ["type"]
                }
            }
        }
    }
]

GENERATE_TAGS_TOOL = [
    {
        "toolSpec": {
            "name": "generate_furniture_tags",
            # "description": """
            # Return up to five matching tags based on furniture information.
            # Focus on the most relevant attributes such as:
            # - Product type (e.g., sofa, chair, table, bed)
            # - Material & Finish (e.g., wood, marble, fabric, metal, leather)
            # - Design & Style (e.g., modern, minimal, vintage, nordic, industrial)
            # - Space & Usage (e.g., living-room, bedroom, kitchen, office, studio)
            #
            # NOTE: Avoid duplicates or irrelevant tags.
            # """,
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "tags": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
                                "minLength": 1,
                                "maxLength": 30
                            },
                            "minItems": 1,
                            "maxItems": 5,
                            "uniqueItems": True
                        }
                    },
                    "required": ["tags"]
                }
            }
        }
    }
]

GENERATE_DESCRIPTION_TOOL = [
    {
        "toolSpec": {
            "name": "generate_furniture_description",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "It must be Korean.",
                            "minLength": 30,
                            "maxLength": 500
                        }
                    },
                    "required": ["description"]
                }
            }
        }
    }
]

SYSTEM_PROMPT = [
    {
        "text": """
        You are an expert furniture curator and product content creator. 
        When given an input that includes furniture images and/or basic product information, 
        you must generate structured output describing the furniture in a clear and consistent way.
        
        - The input fields are provided as background information only.
        - **Do not copy these input values verbatim into the output.**
        """
    }
]

USER_PROMPT_TEMPLATE =  """
Furniture Name: {name}
Type: {type}
Tags: {tags}
Description: {description}
{prompt}
"""