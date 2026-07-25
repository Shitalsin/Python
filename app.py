import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from generate_answer import ask_patchcontext

st.set_page_config(page_title="PatchContext", page_icon="🔍")

st.title("🔍 PatchContext")

st.write("Ask why a design decision was made in the FastAPI codebase.")

query = st.text_input("Your question:")

if st.button("Ask"):
    if query:
        with st.spinner("Searching commits, PRs, and issues..."):
            answer, cited_sources, is_safe, warnings = ask_patchcontext(query)

        st.subheader("Answer")
        st.write(answer)

        if not is_safe:
            st.warning("⚠️ This answer may not be fully reliable:")
            for w in warnings:
                st.write("-", w)

        if cited_sources:
            st.subheader("Sources")
            for source in cited_sources:
                st.write(f"**[Source {source['source_number']}]** ({source['type']})")
                st.write(source['url'])
                st.write(source['text_snippet'])
                st.divider()
    else:
        st.warning("Please enter a question.")