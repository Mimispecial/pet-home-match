from pathlib import Path
import json

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Evaluate one designated applicant's public declarations"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"need_mask": "11", "compatibility": "MATCH"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_bilateral_pet_match():
    shelter_account, applicant_account = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "pet_home_match.py")
    deployed = factory.deploy_contract_tx(args=[applicant_account.address, "Milo", "Milo is an adult shelter dog who enjoys two calm walks each day, rests indoors, and has lived comfortably without other pets.", "Use only declared schedules, pet arrangements, and care plans; never infer protected or private traits."], account=shelter_account, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    shelter = factory.build_contract(address, account=shelter_account)
    applicant = factory.build_contract(address, account=applicant_account)
    ok(shelter.define_need(args=["ROUTINE", "The home declares availability for two calm walks and indoor rest each day."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(shelter.define_need(args=["PETS", "The home declares that no other pets currently share the residence."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(shelter.invite_home_profile(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(applicant.submit_home_profile(args=["A quiet indoor home with a secure entry and dedicated resting area is declared for Milo.", "The routine includes a calm morning walk, indoor rest, and calm evening walk every day.", "The applicant declares that no other pets currently live in the home."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(applicant.evaluate_declared_match(args=[]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(shelter.record_shelter_response(args=["SHORTLIST", "The declared care plan satisfies the frozen public needs and may proceed to applicant confirmation."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(applicant.respond_to_shortlist(args=["CONFIRM", "The applicant confirms continued interest after reviewing the public placement information."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(shelter.complete_placement_record(args=["The shelter and applicant completed separate confirmations and recorded the placement workflow outcome."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert shelter.get_state(args=[]).call()["state"] == "COMPLETE"
