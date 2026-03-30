A system-wide dependency review uncovered configuration files under /app/data containing obsolete package references that no longer comply with current deployment standards. Each outdated reference must be modernized directly within the original files, and the entire operation must yield a reproducible audit trail for compliance verification.

Modernization Execution

Every detected outdated reference must be rewritten in place with the literal string MODERN_PACKAGE_REF.
The transformation must preserve each file’s encoding, formatting, and structural integrity.

Outdated Reference Detection

A deprecated reference is defined as any substring beginning with pkg- followed by exactly 24 lowercase hexadecimal characters (a–f, 0–9).
Pattern matching must be strictly case-sensitive, excluding uppercase or mixed-case variants.
When multiple references appear on a single line, each must be counted and individually replaced.

Cross-Line Matching

In addition to same-line matches, tokens that break across line boundaries MUST also be detected and remediated. Specifically:
- Treat a sequence where `pkg-` appears at the end of a line and the required 24-character lowercase hexadecimal segment continues on the next line **without any intervening non-hex characters** as a single valid match.
- Count and replace each such cross-line occurrence exactly once, just like same-line matches.
- The replacement MUST overwrite only the matched span (which may cover multiple lines) with the exact literal `MODERN_PACKAGE_REF`, preserving all surrounding characters and formatting outside the matched span.

Directory Inspection

Perform a recursive scan of all regular files beneath /app/data, including hidden files and directories.
Symbolic links must never be traversed—skip them entirely, regardless of where they resolve.

Edge Conditions

If /app/data contains no files, generate a CSV containing only the header row.
Zero-length files must still appear in the final report with a recorded count of 0.

Compliance Report Generation

Produce /app/output/result.csv with the exact header:

count,path

Each subsequent record must follow the format <count>,<absolute_path>, and every path must begin with /app/data/.
Please note the format of the csv file. The output must comply with its specific format and cannot break this format rule. When encountering special characters, if necessary, please use quotes to include the file name.
The operation must be deterministic: identical input sets produce identical byte-level results, and no extraneous files may be created.

Delivery Specification

Provide one executable Bash script located at /tmp/solution.
It must execute successfully without arguments as:

/tmp/solution


Deliverable Summary

The deliverable is a single Linux Bash script located at /tmp/solution, responsible for performing the full modernization of outdated package references and producing deterministic, standards-compliant reports.