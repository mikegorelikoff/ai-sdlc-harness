---
title: Research source register
description: Primary authoritative sources and the claims they validate; repository conventions remain labeled separately.
---

# Research source register

| Source | Claim supported |
| --- | --- |
| [ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html) | A software life cycle is a framework of processes spanning conception, development, operation, support, maintenance, and retirement; the standard does not mandate one methodology |
| [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | Requirements engineering is iterative across the life cycle and produces managed requirements information items |
| [NIST Secure Software Development Framework, SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | Secure practices across the SDLC, third-party component controls, vulnerability response |
| [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | Governance, mapping, measurement, management, human/organizational responsibility |
| [NIST AI 600-1 Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | Confabulation, statistical-generation risk, measurement/monitoring/human oversight |
| [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | Direct/indirect injection, untrusted content separation, disclosure/action risk |
| [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) | Least functionality/permission/autonomy and protected human approval for high-impact actions |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | Testable application-security verification requirements |
| [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Accessibility criteria need automated and human evaluation |
| [GitHub secure use of Actions](https://docs.github.com/en/actions/reference/security/secure-use) | Full commit SHA is the immutable action reference |
| [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches) | Required status checks/reviews are platform-enforced controls |
| [GitHub licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) | Default copyright applies without an explicit license |
| [GitHub immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases) | Release tag/assets and attestation integrity controls |
| [pip secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/) | Fully pinned transitive dependencies and hash checking for secure installs |
| [npm npx](https://docs.npmjs.com/cli/v7/commands/npx/) | Missing packages can be acquired/executed through npm cache, creating a bootstrap boundary |
| [Git documentation](https://git-scm.com/docs) | Branch, diff, status, remote, commit, and tag command semantics |
| [Python downloads/documentation](https://www.python.org/downloads/) | Official runtime acquisition and supported interpreter source |
| [Node.js downloads](https://nodejs.org/en/download) | Official runtime acquisition |
| [OpenAI Codex CLI](https://learn.chatgpt.com/docs/codex/cli) | Official Codex CLI installation, invocation, and update route used by the host setup guide |
| [OpenAI authentication](https://learn.chatgpt.com/docs/auth.md) | Official sign-in and API-key authentication choices and credential boundary |
| [CISA Secure by Design](https://www.cisa.gov/securebydesign) | Security ownership and secure defaults belong in product design and organizational practice, not only downstream testing |

These sources validate industry or vendor claims. The 18-stage refinement
order, folder names, TOON schemas, PM/PO convention, skill precedence, and
quick/full modes are repository conventions, not formal standards. The support
matrix and rollout guidance are recommendations bounded by recorded evidence.
