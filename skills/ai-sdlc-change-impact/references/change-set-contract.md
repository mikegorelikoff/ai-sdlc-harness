# Change Set Contract

The input is a UTF-8 JSON object using schema `ai-sdlc-change-set/v1` with a
non-empty `changes` array. Every change requires:

- unique `id`, such as `CHG-001`;
- stable `changed_ref`, such as `AC-004` or `DEC-012`;
- `source.path`, relative to the feature root without `..` traversal;
- positive integer `source.line` containing the exact changed reference;
- non-empty `source.detail` describing what changed.

Example:

```json
{
  "schema": "ai-sdlc-change-set/v1",
  "changes": [
    {
      "id": "CHG-001",
      "changed_ref": "AC-004",
      "source": {
        "path": "requirements.md",
        "line": 121,
        "detail": "Retry behavior is now mandatory."
      }
    }
  ]
}
```
