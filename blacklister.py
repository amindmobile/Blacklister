import ipaddress
from zipfile import ZipFile
from io import BytesIO
import requests
import yaml
from pathlib import Path
from typing import List, Set, BinaryIO, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BlocklistProcessor:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)

    @staticmethod
    def _load_config(config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path) as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {
                "blocklists": [
                    {
                        "name": "bogon",
                        "url": "http://list.iblocklist.com/?list=lujdnbasfaaixitgmxpp&fileformat=cidr&archiveformat=zip",
                        "output_file": "bogon.rsc"
                    }
                ]
            }

    def download(self, url: str) -> BinaryIO:
        """Download archive from URL."""
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            logger.error(f"Failed to download {url}: {e}")
            raise

    @staticmethod
    def extract_zip_contents(stream: BinaryIO) -> List[bytes]:
        """Extract and read the first file from ZIP archive."""
        with ZipFile(stream) as zip_file:
            archived_file_name = zip_file.namelist()[0]
            with zip_file.open(archived_file_name) as unzipped_file:
                return unzipped_file.readlines()

    @staticmethod
    def cleanse_contents(contents: List[bytes]) -> Set[str]:
        """Filter and validate IP networks."""
        valid_ips = set()
        for ip_bytes in contents:
            try:
                ip_str = ip_bytes.decode().strip()
                ipaddress.ip_network(ip_str)  # Validate the IP/network
                valid_ips.add(ip_str)
            except (ValueError, UnicodeDecodeError):
                continue
        return valid_ips

    @staticmethod
    def generate_firewall_rules(list_name: str, subnets: Set[str], output_path: Union[str, Path]) -> None:
        """Generate Mikrotik firewall rules file."""
        firewall_prefix = f'/ip firewall address-list add list={list_name.upper()} address='

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open('w') as f:
            for subnet in sorted(subnets):
                f.write(f"{firewall_prefix}{subnet}\n")

        logger.info(f"Firewall rules exported to {output_path}")

    def process_blocklist(self, name: str, url: str, output_file: str) -> None:
        """Process a single blocklist."""
        logger.info(f"Processing blocklist {name} from {url}")

        try:
            zip_stream = self.download(url)
            contents = self.extract_zip_contents(zip_stream)
            valid_subnets = self.cleanse_contents(contents)
            self.generate_firewall_rules(name, valid_subnets, output_file)
        except Exception as e:
            logger.error(f"Failed to process {name}: {e}")

    def process_all_blocklists(self):
        """Process all blocklists from config."""
        for blocklist in self.config.get("blocklists", []):
            self.process_blocklist(
                name=blocklist["name"],
                url=blocklist["url"],
                output_file=blocklist["output_file"]
            )


if __name__ == "__main__":
    processor = BlocklistProcessor()
    processor.process_all_blocklists()
