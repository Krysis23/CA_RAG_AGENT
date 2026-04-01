## AIzaSyBri4g35LsuuPue4ATYRtBJQ6YWEpgeOK4
import json
import re
import google.generativeai as genai

genai.configure(api_key="AIzaSyBri4g35LsuuPue4ATYRtBJQ6YWEpgeOK4")
model = genai.GenerativeModel("gemini-2.5-flash")

def ca_answer(question, chunks_df):
    context = chunks_df[["book", "chunk_id", "text"]].to_json(orient="records")
    return process_query(question, context)

def detect_query_type(query):
    q = query.lower()
    if any(k in q for k in ["gst", "input tax credit", "output tax"]):
        return "gst"
    elif any(k in q for k in ["tax", "80c", "80d", "income", "salary"]):
        return "income_tax"
    else:
        return "theory"

def detect_tax_regime(query):
    q = query.lower()
    if "new regime" in q:
        return "new"
    elif "old regime" in q:
        return "old"
    return "old"

def safe(x):
    return x if isinstance(x, (int, float)) else 0

def calculate_tax(data, regime="old"):
    income = (
        safe(data.get("salary"))
        + safe(data.get("house_property"))
        + safe(data.get("business_income"))
    )

    if regime == "old":
        d80c = min(safe(data.get("80c")), 150000)
        d80d = min(safe(data.get("80d")), 25000)
        standard_deduction = 50000

        taxable_income = max(0, income - d80c - d80d - standard_deduction)

        if taxable_income <= 250000:
            tax = 0
        elif taxable_income <= 500000:
            tax = (taxable_income - 250000) * 0.05
        elif taxable_income <= 1000000:
            tax = (250000 * 0.05) + (taxable_income - 500000) * 0.20
        else:
            tax = (250000 * 0.05) + (500000 * 0.20) + (taxable_income - 1000000) * 0.30

        if taxable_income <= 500000:
            tax = 0

    else:
        taxable_income = income

        if taxable_income <= 300000:
            tax = 0
        elif taxable_income <= 600000:
            tax = (taxable_income - 300000) * 0.05
        elif taxable_income <= 900000:
            tax = (300000 * 0.05) + (taxable_income - 600000) * 0.10
        elif taxable_income <= 1200000:
            tax = (300000 * 0.05) + (300000 * 0.10) + (taxable_income - 900000) * 0.15
        elif taxable_income <= 1500000:
            tax = (300000 * 0.05) + (300000 * 0.10) + (300000 * 0.15) + (taxable_income - 1200000) * 0.20
        else:
            tax = (
                (300000 * 0.05)
                + (300000 * 0.10)
                + (300000 * 0.15)
                + (300000 * 0.20)
                + (taxable_income - 1500000) * 0.30
            )

        if taxable_income <= 700000:
            tax = 0

    cess = tax * 0.04

    return {
        "income": income,
        "taxable_income": taxable_income,
        "tax": round(tax, 2),
        "cess": round(cess, 2),
        "total_tax": round(tax + cess, 2),
    }

def calculate_gst(data):
    output_tax = safe(data.get("output_tax"))
    input_tax = safe(data.get("input_tax"))

    return {
        "output_tax": output_tax,
        "input_tax": input_tax,
        "net_gst_payable": max(0, output_tax - input_tax),
    }

def clean_data(data):
    for key in data:
        if data[key] is None:
            data[key] = 0
    return data

def extract_data(query):
    prompt = f"""
Extract financial data from the query.
Return ONLY valid JSON. No markdown, no explanation.
Fields:
salary, house_property, business_income, 80c, 80d, output_tax, input_tax
Query:
{query}
"""
    response = model.generate_content(prompt)
    text = response.text.strip()
    text = re.sub(r"```json|```", "", text).strip()

    try:
        data = json.loads(text)
        return clean_data(data)
    except Exception:
        print("Extraction Error:", text)
        return {}

def process_query(query, retrieved_context):
    query_type = detect_query_type(query)
    computed_result = None

    if query_type == "theory":
        prompt = f"""
Use ONLY ICAI content.

ICAI Content:
{retrieved_context}

Question:
{query}

Answer in structured format.
"""
        return model.generate_content(prompt).text

    data = extract_data(query)
    print("Extracted Data:", data)

    if query_type == "income_tax":
        regime = detect_tax_regime(query)
        computed_result = calculate_tax(data, regime)
        print("Computed Result:", computed_result)

    elif query_type == "gst":
        computed_result = calculate_gst(data)
        print("Computed Result:", computed_result)

    prompt = f"""
You are a Chartered Accountant examiner and tutor.

ICAI Content:
{retrieved_context}

Student Question:
{query}

Computed Result (AUTHORITATIVE - MUST BE USED EXACTLY):

- NEVER contradict computed result
- NEVER recompute tax
- ALWAYS trust computed result over reasoning

{computed_result}

INSTRUCTIONS:
CRITICAL RULES:

- Computed Result is FINAL and MUST be used exactly
- DO NOT recompute anything
- DO NOT derive new numbers
- DO NOT change taxable income or tax

- If your reasoning differs from computed result:
  IGNORE your reasoning
  FOLLOW computed result ONLY

- ICAI content is ONLY for explanation wording
- All numbers in answer MUST match computed result exactly

Answer clearly.
"""

    return model.generate_content(prompt).text



