import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="GG Labor Roster Planner", page_icon="📋", layout="wide")

# Custom soothing faint-green theme styling
st.markdown("""
    <style>
    /* Main Background - Faint Soothing Green */
    .stApp {
        background-color: #F2F7F4 !important;
    }
    
    /* Sidebar Background - Soft Mint Accent */
    div[data-testid="stSidebar"] {
        background-color: #E3EFE8 !important;
    }
    
    /* Input Boxes and Cards */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-radius: 6px;
    }
    
    /* Clean Text Containers */
    .stMarkdown, .stText {
        color: #1A2E22;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE MASTER SKILLS LIST ---
if 'skills_list' not in st.session_state:
    st.session_state.skills_list = [
        "Clip/Shoot + Pollination",
        "Truss Support",
        "De-leafing",
        "Lowering",
        "Pruning",
        "Leading Hand",
        "Others"
    ]

# --- INITIALIZE MULTI-SKILL STAFF DATABASE ---
if 'staff_db' not in st.session_state:
    st.session_state.staff_db = [
        # GG Members
        {"name": "Marie", "category": "GG", "skills": ["Truss Support", "Lowering", "De-leafing"], "notes": "Must work"},
        {"name": "Kid", "category": "GG", "skills": ["Truss Support", "Clip/Shoot + Pollination"], "notes": "Must work"},
        {"name": "Ting", "category": "GG", "skills": ["Truss Support", "Pruning"], "notes": "Must work"},
        
        # Leading Hands
        {"name": "Rebecca", "category": "Leading Hand", "skills": ["Leading Hand"], "notes": "Supervising"},
        {"name": "Rene", "category": "Leading Hand", "skills": ["Leading Hand", "Others"], "notes": "Sulphur Pots"},
        
        # TOTC Members
        {"name": "Alfredo", "category": "TOTC", "skills": ["Clip/Shoot + Pollination", "Truss Support", "Lowering"], "notes": "Min 30h"},
        {"name": "Enock", "category": "TOTC", "skills": ["Clip/Shoot + Pollination", "De-leafing"], "notes": "Min 30h"},
        {"name": "Dick", "category": "TOTC", "skills": ["Clip/Shoot + Pollination", "Pruning"], "notes": "Min 30h"},
        {"name": "Dan", "category": "TOTC", "skills": ["De-leafing", "Lowering"], "notes": "Min 30h"},
        {"name": "Will", "category": "TOTC", "skills": ["De-leafing", "Truss Support"], "notes": "Min 30h"},
        {"name": "Terry", "category": "TOTC", "skills": ["Others", "De-leafing"], "notes": "Min 30h"},
        
        # Ursons
        {"name": "Nikki", "category": "Urson", "skills": ["Clip/Shoot + Pollination", "De-leafing"], "notes": ""},
        {"name": "Piayamat (Bina)", "category": "Urson", "skills": ["Clip/Shoot + Pollination", "Truss Support"], "notes": ""},
        {"name": "Tiara", "category": "Urson", "skills": ["Clip/Shoot + Pollination"], "notes": ""},
        {"name": "Shisir", "category": "Urson", "skills": ["Clip/Shoot + Pollination", "Lowering"], "notes": ""},
        {"name": "Rosyfa", "category": "Urson", "skills": ["Clip/Shoot + Pollination"], "notes": ""},
        {"name": "Tommy", "category": "Urson", "skills": ["Clip/Shoot + Pollination", "Others"], "notes": ""},
        {"name": "Audrey", "category": "Urson", "skills": ["Clip/Shoot + Pollination"], "notes": ""},
        {"name": "Han", "category": "Urson", "skills": ["Clip/Shoot + Pollination"], "notes": ""},
        {"name": "Rosie", "category": "Urson", "skills": ["Clip/Shoot + Pollination"], "notes": "Mon-Wed Only"},
        {"name": "Dhia", "category": "Urson", "skills": ["De-leafing", "Pruning"], "notes": ""},
        {"name": "Cassy", "category": "Urson", "skills": ["De-leafing"], "notes": ""},
        {"name": "Erica", "category": "Urson", "skills": ["De-leafing", "Truss Support"], "notes": ""},
        {"name": "Lin", "category": "Urson", "skills": ["Truss Support", "Lowering"], "notes": ""},
        {"name": "Moka", "category": "Urson", "skills": ["Truss Support"], "notes": ""},
        {"name": "Panyawat", "category": "Urson", "skills": ["Others"], "notes": "Cleaning"},
        {"name": "AkashDeep", "category": "Urson", "skills": ["Others"], "notes": "Stem Supports"}
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
st.markdown("Dynamic multi-skill planner with GG, TOTC, and Urson priority allocation.")
st.markdown("---")

# --- SIDEBAR: STAFF & SKILL CONTROLS ---
st.sidebar.header("⚙️ Roster & Staff Controls")

# Add New Staff
with st.sidebar.expander("➕ Add New Staff Member"):
    new_name = st.text_input("Name")
    new_cat = st.selectbox("Category", ["GG", "TOTC", "Urson", "Leading Hand"])
    
    opts = st.session_state.skills_list
    skill1 = st.selectbox("Primary Skill", opts)
    skill2 = st.selectbox("Secondary Skill (Optional)", ["None"] + opts)
    skill3 = st.selectbox("Tertiary Skill (Optional)", ["None"] + opts)
    
    new_note = st.text_input("Notes (e.g. Mon-Wed only)")
    
    if st.button("Add Staff"):
        if new_name.strip():
            skills_arr = [skill1]
            if skill2 != "None": skills_arr.append(skill2)
            if skill3 != "None": skills_arr.append(skill3)
            
            st.session_state.staff_db.append({
                "name": new_name.strip(), 
                "category": new_cat, 
                "skills": skills_arr, 
                "notes": new_note
            })
            st.sidebar.success(f"Added {new_name}")
            st.rerun()

# Update / Train Existing Staff Skills
with st.sidebar.expander("🎓 Update / Train Staff Skills"):
    staff_names = [s["name"] for s in st.session_state.staff_db]
    selected_member_name = st.selectbox("Select Team Member", options=[""] + staff_names)
    
    if selected_member_name:
        # Find selected person
        person = next((s for s in st.session_state.staff_db if s["name"] == selected_member_name), None)
        if person:
            curr_skills = person.get("skills", [])
            p_skill = curr_skills[0] if len(curr_skills) > 0 else st.session_state.skills_list[0]
            s_skill = curr_skills[1] if len(curr_skills) > 1 else "None"
            t_skill = curr_skills[2] if len(curr_skills) > 2 else "None"
            
            opts = st.session_state.skills_list
            up_skill1 = st.selectbox("Primary Skill", opts, index=opts.index(p_skill) if p_skill in opts else 0, key="up_s1")
            up_skill2 = st.selectbox("Secondary Skill", ["None"] + opts, index=(["None"] + opts).index(s_skill) if s_skill in (["None"] + opts) else 0, key="up_s2")
            up_skill3 = st.selectbox("Tertiary Skill", ["None"] + opts, index=(["None"] + opts).index(t_skill) if t_skill in (["None"] + opts) else 0, key="up_s3")
            
            if st.button("Save Trained Skills"):
                new_s_arr = [up_skill1]
                if up_skill2 != "None": new_s_arr.append(up_skill2)
                if up_skill3 != "None": new_s_arr.append(up_skill3)
                person["skills"] = new_s_arr
                st.sidebar.success(f"Updated skills for {selected_member_name}")
                st.rerun()

# Master Skills List
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

# Permanent Remove Staff
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

    for d_task in tasks_to_delete:
        if d_task in updated_tasks:
            del updated_tasks[d_task]
        st.session_state.active_tasks = updated_tasks
        st.rerun()

    st.session_state.active_tasks = updated_tasks

task_requirements = {t: c for t, c in st.session_state.active_tasks.items() if c > 0}
total_requested = sum(task_requirements.values())

st.markdown("---")

# --- MULTI-SKILL SMART ALLOCATION ENGINE ---
available_pool = [s for s in st.session_state.staff_db if s["name"] not in absent_staff]

# Sorting priority: GG (1) > TOTC/Leading Hand (2) > Urson (3)
priority_map = {"GG": 1, "TOTC": 2, "Leading Hand": 2, "Urson": 3}
available_pool.sort(key=lambda x: priority_map.get(x["category"], 4))

allocated_roster = {task: [] for task in task_requirements}
unassigned_staff = []

for person in available_pool:
    assigned = False
    person_skills = person.get("skills", [person.get("primary_task", "Others")])
    
    # Check Primary -> Secondary -> Tertiary skill match in background
    for sk in person_skills:
        if sk in task_requirements and len(allocated_roster[sk]) < task_requirements[sk]:
            allocated_roster[sk].append(person)
            assigned = True
            break
            
    # Fallback for GG / TOTC staff
    if not assigned and person["category"] in ["GG", "TOTC"]:
        for task, req_count in task_requirements.items():
            if task != "Leading Hand" and len(allocated_roster[task]) < req_count:
                allocated_roster[task].append(person)
                assigned = True
                break
                
    if not assigned:
        unassigned_staff.append(person)

# --- DISPLAY RESULTS ---
st.subheader(f"📊 Labor Allocation Plan (Total Requested: {total_requested} Staff)")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("### 📋 Roster Breakdown (Name | Category)")
    
    for task, members in allocated_roster.items():
        st.markdown(f"**{task} (Total: {len(members)} / {task_requirements[task]})**")
        for m in members:
            note_str = f" — *{m['notes']}*" if m['notes'] else ""
            # Clean display: no skill list clutter on main screen
            st.write(f"- **{m['name']}** [{m['category']}]{note_str}")
        st.markdown("---")

with col2:
    st.markdown("### 📱 Copy-Paste Text Request for Booking")
    
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

if unassigned_staff:
    st.warning(f"⚠️ **{len(unassigned_staff)} Available Staff Not Allocated:** " + ", ".join([u["name"] for u in unassigned_staff]))
