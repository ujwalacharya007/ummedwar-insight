import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_excel("dtt.xlsx")

# --------------------------
# CLEAN & EXTRACT MAIN FIELDS
# --------------------------

clean_df = df.iloc[:, 0:7]   # take first 7 columns only
clean_df.columns = ["Province", "District", "Area", "Candidate Name", "Gender", "Party", "Votes"]

# Drop header repeating row
clean_df = clean_df[clean_df["Province"] != "प्रदेश"]

# Convert filters to string (IMPORTANT FIX)
clean_df["Province"] = clean_df["Province"].astype(str)
clean_df["District"] = clean_df["District"].astype(str)
clean_df["Area"] = clean_df["Area"].astype(str)

# Convert numeric fields
clean_df["Votes"] = pd.to_numeric(clean_df["Votes"], errors="coerce")

# --------------------------
# STREAMLIT UI
# --------------------------
st.set_page_config(page_title="Election Insight Dashboard 🇳🇵", layout="wide")

st.title("Election Insight Dashboard 🇳🇵")
st.write("Filter by Province, District, or Area to explore candidates & insights.")

# Filters
province = st.selectbox("Province", ["All"] + sorted(clean_df["Province"].unique()))
district = st.selectbox("District", ["All"] + sorted(clean_df["District"].unique()))
area = st.selectbox("Area (क्षेत्र)", ["All"] + sorted(clean_df["Area"].unique()))

# Apply filters
filtered = clean_df.copy()

if province != "All":
    filtered = filtered[filtered["Province"] == province]
if district != "All":
    filtered = filtered[filtered["District"] == district]
if area != "All":
    filtered = filtered[filtered["Area"] == area]

# Display table
st.subheader("Filtered Candidates")
st.dataframe(filtered, use_container_width=True)

# --------------------------
# VISUALIZATIONS
# --------------------------

if filtered.shape[0] > 0 and filtered["Votes"].notna().any():
    st.subheader("📊 Vote Comparison")
    fig = px.bar(filtered, x="Candidate Name", y="Votes", color="Party",
                 title="Votes by Candidate")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏳️ Party Distribution")
    fig2 = px.pie(filtered, names="Party", title="Party Representation")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("👥 Gender Distribution")
    fig3 = px.histogram(filtered, x="Gender", color="Gender",
                        title="Gender Ratio")
    st.plotly_chart(fig3, use_container_width=True)

# --------------------------
# INSIGHTS
# --------------------------
st.subheader("💡 Key Insights")

if filtered.shape[0] > 0:
    top = filtered.loc[filtered["Votes"].idxmax()]
    st.write(f"**Top Candidate:** {top['Candidate Name']} ({top['Votes']} votes)")
    st.write(f"**Total Candidates:** {filtered.shape[0]}")
    st.write(f"**Total Parties Represented:** {filtered['Party'].nunique()}")
