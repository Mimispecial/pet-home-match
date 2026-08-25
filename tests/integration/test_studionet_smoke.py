import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


@pytest.mark.integration
def test_studionet_pet_home_match(default_account, secondary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "pet_home_match.py")
    deployed = ok(factory.deploy_contract_tx(args=[secondary_account.address, "Milo", "Milo is an adult shelter dog who enjoys two calm walks each day, rests indoors, and has lived comfortably without other pets.", "Use only declared schedules, pet arrangements, and care plans; never infer protected or private traits."], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    shelter = factory.build_contract(address, account=default_account)
    applicant = factory.build_contract(address, account=secondary_account)
    ok(shelter.define_need(args=["ROUTINE", "The home declares availability for two calm walks and indoor rest each day."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(shelter.define_need(args=["PETS", "The home declares that no other pets currently share the residence."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(shelter.invite_home_profile(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(applicant.submit_home_profile(args=["A quiet indoor home with a secure entry and dedicated resting area is declared for Milo.", "The routine includes a calm morning walk, indoor rest, and calm evening walk every day.", "The applicant declares that no other pets currently live in the home."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(applicant.evaluate_declared_match(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    state = shelter.get_state(args=[]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["state"] == "SHELTER_RESPONSE"
    assert state["compatibility"] in ("MATCH", "REVIEW", "NO_MATCH")
    observed = {"compatibility": state["compatibility"], "need_mask": state["need_mask"]}
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": observed}, sort_keys=True))
