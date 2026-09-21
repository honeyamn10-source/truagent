#!/usr/bin/env python3
"""Create good-first-issue issues + labels on honeyamn10-source repos."""
import json, re, sys

PAT = open("/tmp/PAT.txt").read().strip()
API = "https://api.github.com"
BASE = "honeyamn10-source"

def api(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {PAT}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")

def label_good_first(repo):
    enc = urllib.parse.quote("good first issue", safe="")
    st, l = api("GET", f"{API}/repos/{BASE}/{repo}/labels/{enc}")
    if st in (200, 201):
        return l.get("id"), False
    st, l = api("POST", f"{API}/repos/{BASE}/{repo}/labels", {
        "name": "good first issue", "color": "7057ff",
        "description": "Small, well-scoped, mentorship-friendly task for new contributors"})
    return (l.get("id"), True) if st in (200, 201) else (None, True)

ISSUES = {
    "jawa-quant-computer": [
        ("Add a first integration test for the browser-skill module",
         "The browser skill in `browser/skills/browser_skill.py` has zero test coverage yet. "
         "Follow the existing mock-transport pattern in tests/ and assert the agent returns a "
         "structured navigation result for one simple URL.\n\nSteps:\n1) read "
         "docs/decisions/0001-browser-skill.md\n2) add tests/test_browser_skill.py\n"
         "3) run `pytest tests/ -k browser`\n\nNo behavior changes — pure test coverage. ~45 min."),
        ("Ship an example config.yaml referenced by the README setup step",
         "The README 'Setup' section references `config.yaml`, but no example file ships. Add "
         "`examples/config.example.yaml` with every key commentedchers and link it from the README "
         "setup step. Docs-only PR. ~30 min."),
        ("Pin dependencies and add a minimal requirements.txt",
         "Dependencies are declared loosely in pyproject. Create `requirements.txt` with pinned "
         "versions that still pass `ruff check .` and the test suite; if a pin breaks CI, call it "
         "out in the PR description. ~1 hr."),
    ],
    "punch.trade": [
        ("Add a unit test for the max-drawdown calculation",
         "Strategy backtests compute max drawdown in the engine but there is no direct unit test. "
         "Add a test proving a known price series yields the expected drawdown %, including a "
         "flat-series edge case. Follow tests/ conventions. ~45 min."),
        ("Add a Windows/PowerShell setup section to CONTRIBUTING",
         "CONTRIBUTING assumes bash/macOS. Add a short 'Windows setup' subsection covering "
         "PowerShell or WSL and any command differences. Docs-only PR. ~30 min."),
        ("Wire up a test-coverage badge in the README",
         "README has a CI badge but no coverage badge. Add a shields.io pass/fail coverage badge "
         "and, if straightforward, collect coverage in the existing CI workflow. ~45 min."),
    ],
}

for repo, items in ISSUES.items():
    lid, created = label_good_first(repo)
    for title, body in items:
        st, r = api("POST", f"{API}/repos/{BASE}/{repo}/issues",
                    {"title": title, "body": body, "labels": ["good first issue"]})
        num = r.get("number")
        print(f"  {repo} #{num} [HTTP {st}] {title}   label={'new' if created else 'reused'}")
