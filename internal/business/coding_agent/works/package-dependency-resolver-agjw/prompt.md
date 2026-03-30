Goal: Analyze package dependency files across multiple projects, detect version conflicts, and produce a CSV conflict resolution report.

Deliverable
- Create a Bash script at /app/solution.sh.
- Tests run it with bash and APP_ROOT=/app; the executable bit is optional.
- Use these paths:
  - PROJECTS="$APP_ROOT/projects"
  - OUT="$APP_ROOT/out"
  - CONFLICTS_CSV="$OUT/conflicts.csv"
  - GRAPH_CSV="$OUT/dependency_graph.csv"
- Your script must create OUT as needed and always write both CSVs.

Requirements
- Scan project directories under /app/projects recursively
  * Handle filenames with spaces correctly
  * Do not follow symlinked directories; only walk real directories
  * Skip symlinks to files

- Parse dependency files in multiple formats:
  * requirements.txt (Python): package==version or package>=version or package
  * package.json (Node.js): JSON format with "dependencies" and "devDependencies"
  * Cargo.toml (Rust): TOML format with [dependencies] section
  * Handle malformed files gracefully (skip them)
  * Extract package name and version constraints

- For each unique package across all projects, compute:
  * package_name: Name of the package (case-sensitive)
  * version_count: Number of distinct version constraints found
  * versions: Comma-separated sorted list of all version constraints (e.g., "1.0.0,2.0.0,>=1.5")
  * project_count: Number of projects using this package
  * projects: Comma-separated sorted list of project paths (relative to /app/projects)
  * conflict: "YES" if version_count > 1, otherwise "NO"
  * severity: Conflict severity level (CRITICAL, HIGH, MEDIUM, LOW, NONE)
  * resolvable: "YES" if all version constraints can be satisfied together, "NO" if incompatible

- Conflict Severity Calculation Rules:
  * CRITICAL: Multiple exact version requirements that differ (e.g., "==1.0.0" and "==2.0.0")
  * HIGH: Non-overlapping version ranges (e.g., ">=2.0.0" and "<1.5.0")  
  * MEDIUM: Overlapping ranges but with constraints (e.g., ">=1.0.0,<2.0.0" and ">=1.5.0,<3.0.0")
  * LOW: Compatible broad ranges (e.g., ">=1.0.0" and ">=1.5.0")
  * NONE: No conflict (single version or identical constraints)

- Resolvability Determination:
  * "YES": There exists at least one version that satisfies ALL constraints
  * "NO": No single version can satisfy all constraints simultaneously
  * Must parse semantic versioning constraints: ==, !=, <, <=, >, >=, ~=, ^
  * For exact versions: must be identical to be resolvable
  * For ranges: must have non-empty intersection

- Version Normalization Rules:
  * Strip 'v' prefix: "v1.0.0" → "1.0.0"
  * Normalize to semantic versioning: "1.0" → "1.0.0"
  * Handle pre-release versions: "1.0.0-alpha" → "1.0.0-alpha"
  * Normalize constraints before comparison

- Calculate Minimum Satisfying Version:
  * For resolvable conflicts, determine the minimum version that satisfies ALL constraints
  * Example: >=1.5.0 AND <2.0.0 → min_version: "1.5.0"
  * Example: >=2.0.0 AND >=1.5.0 → min_version: "2.0.0"
  * For non-resolvable: min_version is empty string

- Output /app/out/conflicts.csv with exact header:
  package_name,version_count,versions,project_count,projects,conflict,severity,resolvable,min_version
  * package_name is the package identifier
  * versions is comma-separated, sorted by semantic version (not lexicographically)
  * projects is comma-separated, sorted lexicographically
  * severity must be one of: CRITICAL, HIGH, MEDIUM, LOW, NONE
  * resolvable must be: "YES" or "NO"
  * min_version: minimum version satisfying all constraints (empty if not resolvable)
  * Sort rows by severity (CRITICAL, HIGH, MEDIUM, LOW, NONE), then conflict (YES first), then package_name
  * Each package must appear exactly once; no duplicate rows

- Build dependency graph by analyzing package relationships:
  * For each project, identify which packages it depends on
  * Create edges: project -> package_name (with version)

