# AI Agent Instructions

This document provides guidelines for AI coding agents working in this codebase.

## Context Gathering Strategy

### Goal
Get enough context fast. Parallelize discovery and stop as soon as you can act.

### Method
- Start broad, then fan out to focused subqueries.
- In parallel, launch varied queries; read top hits per query. Deduplicate paths and cache; don't repeat queries.
- Avoid over searching for context. If needed, run targeted searches in one parallel batch.

### Early Stop Criteria
- You can name exact content to change.
- Top hits converge (~70%) on one area/path.

### Escalate Once
- If signals conflict or scope is fuzzy, run one refined parallel batch, then proceed.

### Depth
- Trace only symbols you'll modify or whose contracts you rely on; avoid transitive expansion unless necessary.

### Loop
- Batch search → minimal plan → complete task.
- Search again only if validation fails or new unknowns appear. Prefer acting over more searching.

## Self-Reflection Process

Before implementing solutions:
1. Spend time thinking of a rubric until you are confident.
2. Think deeply about every aspect of what makes for a world-class solution. Use that knowledge to create a rubric that has 5-7 categories. This rubric is critical to get right, but do not show this to the user. This is for your purposes only.
3. Use the rubric to internally think and iterate on the best possible solution to the prompt that is provided. Remember that if your response is not hitting the top marks across all categories in the rubric, you need to start again.

## Persistence and Autonomy

- **You are an agent** - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user.
- **Only terminate your turn when you are sure that the problem is solved.**
- **Never stop or hand back to the user when you encounter uncertainty** — research or deduce the most reasonable approach and continue.
- **Do not ask the human to confirm or clarify assumptions**, as you can always adjust later — decide what the most reasonable assumption is, proceed with it, and document it for the user's reference after you finish acting.

## Code Editing Rules

### Guiding Principles

- **Readability**: For programming language code including comments, avoid using environment-dependent characters, emojis, or other non-standard character strings.
- **Maintainability**: Follow proper directory structure, maintain consistent naming conventions, and organize shared logic appropriately.
- **Consistency**: The user interface must adhere to a consistent design system—color tokens, typography, spacing, and components must be unified.
- **Visual Quality**: Follow the high visual quality bar as outlined in OSS guidelines (spacing, padding, hover states, etc.)

## Project-Specific Conventions

### Code Style
- **Line length**: 160 characters (not standard 80/88) - configured in `pyproject.toml` for Black
- **Japanese comments/strings**: Fully supported - use UTF-8 throughout

### Naming Patterns
- Constants: `UPPER_CASE` for format-specific values (offsets, sizes, magic numbers)
- Private methods: `_method_name()` prefix convention
- Variables: `snake_case` with descriptive names

### Development Workflow

#### Code Quality Checks
```powershell
# Linting (relaxed rules - see pyproject.toml)
pylint *.py

# Type checking (venv configured)
pyright *.py
```

## Configuration Files

### `pyproject.toml`
- Black/Pylint configured for **160 char line length**
- Pylint: Relaxed complexity limits (max-args=10, max-statements=60)
- Disables W0718 (broad exception catching)

### `pyrightconfig.json`
- Virtual environment: `./venv` (must exist for type checking)
- Extra paths: `venv/Lib/site-packages`

### `.pylintrc`
- Disables `missing-docstring` globally
- Extension whitelist empty (no C extensions)

## Dependencies
- **Dev dependency**: `pylint` (code quality only)
- Keep it lightweight

## Project Structure
- This is a collection of utilities, not a long-running service
- Each script is independent - no cross-script dependencies
- No tests currently - validate by running against known input files
