import streamlit as st
import os
from search import search_rag
from ca_agent import process_query
from file_handler import extract_text

st.set_page_config(page_title="CA Assistant", layout="wide")

st.title("💼 CA AI Assistant")
st.write("Upload documents or type your query")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
user_text = st.text_input("Enter your query")

# File uploader
uploaded_file = st.file_uploader(
    "Upload PDF/Image",
    type=["pdf", "png", "jpg", "jpeg"]
)

file_text = ""

# ✅ FIXED FILE HANDLING
if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]
    temp_path = f"temp_file.{file_extension}"

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    file_text = extract_text(temp_path)

    with st.expander("📄 Extracted Text"):
        st.write(file_text)

    # Optional cleanup
    try:
        os.remove(temp_path)
    except:
        pass

# Combine input
final_query = (user_text + " " + file_text).strip()
final_query = final_query.replace("\n", " ")

# Submit button
if st.button("Submit"):

    if not final_query:
        st.warning("Please enter query or upload file")
    else:
        with st.spinner("Processing..."):

            # RAG search
            chunks = search_rag(final_query, top_k=3)

            level_order = {
                "final": 0,
                "intermediate": 1,
                "foundation": 2
            }

            if "level" in chunks.columns:
                chunks = chunks.sort_values(
                    by="level",
                    key=lambda col: col.map(level_order)
                )

            retrieved_context = chunks.to_json(orient="records")

            # Process
            answer = process_query(final_query, retrieved_context)

            # Save history
            st.session_state.history.append((final_query, answer))

# Display chat history
st.subheader("💬 Conversation")

for q, a in reversed(st.session_state.history):
    st.markdown(f"**🧑‍💼 You:** {q}")
    st.markdown(f"**🤖 AI:** {a}")
    st.markdown("---")