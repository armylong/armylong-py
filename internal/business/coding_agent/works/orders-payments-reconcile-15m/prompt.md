You are in a Linux container with bash, coreutils, gawk, grep, sed, jq, findutils, gzip preinstalled.
Your goal: read order / payment / refund inputs in /app/data/in, reconcile them, and write six outputs to /app/out:

REQUIRED OUTPUTS (exact filenames and formats):
1) /app/out/inventory.csv
   Header:
     filename,relpath,bytes,lines,is_jsonl
   Rows:
     One row per input file present in /app/data/in, sorted by relpath (byte-wise order).
     bytes = file size in bytes
     lines = count of LF characters in the file
     is_jsonl = 1 for *.jsonl, else 0
   Constraints:
     ASCII only; LF newlines; exactly one trailing newline; no TABs or trailing spaces anywhere.

2) /app/out/orders.csv
   Header:
     order_id,customer_id,ts,epoch,amount_cents,source_relpath
   Semantics:
     Read all CSV files matching /app/data/in/orders-*.csv. Each row provides:
     - order_id (string), customer_id (string), ts (timestamp string), amount_cents (integer)
     Convert ts to UTC epoch seconds (integer) and emit one row per *deduplicated* order:
       • Dedup key: order_id
       • Choose the row with the *earliest* epoch; if there is a tie, choose the lexicographically smaller source_relpath.
     Sort all emitted rows by order_id.
   Constraints:
     ASCII only; LF newlines; one trailing newline; no TABs or trailing spaces.

3) /app/out/matches.csv
   Header:
     order_id,order_ts,payment_ts,latency_sec,amount_cents,matched_payment_relpath
   Semantics:
     Read payments from /app/data/in/payments.jsonl (if present). Each JSON object may contain:
       order_id (string), ts (timestamp), amount_cents (integer), status (string).
     For each row in orders.csv, find payment events that satisfy ALL:
       • same order_id
       • status == "captured"
       • amount_cents exactly equals the order’s amount_cents
       • |payment_epoch - order_epoch| ≤ 900 seconds (15 minutes)
     If multiple payments match, pick the one with the earliest payment_epoch; on tie, pick lexicographically smaller matched_payment_relpath.
     Emit one row per matched order. Sort by order_id.
   Constraints:
     ASCII only; LF newlines; one trailing newline; no TABs or trailing spaces.

4) /app/out/cancellations.csv
   Header:
     order_id,order_ts,refund_ts,delta_sec
   Semantics:
     Read refunds from /app/data/in/refunds.jsonl (if present). Each JSON object may contain:
       order_id (string), ts (timestamp).
     For each row in orders.csv, find refunds with refund_epoch ≥ order_epoch. If any exist, choose the *earliest* refund_epoch;
     on tie, pick lexicographically smaller source relpath ("refunds.jsonl"). Emit at most one row per order. Sort by order_id.
   Constraints:
     ASCII only; LF newlines; one trailing newline; no TABs or trailing spaces.

5) /app/out/sessions.csv
   Header:
     session_id,customer_id,start,end,req_count,amt_sum_cents
   Semantics:
     Build per-customer sessions from orders.csv using the deduplicated orders:
       • A new session starts when the gap from the previous order by the same customer is > 300 seconds; otherwise the order joins the current session.
       • For each session, start = ISO8601 of first order epoch (UTC, "YYYY-MM-DDTHH:MM:SSZ"), end = ISO8601 of last order epoch.
       • req_count = number of orders in the session; amt_sum_cents = sum of amount_cents in the session.
       • session_id = "<customer_id>:<start_epoch>"
     Output rows sorted lexicographically by session_id.
   Constraints:
     ASCII only; LF newlines; one trailing newline; no TABs or trailing spaces.

6) /app/out/summary.txt
   Strict 6 lines, exactly in this order (key=value):
     total_input_files=<N>
     total_orders_dedup=<N>
     matched_orders=<N>
     canceled_orders=<N>
     total_sessions=<N>
     unmatched_orders=<N>
   Semantics:
     • total_input_files: number of rows in inventory.csv (excluding header)
     • total_orders_dedup: number of rows in orders.csv (excluding header)
     • matched_orders: number of rows in matches.csv
     • canceled_orders: number of rows in cancellations.csv
     • total_sessions: number of rows in sessions.csv
     • unmatched_orders: total_orders_dedup minus the number of distinct order_id that appear in matches.csv or cancellations.csv
   Constraints:
     ASCII only; LF newlines; one trailing newline; no TABs or trailing spaces.

GENERAL RULES (only output-observable requirements):
  • All timestamps you emit as ISO strings must be UTC Zulu format: "YYYY-MM-DDTHH:MM:SSZ".
  • All sorting statements above are about the *final output order*. How you implement sorting is up to you.
  • CSV inputs may include quoted fields; handle them so that emitted values reflect the actual field contents correctly.
  • You must not rely on external network resources; work entirely with files provided in the container.
  • Do not assume any outputs exist beforehand; create /app/out files fresh each run and overwrite if present.

NOTES (non-binding hints, not enforced by tests):
  • Common tools that can help: awk, sed, sort, jq, date, paste, join, etc.
  • Converting timestamps robustly (including offsets like +00:00 or -05:00) is often necessary before comparing seconds.
  • When tie-break rules mention “lexicographically smaller path”, compare the literal path strings as bytes.