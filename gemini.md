# gemini.md — Project Constitution
## Project: Mastery Reinforcement & Retry Decision Engine
**Status:** SPEC LOCKED v3 | **Updated:** 2026-03-04

---

## I. Core Class

```
MasteryEvaluator
  ├── attempts: int   (increments on each evaluate() call)
  └── history: list   (appends each score in order)
```

---

## II. Weighted Mastery Score (Sᵥ)

| Condition | Formula |
|---|---|
| `len(history) == 1` | `Sᵥ = history[0]` |
| `len(history) > 1` | `Sᵥ = (history[-1] × 0.7) + (history[-2] × 0.3)` |

---

## III. Decision Matrix (checked in order)

| Priority | Condition | Status |
|---|---|---|
| 1 | `Sᵥ >= 85` | `PROGRESS` |
| 2 | `attempts >= 3` | `PIVOT` |
| 3 | else | `RETRY` |

**Note:** PROGRESS check precedes circuit breaker — genuine mastery at attempt ≥ 3 is still honoured.

---

## IV. Simulation Scenarios

| Archetype | Scores | Expected |
|---|---|---|
| Sudden Drop | [90, 40] | `RETRY` |
| Steady Climb | [60, 75, 86] | `PIVOT`* |
| Stagnant | [70, 72, 71] | `PIVOT` |

> *Mathematical note: Sᵥ([60,75,86]) = 86×0.7 + 75×0.3 = **82.7** < 85.
> Circuit breaker fires at attempt 3. Output: `PIVOT`.

---

## V. Data Schema

### Input (per evaluate() call)
```json
{ "score": 0-100 }
```

### Output
```json
{
  "status": "PROGRESS | PIVOT | RETRY | DATA_ERROR",
  "weighted_score": 0.0,
  "attempts": 1,
  "history": [...],
  "reason": "string"
}
```

---

## VI. Behavioral Invariants

1. Decision matrix is checked **in order** — PROGRESS first, PIVOT second, RETRY last.
2. Invalid scores (non-numeric, out of range) → `DATA_ERROR` immediately.
3. Output tone: UPPERCASE, clinical (e.g., `STATUS: PIVOT`).
4. All business logic in `tools/mastery_engine.py` only.
5. **[PERMANENT INVARIANT]** Weighted Score formula: `Sᵥ = (current × 0.7) + (previous × 0.3)`. The 70/30 split is a deliberate architectural decision — it prioritizes recency (70% weight to the latest attempt) while holding trajectory context (30% from prior attempt). This weighting is **not negotiable** and must never be changed without explicit architectural review. It is the mathematical basis for why `[60, 75, 86]` yields Sᵥ=82.7 and correctly fires PIVOT rather than PROGRESS.
6. **[PERMANENT INVARIANT]** MASTERY_THRESHOLD = 85. The Gatekeeper operates at 85, not 80. An 80-point gate conflates "improving" with "masterful". The 85 gate ensures learners who merely trend upward do not bypass foundational review.

---

## VII. Maintenance Log

| Date | Change | Author |
|---|---|---|
| 2026-03-04 | v1 — Initial constitution | System Pilot |
| 2026-03-04 | v2 — Refined spec applied (MasteryEvaluator class, threshold=85, 3 scenarios) | System Pilot |
| 2026-03-04 | v3 — Phase 5 Trigger complete. 70/30 weighting logic archived as permanent architectural invariant (VI.5). Threshold=85 confirmed as permanent by user (VI.6). Docker execution validated. | System Pilot |
