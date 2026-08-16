import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="GG Labor Roster Planner", page_icon="📋", layout="wide")

# Custom high-contrast styling
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    div[data-testid="stSidebar"] { background-color: #F0F4F8 !important; }
    .task-header { background-color: #E6F2FF; padding: 10px; border-radius: 5px; font-weight: bold; }
    .copy-box { background-color: #F8F9FA; padding: 15px; border: 1px solid #D0D0D0; border-radius: 5px; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE DATABASE ---
if 'staff_db' not in st.session_state:
    st.session_state.staff_db = [
        # GG Members
        {"name": "Marie", "category": "GG", "primary_task": "Truss Support", "notes": "Must work"},
        {"name": "Kid", "category": "GG", "primary_task": "Truss Support", "notes": "Must work"},
        {"name": "Ting", "category": "GG", "primary_task": "Truss Support", "notes": "Must work"},
        
        # Leading Hands
        {"name": "Rebecca", "category": "Leading Hand", "primary_task": "Leading Hand", "notes": "Supervising"},
        {"name": "Rene", "category": "Leading Hand", "primary_task": "Leading Hand", "notes": "Sulphur Pots"},
        
        # TOTC Members (Min 30 hrs)
        {"name": "Alfredo", "category": "TOTC", "primary_task": "Clip/Shoot + Pollination", "notes": "Min 30h"},
        {"name": "Enock", "category": "TOTC", "primary_task": "Clip/Shoot + Pollination", "notes": "Min 30h"},
        {"name": "Dick", "category": "TOTC", "primary_task": "Clip/Shoot + Pollination", "notes": "Min 30h"},
        {"name": "Dan", "category": "TOTC", "primary_task": "De-leafing", "notes": "Min 30h"},
        {"name": "Will", "category": "TOTC", "primary_task": "De-leafing", "notes": "Min 30h"},
        {"name": "Terry", "category": "TOTC", "primary_task": "Others", "notes": "Min 30h"},
        
        # Ursons (Casuals)
        {"name": "Nikki", "category": "Urson", "primary_task": "Clip/Shoot + Pollination", "notes": ""},
        {"name": "Piayamat (Bina)", "category": "Urson", "primary_task": "Clip/Shoot + Pollination", "notes": ""},
        {"name": "Tiara", "category": "Urson", "primary_task": "Clip/Shoot + Pollination", "notes": ""},
        {"name": "Shisir", "category": "Urson", "primary_task": "Clip/Shoot + Pollination", "notes": ""},
        {"name": "Rosyfa", "category": "Urson", "primary_task": "Clip/Shoot + Pollination", "notes": ""},
        {"name": "Tommy", "category": "Urson", "primary_task": "Clip/Shoot + Pollination", "notes": ""},
        {"name": "Audrey", "category": "Urson", "primary_task": "Clip/Shoot + Pollination", "notes": ""},
        {"name": "Han", "category": "Urson", "primary_task": "Clip/Shoot + Pollination", "notes": ""},
        {"name": "Rosie", "category": "Urson", "primary_task": "Clip/Shoot + Pollination", "notes": "Mon-Wed Only"},
        {"name": "Dhia", "category": "Urson", "primary_task": "De-leafing", "notes": ""},
        {"name": "Cassy", "category": "Urson", "primary_task": "De-leafing", "notes": ""},
        {"name": "Erica", "category": "Urson", "primary_task": "De-leafing", "notes": ""},
        {"name": "Lin", "category": "Urson", "primary_task": "Truss Support", "notes": ""},
        {"name": "Moka", "category": "Urson", "primary_task": "Truss Support", "notes": ""},
        {"name": "Panyawat", "category": "Urson", "primary_task": "Others", "notes": "Cleaning"},
        {"name": "AkashDeep", "category": "Urson", "primary_task": "Others", "notes": "Stem Supports"}
    ]

# Header
st.title("📋 Glasshouse 3 - Weekly Labor Booking Planner")
st.markdown("Generate precise labor booking requests based on GG, TOTC, and Urson priority rules.")
st.markdown("---")

# --- SIDEBAR: STAFF DATABASE MANAGEMENT ---
st.sidebar.header("⚙️ Roster & Staff Database")

# Option to add new staff
with st.sidebar.expander("➕ Add New Staff Member"):
    new_name = st.text_input("Name")
    new_cat = st.selectbox("Category", ["GG", "TOTC", "Urson", "Leading Hand"])
    new_task = st.selectbox("Primary Skill/Task", ["Clip/Shoot + Pollination", "De-leafing", "Truss Support", "Others", "Leading Hand", "Lowering", "Pruning"])
    new_note = st.text_input("Notes (e.g. Mon-Wed only)")
    if st.button("Add Staff"):
        if new_name.strip():
            st.session_state.staff_db.append({"name": new_name.strip(), "category": new_cat, "primary_task": new_task, "notes": new_note})
            st.sidebar.success(f"Added {new_name}")
            st.rerun()

# Option to remove staff permanently
with st.sidebar.expander("🗑️ Permanent Remove Staff"):
    staff_names = [s["name"] for s in st.session_state.staff_db]
    to_remove = st.selectbox("Select Staff to Remove", options=[""] + staff_names)
    if st.button("Delete Permanently"):
        if to_remove:
            st.session_state.staff_db = [s for s in st.session_state.staff_db if s["name"] != to_remove]
            st.sidebar.warning(f"Removed {to_remove}")
            st.rerun()

st.sidebar.markdown("---")

# --- MAIN FORM INPUTS ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("1. Availability & Absence Check")
    all_names = [s["name"] for s in st.session_state.staff_db]
    absent_staff = st.multiselect("Select staff on leave / quit / absent for next week:", options=all_names)

with col_right:
    st.subheader("2. Weekly Task Headcount Requirements")
    
    # Task Demand Inputs
    lh_count = st.number_input("Leading Hands Required", min_value=1, value=2)
    clip_count = st.number_input("Clip/Shoot + Pollination Staff Required", min_value=0, value=12)
    truss_count = st.number_input("Truss Support Staff Required", min_value=0, value=5)
    deleaf_count = st.number_input("De-leafing Staff Required", min_value=0, value=5)
    other_count = st.number_input("Other Jobs (Cleaning/Stem Support) Staff Required", min_value=0, value=3)
    
    # Optional Custom Task
    add_custom_task = st.checkbox("Add Extra Task (e.g., Lowering/Pruning)")
    custom_task_name = ""
    custom_task_count = 0
    if add_custom_task:
        c1, c2 = st.columns(2)
        custom_task_name = c1.text_input("Task Name", value="Lowering")
        custom_task_count = c2.number_input("Staff Needed", min_value=1, value=4)

# Build Target Requirements Dict
task_requirements = {
    "Leading Hand": lh_count,
    "Clip/Shoot + Pollination": clip_count,
    "Truss Support": truss_count,
    "De-leafing": deleaf_count,
    "Others": other_count
}
if add_custom_task and custom_task_name:
    task_requirements[custom_task_name] = custom_task_count

total_requested = sum(task_requirements.values())

st.markdown("---")

# --- ALLOCATION ENGINE ---
# Filter available staff
available_pool = [s for s in st.session_state.staff_db if s["name"] not in absent_staff]

# Sorting priority: 1. GG (Must work), 2. TOTC (Min 30h), 3. Ursons
priority_map = {"GG": 1, "TOTC": 2, "Leading Hand": 2, "Urson": 3}
available_pool.sort(key=lambda x: priority_map.get(x["category"], 4))

allocated_roster = {task: [] for task in task_requirements}
unassigned_staff = []

# Step 1: Assign Primary Tasks based on Skills & Category Priority
for person in available_pool:
    assigned = False
    p_task = person["primary_task"]
    
    # Try placing in primary skill task if demand remains
    if p_task in task_requirements and len(allocated_roster[p_task]) < task_requirements[p_task]:
        allocated_roster[p_task].append(person)
        assigned = True
    else:
        # Fallback: fill other open requirements for high priority staff (GG/TOTC)
        if person["category"] in ["GG", "TOTC"]:
            for task, req_count in task_requirements.items():
                if task != "Leading Hand" and len(allocated_roster[task]) < req_count:
                    allocated_roster[task].append(person)
                    assigned = True
                    break
    
    if not assigned:
        unassigned_staff.append(person)

# --- DISPLAY RESULTS ---
st.subheader(f"📊 Labor Allocation Plan (Total Requested: {total_requested} Staff)")

# 2-Column Side-by-Side Roster Table & Quick Copy
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("### 📋 Roster Breakdown (Name | Category | Task)")
    
    roster_rows = []
    for task, members in allocated_roster.items():
        st.markdown(f"**{task} (Total: {len(members)} / {task_requirements[task]})**")
        for m in members:
            note_str = f" ({m['notes']})" if m['notes'] else ""
            st.write(f"- **{m['name']}** [{m['category']}]{note_str}")
            roster_rows.append({"Name": m["name"], "Category": m["category"], "Task": task, "Notes": m["notes"]})
        st.markdown("---")

with col2:
    st.markdown("### 📱 Copy-Paste Text Request for Booking")
    st.markdown("Copy this exact summary block to send via Message or WhatsApp:")
    
    # Generate clean text format
    text_output = f"GH3 - WEEKLY LABOR BOOKING REQUEST\n"
    text_output += f"Total Staff Required: {total_requested}\n"
    text_output += "-----------------------------------\n\n"
    
    for task, members in allocated_roster.items():
        text_output += f"*{task.upper()} ({len(members)})*\n"
        for idx, m in enumerate(members, 1):
            note = f" - {m['notes']}" if m['notes'] else ""
            text_output += f"{idx}. {m['name']} ({m['category']}){note}\n"
        text_output += "\n"
        
    if unassigned_staff:
        text_output += "*EXCLUDED / STANDBY STAFF*\n"
        for u in unassigned_staff:
            text_output += f"- {u['name']} ({u['category']})\n"

    st.code(text_output, language="text")

# Unallocated / Excluded Warning
if unassigned_staff:
    st.warning(f"⚠️ **{len(unassigned_staff)} Available Staff Not Called/Allocated:** " + ", ".join([u["name"] for u in unassigned_staff]))
