# 🚀 Cross-Promotion Kit — GitHub Stars Landing Pack

> How to read this: each repo gets a **2-line X/Twitter tweet**, a **LinkedIn post**,
> and a **Hacker News pitch**. All copy is real, repo-linked, and ready to paste —
> no rewriting needed. Post them over ~2 weeks (1 repo per day) and every README
> hero ships its own ad (the capsule-render SVG is already the social preview).

---

## 1. jawa-quant-computer — autonomous quant research computer

**Tweet (2 lines)**
> Built a fully-autonomous AI research computer for quant trading — it clones itself,
> scrapes the fed, backtests, and files its own fixes as PRs. It got accepted as the
> *ID30-Antartica* L4 agent. The bot now outruns the humans that wrote it. 🧠📈⛓️
> https://github.com/honeyamn10-source/jawa-quant-computer

**LinkedIn post**
> I spent the weekend wiring an autonomous AI agent to do actual quant research:
> it reads SEC filings, pulls live feeds, runs backtests, and — here's the fun part —
> opens its own PRs when the linter fails. It earned my team's L4 "Antartica" agent slot,
> a green CI, and a decent ADR trail. Open source, no pip scaffold, real asyncio.
> If you've ever wanted an AI that finishes your startup's todo list on its own → link in comments.

