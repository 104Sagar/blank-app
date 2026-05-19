import streamlit as st

# Configure the page layout to wide mode
st.set_page_config(page_title="Labor Calculator", page_icon="🚜", layout="wide")

# Light theme configuration with high-contrast text and dynamic alert support
st.markdown(
    """
    <style>
    /* Main application background */
    .stApp {
        background-color: #FFFFFF;
        color: #1A1A1A;
    }
    /* Soft light blue background for the left control/option sidebar */
    div[data-testid="stSidebar"] {
        background-color: #E6F2FF !important;
        border-right: 1px solid #CCE3FD;
    }
    /* Grand Summary Metrics styling */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: bold !important;
        color: #1E7E34 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #2A2A2A !important;
        font-weight: 600 !important;
    }
    .main-title {
        font-size: 2.4rem !important;
        font-weight: bold;
        color: #111111;
        margin-bottom: 20px;
    }
    /* Task Card Standard Style */
    .task-card-normal {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        margin-bottom: 15px;
    }
    /* Task Card Overtime/Alert Style (Soft Pink/Red) */
    .task-card-alert {
        background-color: #FFF0F2;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #FFC1CC;
        margin-bottom: 15px;
    }
    .task-card-normal h4 { margin-top: 0px; color: #0056B3; }
    .task-card-alert h4 { margin-top: 0px; color: #D32F2F; }
    
    h2, h3, p, span {
        color: #1A1A1A !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- MAIN SCREEN HEADER ---
st.markdown("<p class='main-title'>Welcome Sagar 👋</p>", unsafe_allow_html=True)
st.markdown("---")


# --- SIDEBAR INPUTS (Light Blue Option Panel) ---
st.sidebar.header("📋 Calculator Inputs")

# 1. Global Timeline Variable (Applies across all tasks instantly)
remaining_days = st.sidebar.slider("📅 Remaining Days in Week", min_value=1.0, max_value=5.0, value=5.0, step=0.5)
max_allowed_hours = remaining_days * 8.0

st.sidebar.markdown(f"**Standard base limit:** {max_allowed_hours:.1f} Hours / Staff")
st.sidebar.markdown("---")

# 2. Number of active tasks config
num_tasks = st.sidebar.selectbox("How many tasks to calculate?", options=[1, 2, 3, 4, 5], index=4)
st.sidebar.markdown("---")

# Pre-defined crop care task workflow defaults
task_defaults = {
    0: {"name": "Clip and Shoot", "kpi": 550, "staff": 12},
    1: {"name": "Lowering", "kpi": 1500, "staff": 6},
    2: {"name": "De-Leafing", "kpi": 600, "staff": 5},
    3: {"name": "Truss Pruning", "kpi": 1100, "staff": 4},
    4: {"name": "Vines and Shoot", "kpi": 1500, "staff": 6}
}

tasks_data = []

# Generate input blocks in the sidebar based on selection
for i in range(num_tasks):
    defaults = task_defaults.get(i, {"name": f"Task {i+1}", "kpi": 180, "staff": 2})
    
    st.sidebar.markdown(f"### 🛠️ Task {i+1}: {defaults['name']}")
    
    task_name = st.sidebar.text_input(f"Task {i+1} Name", value=defaults['name'], key=f"name_{i}")
    display_name = task_name if task_name.strip() != "" else f"Task {i+1}"
    
    density = st.sidebar.number_input(f"[{display_name}] Plant Density", min_value=1, value=640, step=10, key=f"dens_{i}")
    total_rows = st.sidebar.number_input(f"[{display_name}] Total Rows", min_value=1, value=260, step=1, key=f"rows_{i}")
    kpi = st.sidebar.number_input(f"[{display_name}] Target KPI", min_value=1, value=defaults['kpi'], key=f"kpi_{i}")
    staff_count = st.sidebar.number_input(f"[{display_name}] Staff Available", min_value=1, value=defaults['staff'], key=f"staff_{i}")
    
    # Run structural labor math for this task
    t_plants = total_rows * density
    t_man_hours = t_plants / kpi
    t_duration = t_man_hours / staff_count
    
    tasks_data.append({
        "name": display_name,
        "plants": t_plants,
        "man_hours": t_man_hours,
        "duration": t_duration,
        "rows": total_rows,
        "density": density,
        "kpi": kpi,
        "staff": staff_count
    })
    st.sidebar.markdown("---")


# --- MAIN SCREEN CALCULATIONS & DISPLAY ---

# Calculate aggregate crop care totals
crop_care_man_hours = sum(t["man_hours"] for t in tasks_data)

# Staff headcount tracking logic (Exclude "Vines and Shoot" staff to avoid double counting shared team)
unique_staff_total = 0
clip_shoot_staff_count = 0

for t in tasks_data:
    if "vines and shoot" not in t["name"].lower():
        unique_staff_total += t["staff"]
    if "clip and shoot" in t["name"].lower():
        clip_shoot_staff_count = t["staff"]

# Account for pollination diversion: 9 hours total per week per person on Clip & Shoot.
# Dynamically scale this based on remaining days left in the week slider.
pollination_hours_lost_per_person = (9.0 / 5.0) * remaining_days
total_pollination_man_hours_lost = clip_shoot_staff_count * pollination_hours_lost_per_person

# Update Grand Total to include BOTH crop care and the active pollination duty workload
grand_total_man_hours = crop_care_man_hours + total_pollination_man_hours_lost

# Calculate true average total workload across unique crop care headcount
avg_hours_per_person = grand_total_man_hours / unique_staff_total if unique_staff_total > 0 else 0.0

st.subheader("📊 Live Weekly Summary (All Tasks)")

m1, m2 = st.columns(2)
m1.metric("Total Combined Workload", f"{grand_total_man_hours:.1f} Man-Hours")
m2.metric("Avg Workload per Person", f"{avg_hours_per_person:.1f} Hours", help=f"Includes pollination hours. Calculated across {unique_staff_total} unique crew members.")

st.markdown("---")

st.subheader("📝 Task Breakdowns")

# Display results in a high-scannability 2-column layout
main_cols = st.columns(2)

for index, task in enumerate(tasks_data):
    is_clip_shoot = "clip and shoot" in task['name'].lower()
    is_shared_team_task = "lowering" in task['name'].lower() or "vines and shoot" in task['name'].lower()
    
    if is_clip_shoot:
        # Subtract pollination duty from available crop care time
        limit_reference = max_allowed_hours - pollination_hours_lost_per_person
        is_overtime = task['duration'] > limit_reference
        limit_text = f"Remaining Limit minus Pollination ({limit_reference:.1f} Hrs Max)"
    elif is_shared_team_task:
        # Lowering and Vines teams share their shifts and shouldn't breach 20 hours a week each
        is_overtime = task['duration'] > 20.0
        limit_reference = 20.0
        limit_text = "Shared Shift Limit (20.0 Hrs Max)"
    else:
        # Standard workflow limited by tracking slider
        is_overtime = task['duration'] > max_allowed_hours
        limit_reference = max_allowed_hours
        limit_text = f"Remaining Days Limit ({max_allowed_hours:.1f} Hrs Max)"
        
    card_class = "task-card-alert" if is_overtime else "task-card-normal"
    
    # Format status text output neatly
    if is_overtime:
        status_text = f"<span style='color: #D32F2F; font-weight: bold;'>⚠️ Exceeds Limit ({task['duration']:.1f} / {limit_reference:.1f} Hours)</span>"
    else:
        leftover = limit_reference - task['duration']
        status_text = f"<span style='color: #1E7E34; font-weight: bold;'>✅ On Track ({leftover:.1f} Hours Within Budget)</span>"

    # Distribute cards alternating down the 2 columns
    target_col = main_cols[index % 2]
    
    with target_col:
        st.markdown(
            f"""
            <div class="{card_class}">
                <h4>📋 {task['name']}</h4>
                <p style="margin-bottom: 5px;"><b>Inputs:</b> {task['rows']} rows × {task['density']} density | <b>KPI:</b> {task['kpi']} | <b>Staff:</b> {task['staff']}</p>
                <p style="margin-bottom: 5px;"><b>Workload:</b> {task['man_hours']:.1f} Man-Hours</p>
                <p style="margin-bottom: 5px;"><b>Required Clock Time:</b> {task['duration']:.1f} Hours</p>
                <hr style="margin: 10px 0; border: 0; border-top: 1px solid #D0D0D0;">
                <p style="margin-bottom: 5px;"><b>Target parameters:</b> {limit_text}</p>
                <p style="margin-bottom: 0px;"><b>Weekly Status:</b> {status_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )