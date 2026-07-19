#!/usr/bin/env python3
"""Canonical refinement artifact profiles and self-contained context schema."""

from __future__ import annotations

from dataclasses import dataclass


COMMON_CONTEXT_SECTIONS: tuple[str, ...] = (
    "Feature Summary",
    "Actors and Stakeholders",
    "Scope and Boundaries",
    "Workflows and Failure Paths",
    "Requirements and Business Rules",
    "Data, Integrations, and Non-Functional Requirements",
    "Dependencies, Risks, and Constraints",
    "Decisions, Assumptions, and Open Questions",
    "Success Measures",
    "Source Coverage",
)

QUICK_CONTEXT_TOKENS = 4000
STANDARD_CONTEXT_TOKENS = 24000
MAX_ARTIFACT_TOKENS = 24000


@dataclass(frozen=True)
class ArtifactProfile:
    """One lifecycle artifact's canonical output and detailed sections."""

    stage_id: str
    skill: str
    artifact_name: str
    stage_sections: tuple[str, ...]
    predecessors: tuple[str, ...] = ()
    optional: bool = False
    legacy_names: tuple[str, ...] = ()


PROFILES: tuple[ArtifactProfile, ...] = (
    ArtifactProfile(
        "discovery",
        "ai-sdlc-working-backwards-discovery",
        "discovery.md",
        (
            "Customer and Problem Evidence",
            "Current Process and Alternatives",
            "Value Proposition and Business Goals",
            "Users, Roles, and Scenarios",
            "MVP and Priorities",
            "Functional and Non-Functional Needs",
            "Operations, Launch, and Support",
            "Discovery Risks and Dependencies",
        ),
        legacy_names=("discovery-notes.md",),
    ),
    ArtifactProfile(
        "prfaq",
        "ai-sdlc-prfaq-package-synthesis",
        "prfaq.md",
        ("Press Release", "Customer FAQ", "Internal FAQ", "Business Requirements", "Launch Risks"),
        ("discovery",),
    ),
    ArtifactProfile(
        "delivery_package_gap_review",
        "ai-sdlc-delivery-package-gap-review",
        "delivery-gap-review.md",
        ("Evidence Reviewed", "Gap Matrix", "Contradictions", "Blocking Questions", "Readiness Verdict"),
        ("prfaq",),
        legacy_names=("delivery-package-gap-review.md",),
    ),
    ArtifactProfile(
        "requirements_readiness",
        "ai-sdlc-requirements-readiness-review",
        "requirements-readiness.md",
        ("Readiness Score", "Dimension Assessment", "Blocking Gaps", "Required Follow-Up", "Readiness Verdict"),
        ("delivery_package_gap_review",),
    ),
    ArtifactProfile(
        "goal_epic_mapping",
        "ai-sdlc-goal-capability-and-epic-mapping",
        "goal-capability-map.md",
        ("Business Goals", "Role Matrix", "Capability Map", "Epic Map", "Outcome Traceability"),
        ("requirements_readiness",),
        legacy_names=("goal-capability-epic-map.md",),
    ),
    ArtifactProfile(
        "backlog_gap_review",
        "ai-sdlc-backlog-requirements-gap-review",
        "backlog-gap-review.md",
        ("Planning Evidence", "Gap Matrix", "Priority and Scope Gaps", "Dependency Gaps", "Planning Verdict"),
        ("goal_epic_mapping",),
        legacy_names=("backlog-requirements-gap-review.md",),
    ),
    ArtifactProfile(
        "backlog_decomposition",
        "ai-sdlc-backlog-decomposition-and-task-planning",
        "backlog.md",
        ("Epic Backlog", "Story Backlog", "Acceptance Summary", "Priorities and Dependencies", "Cross-Functional Tasks", "Definition of Ready"),
        ("backlog_gap_review",),
    ),
    ArtifactProfile(
        "story_decomposition",
        "ai-sdlc-user-story-decomposition",
        "user-stories.md",
        ("Story Detail Matrix", "Acceptance Criteria Matrix", "Scenario Coverage Matrix", "Story Dependencies and Risks", "Story Readiness"),
        ("backlog_decomposition",),
    ),
    ArtifactProfile(
        "release_slicing",
        "ai-sdlc-release-slicing-and-backlog-readiness-review",
        "release-slicing.md",
        ("MVP Slice", "Release Slice Matrix", "Sequencing and Dependencies", "Milestones and Readiness", "Release Risks", "Release Verdict"),
        ("backlog_decomposition",),
        True,
    ),
    ArtifactProfile(
        "ba_context",
        "ai-sdlc-ba",
        "business-context.md",
        ("Current Behavior", "Desired Behavior", "Actor and Permission Matrix", "Workflow Detail", "Business Rule Catalog", "Acceptance Criteria", "Business Context Gaps"),
        ("story_decomposition",),
    ),
    ArtifactProfile(
        "delivery_spec",
        "ai-sdlc-delivery-spec-synthesis",
        "delivery-spec.md",
        ("Requirement Detail", "Workflow Detail", "Business Rule Detail", "User Story Traceability", "Acceptance Traceability", "QA and Operational Notes", "Handoff Risks"),
        ("ba_context",),
    ),
    ArtifactProfile(
        "qa_plan",
        "ai-sdlc-qa",
        "qa.md",
        ("Acceptance Scenarios", "Regression Targets", "Risk-Based Coverage", "Test Data and Environment", "Validation Commands", "Manual Checks", "Signoff Criteria"),
        ("requirements_readiness",),
        legacy_names=("qa-plan.md",),
    ),
    ArtifactProfile(
        "qa_gap_review",
        "ai-sdlc-qa-requirements-gap-review",
        "qa-gap-review.md",
        ("QA Evidence Reviewed", "Testability Gap Matrix", "Negative and Edge Coverage", "Data and Environment Gaps", "Blocking Questions", "QA Gap Verdict"),
        ("qa_plan",),
        legacy_names=("qa-requirements-gap-review.md",),
    ),
    ArtifactProfile(
        "test_strategy",
        "ai-sdlc-test-scope-and-strategy-design",
        "qa-strategy.md",
        ("Test Scope", "Risk and Coverage Priorities", "Layer and Suite Strategy", "Test Data Strategy", "Environment Dependencies", "Automation Strategy", "Strategy Risks"),
        ("qa_gap_review",),
        legacy_names=("test-strategy.md",),
    ),
    ArtifactProfile(
        "test_cases",
        "ai-sdlc-test-cases",
        "test-cases.md",
        ("Scenario Matrix", "Detailed Test Cases", "Permission and Negative Cases", "Expected Results", "Layer Mapping", "Automation Plan"),
        ("test_strategy",),
    ),
    ArtifactProfile(
        "test_suite",
        "ai-sdlc-test-case-and-suite-synthesis",
        "test-suite.md",
        ("Suite Coverage Matrix", "Smoke Suite", "Regression Suite", "UAT Suite", "Entry Criteria", "Exit Criteria", "Execution Dependencies"),
        ("test_cases",),
        legacy_names=("test-suites.md",),
    ),
    ArtifactProfile(
        "qa_traceability",
        "ai-sdlc-qa-traceability-and-readiness-review",
        "qa-readiness.md",
        ("Requirement-to-Test Traceability", "Risk Coverage", "Coverage Gaps", "Execution Readiness Evidence", "Blocked Coverage", "QA Readiness Verdict"),
        ("test_suite",),
        legacy_names=("qa-traceability.md",),
    ),
    ArtifactProfile(
        "delivery_handoff",
        "ai-sdlc-delivery-handoff-review",
        "delivery-handoff-review.md",
        ("Handoff Evidence", "Requirement and Story Coverage", "QA Readiness", "Ownership and Dependencies", "Decision Coverage", "Implementation Handoff", "Final Verdict"),
        ("delivery_spec", "qa_traceability"),
    ),
)


