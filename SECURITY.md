# Security

## Scope

This repository contains one bounded Intelligent Contract, direct tests, a five-validator GLSim test, and an opt-in StudioNet smoke test. It has no frontend, backend, database, token, payout, proxy upgrade, or repository secret.

## Trust model

Untrusted evidence is delimited as data, model outputs use closed schemas, and validator replay must agree before semantic state is stored.

The deployer is the shelter and names one different applicant. The shelter defines needs and shortlists or declines; the applicant submits the home profile and confirms or withdraws.

## Implemented controls

- Concrete immutable GenVM runner hash; no floating runner dependency.
- Address normalization, explicit role separation, collection caps, one-time actions, and lifecycle locks.
- Bounded text plus strict `[EXPECTED]` and `[LLM_ERROR]` failure classes.
- Sorted, delimited evidence packets and independent validator replay.
- Storage is copied before nondeterministic callbacks; static audit requires zero callback reads from `self`.
- No cross-contract calls, fund custody, transfer, automated purchase, external deletion, or webhook.
- `.env`, caches, artifacts, wallet files, and local secrets are ignored. Live wallets are encrypted outside the workspace.

## Contract-specific safety properties

- Pet needs freeze before the applicant submits a home profile.
- Only the named applicant can submit, clarify, confirm, or withdraw.
- The shelter and applicant make separate decisions after the AI assessment.
- AI cannot infer protected or private traits or make a placement decision.

## Residual risks

- Applicant and shelter statements are declarations and are not externally verified.
- The contract is not a background check, veterinary assessment, legal adoption record, or home inspection.
- A MATCH label only means the declared plan covers the frozen public needs.

Do not use this contract to make legal, medical, financial, employment, admission, credit, or physical-safety decisions beyond the explicit low-risk policy in its source. A new use case requires a fresh deployment and independent domain review.

## Reporting

Report vulnerabilities privately to the repository owner with the contract name, affected method, reproduction, expected invariant, and impact. Never include private keys, wallet passwords, or personal data.
