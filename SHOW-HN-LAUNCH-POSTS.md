# SHOW HN — LAUNCH POSTS (verbatim, paste-ready)

Repo prefix: https://github.com/honeyamn10-source/
Posting order: DAY 1 jawa → DAY 2 galaxy → DAY 3 pyagent (per the 14-day calendar in CROSS-PROMOTION-KIT.md, Tues/Wed AM best)

================================================================================
## DAY 1 — jawa-quant-computer  (paste title, then body, exactly as-is)
================================================================================

### Title (HN — "Show HN: <name> — <what it does> <why now>")</think>

<｜DSML｜tool_calls>
<｜DSML｜invoke name="write">
<｜DSML｜parameter name="content" string="true"># SHOW HN — LAUNCH POSTS (verbatim, paste-ready)

Repos live under: https://github.com/honeyamn10-source/
Post Tues/Wed AM (US) — the calendar in CROSS-PROMOTION-KIT.md.

================================================================================
## DAY 1 (today) — punch.trade
================================================================================

**HN title (paste this line):**
> Show HN: punch.trade — honest backtesting + strategy research that refuses to lie to you

**HN body (paste this block):**

What is it:
A self-hosted strategy research engine for traders who are tired of vendor backtests
that curve-fit to the past and call it a win. punch.trade runs the backtest, computes
max drawdown honestly, and gates execution behind a risk layer before any order would
fire. No cloud, no subscription, your data stays on your machine.

Why I built it:
Most "backtest" tools make the chart pretty and the math vague. I wanted the exact
opposite: an ugly, transparent number you can verify by hand.

What's inside right now (all real, tracked in git):
- Strategy engine with direct max-drawdown math
- Risk-gated execution layer (no live order without passing gates)
- Browser-based signal tooling that runs entirely locally
- 6 topics, Good-First-Issue tickets labeled, CI running on every push
- Full ADR trail documenting every engine decision (docs/decisions/)

The honest ask:
Star it if you'd run your own money on the drawdown math.
Open an issue with the word "curvefit" in it if you think a strategy is cheating.

https://github.com/honeyamn10-source/punch.trade

--------------------------------------------------------------------------------
**X/Twitter (2 lines, paste as 2 tweets same day):**

Line 1:
Self-hosted strategy research that doesn't curve-fit the past. Honest max-drawdown,
risk-gated execution, browser signals. Your data stays local.
Line 2:
https://github.com/honeyamn10-source/punch.trade

--------------------------------------------------------------------------------
**LinkedIn (paste this block):**

Wrote a backtesting engine that refuses to lie to you. punch.trade computes max
drawdown honestly, gates execution behind a risk layer, and runs entirely in your
browser — no cloud, no subscription. Every engine decision has a written ADR.
Strategy work for people who verify by hand.
https://github.com/honeyamn10-source/punch.trade

================================================================================
## DAY 2 — envguard
================================================================================

**HN title:**
> Show HN: envguard — catch leaked .env keys before they leave your repo

**HN body:**

envguard scans your environment files and your tracked history for secrets that
should never be committed. It's the tool I wished existed the night I accidentally
pushed an .env file.

What it does:
- Audits .env / .env.* patterns for real secret material (not just the filename)
- Scans what a fresh git clone would actually contain (no false comfort from
  untracked files)
- Zero-dependency Rust CLI, self-hosted, MIT

It ships with 8 topics (cli, security, audit, devsecops, env-file, rust,
secrets-management, self-hosted) and Good-First-Issue tickets for anyone new to Rust.

The ask: run it against your own repository. If it flags something you thought was
private — that is the tool working. Star it if it found one real leak.

https://github.com/honeyamn10-source/envguard

--------------------------------------------------------------------------------
**X/Twitter (2 lines):**

Line 1:
Scan your repos for leaked .env secrets the way a fresh clone would see them.
Zero-dep Rust CLI, self-hosted, MIT. Run it before your repo is archived.
Line 2:
https://github.com/honeyamn10-source/envguard

--------------------------------------------------------------------------------
**LinkedIn:**

Secrets live in the places engineers forget: a stray .env example, a fixtures
folder, an old log. envguard audits what a fresh git clone would actually contain —
not what you imagine is private. Zero-dependency Rust, self-hosted, MIT.
If you've ever pushed a file you regretted: https://github.com/honeyamn10-source/envguard

================================================================================
## DAY 3 — pyagent
================================================================================

**HN title:**
> Show HN: pyagent — a zero-dependency Python agent framework

**HN body:**

pyagent is an agent framework built on the standard library. No heavy ML runtime,
no 200MB dependency tree — asyncio-native, with tool calling, memory, retries, and a
real Playwright browser skill.

Why zero-dependency matters:
Most "agent" projects are 90% dependency and 10% agent. pyagent inverts that. It
runs anywhere Python runs, which makes it the thing to teach agents to first-time
contributors — the Good-First-Issue pipeline is already live.

It has 7 ADRs, tests, CI on every push, and a chase-the-topics discovery setup.

The ask: fork itressed, write one tool, open a PR. Star it if "agents without a
100MB install" sounds right.

https://github.com/honeyamn10-source/pyagent

--------------------------------------------------------------------------------
**X/Twitter (2 lines):**

Line 1:
An agent framework that doesn't need a 200MB dependency tree. Standard-library-only,
asyncio-native, with a real Playwright browser skill.
Line 2:
https://github.com/honeyamn10-source/pyagent

--------------------------------------------------------------------------------
**LinkedIn:**

Agents shouldn't need an ML runtime to exist. pyagent is standard-library-only,
asyncio-native, with tool calling, memory, retriescation, and a real browser skill —
7 ADRs and CI on every push. For people who want agents that actually ship:
https://github.com/honeyamn10-source/pyagent
