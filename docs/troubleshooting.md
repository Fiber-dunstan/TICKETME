# Troubleshooting Guide

Real issues encountered during TicketMe's development, their root causes, and how they were resolved. Documented here both as a reference and as evidence of the debugging process behind this project.

---

### Python module-name collisions in tests

**Symptom:** Tests for `register_handler` were silently executing `list_events_handler`'s code instead (visible via log output showing the wrong handler's log messages).

**Cause:** Both handlers' files are named `app.py`. Python caches imported modules by name in `sys.modules`, so a plain `import app` in a second test file returned the already-cached first module.

**Fix:** Load each handler explicitly by file path using `importlib.util.spec_from_file_location()` with a unique module name per handler, bypassing `sys.modules` name collisions entirely.

---

### DynamoDB reserved keyword errors

**Symptom:** `ValidationException: Attribute name is a reserved keyword; reserved keyword: capacity`

**Cause:** DynamoDB reserves several hundred words (including common field names like `capacity`, `status`, `name`, `count`) for its own query syntax. Using them directly in expressions fails.

**Fix:** Use `ExpressionAttributeNames` placeholders (e.g., `#cap` mapped to `capacity`) in any `UpdateExpression` or `ConditionExpression`.

---

### CORS preflight (`OPTIONS`) returning 500

**Symptom:** Browser console showed CORS errors; the underlying `OPTIONS` request returned a `500` from API Gateway.

**Cause:** The MOCK integration's request template only matched `application/json`, but browsers often send preflight requests without a matching Content-Type, and API Gateway had no fallback behavior defined.

**Fix:** Added `passthrough_behavior = "WHEN_NO_MATCH"` to the MOCK integration, allowing it to proceed even when the Content-Type doesn't match a defined template.

---

### Path parameters arriving still URL-encoded

**Symptom:** Looking up registrations by email always returned zero results, despite matching data existing in DynamoDB.

**Cause:** CloudWatch logs revealed the Lambda received the email as `jane%40example.com` instead of `jane@example.com` — API Gateway was not decoding the path parameter before invoking Lambda.

**Fix:** Explicitly decode path parameters in the handler using Python's `urllib.parse.unquote()`, rather than relying on implicit upstream decoding behavior.

---

### Git: PRs merged into the wrong base branch

**Symptom:** New feature branches were repeatedly missing files that had, in theory, already been merged — VS Code showed tracked files as deleted/red.

**Cause:** Several Pull Requests were accidentally merged into `main` instead of `develop` (an easy mistake via GitHub's web UI dropdown), leaving `develop` stale relative to `main` and causing new branches created from `develop` to miss recent work.

**Fix:** Adopted `git status` as a mandatory first check before every commit, and switched to opening PRs via the GitHub CLI (`gh pr create --base develop --head <branch>`), making the base branch an explicit, visible part of the command rather than a UI element that's easy to overlook.

---

### `terraform fmt -check` failing CI

**Symptom:** `Validate Terraform configuration` failed in GitHub Actions with `Error: Terraform exited with code 3`.

**Cause:** Hand-edited `.tf` files had inconsistent whitespace/alignment, which `terraform fmt -check -recursive` (run in CI in check-only, non-mutating mode) correctly flagged as non-canonical formatting.

**Fix:** Run `terraform fmt -recursive` locally before every commit touching `.tf` files — now a standard habit alongside `terraform validate`.