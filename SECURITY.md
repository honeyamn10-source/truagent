# Security Policy

## Reporting a vulnerability

Please **do not** open a public issue for security vulnerabilities. Instead,
email the maintainers privately. We will respond within 3 business days.

## Scope

TruAgent is a zero-dependency framework. Because it has no runtime
dependencies, its attack surface is small and fully auditable. Still, please
report:

- Remote code execution vectors (e.g. unsafe `eval`/`exec` usage in examples).
- Prompt-injection patterns that could exfiltrate data.
- Secrets accidentally shipped in the repository.
- Any dependency/transitive-supply-chain concern.

## Safe usage notes

- Never put real API keys in code or committed files. Use environment
  variables or a secrets manager.
- The `calculator_agent.py` example sanitizes its input before `eval`. Do
  not bypass that guard.
- Review tools before wiring them to an agent that can call them
  automatically — an agent is only as safe as its most privileged tool.