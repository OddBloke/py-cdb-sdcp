from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class NetworkStatus(Enum):
    WLAN = "wlan"
    ETH = "eth"


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
    NetworkStatus: NetworkStatus
    NumberOfCloudSDCPServicesConnected: int
    NumberOfVideoStreamConnected: int
    ProtocolVersion: str
    ReleaseFilmMax: int
    RemainingMemory: int
    Resolution: tuple
    SDCPStatus: int  # undocumented
    SupportFileType: List[str]
    TLPInterLayers: int
    TLPNoCapPos: int
    TLPStartCapPos: int
    UsbDiskStatus: int
    XYZsize: tuple

    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> "PrinterAttributes":
        network_status = NetworkStatus(payload.pop("NetworkStatus"))
        resolution = tuple(payload.pop("Resolution").split("x"))
        xyz_size = tuple(payload.pop("XYZsize").split("x"))
        return cls(
            NetworkStatus=network_status,
            Resolution=resolution,
            XYZsize=xyz_size,
            **payload
        )
