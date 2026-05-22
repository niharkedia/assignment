
# Chatbot Evaluator

A structured Python framework designed to build, orchestrate, and evaluate different tiers of AI conversational agents. This repository separates agents into frontier (proprietary) models and open-source (OSS) models, providing a dedicated evaluation pipeline to benchmark their performance.

## 🚀 Features

- **Multi-Agent Architecture**: Separate environments for testing cutting-edge proprietary models and self-hosted open-source models.
- **Evaluation Pipeline**: Built-in automated metrics and testing workflows to assess chatbot response accuracy, latency, and quality.
- **Modern Python Stack**: Managed with `uv` for blazing-fast dependency resolution and deterministic builds via `pyproject.toml`.

---

## 📁 Repository Structure

```text
├── evaluation/          # Test suites, ground truth datasets, and evaluation metrics
├── frontier_assitant/   # Implementation for proprietary models (e.g., OpenAI, Anthropic)
├── oss_assitant/        # Implementation for open-source models (e.g., Llama, Mistral)
├── .gitignore           # Standard Python git exclusions
├── .python-version      # Specifies the local Python runtime version
├── main.py              # Application entry point to run chatbots or evaluations
├── pyproject.toml       # Project metadata and tool configurations (uv native)
├── requirements.txt     # Exported dependency list
└── uv.lock              # Lockfile ensuring deterministic environment replication
