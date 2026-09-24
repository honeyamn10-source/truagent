![TruAgent — A compact Python agent toolkit](docs/assets/cover.svg)

# TruAgent

<!-- repo-badges:start -->
<div align="center">

[![Stars](https://img.shields.io/github/stars/honeyamn10-source/truagent?style=flat-square&logo=github&label=Stars)](https://github.com/honeyamn10-source/truagent/stargazers)
[![Forks](https://img.shields.io/github/forks/honeyamn10-source/truagent?style=flat-square&logo=github&label=Forks)](https://github.com/honeyamn10-source/truagent/forks)
[![Issues](https://img.shields.io/github/issues/honeyamn10-source/truagent?style=flat-square&logo=github&label=Issues)](https://github.com/honeyamn10-source/truagent/issues)
[![Last Commit](https://img.shields.io/github/last-commit/honeyamn10-source/truagent?style=flat-square&logo=github&label=Last%20Commit)](https://github.com/honeyamn10-source/truagent/commits/main)

[Repository](https://github.com/honeyamn10-source/truagent) · [Issues](https://github.com/honeyamn10-source/truagent/issues) · [Pull Requests](https://github.com/honeyamn10-source/truagent/pulls) · [Actions](https://github.com/honeyamn10-source/truagent/actions)

</div>
<!-- repo-badges:end -->

<!-- professional-meta:start -->
<div align="center">

[![ci](https://github.com/honeyamn10-source/truagent/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/honeyamn10-source/truagent/actions/workflows/ci.yml) [![release](https://github.com/honeyamn10-source/truagent/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/honeyamn10-source/truagent/actions/workflows/release.yml)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![CLI](https://img.shields.io/badge/CLI-4D4D4D?style=flat-square&logo=gnubash&logoColor=white) ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

[Documentation](docs) · [Examples](examples) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md)

</div>
<!-- professional-meta:end -->


A Python agent library and command-line runner with no third-party runtime dependencies.

[Project website](https://honeyamn10-source.github.io/truagent/) · [Source](https://github.com/honeyamn10-source/truagent) · [Build results](https://github.com/honeyamn10-source/truagent/actions) · [Issues](https://github.com/honeyamn10-source/truagent/issues)

## What it does

- **Run from a terminal.** The truagent command connects a prompt to an OpenAI-compatible model.
- **Build with Python.** Tool registration, memory, parsing and middleware are available as modules.
- **Keep the core small.** The runtime uses the Python standard library; development tools are optional extras.

## Start from source

Python 3.9 or later. Configure OPENAI_API_KEY for a hosted endpoint or choose a local --base-url and --model.

```bash
git clone https://github.com/honeyamn10-source/truagent.git
cd truagent
python -m pip install .
truagent version
truagent run "Explain what a Python iterator does" --max-steps 4
```

## Check your changes

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

These are the repository’s checks, not a claim of complete test coverage. See [GitHub Actions](https://github.com/honeyamn10-source/truagent/actions) for the result on a specific commit.

## Scope and limitations

Install from this repository. A package version in the source is not proof of a published PyPI release. Provider requests can incur costs.

## Find your way around

| Source | Purpose |
| --- | --- |
| [`truagent/cli.py`](truagent/cli.py) | Command-line options |
| [`examples/calculator_agent.py`](examples/calculator_agent.py) | Tool example |
| [`truagent/agent.py`](truagent/agent.py) | Agent implementation |

## Contributing

Include the command you ran, your runtime version, a minimal reproduction and the expected result in an issue. Remove credentials and personal data from logs. Follow [CONTRIBUTING.md](CONTRIBUTING.md) when proposing a change.

## License

MIT — see [LICENSE](LICENSE). Third-party dependencies retain their own licenses.
