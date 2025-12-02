# Providers & Configuration

This document explains how to configure AutoPR to use real LLM providers.

Environment variables
- AUTOPR_PROVIDER — one of `openai`, `anthropic`, `stub` (default: `stub`)
- OPENAI_API_KEY — API key for OpenAI (if using openai)
- OPENAI_MODEL — optional model (defaults to `gpt-4o`)
- ANTHROPIC_API_KEY — API key for Anthropic
- ANTHROPIC_MODEL — optional model (defaults to `claude-2`)

Security
- Never commit secrets into version control. Use repository secrets for CI.
- Use network-mocking in tests to avoid requiring real keys.

Behavior
- The LLM selection is performed at import time in `autopr.llm` using the value of AUTOPR_PROVIDER. If the selected provider is misconfigured or the client library is not available, AutoPR falls back to the `stub` provider so the application remains usable in offline environments.
