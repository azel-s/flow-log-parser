import csv

from pathlib import Path
import sys


# Field/Header names
FLOW_FIELDS = ['version', 'account-id', 'interface-id', 'srcaddr', 'dstaddr',
               'srcport', 'dstport', 'protocol', 'packets', 'bytes', 'start', 'end', 'action', 'log-status']

REQUIRED_FLOW_FIELDS = ['dstport', 'protocol']
REQUIRED_LOOKUP_FIELDS = ['dstport', 'protocol', 'tag']
REQUIRED_PROTOCOL_FIELDS = ['decimal', 'keyword']


# Not used since this is missing some protocols, e.g. 140 -> Shim6 is not present
# Note: requires 'import socket'
# def generate_protocol_table() -> dict[int, str]:
#     protocol_table = {}

#     # Grab every item that starts with 'IPPROTO_' and put it into a table (key is number, value is name).
#     # i.e. 6 -> 'TCP'
#     IPPROTO_ = "IPPROTO_"
#     for (keyword, decimal) in vars(socket).items():
#         if keyword.startswith(IPPROTO_):
#             protocol_table[decimal] = keyword[len(IPPROTO_):].lower()

#     return protocol_table


def generate_protocol_table(protocol_numbers_path) -> dict[int, str]:
    protocol_table = {}

    if not Path(protocol_numbers_path).exists():
        sys.exit("> Error: The path " +
                 protocol_numbers_path + " does not exist.")

    with open(protocol_numbers_path, mode='r') as file:
        reader = csv.DictReader(file)

        # Make sure all required fields are present
        reader.fieldnames = [name.lower() for name in reader.fieldnames]
        for field in REQUIRED_PROTOCOL_FIELDS:
            if field not in reader.fieldnames:
                sys.exit("> Error: Provided protocol_table is missing fields")

        for row in reader:
            try:
                decimal = int(row['decimal'])
                keyword = row['keyword'].lower()

                protocol_table[decimal] = keyword
            except:
                # This is expected, so log everything else.
                if row['decimal'] != "146-252":
                    print("> Warning: Skipped (Protocol_Table): ", row)

    return protocol_table


def generate_lookup_table(lookup_table_path: str) -> dict[(int, str), str]:
    if not Path(lookup_table_path).exists():
        sys.exit("> Error: The path " + lookup_table_path + " does not exist.")

    lookup_table = {}

    with open(lookup_table_path, mode='r') as file:
        reader = csv.DictReader(file)

        # Make sure all required fields are present
        reader.fieldnames = [name.lower() for name in reader.fieldnames]
        for field in REQUIRED_LOOKUP_FIELDS:
            if field not in reader.fieldnames:
                sys.exit("> Error: Provided lookup_table is missing fields")

        for row in reader:
            try:
                port = int(row['dstport'])
                protocol = row['protocol'].lower()
                tag = row['tag'].lower()

                lookup_table[(port, protocol)] = tag
            except:
                print("> Warning: Skipped (Lookup_Table): ", row)

    return lookup_table


def get_counts_from_flow_log(protocol_numbers_path: str, lookup_table_path: str, flow_log_path: str, has_header=False, delimiter=' ') -> tuple[dict[str, int], dict[(int, str), int]]:
    protocol_table = generate_protocol_table(protocol_numbers_path)
    lookup_table = generate_lookup_table(lookup_table_path)

    tag_counts = {}
    port_protocol_counts = {}

    if not Path(flow_log_path).exists():
        sys.exit("> Error: The path " + flow_log_path + " does not exist.")

    with open(flow_log_path, mode='r') as file:
        reader = csv.DictReader(
            file, delimiter=delimiter, fieldnames=FLOW_FIELDS if not has_header else None)

        # Make sure all required fields are present
        reader.fieldnames = [name.lower() for name in reader.fieldnames]
        for field in REQUIRED_FLOW_FIELDS:
            if field not in reader.fieldnames:
                sys.exit("> Error: Provided flow log file is missing fields")

        for row in reader:
            try:
                port = int(row['dstport'])
                protocol = protocol_table.get(int(row['protocol']))

                key = (port, protocol)

                port_protocol_counts[key] = port_protocol_counts.get(
                    key, 0) + 1

                tag = lookup_table.get(key, "untagged")
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            except:
                print("> Warning: Skipped (Flow_Log): ", row)

    return tag_counts, port_protocol_counts


def write_tag_counts(tag_counts_path: str, tag_counts: dict[str, int]):
    Path(tag_counts_path).parent.mkdir(parents=True, exist_ok=True)

    with open(tag_counts_path, 'w+', newline='') as file:
        writer = csv.DictWriter(file, ['Tag', 'Count'])

        writer.writeheader()
        for tag, count in tag_counts.items():
            writer.writerow({'Tag': tag, 'Count': count})

        print("> Success: Tag Counts can be found at", tag_counts_path)


def write_port_protocol_counts(port_protocol_counts_path: str, port_protocol_counts: dict[(int, str), int]):
    Path(port_protocol_counts_path).parent.mkdir(parents=True, exist_ok=True)

    with open(port_protocol_counts_path, 'w+', newline='') as file:
        writer = csv.DictWriter(file, ['Port', 'Protocol', 'Count'])

        writer.writeheader()
        for (port, protocol), count in port_protocol_counts.items():
            writer.writerow(
                {'Port': port, 'Protocol': protocol, 'Count': count})

        print("> Success: Port/Protocol Combination Counts can be found at:",
              port_protocol_counts_path)
