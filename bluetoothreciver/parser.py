from typing import Dict, Any
from datetime import datetime


class AirPodsMapper:
    mapper = {
        "e": "AirPods Pro",
        "3": "AirPods 3",
        "f": "AirPods 2",
        "2": "AirPods 1",
        "a": "AirPods Max",
    }

    @staticmethod
    def map(data: str) -> str:
        return AirPodsMapper.mapper.get(data, "Unknown")


class HexParser:
    @staticmethod
    def parse(data: bytes) -> Dict[str, Any]:
        if data is None:
            return dict(status=0, model="AirPods not found")

        model = AirPodsMapper.map(chr(data[7]))

        flip = HexParser.__is_flipped(data)

        status_tmp = int("" + chr(data[12 if flip else 13]), 16)
        left_status = 100 if status_tmp == 10 else (status_tmp * 10 + 5 if status_tmp <= 10 else -1)

        # Checking right AirPod for availability and storing charge in variable
        status_tmp = int("" + chr(data[13 if flip else 12]), 16)
        right_status = (
            100 if status_tmp == 10 else (status_tmp * 10 + 5 if status_tmp <= 10 else -1)
        )

        # Checking AirPods case for availability and storing charge in variable
        status_tmp = int("" + chr(data[15]), 16)
        case_status = 100 if status_tmp == 10 else (status_tmp * 10 + 5 if status_tmp <= 10 else -1)

        # On 14th position we can get charge status of AirPods
        charging_status = int("" + chr(data[14]), 16)
        charging_left: bool = (charging_status & (0b00000010 if flip else 0b00000001)) != 0
        charging_right: bool = (charging_status & (0b00000001 if flip else 0b00000010)) != 0
        charging_case: bool = (charging_status & 0b00000100) != 0

        # Return result info in dict format
        return dict(
            status=1,
            charge=dict(left=left_status, right=right_status, case=case_status),
            charging_left=charging_left,
            charging_right=charging_right,
            charging_case=charging_case,
            model=model,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data=data.decode("utf-8"),
        )

    @staticmethod
    def __is_flipped(data: bytes) -> bool:
        return (int("" + chr(data[10]), 16) & 0x02) == 0
