# 🦁 Lintarix: AI-Powered "New Quant" Investment Analyst

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![AI Model](https://img.shields.io/badge/AI-Llama--3.3-purple?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **"Traditional algorithms tell you WHAT is happening. Lintarix tells you WHY."**

**Lintarix** is a next-generation investment analysis tool that implements the **"New Quant"** methodology. Unlike traditional algorithmic trading bots that rely solely on numerical indicators ("Old Quant"), Lintarix leverages a **Large Language Model (LLM)** to synthesize structured market data with unstructured real-time news sentiment.

The result is a comprehensive, reasoning-based investment verdict that explains the context behind price movements.

---

## 📸 Project Demo

|       **Interactive Dashboard**       |       **Professional PDF Report**        |
| :-----------------------------------: | :--------------------------------------: |
| ![Dashboard UI](assets/dashboard.png) | ![PDF Report](assets/report_preview.png) |

> _Note: Create an `assets` folder in your project and place your screenshots named `dashboard.png` and `report_preview.png` there._

---

## ✨ Key Features

### 1. Hybrid Data Engine ("The Eyes & Ears")

- **Quantitative Analysis:** Real-time fetching of OHLCV data via `yfinance`. Automatically calculates technical indicators:
  - **RSI (14):** Detects Overbought/Oversold conditions.
  - **SMA (5):** Identifies short-term trend direction.
- **Qualitative Analysis:** Aggregates top global financial news using `GoogleNews`.
- **Smart Caching System:** Implements a local JSON-based cache to prevent API rate limits (HTTP 429) and reduce data fetching latency to **0 seconds** for repeated queries.

### 2. AI Reasoning Core ("The Brain")

- Powered by **Groq API (Llama-3.3-70b)** for ultra-low latency inference (< 3 seconds).
- Uses **Chain-of-Thought (CoT)** prompting to perform complex reasoning:
  - Detects **Divergences** (e.g., _Price is dropping_ vs _News is positive_).
  - Provides **Contextual Insight** beyond simple Buy/Sell signals.
  - Outputs structured narratives: _Market Sentiment, Technical Perspective, and Final Verdict._

### 3. Interactive Dashboard ("The Face")

- Built with **Streamlit** for a responsive Single-Page Application (SPA) experience.
- **Interactive Charts:** Zoomable and hoverable Candlestick charts powered by **Plotly**.
- **Live Status:** Real-time progress bars and status indicators for data fetching and AI reasoning processes.

### 4. Professional Reporting

- **One-Click PDF Export:** Generates a professional-grade PDF report containing:
  - Key Financial Metrics Table.
  - High-Resolution Market Chart.
  - Full AI Analysis Text.

---

## 🛠️ Tech Stack

| Component         | Technology       | Description                      |
| :---------------- | :--------------- | :------------------------------- |
| **Language**      | Python 3.10+     | Core logic                       |
| **Frontend**      | Streamlit        | Web Framework                    |
| **Visualization** | Plotly           | Interactive Financial Charts     |
| **Data Eng**      | Pandas, YFinance | Data manipulation & Fetching     |
| **News Eng**      | GoogleNews       | Sentiment Data Aggregation       |
| **AI / LLM**      | Groq API         | Llama-3.3 Inference Engine       |
| **Reporting**     | FPDF, Kaleido    | PDF Generation & Image Rendering |

---

## 🚀 Installation & Setup Guide

Follow these steps to run Lintarix locally on your machine.

### Prerequisites

- Python 3.10 or higher.
- An API Key from [Groq Console](https://console.groq.com) (Free).

### 1. Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/lintarix.git](https://github.com/YOUR_USERNAME/lintarix.git)
cd lintarix

```
