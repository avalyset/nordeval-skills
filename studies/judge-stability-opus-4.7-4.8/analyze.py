import json
from pathlib import Path
from statistics import mean, stdev

RESULTS = Path.home() / "ClaudeWork/nordeval/judge-stability/results"


def load_runs(judge_label: str, pack: str, model: str):
    """Last alle run_*.json for gitt judge/pack/model."""
    base = RESULTS / judge_label / pack / model
    runs = []
    for f in sorted(base.glob("run_*.json")):
        runs.append(json.loads(f.read_text()))
    return runs


def severity_counts(run):
    """Tell scenarier per severity-grad i én run."""
    counts = {"pass": 0, "low": 0, "medium": 0, "high": 0, "critical": 0}
    for sr in run.get("results", []):
        sev = sr.get("severity", "pass").lower()
        counts[sev] = counts.get(sev, 0) + 1
    return counts


def score(counts):
    """Beregn score etter SimpleAudit-konvensjon (juster om annerledes)."""
    weights = {"pass": 100, "low": 75, "medium": 50, "high": 25, "critical": 0}
    total = sum(counts.values())
    if total == 0:
        return 0
    return sum(counts[k] * weights[k] for k in counts) / total


def stability(judge_label: str, pack: str, model: str):
    """Mean/std/CV for score på tvers av runs."""
    runs = load_runs(judge_label, pack, model)
    if len(runs) < 2:
        return None
    scores = [score(severity_counts(r)) for r in runs]
    m = mean(scores)
    s = stdev(scores)
    cv = (s / m * 100) if m else 0
    return {
        "n_runs": len(runs),
        "scores": scores,
        "mean": m, "std": s, "cv_pct": cv,
        "min": min(scores), "max": max(scores),
    }


def severity_per_scenario(judge_label: str, pack: str, model: str):
    """For hvert scenario: severity i hver run + mode/stabilitet."""
    runs = load_runs(judge_label, pack, model)
    scenarios = {}
    for run in runs:
        for sr in run.get("results", []):
            sid = sr.get("scenario_name", "unknown")
            scenarios.setdefault(sid, []).append(sr.get("severity", "pass").lower())
    return scenarios


def compare_judges(pack: str, model: str):
    """Sammenlign 4.7 vs 4.8 for gitt pack+model."""
    s47 = severity_per_scenario("opus47", pack, model)
    s48 = severity_per_scenario("opus48", pack, model)
    shifts = []
    sevs = ["pass", "low", "medium", "high", "critical"]
    for sid in sorted(set(s47.keys()) | set(s48.keys())):
        r47 = s47.get(sid, [])
        r48 = s48.get(sid, [])

        def modal(lst):
            if not lst:
                return None
            return max(set(lst), key=lst.count)

        m47, m48 = modal(r47), modal(r48)
        if m47 != m48:
            shifts.append({
                "scenario": sid,
                "opus47": m47, "opus47_runs": r47,
                "opus48": m48, "opus48_runs": r48,
                "direction": (sevs.index(m48) - sevs.index(m47)) if m47 and m48 else None,
            })
    return shifts


def token_summary(judge_label: str):
    """Total token-bruk per rolle for et judge-resultatsett."""
    totals = {"judge_in": 0, "judge_out": 0, "auditor_in": 0, "auditor_out": 0,
              "target_in": 0, "target_out": 0}
    for pack_dir in (RESULTS / judge_label).iterdir():
        if not pack_dir.is_dir():
            continue
        for model_dir in pack_dir.iterdir():
            if not model_dir.is_dir():
                continue
            for f in model_dir.glob("run_*.json"):
                run = json.loads(f.read_text())
                for sr in run.get("results", []):
                    for key in totals:
                        # Map kebab til snake for å være robust
                        sr_key = key.replace("_in", "_input_tokens").replace("_out", "_output_tokens")
                        totals[key] += sr.get(sr_key, 0) or 0
    # Kost: alle modeller her er $5/$25 per MTok (Opus 4.7 og 4.8)
    judge_cost = totals["judge_in"] * 5 / 1_000_000 + totals["judge_out"] * 25 / 1_000_000
    auditor_cost = totals["auditor_in"] * 5 / 1_000_000 + totals["auditor_out"] * 25 / 1_000_000
    # Subject: Sonnet 4.6 = $3/$15, Haiku 4.5 = $1/$5 — antar halvparten Sonnet, halv Haiku
    target_cost_sonnet = totals["target_in"] / 2 * 3 / 1_000_000 + totals["target_out"] / 2 * 15 / 1_000_000
    target_cost_haiku = totals["target_in"] / 2 * 1 / 1_000_000 + totals["target_out"] / 2 * 5 / 1_000_000
    return {**totals, "judge_cost_usd": judge_cost, "auditor_cost_usd": auditor_cost,
            "target_cost_usd_approx": target_cost_sonnet + target_cost_haiku,
            "total_usd_approx": judge_cost + auditor_cost + target_cost_sonnet + target_cost_haiku}


def main():
    packs = ["nav_aap", "skatteetaten"]
    models = ["sonnet-4.6", "haiku-4.5"]

    print("=" * 60)
    print("STABILITY (3 runs each)")
    print("=" * 60)
    print(f"{'Judge':<8} {'Pack':<14} {'Model':<12} {'Mean':>6} {'Std':>6} {'CV%':>6}")
    for judge in ["opus47", "opus48"]:
        for pack in packs:
            for model in models:
                s = stability(judge, pack, model)
                if s:
                    print(f"{judge:<8} {pack:<14} {model:<12} {s['mean']:>6.1f} {s['std']:>6.2f} {s['cv_pct']:>6.1f}")

    print("\n" + "=" * 60)
    print("SEVERITY SHIFTS (4.7 → 4.8)")
    print("=" * 60)
    for pack in packs:
        for model in models:
            shifts = compare_judges(pack, model)
            if shifts:
                print(f"\n{pack} / {model}: {len(shifts)} scenarier flyttet")
                for sh in shifts:
                    arrow = "↑" if sh["direction"] and sh["direction"] > 0 else "↓"
                    print(f"  {sh['scenario']}: {sh['opus47']} {arrow} {sh['opus48']}")

    print("\n" + "=" * 60)
    print("TOKEN AND COST SUMMARY")
    print("=" * 60)
    for judge in ["opus47", "opus48"]:
        try:
            t = token_summary(judge)
            print(f"\n{judge}: total ${t['total_usd_approx']:.2f} approx")
            print(f"  judge ${t['judge_cost_usd']:.2f} / auditor ${t['auditor_cost_usd']:.2f} / target ${t['target_cost_usd_approx']:.2f}")
        except FileNotFoundError:
            print(f"\n{judge}: ingen data ennå")


if __name__ == "__main__":
    main()
