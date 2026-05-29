# nordeval-skills

Agent Skills for Norwegian public-sector domains, designed for use with Claude (Claude Code, Claude.ai, Claude API) and compatible Agent Skills implementations.

These skills are companion artifacts to the [nordeval evaluation suite](https://github.com/avalyset/simpleaudit) — domain packs for `kelkalot/simpleaudit`. The eval suite measures factual accuracy and safety behavior; these skills aim to prevent the failure modes the eval suite identifies.

## Available skills

- **nav-aap** — Norwegian work assessment allowance (Arbeidsavklaringspenger), folketrygdloven kap. 11
- **skatteetaten** — Norwegian tax administration domain (personal tax, VAT thresholds, appeals)

## Methodology

Each skill is grounded in primary sources (lovdata.no, nav.no, skatteetaten.no, Stortingets skattevedtak). Facts carry date stamps. Failure modes documented in the companion eval suite are explicitly addressed in skill instructions.

## Studies

- **[Judge Stability: Opus 4.7 → 4.8 on Norwegian Public-Sector Evals](studies/judge-stability-opus-4.7-4.8/)** (2026-05-29) — Live-API validation of SimpleAudit PR #20 repeated-run infrastructure and cross-version judge stability on nav_aap and skatteetaten packs. Headline finding: a HIGH-severity Klagefrist scenario under Opus 4.7 collapses to LOW under Opus 4.8 when judging the same Haiku 4.5 outputs. Archived version: https://doi.org/10.17605/OSF.IO/VZ8XJ

## License

Apache License 2.0. Copyright 2026 EcoDeco AS.

## Status

Companion to merged upstream contributions in kelkalot/simpleaudit:
nav_aap (PR #17, merged 2026-05-08) and skatteetaten (PR #18, merged
2026-05-11). These skills encode the same domain research used to build
those evaluation packs.
