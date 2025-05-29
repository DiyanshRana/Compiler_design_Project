import streamlit as st
import radon.raw as rr
import radon.metrics as rm
import radon.complexity as rc
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import pandas as pd
import ast

from analyzer_utils import get_reserved_word_frequency
from ast_utils import make_ast

# Function to convert a dictionary to DataFrame
def convert_to_df(mydict):
    return pd.DataFrame(list(mydict.items()), columns=["Keywords", "Counts"])

# Function to create and show a wordcloud
def plot_wordcloud(docx):
    if not docx.strip():
        st.warning("No code provided for word cloud.")
        return
    my_wordcloud = WordCloud(width=800, height=400).generate(docx)
    fig = plt.figure(figsize=(10, 5))
    plt.imshow(my_wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(fig)

# Main Streamlit app
def main():
    st.set_page_config(page_title="Static Code Analyzer", layout="wide")
    st.title("🧠 Static Code Analysis App (Python)")

    with st.form(key="code_input_form"):
        raw_code = st.text_area("📝 Enter your Python code here:", height=300)
        submit_button = st.form_submit_button(label="🔍 Analyze Code")

    if not raw_code.strip():
        st.info("Please enter some code to analyze.")
        return

    if submit_button:
        results = get_reserved_word_frequency(raw_code)

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Code Metrics", "🔑 Keywords", "🆔 Identifiers", "🌲 AST View"])

        with tab1:
            st.subheader("🔎 Static Code Analysis Metrics")
            st.code(raw_code, language="python")

            try:
                basic_metrics = rr.analyze(raw_code)
                mi = rm.mi_visit(raw_code, True)
                cc = rc.cc_visit(raw_code)
                hal = rm.h_visit(raw_code)

                st.write("**Raw Metrics**")
                st.json(basic_metrics)

                col1, col2 = st.columns(2)
                col1.metric("📈 Maintainability Index", round(mi, 2))
                col2.metric("🧩 Cyclomatic Complexity", len(cc))

                with st.expander("🧮 Halstead Metrics"):
                    st.json(hal[0])

            except Exception as e:
                st.error(f"Error analyzing code: {e}")

        with tab2:
            st.subheader("🔑 Python Keywords Frequency")
            df = convert_to_df(results["reserved"])
            if not df.empty:
                st.altair_chart(
                    alt.Chart(df).mark_bar().encode(x="Keywords", y="Counts", color="Keywords"),
                    use_container_width=True
                )

                t1, t2, t3 = st.tabs(["🌥️ WordCloud", "📋 Frequency Table", "📊 Pie Chart"])
                with t1:
                    plot_wordcloud(" ".join(results["reserved"].keys()))
                with t2:
                    st.dataframe(df)
                with t3:
                    st.plotly_chart(px.pie(df, values="Counts", names="Keywords", title="Keyword Usage"))

            else:
                st.info("No Python keywords found in the code.")

        with tab3:
            st.subheader("🆔 Identifiers")
            df = convert_to_df(results["identifiers"])
            if not df.empty:
                st.altair_chart(
                    alt.Chart(df).mark_bar().encode(x="Keywords", y="Counts", color="Keywords"),
                    use_container_width=True
                )
                plot_wordcloud(" ".join(results["identifiers"].keys()))
            else:
                st.info("No identifiers found.")

        with tab4:
            st.subheader("🌲 Abstract Syntax Tree (AST)")
            try:
                tree_data = make_ast(raw_code)
                st.json(tree_data)
            except Exception as e:
                st.error(f"Failed to parse code into AST: {e}")

if __name__ == "__main__":
    main()
6