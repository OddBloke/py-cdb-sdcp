import collections
import json
import os
import time
from pprint import pprint
from threading import Thread

import websocket


def on_error(ws, error):
    print("ERR:", error)


def on_close(ws, close_status_code, close_msg):
    return
    print("### closed ###", close_status_code, close_msg)


class SDCPHandler:

    def __init__(self, printer_ip: str, mainboard_id: str):
        # TODO: Fetch mainboard_id via port 3000
        self._ws = websocket.WebSocketApp(
            f"ws://{printer_ip}:3030/websocket",
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=on_error,
            on_close=on_close,
        )
        self._ready = False
        Thread(target=self._ws.run_forever).start()

        self.mainboard_id = mainboard_id
        self._responses = collections.defaultdict(list)

        while not self._ready:
            time.sleep(0.1)

    def _on_open(self, ws):
        #print("Opened connection")
        self._ready = True

    def _on_message(self, wsapp: websocket.WebSocketApp, message: str):
        #print("MSG:\n", message)
        message = json.loads(message)
        topic = message["Topic"]
        self._responses[topic].append(message)

    def close(self):
        self._ws.close()

    def _request(self, cmd: int, data: "Optional[Dict]" = None) -> ...:
        if data is None:
            data = {}
        msg = json.dumps({
            "Id": "TODO",
            "Data": {
                "Cmd": cmd,
                "Data": data,
                "RequestID": "TODO",
                "MainboardID": self.mainboard_id,
                "TimeStamp": 0,
                "From": 0,
            },
            "Topic": f"sdcp/request/{self.mainboard_id}",
        })
        return self._ws.send(msg)

    def request_status_refresh(self):
        self._request(0)

    def get_status(self):
        self.request_status_refresh()

        expected_topic = f"sdcp/status/{self.mainboard_id}"
        while expected_topic not in self._responses:
            time.sleep(0.1)

        return self._responses[expected_topic][0]


def main():
    #websocket.enableTrace(True)
    handler = SDCPHandler(os.environ["SDCP_PRINTER_IP"], os.environ["SDCP_MAINBOARD_ID"])
    pprint(handler.get_status())
    handler.close()


if __name__ == "__main__":
    main()
