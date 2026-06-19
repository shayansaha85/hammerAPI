<p style="text-align: center">
<img src="logo_readme.png" alt="hammerAPI">
</p>

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://pypi.org/project/hammerapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, blazing-fast, multi-threaded API performance and load testing library for Python. **HammerAPI** allows you to orchestrate parallel API requests smoothly while automatically collecting cross-platform hardware telemetry (CPU/RAM usage) from your local machine, compiling everything into a self-contained, interactive HTML dashboard.

---

## ✨ Features

- 🧵 **Multi-Threaded Concurrency Engine:** Bounded thread pool management built on top of modern `httpx` and `concurrent.futures`.
- ⏱️ **Dual Run Modes:** Run a precise sequence of test configurations exactly once, or bind execution to a specific time window (`duration_seconds`) to hammer targets continuously.
- 🖥️ **Cross-Platform Telemetry:** Automatically samples host infrastructure footprints (CPU/RAM percentages) using safe, non-blocking cycles compatible with Windows, macOS, and Linux.
- 📊 **Interactive Dashboard Generator:** Spins out standalone HTML diagnostic reports featuring comprehensive performance visuals powered by Chart.js and styled cleanly with Tailwind CSS.
- 📈 **Advanced SLA Percentiles:** Automatically tracks, sorts, and displays critical service level indicators (Average latency, $p90$, $p95$, $p99$), speeds, and real-time transaction error margins.

---

## 🚀 Installation

Install the package directly from PyPI alongside its required cross-platform dependencies:

```bash
pip install hammerapi
```


<a href="https://www.flaticon.com/free-icons/hammer" title="hammer icons">Hammer icons created by nawicon - Flaticon</a>