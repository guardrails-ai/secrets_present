## Overview

| Developed by | Guardrails AI |
| --- | --- |
| Date of development | Feb 15th, 2024 |
| Validator type | Safety |
| Blog | - |
| License | Apache 2 |
| Input/Output | Input, Output |

## Description

This validator monitors any text (input or output) and detects secrets present in the text. Under-the-hood, the validator uses the `detect-secrets` library to check whether the text contains any secrets. If any secrets are detected, the validator fails and returns the text with the secrets replaced with asterisks. Otherwise, the validator returns the generated code snippet.

## Installation

```bash
$ gudardrails hub install hub://guardrails/detect_secrets
```

## Usage Examples



### Initialization

```python
from guardrails.hub import DetectSecrets

detect_secrets_guardrail = DetectSecrets(
    on_fail="fix"
)
```

### Invocation

```python
guard = Guard.from_string(validators=[detect_secrets_guardrail])
```

## Intended use

- Primary intended uses: Detecting
- Out-of-scope use cases:

## API Ref

- `value` - The generated code snippet

## Expected deployment metrics

|  | CPU | GPU |
| --- | --- | --- |
| Latency |  | - |
| Memory |  | - |
| Cost |  | - |
| Expected quality |  | - |

## Resources required

- Dependencies: `detect-secrets`
- Foundation model access keys: N/A
- Compute: N/A

## Validator Performance

### Evaluation Dataset

N/A

### Model Performance Measures

N/A

### Decision thresholds

N/A
