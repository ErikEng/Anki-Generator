# Standard library
# from dataclasses import dataclass

from typing import Dict, Any

# Internal modules

# @dataclass(frozen=True)
class Mode:
    name: str
    input_name: str
    output_name: str

    # @classmethod
    def __init__(self, raw) -> "mode":
        self.name = raw["name"]
        self.input_name = raw["input_name"]
        self.output_name = raw["output_name"]
        # return self(name=name, output_name=output_name, input_name=input_name)

def get_mode_dto(dto_name)->Mode:
    if dto_name == "split_mode":
        # mode = new Mode()
        dict = {"name" :"split_mode", "input_name": "input.txt", "output_name":"output"}

    elif dto_name == "format_to_ascii":
        dict = {"name" :"format_to_ascii", "input_name": "input.txt", "output_name":"output"}

    elif dto_name == "timestamp_removal_mode":
        dict = {"name" :"timestamp_removal_mode", "input_name": "input.txt", "output_name":"output"}
    else:
        raise Exception(f"mode:{dto_name} could not be found")
    mode = Mode(dict)

    return mode
