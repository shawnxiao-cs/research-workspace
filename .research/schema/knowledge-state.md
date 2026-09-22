# Knowledge State v0.1

A knowledge state is a vector, not a single score.

| Dimension | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| awareness | unknown | exposed | understood | proficient | research-ready |
| conceptual | unknown | exposed | understood | proficient | research-ready |
| mathematical | unknown | exposed | understood | proficient | research-ready |
| implementation | unknown | followed | modified | independently implemented | research-ready implementation |
| application | unknown | observed | guided use | independent use | research-ready application |
| research | unknown | observed | guided analysis | independent analysis | research-ready |

Learned does not imply implemented. A researcher may legitimately have `conceptual: 2` and `implementation: 0` for Transformer.

```yaml
Transformer:
  conceptual: 2
  implementation: 0
```

Keep self-assessment and verified evidence distinguishable. Never call level 4 "expert"; it means research-ready for that dimension.

## Canonical profile location

`templates/researcher-profile.yaml` is the public template. The live researcher profile is a YAML configuration object at `.research/config/researcher-profile.yaml`.
Because it may contain personal research and learning information, the live profile is ignored by default.
Users may intentionally remove `.research/config/researcher-profile.yaml` from `.gitignore` if they explicitly want to version-control their profile.
Unknown dimensions may remain `null`; do not silently convert them to `0`.
