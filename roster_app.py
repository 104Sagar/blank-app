import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="GG Labor Roster Planner", page_icon="📋", layout="wide")

# Custom soothing high-contrast theme styling
st.markdown("""
    <style>
    /* Main Background - Soft Neutral Gray/Blue */
    .stApp {
        background-color: #F4F6F9 !important;
    }
    
    /* Sidebar Background */
    div[data-testid="stSidebar"] {
        background-color: #EBF0F5 !important;
    }
    
    /* Input Boxes and Cards */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-radius: 6px;
    }
    
    /* Task Header Blocks */
    .task-header {
        background-color: #E2E8F0;
        padding: 10px;
        border-radius: 6px;
        font-weight: bold;
    }
    
    /* Clean Text Containers */
    .stMarkdown, .stText {
        color: #1E293B;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE MASTER SKILLS LIST ---
if 'skills_list' not in st.session_state:
    st.session_state.skills_list = [
        "Clip/Shoot + Pollination",
        "Truss Support",
        "De-leafing",
        "Others",
        "Leading Hand",
        "Lowering",
        "Pruning"
    ]

# --- INITIALIZE STAFF DATABASE ---
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

# Default Active Tasks Setup
if 'active_tasks' not in st.session_state:
    st.session_state.active_tasks = {
        "Leading Hand": 2,
        "Clip/Shoot + Pollination": 12,
        "Truss Support": 5,
        "De-leafing": 5,
        "Others": 3
    }

# Header
st.title("📋 Glasshouse 3 - Weekly Labor Booking Planner")
st.markdown("Dynamic task & skill planner with GG, TOTC, and Urson priority allocation.")
st.markdown("---")

# --- SIDEBAR: STAFF & SKILL CONTROLS ---
st.sidebar.header("⚙️ Roster & Staff Controls")

# Option to add new staff & custom skills
with st.sidebar.expander("➕ Add New Staff Member"):
    new_name = st.text_input("Name")
    new_cat = st.selectbox("Category", ["GG", "TOTC", "Urson", "Leading Hand"])
    
    # Skill Selector with option to add a brand new skill
    skill_options = st.session_state.skills_list + ["➕ Add New Custom Skill..."]
    selected_skill = st.selectbox("Primary Skill/Task", skill_options)
    
    final_skill = selected_skill
    if selected_skill == "➕ Add New Custom Skill...":
        custom_skill_input = st.text_input("Enter New Skill Name")
        if custom_skill_input.strip():
            final_skill = custom_skill_input.strip()

    new_note = st.text_input("Notes (e.g. Mon-Wed only)")
    
    if st.button("Add Staff"):
        if new_name.strip() and final_skill and final_skill != "➕ Add New Custom Skill...":
            if final_skill not in st.session_state.skills_list:
                st.session_state.skills_list.append(final_skill)
                
            st.session_state.staff_db.append({
                "name": new_name.strip(), 
                "category": new_cat, 
                "primary_task": final_skill, 
                "notes": new_note
            })
            st.sidebar.success(f"Added {new_name} ({final_skill})")
            st.rerun()

# Option to manage skill master list directly
with st.sidebar.expander("🏷️ Master Skills List"):
    st.markdown("**Current Skills:**")
    for s in st.session_state.skills_list:
        st.write(f"- {s}")
    
    add_skill_direct = st.text_input("Add Skill to System", key="add_skill_direct_key")
    if st.button("Save New Skill"):
        if add_skill_direct.strip() and add_skill_direct.strip() not in st.session_state.skills_list:
            st.session_state.skills_list.append(add_skill_direct.strip())
            st.sidebar.success(f"Added Skill: {add_skill_direct.strip()}")
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
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("1. Availability & Absence Check")
    all_names = [s["name"] for s in st.session_state.staff_db]
    absent_staff = st.multiselect("Select staff on leave / quit / absent for next week:", options=all_names)

with col_right:
    st.subheader("2. Weekly Task Setup & Headcounts")
    
    # Task Addition Box
    with st.expander("➕ Add Task Heading for Next Week", expanded=False):
        task_add_options = st.session_state.skills_list + ["➕ Other Custom Task"]
        chosen_task_opt = st.selectbox("Select Task Heading", task_add_options)
        
        task_name_to_add = chosen_task_opt
        if chosen_task_opt == "➕ Other Custom Task":
            custom_t_input = st.text_input("Type Custom Task Heading")
            if custom_t_input.strip():
                task_name_to_add = custom_t_input.strip()
                
        new_task_headcount = st.number_input("Headcount Needed", min_value=1, value=4)
        
        if st.button("Add Task to Roster"):
            if task_name_to_add and task_name_to_add != "➕ Other Custom Task":
                if task_name_to_add not in st.session_state.skills_list:
                    st.session_state.skills_list.append(task_name_to_add)
                st.session_state.active_tasks[task_name_to_add] = new_task_headcount
                st.success(f"Added task: {task_name_to_add}")
                st.rerun()

    st.markdown("**Adjust Required Headcount or Delete Tasks:**")
    
    # Render all active tasks with headcount adjuster and delete button
    updated_tasks = {}
    tasks_to_delete = []
    
    for task_name, count in list(st.session_state.active_tasks.items()):
        c1, c2, c3 = st.columns([2.5, 1.5, 0.8])
        c1.markdown(f"**{task_name}**")
        new_cnt = c2.number_input(f"Headcount", min_value=0, value=count, key=f"cnt_{task_name}", label_visibility="collapsed")
        
        if c3.button("🗑️", key=f"del_{task_name}"):
            tasks_to_delete.append(task_name)
        else:
            updated_tasks[task_name] = new_cnt

    # Remove deleted tasks
    for d_task in tasks_to_delete:
        if d_task in updated_tasks:
            del updated_tasks[d_task]
        st.session_state.active_tasks = updated_tasks
        st.rerun()

    st.session_state.active_tasks = updated_tasks

task_requirements = {t: c for t, c in st.session_state.active_tasks.items() if c > 0}
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
    
    if p_task in task_requirements and len(allocated_roster[p_task]) < task_requirements[p_task]:
        allocated_roster[p_task].append(person)
        assigned = True
    else:
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
