
# Log Reducer

Log Reducer is a Python tool designed to parse and reduce log files based on keywords or IP addresses. It organizes log entries into separate files, making it easier to analyze and manage log data.

## Features

- Parse log files and extract lines based on specified keywords or IP addresses.
- Organize log entries into separate files for each keyword or IP address.
- Generate global log files containing all matched lines for both keywords and IP addresses.
- Supports recursive processing of log files within a specified folder.

## Getting Started

### Prerequisites

- Python 3.x
- (Optional) Virtual environment for isolating dependencies

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/abdou0xdz/log-reducer.git
    ```

2. Navigate to the project folder:

    ```bash
    cd log-reducer
    ```

3. (Optional) Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

```bash
python log_reducer.py log_folder output_folder -k keyword1 keyword2 -ip 192.168.1.1 10.0.0.1
```

Replace `log_folder` with the path to the folder containing your log files and `output_folder` with the desired output directory.

- Use the `-k` option followed by keywords to filter logs based on keywords.
- Use the `-ip` option followed by IP addresses to filter logs based on IP addresses.

Example with keyword file and IP file:

```bash
python log_reducer.py log_folder output_folder -kf keyword_file.txt -ipf ip_file.txt
```

### Options

- `-k, --keywords`: Keyword(s) to filter logs.
- `-kf, --keyword_file`: File containing a list of keywords.
- `-ip, --ip_addresses`: IP address(es) pattern to filter logs.
- `-ipf, --ip_file`: File containing a list of IP addresses.
- `--skip-reserved`: Skip reserved and local IP addresses.

## Contributing

Contributions are welcome! Please follow the [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.