
# Copyright [2025] [Aleksandr V. Krasilnikov] Licensed under the Apache License, Version 2.0;
import ipaddress
from zipfile import ZipFile, BadZipFile
from io import BytesIO
import requests
import yaml
from pathlib import Path
from typing import List, Set, BinaryIO, Union, Optional
import logging
from datetime import datetime

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BlocklistProcessor:
    def __init__(self, config_path: str = "config.yaml", output_dir: str = "firewall_rules"):
        self.config = self._load_config(config_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

    @staticmethod
    def _load_config(config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path) as f:
                return yaml.safe_load(f) or {"blocklists": []}
        except FileNotFoundError:
            logger.error(f"Configuration file {config_path} not found!")
            return {"blocklists": []}
        except yaml.YAMLError as e:
            logger.error(f"Error in configuration file: {e}")
            return {"blocklists": []}

    def download(self, url: str) -> Optional[BytesIO]:
        """Download content from URL."""
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            logger.error(f"Error downloading {url}: {e}")
            return None

    def extract_contents(self, stream: Optional[BytesIO], content_format: str) -> List[str]:
        """Extract contents from ZIP archive or text file."""
        if stream is None:
            return []

        try:
            if content_format == "zip":
                with ZipFile(stream) as zip_file:
                    archived_file = zip_file.namelist()[0]
                    with zip_file.open(archived_file) as f:
                        return [line.decode('utf-8', errors='ignore').strip()
                                for line in f if line.strip()]

            # Handling text format
            stream.seek(0)
            return [line.decode('utf-8', errors='ignore').strip()
                    for line in stream if line.strip()]

        except (BadZipFile, IndexError) as e:
            logger.error(f"Error processing archive: {e}", exc_info=True)
            return []

    def cleanse_contents(self, contents: List[str]) -> Set[str]:
        """Filter and validate IP addresses/networks."""
        valid_ips = set()
        for line in contents:
            if not line or line.startswith((';', '#', '//')):
                continue

            # Extract IP/CIDR and ignore comments
            ip_part = line.split()[0].split(';')[0].strip()

            try:
                network = ipaddress.ip_network(ip_part)
                valid_ips.add(str(network))
            except ValueError:
                logger.debug(f"Invalid IP range format: {line}")

        return valid_ips

    def generate_firewall_rules(self, list_name: str, subnets: Set[str], output_file: str) -> bool:
        """Generate Mikrotik firewall rules file."""
        if not subnets:
            logger.warning(f"List {list_name} contains no valid subnets - file won't be created")
            return False

        output_path = self.output_dir / output_file
        rule_template = f"/ip firewall address-list add list={list_name.upper()} address="

        try:
            with output_path.open('w') as f:
                f.write(f"# Generated at {datetime.now()}\n")
                f.write(f"# Source: {list_name}\n")
                f.write(f"# Total networks: {len(subnets)}\n\n")

                for subnet in sorted(subnets):
                    f.write(f"{rule_template}{subnet}\n")

            logger.info(f"File {output_path} successfully created ({len(subnets)} rules)")
            return True
        except IOError as e:
            logger.error(f"Error writing to file {output_path}: {e}")
            return False

    def process_blocklist(self, blocklist: dict) -> None:
        """Process a single blocklist."""
        name = blocklist.get("name", "unnamed")
        url = blocklist.get("url")

        if not url:
            logger.error(f"List {name} doesn't contain URL - skipping")
            return

        format = blocklist.get("format", "zip" if url.lower().endswith('.zip') else "text")
        output_file = blocklist.get("output_file", f"{name}.rsc")

        logger.info(f"Processing list {name}...")

        content_stream = self.download(url)
        if content_stream is None:
            return

        contents = self.extract_contents(content_stream, format)
        if not contents:
            logger.warning(f"List {name} contains no data")
            return

        valid_subnets = self.cleanse_contents(contents)
        self.generate_firewall_rules(name, valid_subnets, output_file)

    def process_all_blocklists(self) -> None:
        """Process all lists from configuration."""
        if not self.config.get("blocklists"):
            logger.error("No blocklists to process in configuration!")
            return

        logger.info(f"Starting processing of {len(self.config['blocklists'])} lists...")

        for blocklist in self.config["blocklists"]:
            self.process_blocklist(blocklist)

        logger.info("All lists processing completed")


if __name__ == "__main__":
    # You can specify your own config and output directory
    processor = BlocklistProcessor(
        config_path="config.yaml",
        output_dir="generated_firewall_rules"
    )
    processor.process_all_blocklists()
