# nordeval-skills

Agent Skills for Norwegian public-sector domains, designed for use with Claude (Claude Code, Claude.ai, Claude API) and compatible Agent Skills implementations.

These skills are companion artifacts to the [nordeval evaluation suite](https://github.com/avalyset/simpleaudit) — domain packs for `kelkalot/simpleaudit`. The eval suite measures factual accuracy and safety behavior; these skills aim to prevent the failure modes the eval suite identifies.

## Available skills

- **nav-aap** — Norwegian work assessment allowance (Arbeidsavklaringspenger), folketrygdloven kap. 11
- **skatteetaten** — Norwegian tax administration domain (personal tax, VAT thresholds, appeals)

## Methodology

Each skill is grounded in primary sources (lovdata.no, nav.no, skatteetaten.no, Stortingets skattevedtak). Facts carry date stamps. Failure modes documented in the companion eval suite are explicitly addressed in skill instructions.

## License

Apache License 2.0. Copyright 2026 EcoDeco AS.

## Status

Companion to merged upstream contributions in kelkalot/simpleaudit:
nav_aap (PR #17, merged 2026-05-08) and skatteetaten (PR #18, merged
2026-05-11). These skills encode the same domain research used to build
those evaluation packs.
