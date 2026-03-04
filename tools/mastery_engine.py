from typing import Optional

MASTERY_THRESHOLD = 85
CIRCUIT_BREAKER   = 3


class MasteryEvaluator:
    """
    Tracks a learner's attempt history for a single topic.
    Feeds scores one at a time and returns a deterministic verdict.
    """

    def __init__(self) -> None:
        self.attempts: int        = 0
        self.history:  list[float] = []

    def _compute_weighted_score(self) -> float:
        if len(self.history) == 1:
            return self.history[0]
        current  = self.history[-1]
        previous = self.history[-2]
        return round((current * 0.7) + (previous * 0.3), 2)

    def evaluate(self, score) -> dict:
        if not isinstance(score, (int, float)) or not (0 <= score <= 100):
            return {
                "status":         "DATA_ERROR",
                "weighted_score": None,
                "attempts":       self.attempts,
                "history":        list(self.history),
                "reason":         f"Invalid score: '{score}'. Must be a number in [0, 100].",
            }

        self.history.append(float(score))
        self.attempts += 1

        sw = self._compute_weighted_score()

        if sw >= MASTERY_THRESHOLD:
            status = "PROGRESS"
            reason = f"Sᵥ ({sw}) ≥ {MASTERY_THRESHOLD}. Mastery achieved."
        elif self.attempts >= CIRCUIT_BREAKER:
            status = "PIVOT"
            reason = (f"Circuit breaker triggered after {self.attempts} attempts. "
                      "Suggest foundational review.")
        else:
            status = "RETRY"
            reason = (f"Sᵥ ({sw}) < {MASTERY_THRESHOLD}. "
                      "Insufficient mastery; re-test required.")

        return {
            "status":         status,
            "weighted_score": sw,
            "attempts":       self.attempts,
            "history":        list(self.history),
            "reason":         reason,
        }

    def reset(self) -> None:
        self.attempts = 0
        self.history  = []


SCENARIOS: dict[str, list] = {
    "Sudden Drop":  [90, 40],
    "Steady Climb": [60, 75, 86],
    "Stagnant":     [70, 72, 71],
}


def run_simulation() -> None:
    """
    Iterates through each scenario, feeds scores one-by-one into a fresh
    MasteryEvaluator, and reports the final decision.
    """
    col_w   = [18, 22, 8, 22]
    total_w = sum(col_w) + len(col_w) * 3 + 1

    banner = " MASTERY DECISION ENGINE — GATEKEEPER v1.0 "
    print("=" * total_w)
    print(banner.center(total_w))
    print(f"  Threshold: PROGRESS ≥ {MASTERY_THRESHOLD} | PIVOT: attempts ≥ {CIRCUIT_BREAKER} | else: RETRY")
    print("=" * total_w)

    header = (
        f"{'ARCHETYPE':<{col_w[0]}} | "
        f"{'SCORE SEQUENCE':<{col_w[1]}} | "
        f"{'Sᵥ':>{col_w[2]}} | "
        f"{'FINAL DECISION':<{col_w[3]}}"
    )
    print(header)
    print("-" * total_w)

    for name, scores in SCENARIOS.items():
        evaluator = MasteryEvaluator()
        result    = None

        for score in scores:
            result = evaluator.evaluate(score)

        if result is None:
            print(f"  {name:<{col_w[0]-2}} | {'[]':<{col_w[1]}} | {'':{col_w[2]}} | DATA_ERROR")
            continue

        seq_str = str(scores)
        sw_str  = (f"{result['weighted_score']:.1f}"
                   if result["weighted_score"] is not None else "N/A")
        status  = f"STATUS: {result['status']}"

        print(
            f"  {name:<{col_w[0]-2}} | "
            f"{seq_str:<{col_w[1]}} | "
            f"{sw_str:>{col_w[2]}} | "
            f"{status:<{col_w[3]}}"
        )
        print(f"  {'':{col_w[0]-2}}   {'REASON':>{col_w[1]}} : {result['reason']}")
        print()

    print("=" * total_w)
    print()
    print("  ⚑  INTEGRITY NOTE")
    print("  " + "─" * 53)
    print("  'Steady Climb' [60, 75, 86] → Sᵥ = 86×0.7 + 75×0.3 = 82.7")
    print(f"  82.7 < {MASTERY_THRESHOLD} (PROGRESS gate) and attempts = 3 ≥ {CIRCUIT_BREAKER}.")
    print("  Circuit breaker fires → STATUS: PIVOT.")
    print("  To achieve PROGRESS at attempt 3, the 3rd score must be ≥ 90 given prev=75.")
    print("  Formula: current ≥ (85 − 75×0.3) / 0.7 ≈ 89.3")
    print()


if __name__ == "__main__":
    run_simulation()
