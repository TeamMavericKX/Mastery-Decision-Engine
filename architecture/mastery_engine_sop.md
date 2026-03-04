# SOP: Mastery Engine — Standard Operating Procedure
## Layer 1: Architecture | Updated: 2026-03-04

---

## 1. Purpose
Determine whether a learner should PROGRESS, RETRY, or PIVOT based on a sequence of test scores evaluated through the `MasteryEvaluator` class.

## 2. Input
A list of scores (integers 0–100) representing successive test attempts for a single topic.

## 3. Processing Steps

```
Step 1: Instantiate MasteryEvaluator()
Step 2: For each score in sequence:
    a. Call evaluator.evaluate(score)
    b. Validate score (0-100, numeric) → DATA_ERROR if invalid
    c. Append score to history, increment attempts
    d. Compute Sᵥ:
       - If len(history) == 1 → Sᵥ = history[0]
       - If len(history) > 1  → Sᵥ = (history[-1] × 0.7) + (history[-2] × 0.3)
    e. Apply Decision Matrix:
       - IF Sᵥ >= 85           → STATUS: PROGRESS
       - ELIF attempts >= 3    → STATUS: PIVOT
       - ELSE                  → STATUS: RETRY
Step 3: Return final status for that archetype
```

## 4. Edge Cases

| Edge Case | Behavior |
|---|---|
| Score = 100, single attempt | Sᵥ = 100 → PROGRESS |
| Scores drop sharply (e.g., 90 → 40) | Sᵥ = 55 → RETRY (regression captured) |
| Scores plateau below 85 for 3 attempts | Circuit breaker → PIVOT |
| Empty score list | → DATA_ERROR |
| Non-numeric value in list | → DATA_ERROR |

## 5. Golden Rules
- **PROGRESS check is always first.** Circuit breaker does NOT block genuine mastery.
- **Logic changes here first**, then propagate to `tools/mastery_engine.py`.

## 6. Change Log

| Date | Change |
|---|---|
| 2026-03-04 | Initial SOP created |
