import os
import json
from django.conf import settings


def get_contract_abi(name):
    # base = settings.BASE_DIR
    # base = base.replace("backend", "")
    abi_path = os.path.join(
        settings.BASE_DIR,
        "..",
        "contracts",
        "artifacts",
        "contracts",
        f"{name}.sol",
        f"{name}.json",
    )
    # Open and load the ABI file
    with open(abi_path, "r") as abi_file:
        contract_abi = json.load(abi_file)

    return contract_abi["abi"]
