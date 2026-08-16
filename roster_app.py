import streamlit as st
import pandas as pd
import json
import os

# Page setup
st.set_page_config(page_title="GG Labor Roster Planner", page_icon="📋", layout="wide")

# File path for persistent database storage
DATA_FILE = "staff_db.json"

# --- PREMIUM MODERN UI CSS STYLING ---
st.markdown("""
    <style>
    /* Main App Background with Soft Botanical Gradient */
    .stApp {
        background: linear-gradient(135deg, #E6EFE9 0%, #F4F8F5 40%, #E2ECE5 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Sidebar Styling */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #DCE7DF 0%, #E8F0EA 100%) !important;
        border-right: 1px solid rgba(46, 125, 50, 0.12) !important;
    }

    /* Card Containers for Main Columns */
    div[data-testid="stColumn"] {
        background: rgba(255, 255, 255, 0.82) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px !important;
        padding: 1rem !important;
        box-shadow: 0 8px 24px rgba(27, 47, 33, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #D5E3D8 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
        margin-bottom: 0.75rem !important;
    }

    /* Form Inputs */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="base-input"] {
        border-radius: 10px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #C5DACB !important;
    }

    /* Primary Buttons & Form Submit Buttons */
    .stButton > button[kind="primary"], .stFormSubmitButton > button {
        border-radius: 10px !important;
        background: linear-gradient(135deg, #2D6A4F 0%, #1B4332 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.45rem 1.1rem !important;
        box-shadow: 0 4px 12px rgba(45, 106, 79, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }

    /* Trash / Tertiary Action Buttons Styling (Fixes Mobile Green Block) */
    .stButton > button[kind="tertiary"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 1.2rem !important;
        padding: 0.2rem 0.4rem !important;
        color: #D32F2F !important;
        width: auto !important;
    }

    /* Code Output Box Styling */
    div[data-testid="stCodeBlock"] {
        border-radius: 12px !important;
        border: 1px solid #D1E0D5 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- MASTER SKILLS LIST ---
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

# Clean Default Staff Data (No "Must work" or "Min 30h" tags)
DEFAULT_STAFF_DB = [
    {"name": "Marie", "category": "GG", "skills": ["Truss Support", "Lowering", "De-leafing"], "notes": ""},
    {"name": "Kid", "category": "GG", "skills": ["Truss Support", "Clip/Shoot + Pollination"], "notes": ""},
    {"name": "Ting", "category": "GG", "skills": ["Truss Support", "Pruning"], "notes": ""},
    {"name": "Rebecca", "category": "Leading Hand", "skills": ["Leading Hand"], "notes": ""},
    {"name": "Rene", "category": "Leading Hand", "skills": ["Leading Hand", "Others"], "notes": ""},
    {"name": "Alfredo", "category": "TOTC", "skills": ["Clip/Shoot + Pollination", "Truss Support", "Lowering"], "notes": ""},
    {"name": "Enock", "category": "TOTC", "skills": ["Clip/Shoot + Pollination", "De-leafing"], "notes": ""},
    {"name": "Dick", "category": "TOTC", "skills": ["Clip/Shoot + Pollination", "Pruning"], "notes": ""},
    {"name": "Dan", "category": "TOTC", "skills": ["De-leafing", "Lowering"], "notes": ""},
    {"name": "Will", "category": "TOTC", "skills": ["De-leafing", "Truss Support"], "notes": ""},
    {"name": "Terry", "category": "TOTC", "skills": ["Others", "De-leafing"], "notes": ""},
    {"name": "Nikki", "category": "Urson", "skills": ["Clip/Shoot + Pollination", "De-leafing"], "notes": ""},
    {"name": "Piayamat (Bina)", "category": "Urson", "skills": ["Clip/Shoot + Pollination", "Truss Support"], "notes": ""},
    {"name": "Tiara", "category": "Urson", "skills": ["Clip/Shoot + Pollination"], "notes": ""},
    {"name": "Shisir", "category": "Urson", "skills": ["Clip/Shoot + Pollination", "Lowering"], "notes": ""},
    {"name": "Rosyfa", "category": "Urson", "skills": ["Clip/Shoot + Pollination"], "notes": ""},
    {"name": "Tommy", "category": "Urson", "skills": ["Clip/Shoot + Pollination", "Others"], "notes": ""},
    {"name": "Audrey", "category": "Urson", "skills": ["Clip/Shoot + Pollination"], "notes": ""},
    {"name": "Han", "category": "Urson", "skills": ["Clip/Shoot + Pollination"], "notes": ""},
    {"name": "Rosie", "category": "Urson", "skills": ["Clip/Shoot + Pollination"], "notes": ""},
    {"name": "Dhia", "category": "Urson", "skills": ["De-leafing", "Pruning"], "notes": ""},
    {"name": "Cassy", "category": "Urson", "skills": ["De-leafing"], "notes": ""},
    {"name": "Erica", "category": "Urson", "skills": ["De-leafing", "Truss Support"], "notes": ""},
    {"name": "Lin", "category": "Urson", "skills": ["Truss Support", "Lowering"], "notes": ""},
    {"name": "Moka", "category": "Urson", "skills": ["Truss Support"], "notes": ""},
    {"name": "Panyawat", "category": "Urson", "skills": ["Others"], "notes": ""},
    {"name": "AkashDeep", "category": "Urson", "skills": ["Others"], "notes": ""}
]

# Read/Write Persistence File
def load_staff_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_STAFF_DB
    return DEFAULT_STAFF_DB

def save_staff_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Initialize Session State
if 'staff_db' not in st.session_state:
    st.session_state.staff_db = load_staff_data()

if 'active_tasks' not in st.session_state:
    st.session_state.active_tasks = {
        "Leading Hand": 2,
        "Clip/Shoot + Pollination": 12,
        "Truss Support": 5,
        "De-leafing": 5,
        "Others": 3
    }

# Title
st.title("📋 Glasshouse 3 - Weekly Labor Booking Planner")
st.markdown("---")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ Roster & Staff Controls")

# 1. Add New Staff
with st.sidebar.expander("➕ Add New Staff Member"):
    with st.form("add_staff_form", clear_on_submit=True):
        new_name = st.text_input("Name")
        new_cat = st.selectbox("Category", ["GG", "TOTC", "Urson", "Leading Hand"])
        
        opts = st.session_state.skills_list
        skill1 = st.selectbox("Primary Skill", opts)
        skill2 = st.selectbox("Secondary Skill (Optional)", ["None"] + opts)
        skill3 = st.selectbox("Tertiary Skill (Optional)", ["None"] + opts)
        
        new_note = st.text_input("Notes (Optional)")
        
        submit_add = st.form_submit_button("Add Staff")
        if submit_add and new_name.strip():
            skills_arr = [skill1]
            if skill2 != "None": skills_arr.append(skill2)
            if skill3 != "None": skills_arr.append(skill3)
            
            st.session_state.staff_db.append({
                "name": new_name.strip(), 
                "category": new_cat, 
                "skills": skills_arr, 
                "notes": new_note.strip()
            })
            save_staff_data(st.session_state.staff_db)
            st.sidebar.success(f"Added {new_name}!")
            st.rerun()

# 2. Update / Train Staff Skills (Fixed State Processing)
with st.sidebar.expander("🎓 Update / Train Staff Skills", expanded=True):
    staff_names = [s["name"] for s in st.session_state.staff_db]
    selected_member_name = st.selectbox("Select Team Member", options=[""] + staff_names, key="skill_select_member")
    
    if selected_member_name:
        person = next((s for s in st.session_state.staff_db if s["name"] == selected_member_name), None)
        if person:
            curr_skills = person.get("skills", [])
            p_skill = curr_skills[0] if len(curr_skills) > 0 else st.session_state.skills_list[0]
            s_skill = curr_skills[1] if len(curr_skills) > 1 else "None"
            t_skill = curr_skills[2] if len(curr_skills) > 2 else "None"
            
            opts = st.session_state.skills_list
            
            with st.form(key="update_skills_form_container"):
                up_skill1 = st.selectbox("Primary Skill", opts, index=opts.index(p_skill) if p_skill in opts else 0)
                up_skill2 = st.selectbox("Secondary Skill", ["None"] + opts, index=(["None"] + opts).index(s_skill) if s_skill in (["None"] + opts) else 0)
                up_skill3 = st.selectbox("Tertiary Skill", ["None"] + opts, index=(["None"] + opts).index(t_skill) if t_skill in (["None"] + opts) else 0)
                
                submit_update = st.form_submit_button("Save Trained Skills")
                if submit_update:
                    new_s_arr = [up_skill1]
                    if up_skill2 != "None": new_s_arr.append(up_skill2)
                    if up_skill3 != "None": new_s_arr.append(up_skill3)
                    
                    for s in st.session_state.staff_db:
                        if s["name"] == selected_member_name:
                            s["skills"] = new_s_arr
                            break
                    save_staff_data(st.session_state.staff_db)
                    st.sidebar.success(f"Updated skills for {selected_member_name}!")
                    st.rerun()

# 3. Master Skills List
with st.sidebar.expander("🏷️ Master Skills List"):
    st.markdown("**Current Skills:**")
    for s in st.session_state.skills_list:
        st.write(f"- {s}")
    
    add_skill_direct = st.text_input("Add Skill to System", key="add_skill_direct_key")
    if st.button("Save New Skill", type="primary"):
        if add_skill_direct.strip() and add_skill_direct.strip() not in st.session_state.skills_list:
            st.session_state.skills_list.append(add_skill_direct.strip())
            st.sidebar.success(f"Added Skill: {add_skill_direct.strip()}")
            st.rerun()

# 4. Remove Staff
with st.sidebar.expander("🗑️ Permanent Remove Staff"):
    staff_names = [s["name"] for s in st.session_state.staff_db]
    to_remove = st.selectbox("Select Staff to Remove", options=[""] + staff_names)
    if st.button("Delete Permanently", type="primary"):
        if to_remove:
            st.session_state.staff_db = [s for s in st.session_state.staff_db if s["name"] != to_remove]
            save_staff_data(st.session_state.staff_db)
            st.sidebar.warning(f"Removed {to_remove}")
            st.rerun()

# 5. Backup Data
with st.sidebar.expander("💾 Backup / Export Data"):
    json_data = json.dumps(st.session_state.staff_db, indent=4)
    st.download_button(
        label="📥 Download Staff DB Backup",
        data=json_data,
        file_name="staff_db_backup.json",
        mime="application/json"
    )

st.sidebar.markdown("---")

# --- MAIN FORM INPUTS ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("1. Availability Check")
    all_names = [s["name"] for s in st.session_state.staff_db]
    absent_staff = st.multiselect("Select staff absent / on leave for next week:", options=all_names)

with col_right:
    st.subheader("2. Weekly Task Headcounts")
    
    with st.expander("➕ Add Task Heading", expanded=False):
        task_add_options = st.session_state.skills_list + ["➕ Other Custom Task"]
        chosen_task_opt = st.selectbox("Select Task Heading", task_add_options)
        
        task_name_to_add = chosen_task_opt
        if chosen_task_opt == "➕ Other Custom Task":
            custom_t_input = st.text_input("Type Custom Task Heading")
            if custom_t_input.strip():
                task_name_to_add = custom_t_input.strip()
                
        new_task_headcount = st.number_input("Headcount Needed", min_value=1, value=4)
        
        if st.button("Add Task to Roster", type="primary"):
            if task_name_to_add and task_name_to_add != "➕ Other Custom Task":
                if task_name_to_add not in st.session_state.skills_list:
                    st.session_state.skills_list.append(task_name_to_add)
                st.session_state.active_tasks[task_name_to_add] = new_task_headcount
                st.success(f"Added task: {task_name_to_add}")
                st.rerun()

    st.markdown("**Adjust Required Headcount:**")
    
    updated_tasks = {}
    tasks_to_delete = []
    
    for task_name, count in list(st.session_state.active_tasks.items()):
        c1, c2, c3 = st.columns([3, 1.5, 0.6])
        c1.markdown(f"**{task_name}**")
        new_cnt = c2.number_input(f"Headcount", min_value=0, value=count, key=f"cnt_{task_name}", label_visibility="collapsed")
        
        # Trash button uses type="tertiary" to look clean on mobile
        if c3.button("🗑️", key=f"del_{task_name}", type="tertiary"):
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

priority_map = {"GG": 1, "TOTC": 2, "Leading Hand": 2, "Urson": 3}
available_pool.sort(key=lambda x: priority_map.get(x["category"], 4))

allocated_roster = {task: [] for task in task_requirements}
unassigned_staff = []

for person in available_pool:
    assigned = False
    person_skills = person.get("skills", [person.get("primary_task", "Others")])
    
    for sk in person_skills:
        if sk in task_requirements and len(allocated_roster[sk]) < task_requirements[sk]:
            allocated_roster[sk].append(person)
            assigned = True
            break
            
    if not assigned and person["category"] in ["GG", "TOTC"]:
        for task, req_count in task_requirements.items():
            if task != "Leading Hand" and len(allocated_roster[task]) < req_count:
                allocated_roster[task].append(person)
                assigned = True
                break
                
    if not assigned:
        unassigned_staff.append(person)

# --- DISPLAY RESULTS & TWO COPY-PASTE LISTS ---
st.subheader(f"📊 Labor Allocation Plan (Total Requested: {total_requested} Staff)")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📋 Live Roster Breakdown")
    for task, members in allocated_roster.items():
        st.markdown(f"**{task} ({len(members)} / {task_requirements[task]})**")
        for m in members:
            note_str = f" (*{m['notes']}*)" if m.get('notes') else ""
            st.write(f"- **{m['name']}** [{m['category']}]{note_str}")
        st.markdown("---")

with col2:
    st.markdown("### 📱 Copy-Paste Ready Lists")
    
    # BOX 1: LIST BY TASK
    task_text_output = f"GH3 - WEEKLY LABOR BOOKING REQUEST (BY TASK)\n"
    task_text_output += f"Total Staff Required: {total_requested}\n"
    task_text_output += "-----------------------------------\n\n"
    
    for task, members in allocated_roster.items():
        task_text_output += f"*{task.upper()} ({len(members)})*\n"
        for idx, m in enumerate(members, 1):
            note = f" - {m['notes']}" if m.get('notes') else ""
            task_text_output += f"{idx}. {m['name']} ({m['category']}){note}\n"
        task_text_output += "\n"
        
    if unassigned_staff:
        task_text_output += "*STANDBY / UNASSIGNED STAFF*\n"
        for u in unassigned_staff:
            task_text_output += f"- {u['name']} ({u['category']})\n"

    st.markdown("**1. Grouped by Task Heading:**")
    st.code(task_text_output, language="text")

    # BOX 2: LIST BY EMPLOYEE CATEGORY
    category_map = {"GG": [], "Leading Hand": [], "TOTC": [], "Urson": []}
    
    for task, members in allocated_roster.items():
        for m in members:
            cat = m["category"]
            if cat not in category_map:
                category_map[cat] = []
            category_map[cat].append({"name": m["name"], "task": task, "notes": m.get("notes", "")})

    cat_text_output = f"GH3 - WEEKLY LABOR BOOKING REQUEST (BY CATEGORY)\n"
    cat_text_output += f"Total Staff Required: {total_requested}\n"
    cat_text_output += "-----------------------------------\n\n"

    cat_order = ["GG", "Leading Hand", "TOTC", "Urson"]
    for cat in cat_order:
        if cat in category_map and category_map[cat]:
            cat_members = category_map[cat]
            cat_text_output += f"*{cat.upper()} ({len(cat_members)})*\n"
            for idx, m in enumerate(cat_members, 1):
                note = f" - {m['notes']}" if m['notes'] else ""
                cat_text_output += f"{idx}. {m['name']} - {m['task']}{note}\n"
            cat_text_output += "\n"

    if unassigned_staff:
        cat_text_output += "*STANDBY / UNASSIGNED STAFF*\n"
        for u in unassigned_staff:
            cat_text_output += f"- {u['name']} ({u['category']})\n"

    st.markdown("**2. Grouped by Employee Category:**")
    st.code(cat_text_output, language="text")

if unassigned_staff:
    st.warning(f"⚠️ **{len(unassigned_staff)} Available Staff Not Allocated:** " + ", ".join([u["name"] for u in unassigned_staff]))
