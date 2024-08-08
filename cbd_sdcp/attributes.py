from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class PrinterAttributes:
    BrandName: str
    CameraStatus: int
    Capabilities: List[str]
    DevicesStatus: Dict[str, int]
    FirmwareVersion: str
    MachineName: str
    MainboardID: str
    MainboardIP: str
    MaximumCloudSDCPSercicesAllowed: int
    MaximumVideoStreamAllowed: int
    Name: str
    NetworkStatus: str  # TODO: Enum wlan|eth
    NumberOfCloudSDCPServicesConnected: int
    NumberOfVideoStreamConnected: int
    ProtocolVersion: str
    ReleaseFilmMax: int
    RemainingMemory: int
    Resolution: str  # TODO: tuple?
    SDCPStatus: int  # undocumented
    SupportFileType: List[str]
    TLPInterLayers: int
    TLPNoCapPos: int
    TLPStartCapPos: int
    UsbDiskStatus: int
    XYZsize: str  # TODO: tuple?

    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> "PrinterAttributes":
        return cls(**payload)
