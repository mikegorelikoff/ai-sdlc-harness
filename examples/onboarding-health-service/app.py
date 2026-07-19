"""Tiny dependency-free route function for the onboarding tutorial."""


def route(path: str) -> tuple[int, dict[str, str]]:
    """Return a status code and JSON-compatible body for one path."""
    if path == "/version":
        return 200, {"version": "1.0"}
    return 404, {"error": "not found"}
