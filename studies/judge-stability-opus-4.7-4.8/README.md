# Judge Stability: Opus 4.7 → 4.8 on Norwegian Public-Sector Evals

Live-API validation of SimpleAudit PR #20 (repeated-run infrastructure) and
cross-version judge stability study on nav_aap and skatteetaten packs.

- **Publication:** [PUBLICATION.md](PUBLICATION.md)
- **Correction (2026-06-11):** [ADDENDUM_2026-06-11_klagefrist-correction.md](ADDENDUM_2026-06-11_klagefrist-correction.md) — corrects the Klagefrist headline (conversation drift, not judge-grading drift). Controlled re-grade raw data in `results/temp-version-factorial/`.
- **DOI / archived version:** https://doi.org/10.17605/OSF.IO/VZ8XJ
- **Reproduction script:** [analyze.py](analyze.py)
- **Raw data:** `results/opus47/` and `results/opus48/`
- **N=5 extension data:** `results/opus47/skatteetaten/haiku-4.5/run_3.json`, `run_4.json`, same for opus48. Run details in `results/n5_extension_summary.json`.
- **Run logs:** `logs/`

Date: 2026-05-29. Author: Eirik Botten Nicolaysen, EcoDeco AS.
