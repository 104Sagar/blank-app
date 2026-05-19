import streamlit as st

st.set_page_config(page_title="Labor Calculator", page_icon="🚜", layout="centered")

st.title("🚜 Labor Calculator")
st.write("Modify any number below to see the instant change in timelines.")
st.markdown("---")

# Main screen inputs with 640 as your permanent default row density
density = st.number_input("1. Plant Density (Plants inside ONE row)", min_value=1, value=640, step=10)
total_rows = st.number_input("2. Total Number of Rows", min_value=1, value=20, step=1)
kpi = st.number_input("3. Target KPI (Speed in plants per hour)", min_value=1, value=180, step=5)
staff_count = st.number_input("4. Number of Staff Available", min_value=1, value=2, step=1)

# Calculations
total_plants = total_rows * density
total_man_hours = total_plants / kpi
duration_hours = total_man_hours / staff_count

st.markdown("---")
st.subheader("📊 Live Calculation Results")

m1, m2, m3 = st.columns(3)
m1.metric("Total Plants", f"{total_plants:,}")
m2.metric("Total Workload", f"{total_man_hours:.1f} Hours")
m3.metric("Actual Time to Finish", f"{duration_hours:.1f} Hours")

st.info(
    f"💡 With **{staff_count} staff** working at a KPI of **{kpi} plants/hour**, "
    f"it will take **{duration_hours:.1f} hours** of clock time to finish all **{total_plants:,} plants**."
)