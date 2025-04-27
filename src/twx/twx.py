import argparse
import csv
import datetime as dt
from dotenv import load_dotenv
import gzip
import json
import logging
import os
import requests
import urllib.parse
import urllib.request

import twx
from twx import Tempest

logger = logging.getLogger(__name__)

# The number of seconds in a day.
ONE_DAY_IN_SECONDS = 24 * 3600

def _parse_args():
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        prog="twx",
        description="Tempest API client",
    )

    parser.add_argument(
        "--api_token",
        required=True,
        help="Tempest API token to use when making API requests.",
    )

    parser.add_argument(
        "--device_id",
        required=True,
        type=int,
        help="The id(s) of the device(s) to sync data for.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Emit progress information.",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )

    return parser.parse_args()

def main():
    args = _parse_args()
    logging.basicConfig(level=args.loglevel)

    twx = Tempest(auth=args.api_token)
    results = twx.observations_station(args.device_id)
    print(results)

    # for device_id in args.device_id:
    #     _fetch_device_data_for_range(args.api_token, device_id)

if __name__ == "__main__":
    main()
