# PRD: AI-Powered Pull Request Generator & Reviewer

Project overview and detailed product requirements originally provided by the user.

Summary
-------
Developers waste time writing PR titles/descriptions, and reviewers perform repetitive tasks. This tool will automate PR title/description generation, AI code review, and test validation with integration into GitHub/GitLab/Bitbucket.

Key features and MVP scope
-------------------------
- Auto PR Title & Description generation
- AI code review for logic issues, edge cases, code smells
- Test & CI summary (parse CI output)
- Integrations: GitHub App, CLI, (VS Code extension later)
- MVP (2-3 weeks): title generation, description generation, basic reviewer summary, GitHub Action integration, CLI tool

Architecture
------------
See PRD in the original spec for a diagram and tech stack recommendations (FastAPI or Express; LLMs such as OpenAI/GPT/Claude; embeddings for understanding diffs; AST parsers for language-specific analysis).

Success metrics
---------------
- Time saved per PR
- Adoption across repos
- Reduction in review time
- Developer satisfaction
