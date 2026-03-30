Performance degradation in large-scale deployments often traces back to code constructs that waste CPU cycles, consume excess memory, and degrade response times. Left unchecked, these anti-patterns can turn robust systems into sluggish bottlenecks. To protect production reliability, /app/data must be fully audited to uncover and neutralize these inefficient sequences before they escalate into user-facing issues.


File Discovery Protocol
  •	Recursively scan the entire /app/data tree, including hidden files and directories.
  •	Symbolic links must be ignored to prevent accidental recursion or unintended access.

Optimization Rules
  •	Every detected anti-pattern must be replaced in place with the marker OPTIMIZED_REPLACEMENT.
  •	Substitutions must leave surrounding code and structure unchanged to avoid collateral disruptions.

Performance Anti-Pattern Detection
  •	Match strings beginning with slow followed by exactly 35 alphanumeric characters.
  •	Detection is case-sensitive.
  •	If a line contains multiple matches, each one must be logged and replaced individually.

Report Generation
  •	Produce the analysis output at /app/output/result.csv.
  •	The header must read exactly: count,path.
  •	Each subsequent row records <detection_count>,<absolute_file_path>, with paths always starting /app/data/.
  •	CSV compliance is mandatory: filenames with quotes or commas must be quoted properly, with embedded quotes doubled.
  •	Results must be deterministic—identical input produces byte-for-byte identical output with no stray files.

Edge Case Handling
  •	If /app/data is empty, still generate a valid CSV containing only the header line.
  •	Zero-byte files must appear in the report with a detection count of 0.

Implementation Requirements
  •	Provide an executable Bash script named solution stored at /tmp/solution.
  •	The script must run to completion with no arguments when invoked as:

/tmp/solution

Deliverable Specification
  •	The required deliverable is the Linux Bash script file located at /tmp/solution.