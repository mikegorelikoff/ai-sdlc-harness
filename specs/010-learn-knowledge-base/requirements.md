---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "010-learn-knowledge-base"
  artifact: "requirements.md"
  path: "specs/010-learn-knowledge-base/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/010-learn-knowledge-base/_ai_sdlc/state.toon"
  decision_log: "specs/010-learn-knowledge-base/decision-log.md"
  status: "review"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "DEC-001"
    - "DEC-003"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
  related_artifacts:
    - "specs/010-learn-knowledge-base/decision-log.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
    - "learn-curriculum"
---

# Requirements

## Goal
Create an original, bottom-up Learn curriculum that takes complete beginners from generative-AI foundations to safe independent use of the AI SDLC Harness in a real repository, while preserving canonical operational documentation.

## Problem Statement
The current site has strong operational and foundational pages, but its visible Start journey assumes too much prior knowledge, distributes the teaching sequence across documentation types, and lacks deterministic curriculum-depth and provenance controls. Learners need a coherent prerequisite order, exercises with evidence, source adaptation records, and explicit human-authority boundaries.

## Scope
Replace the visible Start navigation label with Learn while retaining docs/start.md and its public URL. Add nine substantial Learn chapters plus the hub. Integrate existing canonical pages through links. Add source and curriculum governance, a verified source registry, token and structure validators, source validation, tests, dependency pins, home and README entry points, independent multi-role review evidence, and regression validation.

## Actors
Complete beginners; chat-interface users; product managers and product owners; business analysts; QA practitioners; developers; technical leads; architects; security and governance reviewers; delivery leaders; Heads of AI Practice; documentation maintainers; harness maintainers.

## Inputs
The user curriculum mission; current repository documentation, skills, scripts, tests, navigation, installation behavior, and governance contracts; verified authoritative external research used only for topic validation and teaching patterns.

## Outputs
A ten-page Learn journey; six-section navigation; original exercises and answer explanations; source provenance data; maintainer governance; deterministic Learn token, structure, source, navigation, link, and build validation; review findings and corrections.

## Functional Requirements
FR-001: Learn contains the hub and nine ordered chapters from AI foundations through role paths. FR-002: Every Learn page implements the learner contract and observable Can explain, Can do, Can prove outcomes. FR-003: Each page has original harness examples, bounded practice, permissions, recovery, evidence, knowledge checks, previous and next links, and visible adaptation notes. FR-004: The hub supports beginner, experienced-AI, installed-harness, and role fast lanes without granting approval authority. FR-005: Canonical skill, command, role, glossary, Evidence Council, Quality Lenses, installation, adoption, and execution contracts remain owned by existing pages. FR-006: Source records are verified, pinned where applicable, classified, and mapped to page declarations. FR-007: Independent read-only reviewers receive the same bounded diff, use the required schema, and preserve disagreement without majority voting.

## Non-Functional Requirements
NFR-001: Every Learn page measures 6000 through 8000 inclusive o200k_base tokens after exact normalization. NFR-002: Long pages remain accessible and navigable through descriptive headings, visible contents, short paragraphs, nearby examples, collapsible detail, usable tables, and meaningful links. NFR-003: Content is original synthesis without padding, structural cloning, copied examples, or duplicated canonical contracts. NFR-004: Validation is deterministic, integrated with existing documentation validation, and tested at exact boundaries. NFR-005: Existing public URLs, unrelated work, existing tests, and canonical ownership remain intact.

## Constraints
Exactly six top-level navigation sections: Home, Learn, Reference, Use, Adopt, About. Reference remains in the first three. No page appears twice in navigation. docs/start.md stays at its path. Learn pages measure 6000 to 8000 tokens. No external text, diagrams, quizzes, or structures are copied one-to-one. No commit is authorized. Generated site output remains untracked.

## Acceptance Criteria
AC-001: Navigation has the six required sections in order, Learn replaces Start, Reference is third, no page is duplicated, and existing paths remain valid. AC-002: The hub and nine chapters each measure 6000 to 8000 tokens and pass metadata, section, order, link, heading, and accessibility checks. AC-003: The curriculum covers the twelve-step journey, required concepts and roles, original examples, exercises, answers, recovery, and observable evidence without padding. AC-004: Existing operational reference remains canonical; Learn summarizes, demonstrates, and links. AC-005: Source registry and policies record verified sources, pins, reuse classes, transformations, exclusions, destinations, freshness, and attribution; page declarations match visible notes. AC-006: Token, structure, and source validators integrate with validate_docs.py, dependencies are pinned, and requested boundary and failure tests pass. AC-007: README and Home direct beginners to Learn while preserving experienced fast routes and reciprocal canonical links. AC-008: Nine independent read-only roles inspect the same diff, report evidence in schema, accepted corrections are applied, and four required roles recheck. AC-009: Catalog, docs validation, token report, tests, strict build, rendered validation, compatibility, and supported installation smoke pass. AC-010: No unrelated changes, generated site commit, discarded work, or commit.

## Out of Scope
Changing runtime behavior, redefining skill contracts, certifying compliance, granting approval authority, copying curricula, publishing a GitHub Release, or replacing operational tutorials and how-to guides with lesson duplicates.

## Assumptions
The detailed user mission is accepted requirements input. Repository behavior is authoritative. External resources are research inputs only. The review date is 2026-07-21. Existing public pages remain discoverable by relocation within the six groups rather than deletion.

## Open Questions
No question blocks reversible work. The owner may later decide release promotion and whether organization-specific curricula extend the shared sequence.

## Decision Status
DEC-001 through DEC-003 govern architecture, source use, and validation, subject to owner approval.

