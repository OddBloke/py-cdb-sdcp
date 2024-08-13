import os
from pprint import pprint

from cbd_sdcp import Printer


def callback(msg):
    print("MSG", msg)


def main():
    with Printer(os.environ["SDCP_PRINTER_IP"], os.environ["SDCP_MAINBOARD_ID"], non_response_callback=callback) as printer:
        pprint(printer.get_status())
        #pprint(printer.get_attributes())
        #task_ids = printer.retrieve_historical_tasks()
        #pprint(printer.retrieve_task_details(task_ids[0]))
        #print(printer.enable_video_stream())


main()
