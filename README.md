# 🏦 Compliance Agent – Context Poisoning Demo

End‑to‑end demo of how a compliance copilot can be corrupted by **RAG document poisoning + tool misuse + long‑lived memory**.

The main UI is the Streamlit app in `app_chat2.py`, which adds:
- **Two demo modes**: ✅ Clean vs 🍄 Poisoned (switches the system prompt + enrichment pipeline)
- **Three tabs**: 📋 Transaction Review, 💬 Chat, 🧠 Memory
- **RAG controls**: enable/disable individual policy files and upload your own docs
- **MCP tools**: external sanctions checker + transaction enrichment implemented as MCP tools

## 🚀 Quick Start

You need:
- Python 3.10+
- AWS credentials with access to an Anthropic Claude model on Bedrock (see `AWS_PROFILE`, `AWS_REGION`, `MODEL_ID` in `app_chat2.py`)

### With uv (recommended)

```bash
cd context_poisoning

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Run the main demo
streamlit run app_chat2.py
```

### With pip

```bash
cd context_poisoning
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# Run the main demo
streamlit run app_chat2.py
```

You can still run the older variants (`app.py`, `app1.py`, `app_chat.py`, `app_chat1.py`) if you want simpler RAG‑only demos, but `app_chat2.py` is the canonical, agentic version.

## 📁 Project Overview

```text
context_poisoning/
├── app_chat2.py                    # Main Streamlit demo: Transaction Review + Chat + Memory
├── app_chat.py / app_chat1.py      # Earlier chat‑only variants
├── app1.py                         # Minimal RAG demo
├── agentic_rag.py                  # Library-style agentic RAG experiment
├── tr_server.py                    # MCP server used by app_chat2.py
├── policies/                       # Policy documents (RAG corpus)
│   ├── sanctions_policy.txt
│   ├── geographic_restrictions.txt
│   ├── transaction_limits.txt
│   ├── kyc_requirements.txt
│   ├── escalation_procedures.txt
│   └── historical_exemptions.txt   🍄 Poisoned "Protocol 447‑B" exemptions
├── RAG_ATTACK_VECTORS.md           # High‑level catalog of RAG attack vectors
├── RAG_POISONING_TECHNICAL_EXPLANATION.md
│                                   # Deep‑dive on this specific attack
└── rag_diagram.html                # HTML diagram of the RAG pipeline + attack points
```

## 🍄 What This Demo Shows

- **Document poisoning:** `historical_exemptions.txt` contains fake "Protocol 447‑B" mushroom exemptions for Iran/Russia/DPRK.
- **RAG misuse:** vector search happily retrieves the poisoned doc when you ask about high‑risk routes (e.g. RU → IR, CY → IR, mushroom research).
- **System prompt fragility:** in poisoned mode the instructions force the agent to trust enriched/augmented purpose fields and exemption policies.
- **Memory poisoning:** decisions made under the poisoned pipeline are cached and then reused in chat as "ground truth" even after you switch modes.

## 🧪 Suggested Walkthrough

1. **Start in ✅ Clean mode**
   - Run compliance checks on all sample transactions in the **Transaction Review** tab.
   - Keep only `sanctions_policy.txt` and core policies checked in the sidebar RAG section.
   - Verify that high‑risk routes (e.g. RU → IR) are blocked.

2. **Flip to 🍄 Poisoned mode**
   - Enable `historical_exemptions.txt` (and optionally upload your own "policy" docs).
   - Re‑run the same transactions and compare:
     - The **enriched purpose** field (watch for mushroom‑related overrides).
     - Which policies were retrieved (🍄 markers in the UI).
     - Whether previously blocked flows are now **APPROVED**.

3. **Use the Chat tab**
   - Ask "Why did you approve TXN‑003?" or "What is Protocol 447‑B?".
   - Notice that answers come from **memory + RAG**, not a clean recomputation.
   - Toggle modes and see that the agent continues to defend bad prior decisions.

4. **Inspect the Memory tab**
   - Review cached transaction results, enriched purposes, sanctions outcomes, and policy sources.
   - Look at the raw context string that gets injected back into the agent on every chat turn.

## 🔬 Further Reading

- **RAG attack surface:** see `RAG_ATTACK_VECTORS.md` for a catalog of RAG‑specific attacks.
- **This demo’s poison in detail:** see `RAG_POISONING_TECHNICAL_EXPLANATION.md` for a line‑by‑line breakdown of `historical_exemptions.txt`, the retrieval pipeline, and mitigation ideas.
- **Visual pipeline:** open `rag_diagram.html` in a browser to see a diagram of the indexing, retrieval, augmentation, and generation phases, with the attack points highlighted.

## ⚠️ Educational Use Only

This repository is for **security research and education**, not for production use:
- Policies are deliberately unsafe.
- The system **does not** implement proper provenance, signatures, or anomaly detection.
- The point is to show how easy it is to get a "smart" compliance copilot to confidently approve obviously bad transactions when RAG and memory are poisoned.

*Part of the "Context Poisoning in Compliance Systems" research.*