- Output /app/out/dependency_graph.csv with exact header:
  project,package_name,version_constraint,dependency_type
  * project: Relative path from /app/projects
  * package_name: Name of the package
  * version_constraint: Version constraint (e.g., "==1.0.0", ">=2.0", or empty if not specified)
  * dependency_type: Always set to "direct" for all dependencies
  * Sort rows by project, then by package_name
  * Each (project, package_name) pair must appear exactly once

- Handle edge cases:
  * Empty dependency files (only write headers)
  * Projects with no dependency files (no entries in graph)
  * Packages with no version specified (use empty string for version_constraint)
  * Very long package names (500+ characters, keep as-is)
  * Unicode characters in package names
  * JSON parsing errors (skip malformed JSON files)
  * TOML parsing errors (skip malformed TOML files)

- Deterministic: same input -> identical output
- Do not modify input files under /app/projects

Guards (ALL behaviors tested with strict assertions)
- Create OUT as needed: tests remove OUT and assert the script recreates it and writes both CSVs
- Input files under /app/projects must not be modified (verified by checksum)
- Symlinks to files and directories are skipped (tested for both)
- Recursive processing of nested project directories (tested)
- Filenames with spaces handled correctly (tested)
- conflicts.csv sorted by: severity (CRITICAL→HIGH→MEDIUM→LOW→NONE), then conflict (YES first), then package_name (tested)
- dependency_graph.csv sorted by: project, then package_name (tested)
- All CSV headers in exact order specified (tested)
- version_count must equal number of distinct versions in versions field (tested)
- project_count must equal number of projects in projects field (tested)
- Each package appears exactly once in conflicts.csv (tested)
- Each (project, package) pair appears exactly once in dependency_graph.csv (tested)
- Deterministic output (running twice produces identical results, tested)
- Empty dependency files produce header-only CSV (tested)
- Malformed JSON files are skipped gracefully (tested)
- Malformed TOML files are skipped gracefully (tested)
- dependency_type field is always 'direct' for all entries (tested)
- Very long package names (500+ chars) are preserved (tested)
- Package names are case-sensitive: MyPkg != mypkg (tested)
- Packages without version constraints use empty string for version_constraint (tested)
- Version constraint operators (==, >=, <=, ~=, !=, ^) are preserved or normalized consistently (tested)
- Severity levels (CRITICAL, HIGH, MEDIUM, LOW, NONE) calculated correctly (tested)
- Resolvability (YES/NO) determined based on constraint compatibility (tested)
- min_version calculated for resolvable conflicts (tested)
- min_version is empty string for non-resolvable conflicts (tested)
- Version normalization: 'v' prefix removed, expanded to x.y.z format (tested)
- versions field sorted by semantic version, not lexicographically (tested)
- Pre-release versions (1.0.0-alpha, 1.0.0-beta) preserved correctly (tested)
- ~= (compatible release) operator semantic behavior validated (tested)
- ^ (caret) operator semantic behavior for resolvability validated (tested)
- Complex TOML inline tables parsed correctly (tested)

Tips (non-binding)
- Use python3 for JSON parsing (import json)
- Use grep/awk/sed for requirements.txt parsing
- TOML parsing can be done with python3 -c "import tomllib; ..." or basic regex
- Create temporary files with mktemp and clean up with trap
- Use associative arrays or Python dictionaries for aggregation
- Solution should efficiently handle 100+ packages across 10+ projects

Example
Given projects:
- project_a/requirements.txt: "requests==2.28.0\nnumpy>=1.20"
- project_b/package.json: {"dependencies": {"express": "4.18.0", "requests": "2.28.0"}}
- project_c/requirements.txt: "requests==2.30.0\nnumpy>=1.20"

Expected conflicts.csv:
```
package_name,version_count,versions,project_count,projects,conflict
requests,2,"2.28.0,2.30.0",3,"project_a,project_b,project_c",YES
express,1,4.18.0,1,project_b,NO
numpy,1,>=1.20,2,"project_a,project_c",NO
```

Expected dependency_graph.csv:
```
project,package_name,version_constraint,dependency_type
project_a,numpy,>=1.20,direct
project_a,requests,==2.28.0,direct
project_b,express,4.18.0,direct
project_b,requests,2.28.0,direct
project_c,numpy,>=1.20,direct
project_c,requests,==2.30.0,direct
```