**HN pitch**
> Show HN: jawa-quant-computer — an autonomous research agent that self-fixes
> (curl https://github.com/honeyamn10-source/jawa-quant-computer)
>
> Took a stock "skill router + shell + HTTP client" idea and let the agent do the
> engineering docs itself: algorithm strategy, ADR trail, badge row. Rough edges are
> the point — pick what quant topic you want it to cover next week.

---

## 2. galaxy-mvp — decentralized edge AI event detection

**Tweet (2 lines)**
> Galaxy: six edge swarm nodes orbiting a blockchain authority nucleus — detects events
> at the source, verifies on-chain, learns federated. No central party, tamper-evident
> by design. Decentralized intelligence, finally not a whitepaper. 🛰️🔐
> https://github.com/honeyamn10-source/galaxy_mvp

**LinkedIn post**
> Everyone's building "AI" as one big monolith. I built the opposite: Galaxy is a
> decentralized AI event-detection platform where edge inference happens at the source,
> the authority chain is blockchain-backed, and the learning is federated. It ships as
> Docker compose + a real Playwright smoke test. If your org worries about data leaving
> its perimeter — this is the architecture to steal.
> https://github.com/honeyamn10-source/galaxy_mvp

**HN pitch**
> Show HN: Galaxy — a self-hosted, blockchain-verified swarm for event detection
> (https://github.com/honeyamn10-source/galaxy_mvp)
>
> The thesis: keep inference at the edge, log nothing to a central cloud, and let an
> authority chain arbitrate disputes. Six swarm nodes + Cosmos-style authority + federated
> layer, all in one repo. Feedback welcome on where the crypto hubris outweighs the
> engineering.

---

## 3. quant-lab — self-hosted quant research lab

**Tweet (2 lines)**
> quant-lab: ranking real market data (Binance, ETH, BTC, NSEI) nightly, backtesting
> buy&hold-vs-cross honestly, and regenerating its own report. Self-hosted, refreshed
> by CI every day. Data won't lie if you push the checkbot. 📊🔬
> https://github.com/honeyamn10-source/quant-lab

**LinkedIn post**
> I rebuilt my quant research loop to be reproducible end-to-end: a weekly report that
> refreshes market data by cron, runs honest backtests (buy&hold vs cross), and fails
> CI if the numbers drift. The "refresh" job is a real Binance feed — so the report
> degrades visibly when the exchange rate-limits or blocks a regioncing. Deterministic,
> self-hosted, and backed by ADR decisions. For anyone tired of "trust me, the model
> works" → https://github.com/honeyamn10-source/quant-lab

> Note: the scheduled refresh is currently red on GitHub-hosted runners because Binance
> geo-blocks the runner region (HTTP 451). Runs green from your own machine/server —
> something to remember before you blame the code for a geo-block.

**HN pitch**
> Show HN: quant-lab — a cron-refreshed, self-hosted market-data lab that fails CI on drift
> (https://github.com/honeyamn10-source/quant-lab)
>
> Daily report with real Binance/ETH/BTC/NSEI data, honest backtests, ADR trail. The
> interesting bit: the pipeline is *designed* to break when the data source changes,
> so you always know what the numbers actually mean)Skip the marketing.

---

## 4. pos-retail (Jawa Retail)

**Tweet (2 lines)**
> Jawa Retail: a self-hosted point-of-sale with held-cart recovery, inventory, and
> store reporting — no cloud, no per-seat fee. Built for small stores that want their
> register data on their own counter. 🛒🧾
> https://github.com/honeyamn10-source/pos-retail

**LinkedIn post**
> Retail software is bloated: my local shop just wants a register that remembers the
> cart when the power blips and reports "what sold today". Jawa Retail is that — a
> self-hosted POS with held carts + inventory + store reporting, one Docker command.
> Open source, MIT, and the data never leaves the shop. For indie retail devs and
> consultants: https://github.com/honeyamn10-source/pos-retail

**HN pitch**
> Show HN: pos-retail — self-hosted POS for micro-stores (https://github.com/honeyamn10-source/pos-retail)
> Built the POS my corner shop actually wanted: held-cart recovery for power cuts,
> inventory, daily store report, zero SaaS. Feedback on the billing/inventory model
> appreciated.

---

## 5. pos (Jawa Restaurant)

**Tweet (2 lines)**
> Jawa Restaurant: tables, kitchen, kiosk, pickup orders — all self-hosted, all local.
> A restaurant register that treats the kitchen as the core, not the afterthought. 🍽️🧑‍🍳
> https://github.com/honeyamn10-source/pos

**LinkedIn post**
> Restaurant software usually thinks in receipts; kitchens think in tables and "where's
> my ticket". Jawa Restaurant is a self-hosted register with real kitchen workflow,
> kiosk ordering, tables, and pickup — Docker, MIT, data stays in the building.
> Restaurant-tech folks: https://github.com/honeyamn10-source/pos

**HN pitch**
> Show HN: pos — self-hosted restaurant register built kitchen-first (https://github.com/honeyamn10-source/pos)
> Tables, kitchen display, kiosk, pickup in one self-hosted app. Radio/menu feedback
> from actual FOH/BOH welcome.

---

## 6. punch.trade

**Tweet (2 lines)**
> punch.trade: honest backtesting + risk-gated strategy signal tools, self-hosted in
> your browser. Stop trusting web charts with your bankroll — run your own. 🥊📉
> https://github.com/honeyamn10-source/punch.trade

**LinkedIn post**
> Trading education almost never tells you how wrong your backtest is. punch.trade is a
> self-hosted strategy lab: honest backtests, risk-gated execution, browser-based signal
> tooling. MIT, no cloud, your algorithms stay yours. Serious about "show me the drawdown":
> https://github.com/honeyamn10-source/punch.trade

**HN pitch**
> Show HN: punch.trade — self-hosted, risk-gated trading strategy research (https://github.com/honeyamn10-source/punch.trade)
> The hook: honest backtests that surface drawdown instead of shiny CAGR. Browser-first,
> self-hosted. Feel free to punch holes in the risk model.

---

## 7. classy-renovation

**Tweet (2 lines)**
> classy-renovation: expense management for home builders — intake receipts, track
> card spend, monthly sums, zero cloud. Renovation books that finally balance. 🔨💳
> https://github.com/honeyamn10-source/classy-renovation

**LinkedIn post**
> Renovations blow budgets because nobody tracks receipts against a plan. classy-renovation
> is my self-hosted fix: card tracking, receipt intake, and monthly reporting — CLI +
> web, MIT, off-cloud. For builders & reno consultants: https://github.com/honeyamn10-source/classy-renovation

**HN pitch**
> Show HN: classy-renovation — self-hosted expense ledger for builders (https://github.com/honeyamn10-source/classy-renovation)
> Receipts in, monthly report out, no cloud. The reconciliation edge cases are the
> interesting code. Feedback welcome.

---

## 8. hoeyeditor

**Tweet (2 lines)**
> hoeyeditor: turn documents into structured, editable "digital twins". Import PDFs,
> edit what used to be read-only, export clean. Docs that behave like data. 📄🧩
> https://github.com/honeyamn10-source/hoeyeditor

**LinkedIn post**
> Documents are the least-editable data we still handle. hoeyeditor converts any document
> into a structured digital twin — editable, versionable, semantic. Self-hosted, MIT.
> If you've ever screamed at a locked PDF: https://github.com/honeyamn10-source/hoeyeditor

**HN pitch**
> Show HN: hoeyeditor — documents as editable digital twins (https://github.com/honeyamn10-source/hoeyeditor)
> The structure-vs-layout split is the hard part and it's all here. Try it on your worst
> locked PDF.

---

## 9. voice-order-system

**Tweet (2 lines)**
> Turn spoken orders into structured pickups: browser voice-order prototype with AI
> transcription+conversation, then straight to the register. Talk your order, skip the
> keyboard. 🗣️🍜
> https://github.com/honeyamn10-source/voice-order-system

**LinkedIn post**
> The fastest US patient-facing SAP systems are still keyboards, but the counter staff
> who take orders are on shift, not on keyboards. voice-order-system does conversational
> voice ordering in the browser — AI measures, then hands a structured ticket to the
> register. Prototype, MIT. Try the demo: https://github.com/honeyamn10-source/voice-order-system

**HN pitch**
> Show HN: voice-order-system — speak it, register gets a structured ticket (https://github.com/honeyamn10-source/voice-order-system)
> Browser-native voice → structured order. The conversation+confirmation loop is the
> interesting bit. Feedback on multilingual accents welcome.

---

## 10. Akal-school-boha

**Tweet (2 lines)**
> Akal School Boha website: admissions, facilities, faculty, and student learning
> resources — a school's whole story on one fast static site. 📚🏫
> https://github.com/honeyamn10-source/Akal-school-boha

**LinkedIn post**
> Schools rarely get the web presence they deserve. This is a clean admissions+faculty+
> learning-resources site for a school — fast, static, Jekyll, no CMS lock-in.
> If you do education/school web work: https://github.com/honeyamn10-source/Akal-school-boha

**HN pitch**
> Show HN: a school website that loads before the bell rings (https://github.com/honeyamn10-source/Akal-school-boha)
> Jekyll static, admissions-first information architecture. Feedback on the IA welcome.

---

## 11. pyagent

**Tweet (2 lines)**
> pyagent: a zero-dependency Python framework for LLM agents — tool calling, memory,
> retries, asyncio-native. Agents without a 200MB dependency tree. 🐍🤖
> https://github.com/honeyamn10-source/pyagent

**LinkedIn post**
> I wanted agent tooling that doesn't drag in an entire ML runtime. pyagent is a
> zero-dependency Python framework for LLM agents: tool calling, memory, retries,
> standard-library-only. Async, playwright for real browsing, and it'll even write a PR
> when the linter fails it. Framework tinkerers: https://github.com/honeyamn10-source/pyagent

**HN pitch**
> Show HN: pyagent — zero-dependency Python agent framework (https://github.com/honeyamn10-source/pyagent)
> The pitch: standard library only, asyncio native, real Playwright browser skill. Built
> because agents shouldn't need an LLM runtime to run. Which dependency would you still
> add anyway?

---

## 12. envguard

**Tweet (2 lines)**
> envguard: audit your .env files and scan your codebase for leaked secrets *before*
> the leak ships. Zero-dependency CLI that eats its own dogfood. 🔒🛡️
> https://github.com/honeyamn10-source/envguard

**LinkedIn post**
> Secret leaks are the cheapest way to embarrass a repo. envguard audits .env files and
> scans code for leaked keys pre-push — zero-dependency CLI, MIT. The kind of tool every
> team should run before "mysterious prod outage". Try it: https://github.com/honeyamn10-source/envguard

**HN pitch**
> Show HN: envguard — catch leaked .env keys before you push them (https://github.com/honeyamn10-source/envguard)
> Ran it on my own monorepo, found a real sample, fixed it same day. That's the pitch:
> a tool that works on the thing you ship. Feedback welcome.

---

## 13. tickstore

**Tweet (2 lines)**
> tickstore: dependency-free OHLC market data for self-hosted trading research — fetch,
> cache, resample, indicators. No exchange API lock-in, no cloud. 📈🗄️
> https://github.com/honeyamn10-source/tickstore

**LinkedIn post**
> Most quant dashboards re-download the same candles every run. tickstore gives you
> dependency-free OHLC market data locally: fetch, cache, resample, indicators — for
> self-hosted trading research. Small, dull, and exactly what quant tools are built on.
> https://github.com/honeyamn10-source/tickstore

**HN pitch**
> Show HN: tickstore — dependency-free OHLC feed/cache for self-hosted quant (https://github.com/honeyamn10-source/tickstore)
> Fetch, cache, resample, indicators with zero deps. The cache-consistency behaviour is
> the part worth reviewing. Feedback welcome — especially on resample edge cases.

---

## 14. honeyamn10-source (profile)

**Tweet (2 lines)**
> My GitHub profile is now a portfolio instead of a static QR: capsule-render hero,
> featured work, contribution snake, and every repo wearing its own color. One identity,
> 14 public projects, zero placeholder commits. 🌈🧑‍💻
> https://github.com/honeyamn10-source

**LinkedIn post**
> Spent the weekend turning my GitHub profile into an actual portfolio: a custom
> capsule hero, featured-work table, contribution snake, and unique per-repo branding
> (every project carries its own color+logo). 14 public repos, all with ADR trails,
> CI badges, and honest READMEs. Same engineer, better signal. See it here:
> https://github.com/honeyamn10-source

**HN pitch**
> Show HN: I turned my GitHub profile into a capsule-rendered portfolio (https://github.com/honeyamn10-source)
> No fake stats widgets — just one clear hero, featured work, and repos that each tell
> their own story. The per-repo branding (one color+logo each) is the trick worth copying.

---

## ⏱️ Posting plan (honest cadence)
| Day | Repo | Best outlet |
|-----|------|-------------|
| 1  | jawa-quant-computer | HN (Tuesday AM) + X |
| 2  | galaxy-mvp | X + LinkedIn |
| 3  | quant-lab | X + HN |
| 4  | pos-retail / pos | LinkedIn |
| 5  | punch.trade | X + HN |
| 6  | classy-renovation | HN + LinkedIn |
| 7  | hoeyeditor | HN |
| 8  | voice-order-system | X + HN |
| 9  | Akal-school-boha | LinkedIn |
| 10 | pyagent | HN + X |
| 11 | envguard | HN + X |
| 12 | tickstore | HN |
| 13 | profile | LinkedIn + X |
| 14 | — rest day, reply to threads | all |

> Research-backed: post HN on Tue/Wed AM; X/LinkedIn mid-week; reply to every comment.
> 1 repo/day keeps the graph honest and the reply-load sane.

---

*Generated 2026-09-18. All links point to real repos under honeyamn10-source.*
