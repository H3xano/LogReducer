import os
import re
import argparse
import logging
import ipaddress

class LogReducer:
    def __init__(self, log_folder, output_folder, keywords=None, keyword_file=None, ip_addresses=None, ip_file=None, skip_reserved=False):
        self.log_folder = log_folder
        self.output_folder = output_folder
        self.by_ip_folder = os.path.join(output_folder, "by_ip")
        self.by_keyword_folder = os.path.join(output_folder, "by_keyword")
        self.ip_global_file = os.path.join(output_folder, "ip_global.txt")
        self.keyword_global_file = os.path.join(output_folder, "keyword_global.txt")
        self.keywords = self.read_from_file(keyword_file) if keyword_file else keywords
        self.ip_addresses = self.read_from_file(ip_file) if ip_file else ip_addresses
        self.skip_reserved = skip_reserved
        self.current_file = None
        self.logger = self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s [%(levelname)s]: %(message)s',
                            handlers=[logging.FileHandler('log_reducer.log'), logging.StreamHandler()])
        logger = logging.getLogger(__name__)
        return logger

    def read_from_file(self, file_path):
        if file_path:
            with open(file_path, 'r') as file:
                return [line.strip() for line in file]
        return None

    def process_log_files(self):
        self.logger.info(f"Processing logs in {self.log_folder}...")

        for root, dirs, files in os.walk(self.log_folder):
            for file in files:
                self.current_file = os.path.relpath(os.path.join(root, file), self.log_folder)
                self.process_log_file()

    def process_log_file(self):
        self.logger.info(f"Processing log file: {self.current_file}")

        try:
            # Print the absolute path for debugging
            abs_file_path = os.path.abspath(os.path.join(self.log_folder, self.current_file))
            self.logger.debug(f"Absolute file path: {abs_file_path}")

            with open(os.path.join(self.log_folder, self.current_file), 'r') as log_file:
                for line in log_file:
                    self.process_line(line)
        except Exception as e:
            self.logger.error(f"An error occurred while processing file {self.current_file}: {str(e)}")

    def process_line(self, line):
        # Process IP addresses from the provided list or any IP if not provided
        ip_list = self.ip_addresses or [r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b']
        for ip_pattern in ip_list:
            match = re.search(ip_pattern, line)
            if match:
                ip_address = match.group(0)
                if not self.skip_reserved or not self.is_reserved(ip_address):
                    self.export_to_file(line, f"by_ip/{ip_address}.txt", self.ip_global_file)

        # Process keywords from the provided list
        if self.keywords:
            for keyword in self.keywords:
                if re.search(keyword, line):
                    self.export_to_file(line, f"by_keyword/{keyword}.txt", self.keyword_global_file)

    def is_reserved(self, ip):
        try:
            return ipaddress.ip_address(ip).is_private
        except ValueError:
            return False

    def export_to_file(self, line, file_path, global_file_path):
        output_folder = os.path.join(self.output_folder, os.path.dirname(file_path))
        os.makedirs(output_folder, exist_ok=True)

        with open(os.path.join(output_folder, os.path.basename(file_path)), 'a') as output_file:
            output_file.write(f"{self.current_file}: {line}")

        # Append the line to the global file
        with open(global_file_path, 'a') as global_file:
            global_file.write(f"{self.current_file}: {line}")

    def run(self):
        try:
            self.process_log_files()
            self.logger.info("Log reduction completed successfully.")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Reduce logs based on keyword or IP address.")
    parser.add_argument("log_folder", help="Path to the folder containing log files.")
    parser.add_argument("output_folder", help="Path to the folder where reduced logs will be saved.")
    parser.add_argument("-k", "--keywords", nargs='+', help="Keyword(s) to filter logs.")
    parser.add_argument("-kf", "--keyword_file", help="File containing a list of keywords.")
    parser.add_argument("-ip", "--ip_addresses", nargs='+', help="IP address(es) pattern to filter logs.")
    parser.add_argument("-ipf", "--ip_file", help="File containing a list of IP addresses.")
    parser.add_argument("--skip-reserved", action="store_true", help="Skip reserved and local IP addresses.")
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()

    # Create an instance of LogReducer with provided arguments
    log_reducer = LogReducer(log_folder=args.log_folder, output_folder=args.output_folder,
                             keywords=args.keywords, keyword_file=args.keyword_file,
                             ip_addresses=args.ip_addresses, ip_file=args.ip_file,
                             skip_reserved=args.skip_reserved)

    # Run the log reduction process
    log_reducer.run()
