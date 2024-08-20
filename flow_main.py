from pathlib import Path
import argparse

from flow_helper import *

# Default input paths
PROTOCOL_NUMBERS_PATH = "input/protocol_numbers.csv"
FLOW_LOG_PATH = "input/flow_data.log"
LOOKUP_TABLE_PATH = "input/lookup_table.csv"

# Default ouput paths
TAG_COUNTS_PATH = "output/tag_counts.csv"
PORT_PROTOCOL_COUNTS_PATH = "output/port_protocol_counts.csv"


def main():
    protocol_numbers_path, lookup_table_path, flow_log_path, tag_counts_path, port_protocol_counts_path, has_header = get_arguments()

    tag_counts, port_protocol_counts = get_counts_from_flow_log(
        protocol_numbers_path, lookup_table_path, flow_log_path, has_header)

    write_tag_counts(tag_counts_path, tag_counts)
    write_port_protocol_counts(port_protocol_counts_path, port_protocol_counts)


def get_arguments() -> tuple[str, str, str, str, str, bool]:
    protocol_numbers_path = PROTOCOL_NUMBERS_PATH
    flow_log_path = FLOW_LOG_PATH
    lookup_table_path = LOOKUP_TABLE_PATH
    tag_counts_path = TAG_COUNTS_PATH
    port_protocol_counts_path = PORT_PROTOCOL_COUNTS_PATH
    has_header = False

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', "--custom", help="indicates that flow log format is custom (note: header must be present)", action="store_true")
    parser.add_argument('-i', '--input', nargs=3, metavar=('protocol_numbers.csv', 'log_file', 'lookup_table.csv'),
                        help='uses the inputted file paths for parsing')
    parser.add_argument('-o', '--output', nargs=2, metavar=('tag_counts.csv', 'port_protocol_counts.csv'),
                        help='outputs to the provided file paths for reporting results instead of the default ones')
    args = parser.parse_args()

    if not args.input or not args.output:
        print("Current working directory:", Path().resolve(), "\n")
        print("Please enter the path to the following (or leave empty for default):")

    if args.custom:
        has_header = True

    if args.input:
        protocol_numbers_path = args.input[0]
        lookup_table_path = args.input[1]
        flow_log_path = args.input[2]
    else:
        protocol_numbers_path = input(
            "> Input File: protocol_numbers.csv: ").strip() or protocol_numbers_path
        lookup_table_path = input(
            "> Input File: lookup_table.csv: ").strip() or lookup_table_path
        flow_log_path = input(
            "> Input File: flow_log: ").strip() or flow_log_path

    if args.output:
        tag_counts_path = args.output[0]
        port_protocol_counts_path = args.output[1]
    else:
        tag_counts_path = input(
            "> Output File: tag_counts.csv: ").strip() or tag_counts_path
        port_protocol_counts_path = input(
            "> Output File: port_protocol_counts.csv: ").strip() or port_protocol_counts_path

    # Print spacer
    if not args.input or not args.output:
        print()

    return protocol_numbers_path, lookup_table_path, flow_log_path, tag_counts_path, port_protocol_counts_path, has_header


if __name__ == "__main__":
    main()
