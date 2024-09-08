from django.core.management.base import BaseCommand
from django.conf import settings
import time
from web3 import Web3
from post.utils import get_contract_abi

from post.models import ImagePromptTransaction


class Command(BaseCommand):
    help = "Start blockchain event listener for PromptReplied"

    def get_contract(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.IMAGEGEN_RPC_URL))
        self.contract_abi = get_contract_abi(settings.IMAGEGEN_CONTRACT_NAME)
        self.contract = self.w3.eth.contract(
            address=settings.IMAGEGEN_CONTRACT_ADDRESS, abi=self.contract_abi
        )

    def handle(self, *args, **options):
        self.get_contract()
        event_filter = self.contract.events.PromptReplied.create_filter(
            from_block="latest"
        )

        while True:
            for event in event_filter.get_new_entries():
                self.process_event(event)
            time.sleep(10)  # Poll every 10 seconds

    def process_event(self, event):
        task_id = event["args"]["promptId"]
        # Process the event, for example, find the corresponding transaction and update it
        try:
            # Assuming `prompt_id` corresponds to `task_id` in your Django model
            transaction = ImagePromptTransaction.objects.get(task_id=task_id)
            transaction.status = "processed"
            transaction.response = self.contract.functions.getImage(task_id).call()
            transaction.token_id = self.contract.functions.getTokenId(task_id).call()
            transaction.save()
        except ImagePromptTransaction.DoesNotExist:
            print(f"Transaction with taskId {task_id} not found.")
