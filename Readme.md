# Flow Log Reader

## Description

The program reads data flow logs and maps each row according to the destination port and protocol (provided in the lookup table).

A count of each tag as well the count of each port/protocol combo is provided in the output once program finishes executing.
By default, the files are read/written to and from the `input`/`output` folders. To use custom input/output files, simply type
their path when prompted or pass them in as as arguments (more info below).

## How to Compile/Run

- Install Python (tested on 3.11)
- Sample commands:
  - Usage instructions:
    - `python main.py -h`
  - Default behavior:
    - `python main.py`
  - Supply custom input files:
    - `python main.py -i myProtocolNumbers.csv myLookupTable.csv myFlow.log`
  - Supply custom input files with custom format (requires header in flow file):
    - `python main.py -c -i myProtocolNumbers.csv myLookupTable.csv myFlow.log`
  - Supply custom output files (will be created if non-existent):
    - `python main.py -o myTagCounts.csv myPortComboCounts.csv`

## Features/Analysis

- Default log format supported for versions 2-7.
- Custom format supported using `-c` or `--custom`. Header must be present in the provided log.

## Assumptions

- If one of the required fields is missing for a row (i.e. dstport or protocol), then the row is skipped.
- For Tag Counts and Port/Protocol Combination Counts, if the count is zero, the output does not include it.

## Testing

- Most of the testing was done using the provided sample data.
- The additional files used for edge-case testing can be found in the `input` folder.
- Final Note: Many of the errors such as file not exisiting or invalid rows are logged to help alleviate headaches.

