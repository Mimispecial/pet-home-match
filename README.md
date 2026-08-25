# Pet Home Match

Checks one designated applicant's declared home and care plan against shelter-frozen pet needs, followed by separate shelter and applicant confirmations.

## Why it is an Intelligent Contract

Return a need mask and MATCH, REVIEW, or NO_MATCH based only on the applicant's public care declarations. GenLayer validators independently replay that semantic judgment before it becomes shared state. Need setup, designated-applicant authorization, one clarification, shelter shortlist decision, applicant confirmation, and placement record are deterministic.

## Reusable deployment model

Deploy once for one pet and one designated applicant. Use a new deployment for another pet, applicant, or need set.

A completed deployment is an auditable record and is not reset or silently repurposed. Reuse means deploying the same reviewed source with new constructor data.

## Roles and workflow

The deployer is the shelter and names one different applicant. The shelter defines needs and shortlists or declines; the applicant submits the home profile and confirms or withdraws.

State path: `SETTING_NEEDS → APPLICANT_INPUT → READY_TO_MATCH → SHELTER_RESPONSE → APPLICANT_CONFIRMATION → PLACEMENT_RECORD → COMPLETE`

## Evidence boundary

The stored pet profile, public matching rule, ordered needs, and applicant-declared home summary, routine, constraints, and optional clarification. No background check or external record is fetched.

## Core invariants

- Pet needs freeze before the applicant submits a home profile.
- Only the named applicant can submit, clarify, confirm, or withdraw.
- The shelter and applicant make separate decisions after the AI assessment.
- AI cannot infer protected or private traits or make a placement decision.

## Public interface

Write methods: `clarify_home_profile, complete_placement_record, define_need, evaluate_declared_match, invite_home_profile, record_shelter_response, respond_to_shortlist, submit_home_profile`

View methods: `get_need, get_policy, get_state`

`get_policy` exposes the machine-readable operating boundary and confirms that this contract never custodies funds.

## Verification

Pinned GenVM runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/pet_home_match.py
genvm-lint typecheck contracts/pet_home_match.py
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The StudioNet smoke test is opt-in and uses three disposable Mimi-only accounts protected outside the workspace. It asserts finalized successful execution and reads committed state with `LATEST_FINAL`.

## Final StudioNet proof

- Contract: https://explorer-studio.genlayer.com/address/0x6715e279Eb8304Cc07a14fCfaB83016D962e1e61
- Studio import: https://studio.genlayer.com/?import-contract=0x6715e279Eb8304Cc07a14fCfaB83016D962e1e61
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0x2c2f9f2d567a89794dc9f87ec13d88aacd823d7bc2ed008d6e6e873bca8f418e
- Intelligent transaction: https://explorer-studio.genlayer.com/tx/0xcfbd3a4d23c0d6bd0b0f2962256795208789608366ec123003aa21f8bf506cf9
- Observed committed state: `{"compatibility":"MATCH","need_mask":"11"}`
- Audited source SHA-256: `8b52337cc9ec20a24a3af2a278f1c328e1ce30be11d5f69b6e1db1119af1c05b`

## Limitations

- Applicant and shelter statements are declarations and are not externally verified.
- The contract is not a background check, veterinary assessment, legal adoption record, or home inspection.
- A MATCH label only means the declared plan covers the frozen public needs.

## Repository map

- `contracts/pet_home_match.py` — Intelligent Contract source
- `tests/direct` — hardened leader/validator and lifecycle tests
- `tests/integration/test_glsim_consensus.py` — five-validator simulator flow
- `tests/integration/test_studionet_smoke.py` — live opt-in proof
- `deployments/studionet.json` — source-bound public deployment evidence
- `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md` — reviewer material

License: MIT.
