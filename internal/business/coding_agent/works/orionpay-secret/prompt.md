OrionPay's webhook signing secrets have a predictable stem and routinely drift into application configs. Security needs an automated sweep of the mounted data directory before each deployment.

Deliver a Bash-only utility that walks `/app/data`, tallies the number of OrionPay secrets in every regular file it encounters, and emits a deterministic report for downstream tooling.

Reporting Expectations
  • Write the findings to `/app/output/orionpay_scan.csv` with the header `hits,file` on the first line.
  • Each subsequent record must appear as `<count>,<absolute_path>`, using absolute paths that always start with `/app/data/`.
  • Please note the format of the csv file. The output must comply with its specific format and cannot break this format rule. When encountering special characters, if necessary, please use quotes to include the file name.
  • The script must be repeatable: identical input trees produce byte-for-byte identical CSV output and no stray artifacts.

Token Signature
  • Secrets are case-insensitive strings that begin with `OPW-LIVE-` followed immediately by exactly 30 hexadecimal characters (`[0-9A-F]`).
  • Matches that sit side by side on the same line each count once; anything with too few or too many hex characters must be ignored.
  • A valid token must terminate after the thirtieth hex character; the next character (if present) cannot be another hexadecimal digit.

Scan Scope
  • Recursively inspect the entire `/app/data` tree, including hidden files and recursive directories.
  • Process only regular files; never follow or report symlinked entries.
  • Even zero-byte files must appear in the CSV with a hit count of `0`.

Execution Contract
  • Produce an executable named `solution` located in `/tmp`; invoking `/tmp/solution` must exit with status code 0 when the scan succeeds.

Requirements (exactly what is tested):
  • The solution must be an executable file named exactly solution in the /tmp directory.
It is invoked as:
/tmp/solution