"""Start the private MCP server without writing the provider secret to disk."""
import argparse
import getpass
import os
import runpy
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--enable-network", action="store_true", help="Enable potentially billable DrugBank requests")
args = parser.parse_args()
if args.enable_network:
    if not os.environ.get("DRUGBANK_API_KEY"):
        os.environ["DRUGBANK_API_KEY"] = getpass.getpass("DrugBank API key (hidden): ")
    os.environ["DRUGBANK_ENABLE_REQUESTS"] = "1"
else:
    os.environ["DRUGBANK_ENABLE_REQUESTS"] = "0"
runpy.run_path(str(Path(__file__).with_name("server.py")), run_name="__main__")
