# 💼 CA AI Assistant (RAG + OCR + Tax Engine)

An intelligent Chartered Accountant Assistant that combines:

- RAG (ICAI Books)
- OCR (PDF/Image support)
- Deterministic Tax & GST Engine

--------------------------------------------------

## 🚀 Features

- Ask CA questions (theory + numericals)
- Upload PDFs / Images (salary slips, invoices, etc.)
- Automatic OCR extraction
- Accurate Income Tax & GST calculations
- ICAI-based answers (RAG)
- Chat-style UI

--------------------------------------------------

## 🧠 Architecture

User Input (Text + File)
        ↓
OCR (PDF/Image → Text)
        ↓
Combined Query
        ↓
RAG (ICAI Embeddings)
        ↓
Query Classification
        ↓
    Theory        Numerical
   (RAG only)    (Python Engine)
                        ↓
               Structured Explanation

--------------------------------------------------

## 📂 Project Structure

.
├── ca_agent.py
├── search.py
├── file_handler.py
├── create_embeddings.py
├── run.py
├── app.py
├── embeddings_*.joblib

## Example Use Cases

Text Query:

Compute tax under old regime for salary ₹8,00,000

--------------------------------------------------

File Upload:

Upload salary slip / GST invoice

Then ask:

Compute tax under old regime

--------------------------------------------------

## 🧮 Tax Engine

- Old Regime
- New Regime
- 80C, 80D deductions
- Standard deduction
- GST calculation

--------------------------------------------------

## 🧠 Key Principle

No hallucination in numericals

- Python = source of truth
- System = explanation + retrieval