PROFILE_BY_SKILL = {profile.skill: profile for profile in PROFILES}
PROFILE_BY_STAGE = {profile.stage_id: profile for profile in PROFILES}


TABLE_REQUIREMENTS_BY_STAGE: dict[str, dict[str, tuple[str, ...]]] = {
    "delivery_package_gap_review": {
        "Gap Matrix": ("Area", "Gap", "Evidence", "Impact", "Severity", "Owner", "Resolution"),
    },
    "requirements_readiness": {
        "Dimension Assessment": ("Dimension", "Evidence", "Status", "Gap", "Owner"),
    },
    "goal_epic_mapping": {
        "Business Goals": ("Goal ID", "Goal", "Metric", "Target", "Owner", "Source"),
        "Role Matrix": ("Actor", "Role", "Need", "Permission Boundary", "Source"),
        "Capability Map": ("Capability ID", "Capability", "Goal Ref", "Actors", "Dependencies"),
        "Epic Map": ("Epic ID", "Epic", "Capability Ref", "Outcome", "Priority", "Risks"),
    },
    "backlog_gap_review": {
        "Gap Matrix": ("Area", "Gap", "Evidence", "Planning Impact", "Severity", "Owner"),
    },
    "backlog_decomposition": {
        "Epic Backlog": ("Epic ID", "Outcome", "Actors", "Priority", "Dependencies"),
        "Story Backlog": ("Story ID", "Epic Ref", "Actor", "Story", "Priority", "MVP"),
        "Cross-Functional Tasks": ("Task ID", "Owner", "Output", "Dependencies", "Refs"),
    },
    "story_decomposition": {
        "Story Detail Matrix": ("Story ID", "Epic ID", "Actor", "Story", "Value", "Priority", "MVP"),
        "Acceptance Criteria Matrix": ("AC ID", "Story ID", "Given", "When", "Then", "Rule Covered"),
        "Scenario Coverage Matrix": ("Scenario ID", "Story ID", "Type", "Trigger", "Expected Outcome", "AC Ref"),
    },
    "release_slicing": {
        "Release Slice Matrix": ("Slice", "Value", "Stories", "Dependencies", "Exit Criteria", "Risks"),
    },
    "ba_context": {
        "Actor and Permission Matrix": ("Actor", "Role", "Permissions", "Restrictions", "Source"),
        "Workflow Detail": ("Workflow ID", "Trigger", "Actor", "Steps", "End State", "Exceptions", "Source"),
        "Business Rule Catalog": ("Rule ID", "Rule", "Applies To", "Failure Behavior", "Source", "Decision Ref"),
        "Acceptance Criteria": ("AC ID", "Given", "When", "Then", "Rule Ref", "Source"),
    },
    "delivery_spec": {
        "Requirement Detail": ("Requirement ID", "Actor/System", "Requirement", "Source", "Priority", "Acceptance Ref"),
        "Workflow Detail": ("Workflow ID", "Trigger", "Actor", "Steps", "End State", "Exceptions", "Requirement Ref"),
        "Business Rule Detail": ("Rule ID", "Rule", "Applies To", "Source", "Failure Behavior", "Decision Ref"),
    },
    "qa_gap_review": {
        "Testability Gap Matrix": ("Area", "Gap", "Evidence", "Test Impact", "Severity", "Owner", "Resolution"),
    },
    "test_strategy": {
        "Risk and Coverage Priorities": ("Risk", "Likelihood", "Impact", "Coverage Layer", "Priority", "Owner"),
    },
    "test_cases": {
        "Scenario Matrix": ("Scenario ID", "Requirement Ref", "Type", "Preconditions", "Expected Outcome"),
        "Detailed Test Cases": ("Test ID", "Scenario Ref", "Steps", "Expected Result", "Priority", "Automation"),
    },
    "test_suite": {
        "Suite Coverage Matrix": ("Suite", "Purpose", "Test IDs", "Trigger", "Environment", "Owner"),
    },
    "qa_traceability": {
        "Requirement-to-Test Traceability": ("Requirement", "Acceptance Ref", "Test IDs", "Suite", "Status", "Gap"),
        "Execution Readiness Evidence": ("Evidence Area", "Required Signal", "Present", "Gap", "Impact"),
    },
    "delivery_handoff": {
        "Handoff Evidence": ("Area", "Artifact", "Status", "Evidence", "Owner", "Blocker"),
    },
}


def profile_for_skill(skill: str) -> ArtifactProfile | None:
    """Return the canonical refinement profile for a skill, if one exists."""
    return PROFILE_BY_SKILL.get(skill)


def required_sections(profile: ArtifactProfile, flow_mode: str) -> list[str]:
    """Return compact quick sections or self-contained default/full sections."""
    if flow_mode == "quick":
        return list(profile.stage_sections)
    return [*COMMON_CONTEXT_SECTIONS, *profile.stage_sections]


def required_tables(profile: ArtifactProfile) -> dict[str, tuple[str, ...]]:
    """Return detailed table-column requirements for a stage profile."""
    return TABLE_REQUIREMENTS_BY_STAGE.get(profile.stage_id, {})
