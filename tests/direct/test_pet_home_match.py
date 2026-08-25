from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "pet_home_match.py"
SDK = "v0.2.16"
PROMPT = "Evaluate one designated applicant's public declarations"
PROFILE = "Milo is an adult shelter dog who enjoys two calm walks each day, rests indoors, and has previously lived comfortably without other pets."
BOUNDARY = "Use only declared schedules, pet arrangements, and care plans. Never request or infer income, family status, disability, health, race, religion, or another protected or private trait."


def address(account):
    return "0x" + account.hex()


def match_case(vm, direct_deploy, shelter, applicant):
    vm.sender = shelter
    contract = direct_deploy(str(CONTRACT), address(applicant), "Milo", PROFILE, BOUNDARY, sdk_version=SDK)
    contract.define_need("ROUTINE", "The home declares availability for two calm walks and indoor rest each day.")
    contract.define_need("PETS", "The home declares that no other pets currently share the residence.")
    contract.invite_home_profile()
    vm.sender = applicant
    contract.submit_home_profile(
        "The applicant describes a quiet indoor home with a secure entry and a dedicated resting area for Milo.",
        "The declared routine includes a calm morning walk, indoor rest, and a calm evening walk every day.",
        "The applicant declares that no other pets currently live in the home and confirms the stated routine is available.",
    )
    return contract


def test_match_shelter_shortlist_applicant_confirmation_and_placement(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = match_case(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.mock_llm(PROMPT, json.dumps({"need_mask": "11", "compatibility": "MATCH"}))
    contract.evaluate_declared_match()
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True
    direct_vm.sender = direct_alice
    contract.record_shelter_response("SHORTLIST", "The declared care plan satisfies the frozen public pet needs and may proceed to applicant confirmation.")
    direct_vm.sender = direct_bob
    contract.respond_to_shortlist("CONFIRM", "The applicant confirms continued interest after reviewing the shelter's public placement note.")
    direct_vm.sender = direct_alice
    contract.complete_placement_record("The shelter and applicant completed separate confirmations and recorded the placement workflow outcome.")
    assert contract.get_state()["state"] == "COMPLETE"
    assert contract.get_state()["applicant_decision"] == "CONFIRM"


def test_review_result_allows_one_clarification(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = match_case(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.mock_llm(PROMPT, json.dumps({"need_mask": "10", "compatibility": "REVIEW"}))
    contract.evaluate_declared_match()
    direct_vm.sender = direct_bob
    contract.clarify_home_profile("The applicant explicitly confirms that no other pets live in the home and that this arrangement will remain during placement.")
    assert contract.get_state()["state"] == "READY_TO_MATCH"
    assert contract.get_state()["clarification_used"] is True


def test_designated_applicant_and_bad_mask_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    direct_vm.sender = direct_alice
    contract = direct_deploy(str(CONTRACT), address(direct_bob), "Milo", PROFILE, BOUNDARY, sdk_version=SDK)
    contract.define_need("ROUTINE", "The home declares availability for two calm walks and indoor rest each day.")
    contract.define_need("PETS", "The home declares that no other pets currently share the residence.")
    contract.invite_home_profile()
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_applicant"):
        contract.submit_home_profile("An unauthorized home summary cannot enter this bilateral match case.", "An unauthorized routine declaration cannot enter this match case.", "An unauthorized constraint declaration cannot enter this match case.")
    direct_vm.sender = direct_bob
    contract.submit_home_profile("A quiet indoor home with a dedicated resting area is declared for Milo.", "Two calm daily walks and indoor rest are explicitly declared.", "No other pets currently live in the home according to the applicant declaration.")
    direct_vm.mock_llm(PROMPT, json.dumps({"need_mask": "111", "compatibility": "MATCH"}))
    with direct_vm.expect_revert("bad_need_mask"):
        contract.evaluate_declared_match()
    assert contract.get_state()["state"] == "READY_TO_MATCH"
