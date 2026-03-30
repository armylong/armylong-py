Build a concurrent, file-system-cached numeric gradient CLI for basic mathematical functions.

Requirements:
1) Create the following files:
   - /app/gradcalc/gradient.py
   - /app/gradcalc/grad_cli.py

2) The CLI interface:
   - Usage: python3 /app/gradcalc/grad_cli.py <function> <vector>
   - <function> must be one of: "sphere", "rosenbrock"
   - <vector> is a comma-separated list of floats, e.g. "1.0,2.0,-3.5"
   - The CLI must print the gradient as a JSON array on stdout, e.g. "[2.0, 4.0]"

3) Functions:
   - sphere(x) = sum_i x_i^2, shape (n,)
     Analytic gradient: ∇f = 2x
   - rosenbrock(x) with n=2 only:
     f(x, y) = (1 - x)^2 + 100 * (y - x^2)^2
     Numeric gradient required; tests will compare with analytic:
       df/dx = 2*(x - 1) - 400*x*(y - x^2)
       df/dy = 200*(y - x^2)
     If the user gives a vector not of length 2 for rosenbrock, exit with error and non-zero code.

4) Numeric gradient:
   - Use central finite differences with step h = 1e-6:
     g_i = (f(x + h e_i) - f(x - h e_i)) / (2h)
   - Evaluate the 2*n function calls concurrently using a process pool (e.g., concurrent.futures.ProcessPoolExecutor).
   - Concurrency configuration via environment variable:
     - GRAD_NWORKERS: integer > 0 specifying number of worker processes.
       If not set, choose a reasonable default (e.g., min(os.cpu_count(), len(x)), but at least 1).
   - After computing, write a file /app/grad_workers.json containing a JSON list of unique worker PIDs that executed the function calls. This is used to verify concurrency. When a cached result is used (see below), it is okay to either omit this file or write an empty list.

5) File-system caching (gradient-level cache):
   - Cache directory: /app/grad_cache/
   - Cache key: sha1 hash of the string f"{function}|{vector}|h=1e-6|central" where "vector" is exactly the string received by CLI.
   - Cache file path: /app/grad_cache/<key>.json with JSON content:
       {"gradient": [...], "pid": <parent_pid>}
   - Also maintain an append-only log at /app/grad_cache/hits.txt where each run appends either:
       "HIT <key>\n" if the cached gradient was used
       "MISS <key>\n" if the gradient was newly computed and then cached
   - Environment variable GRAD_FORBID_COMPUTE:
       If set to "1", the program MUST NOT perform any new function evaluations. It must:
         - Return a cached result if available (still append "HIT <key>\n") and exit code 0
         - If no cache exists for the given key, exit with code 2 (non-zero) and print an explanatory message to stderr

6) Output:
   - Print only the JSON array of the gradient on stdout (no extra text), e.g. "[0.2, -0.4, 0.6]"

7) Notes:
   - Tests will verify:
     - Correct numeric gradient for rosenbrock (n=2) and sphere (n>=1) within a tolerance
     - That concurrency is used by checking /app/grad_workers.json has >= 2 unique worker PIDs for a test where GRAD_NWORKERS=2 and vector length >= 3
     - Caching behavior (first MISS, then HIT with GRAD_FORBID_COMPUTE=1; and error when cache is forbidden and missing)
   - Do not install test dependencies or copy test scripts/resources in the Docker image.
   - Do not change test files.
   - Implement the CLI robustly and follow the exact file paths and environment variable semantics described.