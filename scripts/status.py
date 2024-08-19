import datetime
import os

from cbd_sdcp import Printer
from cbd_sdcp.status import PrinterStatus


def callback(msg):
    if 'Status' not in msg:
        print(datetime.datetime.now().isoformat(), msg)
        return
    status = PrinterStatus.from_json(msg['Status'])
    print(datetime.datetime.now().isoformat(), status.CurrentStatus[0], f"{status.PrintInfo.CurrentLayer}/{status.PrintInfo.TotalLayer}", status.PrintInfo.Status)

def main():
    with Printer(os.environ["SDCP_PRINTER_IP"], os.environ["SDCP_MAINBOARD_ID"], non_response_callback=callback) as printer:
        printer.recv_forever()


main()
