import json
import uuid
from typing import Any, Dict, Optional

from websockets.sync import client

from .attributes import PrinterAttributes
from .status import PrinterStatus


class Printer:
    def __init__(
        self, printer_ip: str, mainboard_id: str, *, non_response_callback: ... = None
    ):
        self._printer_ip = printer_ip
        self.mainboard_id = mainboard_id
        self._non_response_callback = non_response_callback
        self._response_topic = f"sdcp/response/{self.mainboard_id}"

    def __enter__(self):
        self._ws = client.connect(f"ws://{self._printer_ip}:3030/websocket").__enter__()
        return self

    def __exit__(self, *args):
        self._ws.__exit__(*args)

    def _request(self, cmd: int, data: Optional[Dict] = None) -> ...:
        if data is None:
            data = {}
        request_id = str(uuid.uuid1())
        msg = json.dumps(
            {
                "Id": "TODO",
                "Data": {
                    "Cmd": cmd,
                    "Data": data,
                    "RequestID": request_id,
                    "MainboardID": self.mainboard_id,
                    "TimeStamp": 0,
                    "From": 0,
                },
                "Topic": f"sdcp/request/{self.mainboard_id}",
            }
        )
        self._ws.send(msg)
        response = self._recv(self._response_topic)
        if response["Data"]["RequestID"] != request_id:
            raise Exception("oh no")
        return response

    def _recv(self, expected_topic: str) -> Dict[str, Any]:
        for raw_msg in self._ws:
            msg = json.loads(raw_msg)
            if msg["Topic"] == expected_topic:
                return msg
            if self._non_response_callback is not None:
                self._non_response_callback(msg)

    def get_status(self):
        self._request(0)
        return PrinterStatus.from_json(
            self._recv(f"sdcp/status/{self.mainboard_id}")["Status"]
        )

    def get_attributes(self):
        self._request(1)
        return PrinterAttributes.from_json(
            self._recv(f"sdcp/attributes/{self.mainboard_id}")["Attributes"]
        )

    def enable_video_stream(self):
        return self._request(386, {"Enable": 1})

    def disable_video_stream(self):
        return self._request(386, {"Enable": 0})
