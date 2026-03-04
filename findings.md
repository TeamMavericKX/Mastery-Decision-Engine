# findings.md — Research & Discoveries
## Project: Mastery Reinforcement & Retry Decision Engine
**Updated:** 2026-03-04

---

## Constraints Confirmed
- 100% offline — no external API calls
- Python 3 standard library only (no pip installs required)
- Docker for containerization and execution
- CLI output only (no GUI/web)

## Key Design Discoveries

### Weighted Average Logic
- **Why 70/30?** The 70% weight on the most recent score is intentional: it rewards genuine improvement while being skeptical of historical failure. A learner who scored 30, 35 then suddenly 80 should NOT pass after 3 attempts (Hard Stop overrides).
- **Edge Case:** With only 1 score, use it directly — no weighted calc possible.

### The False Positive Problem
- The "Lucky Guesser" archetype is the critical risk. A learner scoring [30, 35, 80] has a weighted avg of `80*0.7 + 35*0.3 = 56 + 10.5 = 66.5`. This WOULD normally push to RETRY zone, but since attempt_number=3, Hard Stop triggers PIVOT. This is safe.
- If the sequence were [60, 70, 80] at attempt 3, weighted avg = `80*0.7 + 70*0.3 = 56 + 21 = 77`. This is RETRY zone → Hard Stop → PIVOT. The skeptic rule holds.
- Mastery (>= 80 weighted avg) at attempt 3 is still PROGRESS — the gate wasn't compromised, the learner genuinely earned it.

### Docker Strategy
- Single-stage build using `python:3.11-slim` base image — minimal footprint
- Entry point runs `mastery_engine.py` which simulates all archetypes
- No volumes or bind mounts needed — all data is generated programmatically

## Pending Research
- [ ] Validate Python 3.11-slim availability on user machine (will check during Link phase)
