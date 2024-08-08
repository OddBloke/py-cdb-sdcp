from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List


class PrintError(Enum):
    # Names and values from sdcp_print_error_t in
    # https://github.com/cbd-tech/SDCP-Smart-Device-Control-Protocol-V3.0.0/blob/main/SDCP%28Smart%20Device%20Control%20Protocol%29_V3.0.0_EN.md#errornumber
    NONE = 0  # Normal
    CHECK = 1  # File MD5 Check Failed
    FILEIO = 2  # File Read Failed
    INVLAID_RESOLUTION = 3  # Resolution Mismatch
    UNKNOWN_FORMAT = 4  # Format Mismatch
    UNKNOWN_MODEL = 5  # Machine Model Mismatch


class PrintStatus(Enum):
    # Names and values from sdcp_print_status_t in
    # https://github.com/cbd-tech/SDCP-Smart-Device-Control-Protocol-V3.0.0/blob/main/SDCP%28Smart%20Device%20Control%20Protocol%29_V3.0.0_EN.md#status
    IDLE = 0
    HOMING = 1
    DROPPING = 2
    EXPOSURING = 3
    LIFTING = 4
    PAUSING = 5
    PAUSED = 6
    STOPPING = 7
    STOPPED = 8
    COMPLETE = 9
    FILE_CHECKING = 10


@dataclass
class PrintInfo:
    Status: PrintStatus
    CurrentLayer: int
    TotalLayer: int
    CurrentTicks: int
    TotalTicks: int
    ErrorNumber: PrintError
    Filename: str
    TaskId: str

    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> "PrintInfo":
        error = PrintError(payload.pop("ErrorNumber"))
        status = PrintStatus(payload.pop("Status"))
        return cls(ErrorNumber=error, Status=status, **payload)


class MachineStatus(Enum):
    # Names and values from sdcp_machine_status_t in
    # https://github.com/cbd-tech/SDCP-Smart-Device-Control-Protocol-V3.0.0/blob/main/SDCP%28Smart%20Device%20Control%20Protocol%29_V3.0.0_EN.md#differences-between-top-level-status-changes-and-sub-statuses
    IDLE = 0
    PRINTING = 1
    FILE_TRANSFERRING = 2
    EXPOSURE_TESTING = 3
    DEVICES_TESTING = 4


@dataclass
class PrinterStatus:
    CurrentStatus: List[MachineStatus]
    PrintInfo: PrintInfo
    PrintScreen: float
    ReleaseFilm: int
    TempOfUVLED: float
    TimeLapseStatus: int

    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> "PrinterStatus":
        current_statuses = [
            MachineStatus(status) for status in payload.pop("CurrentStatus")
        ]
        print_info = PrintInfo.from_json(payload.pop("PrintInfo"))
        return cls(CurrentStatus=current_statuses, PrintInfo=print_info, **payload)
