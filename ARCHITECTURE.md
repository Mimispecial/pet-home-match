# Architecture

## Deployment boundary

Deploy once for one pet and one designated applicant. Use a new deployment for another pet, applicant, or need set.

Constructor data establishes the deployment subject and fixed role boundary. Later writes add only the bounded records permitted by the lifecycle; a completed instance cannot be reopened.

## Participants

The deployer is the shelter and names one different applicant. The shelter defines needs and shortlists or declines; the applicant submits the home profile and confirms or withdraws.

Addresses are normalized before authorization comparisons. Role checks and lifecycle gates execute before semantic assessment.

## State machine

`SETTING_NEEDS → APPLICANT_INPUT → READY_TO_MATCH → SHELTER_RESPONSE → APPLICANT_CONFIRMATION → PLACEMENT_RECORD → COMPLETE`

The phase-like field is the primary lifecycle lock. Each write advances that path, performs a documented bounded loop, or fails with an `[EXPECTED]` user error.

## Evidence assembly

The stored pet profile, public matching rule, ordered needs, and applicant-declared home summary, routine, constraints, and optional clarification. No background check or external record is fetched.

Before consensus, the contract normalizes bounded text, copies required storage into plain local values, serializes a sorted JSON packet, and places it between explicit START/END delimiters. Nondeterministic callbacks do not read contract storage.

## Consensus boundary

Return a need mask and MATCH, REVIEW, or NO_MATCH based only on the applicant's public care declarations.

The leader callback validates exact JSON shape, field types, closed labels, masks or codes, and length bounds. A validator reruns the same semantic operation and rejects disagreement before state is committed.

## Deterministic boundary

Need setup, designated-applicant authorization, one clarification, shelter shortlist decision, applicant confirmation, and placement record are deterministic.

Important invariants:

- Pet needs freeze before the applicant submits a home profile.
- Only the named applicant can submit, clarify, confirm, or withdraw.
- The shelter and applicant make separate decisions after the AI assessment.
- AI cannot infer protected or private traits or make a placement decision.

No method sends value, pays rewards, escrows assets, deletes external data, calls another contract, or invokes a webhook.

## Failure model

- Invalid caller input or lifecycle use raises `[EXPECTED]` and leaves state unchanged.
- Malformed or out-of-policy model output raises `[LLM_ERROR]` and cannot be stored.
- Validator disagreement cannot commit the semantic result.
- StudioNet proof reads explicitly target `LATEST_FINAL`, avoiding stale pre-final state.
