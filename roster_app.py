import json
import os
import streamlit as st

# Page setup
st.set_page_config(
    page_title="GG Labor Roster Planner", page_icon="📋", layout="wide"
)

# File path for persistent database storage
DATA_FILE = "staff_db.json"

# --- PREMIUM MODERN UI CSS STYLING ---
st.markdown(
    """
    <style>
    /* Main App Background */
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

    /* Trash / Tertiary Action Buttons Styling */
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
""",
    unsafe_allow_html=True,
)

# --- MASTER SKILLS & DEFAULT TARGET KPIS ---
if "skills_list" not in st.session_state:
  st.session_state.skills_list = [
      "Clip/Shoot & Pollination",
      "De-leafing",
      "Lowering",
      "Truss Pruning",
      "Truss Support",
      "Leading Hand",
      "Others",
  ]

if "task_targets" not in st.session_state:
  st.session_state.task_targets = {
      "Clip/Shoot & Pollination": 674.0,
      "De-leafing": 800.0,
      "Lowering": 1333.0,
      "Truss Pruning": 1200.0,
      "Truss Support": 120.0,
      "Leading Hand": 100.0,
      "Others": 100.0,
  }

# Default Staff Data with updated skills for Marie, Kid, Ting, Moka, Lin, Rosyfa
DEFAULT_STAFF_DB = [
    {
        "name": "Marie",
        "category": "GG",
        "skills": [
            "Truss Pruning",
            "Truss Support",
            "Clip/Shoot & Pollination",
        ],
        "task_performance": {
            "Truss Pruning": {"kpi": 1200.0, "quality": "👍", "notes": ""},
            "Truss Support": {"kpi": 120.0, "quality": "👍", "notes": ""},
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
        },
    },
    {
        "name": "Kid",
        "category": "GG",
        "skills": [
            "Truss Pruning",
            "Truss Support",
            "Clip/Shoot & Pollination",
        ],
        "task_performance": {
            "Truss Pruning": {"kpi": 1200.0, "quality": "👍", "notes": ""},
            "Truss Support": {"kpi": 120.0, "quality": "👍", "notes": ""},
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
        },
    },
    {
        "name": "Ting",
        "category": "GG",
        "skills": [
            "Truss Pruning",
            "Truss Support",
            "Clip/Shoot & Pollination",
        ],
        "task_performance": {
            "Truss Pruning": {"kpi": 1200.0, "quality": "👍", "notes": ""},
            "Truss Support": {"kpi": 110.0, "quality": "👍", "notes": ""},
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
        },
    },
    {
        "name": "Rebecca",
        "category": "Leading Hand",
        "skills": ["Leading Hand"],
        "task_performance": {
            "Leading Hand": {"kpi": 100.0, "quality": "👍", "notes": ""}
        },
    },
    {
        "name": "Rene",
        "category": "Leading Hand",
        "skills": ["Leading Hand", "Others"],
        "task_performance": {
            "Leading Hand": {"kpi": 100.0, "quality": "👍", "notes": ""},
            "Others": {"kpi": 100.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Alfredo",
        "category": "TOTC",
        "skills": ["Clip/Shoot & Pollination", "Truss Support"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
            "Truss Support": {"kpi": 120.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Enock",
        "category": "TOTC",
        "skills": ["Clip/Shoot & Pollination", "De-leafing"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
            "De-leafing": {"kpi": 800.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Dick",
        "category": "TOTC",
        "skills": ["Clip/Shoot & Pollination", "Truss Pruning"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
            "Truss Pruning": {"kpi": 90.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Dan",
        "category": "TOTC",
        "skills": ["De-leafing", "Lowering"],
        "task_performance": {
            "De-leafing": {"kpi": 800.0, "quality": "👍", "notes": ""},
            "Lowering": {"kpi": 1333.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Will",
        "category": "TOTC",
        "skills": ["De-leafing", "Truss Support"],
        "task_performance": {
            "De-leafing": {"kpi": 800.0, "quality": "👍", "notes": ""},
            "Truss Support": {"kpi": 125.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Terry",
        "category": "TOTC",
        "skills": ["Others", "De-leafing"],
        "task_performance": {
            "Others": {"kpi": 100.0, "quality": "👍", "notes": ""},
            "De-leafing": {"kpi": 800.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Nikki",
        "category": "Urson",
        "skills": ["Clip/Shoot & Pollination", "De-leafing"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
            "De-leafing": {"kpi": 800.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Piayamat (Bina)",
        "category": "Urson",
        "skills": ["Clip/Shoot & Pollination", "Truss Support"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
            "Truss Support": {"kpi": 120.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Tiara",
        "category": "Urson",
        "skills": ["Clip/Shoot & Pollination"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            }
        },
    },
    {
        "name": "Shisir",
        "category": "Urson",
        "skills": ["Clip/Shoot & Pollination", "Lowering"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
            "Lowering": {"kpi": 1333.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Rosyfa",
        "category": "Urson",
        "skills": ["Truss Pruning", "Truss Support"],
        "task_performance": {
            "Truss Pruning": {"kpi": 95.0, "quality": "👍", "notes": ""},
            "Truss Support": {"kpi": 120.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Tommy",
        "category": "Urson",
        "skills": ["Clip/Shoot & Pollination", "Others"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
            "Others": {"kpi": 100.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Audrey",
        "category": "Urson",
        "skills": ["Clip/Shoot & Pollination"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            }
        },
    },
    {
        "name": "Han",
        "category": "Urson",
        "skills": ["Clip/Shoot & Pollination"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            }
        },
    },
    {
        "name": "Rosie",
        "category": "Urson",
        "skills": ["Clip/Shoot & Pollination"],
        "task_performance": {
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            }
        },
    },
    {
        "name": "Dhia",
        "category": "Urson",
        "skills": ["De-leafing", "Truss Pruning"],
        "task_performance": {
            "De-leafing": {"kpi": 800.0, "quality": "👍", "notes": ""},
            "Truss Pruning": {"kpi": 90.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Cassy",
        "category": "Urson",
        "skills": ["De-leafing"],
        "task_performance": {
            "De-leafing": {"kpi": 800.0, "quality": "👍", "notes": ""}
        },
    },
    {
        "name": "Erica",
        "category": "Urson",
        "skills": ["De-leafing", "Truss Support"],
        "task_performance": {
            "De-leafing": {"kpi": 800.0, "quality": "👍", "notes": ""},
            "Truss Support": {"kpi": 115.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Lin",
        "category": "Urson",
        "skills": [
            "Truss Pruning",
            "Clip/Shoot & Pollination",
            "Truss Support",
        ],
        "task_performance": {
            "Truss Pruning": {"kpi": 1200.0, "quality": "👍", "notes": ""},
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
            "Truss Support": {"kpi": 120.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Moka",
        "category": "Urson",
        "skills": [
            "Truss Pruning",
            "Clip/Shoot & Pollination",
            "Truss Support",
        ],
        "task_performance": {
            "Truss Pruning": {"kpi": 1200.0, "quality": "👍", "notes": ""},
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
            },
            "Truss Support": {"kpi": 110.0, "quality": "👍", "notes": ""},
        },
    },
    {
        "name": "Panyawat",
        "category": "Urson",
        "skills": ["Others"],
        "task_performance": {
            "Others": {"kpi": 100.0, "quality": "👍", "notes": ""}
        },
    },
    {
        "name": "AkashDeep",
        "category": "Urson",
        "skills": ["Others"],
        "task_performance": {
            "Others": {"kpi": 100.0, "quality": "👍", "notes": ""}
        },
    },
]

LEGACY_NOTES_TO_REMOVE = [
    "Must work",
    "Min 30h",
    "Supervising",
    "Sulphur Pots",
]


def load_and_sanitize_staff_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r") as f:
        data = json.load(f)

      modified = False
      for person in data:
        if "task_performance" not in person:
          person["task_performance"] = {}
          modified = True

        skills = person.get("skills", [])
        for i, sk in enumerate(skills):
          if sk in ["Truss Cluster Prune", "Pruning"]:
            skills[i] = "Truss Pruning"
            modified = True

        tp = person.get("task_performance", {})
        for old_k in ["Truss Cluster Prune", "Pruning"]:
          if old_k in tp:
            tp["Truss Pruning"] = tp.pop(old_k)
            modified = True

        for sk in skills:
          if sk not in person["task_performance"]:
            default_t = st.session_state.task_targets.get(sk, 100.0)
            person["task_performance"][sk] = {
                "kpi": default_t,
                "quality": "👍",
                "notes": "",
            }
            modified = True

        if person.get("notes") in LEGACY_NOTES_TO_REMOVE:
          person["notes"] = ""
          modified = True

      if modified:
        save_staff_data(data)
      return data
    except Exception:
      return DEFAULT_STAFF_DB
  return DEFAULT_STAFF_DB


def save_staff_data(data):
  with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=4)


# Initialize Session State
if "staff_db" not in st.session_state:
  st.session_state.staff_db = load_and_sanitize_staff_data()

if "active_tasks" not in st.session_state:
  st.session_state.active_tasks = {
      "Leading Hand": 2,
      "Clip/Shoot & Pollination": 12,
      "De-leafing": 5,
      "Lowering": 4,
      "Truss Pruning": 3,
  }

# Title
st.title("📋 Glasshouse 3 - Weekly Labor Planner")
st.markdown("---")

# --- NAVIGATION TABS ---
(
    tab_planner,
    tab_kpi,
    tab_progress,
    tab_calc,
) = st.tabs([
    "📋 Roster & Copy Lists",
    "⭐ Weekly Task-Specific KPI & Quality Tracker",
    "📈 Staff Progress & Skills",
    "🌱 Labor Planning Calculator",
])

# ==========================================
# TAB 1: ROSTER PLANNER & COPY LISTS
# ==========================================
with tab_planner:
  st.sidebar.header("⚙️ Roster & Staff Controls")

  with st.sidebar.expander("➕ Add New Staff Member"):
    with st.form("add_staff_form", clear_on_submit=True):
      new_name = st.text_input("Name")
      new_cat = st.selectbox(
          "Category", ["GG", "TOTC", "Urson", "Leading Hand"]
      )

      opts = st.session_state.skills_list
      skill1 = st.selectbox("Primary Skill (1st Priority)", opts)
      skill2 = st.selectbox(
          "Secondary Skill (2nd Priority, Optional)", ["None"] + opts
      )
      skill3 = st.selectbox(
          "Tertiary Skill (3rd Priority, Optional)", ["None"] + opts
      )

      submit_add = st.form_submit_button("Add Staff")
      if submit_add and new_name.strip():
        skills_arr = [skill1]
        if skill2 != "None":
          skills_arr.append(skill2)
        if skill3 != "None":
          skills_arr.append(skill3)

        t_perf = {}
        for sk in skills_arr:
          def_t = st.session_state.task_targets.get(sk, 100.0)
          t_perf[sk] = {"kpi": def_t, "quality": "👍", "notes": ""}

        st.session_state.staff_db.append({
            "name": new_name.strip(),
            "category": new_cat,
            "skills": skills_arr,
            "task_performance": t_perf,
        })
        save_staff_data(st.session_state.staff_db)
        st.sidebar.success(f"Added {new_name}!")
        st.rerun()

  with st.sidebar.expander("🎓 Update / Train Staff Skills", expanded=False):
    staff_names = [s["name"] for s in st.session_state.staff_db]
    selected_member_name = st.selectbox(
        "Select Team Member", options=[""] + staff_names, key="skill_select_member"
    )

    if selected_member_name:
      person = next(
          (
              s
              for s in st.session_state.staff_db
              if s["name"] == selected_member_name
          ),
          None,
      )
      if person:
        curr_skills = person.get("skills", [])
        opts = st.session_state.skills_list

        p_skill = (
            curr_skills[0]
            if len(curr_skills) > 0 and curr_skills[0] in opts
            else opts[0]
        )
        s_skill = (
            curr_skills[1]
            if len(curr_skills) > 1 and curr_skills[1] in opts
            else "None"
        )
        t_skill = (
            curr_skills[2]
            if len(curr_skills) > 2 and curr_skills[2] in opts
            else "None"
        )

        with st.form(key=f"update_skills_form_{selected_member_name}"):
          up_skill1 = st.selectbox(
              "Primary Skill (1st Priority)", opts, index=opts.index(p_skill)
          )
          up_skill2 = st.selectbox(
              "Secondary Skill (2nd Priority)",
              ["None"] + opts,
              index=(["None"] + opts).index(s_skill),
          )
          up_skill3 = st.selectbox(
              "Tertiary Skill (3rd Priority)",
              ["None"] + opts,
              index=(["None"] + opts).index(t_skill),
          )

          submit_update = st.form_submit_button("Save Trained Skills")
          if submit_update:
            new_s_arr = [up_skill1]
            if up_skill2 != "None":
              new_s_arr.append(up_skill2)
            if up_skill3 != "None":
              new_s_arr.append(up_skill3)

            person["skills"] = new_s_arr
            if "task_performance" not in person:
              person["task_performance"] = {}
            for sk in new_s_arr:
              if sk not in person["task_performance"]:
                def_t = st.session_state.task_targets.get(sk, 100.0)
                person["task_performance"][sk] = {
                    "kpi": def_t,
                    "quality": "👍",
                    "notes": "",
                }

            save_staff_data(st.session_state.staff_db)
            st.sidebar.success(
                f"Updated skills for {selected_member_name}!"
            )
            st.rerun()

  with st.sidebar.expander("🎯 Master Skills & Target KPIs"):
    st.markdown("**Set Target KPI per Task (Editable):**")
    updated_targets = {}
    for s in st.session_state.skills_list:
      current_target = st.session_state.task_targets.get(s, 100.0)
      t_val = st.number_input(
          f"{s}",
          min_value=0.0,
          value=float(current_target),
          step=1.0,
          key=f"target_kpi_{s}",
      )
      updated_targets[s] = t_val
    st.session_state.task_targets = updated_targets

    st.markdown("---")
    add_skill_direct = st.text_input(
        "Add New Skill to System", key="add_skill_direct_key"
    )
    if st.button("Save New Skill", type="primary"):
      if (
          add_skill_direct.strip()
          and add_skill_direct.strip() not in st.session_state.skills_list
      ):
        st.session_state.skills_list.append(add_skill_direct.strip())
        st.session_state.task_targets[add_skill_direct.strip()] = 100.0
        st.sidebar.success(f"Added Skill: {add_skill_direct.strip()}")
        st.rerun()

  with st.sidebar.expander("🗑️ Permanent Remove Staff"):
    staff_names = [s["name"] for s in st.session_state.staff_db]
    to_remove = st.selectbox("Select Staff to Remove", options=[""] + staff_names)
    if st.button("Delete Permanently", type="primary"):
      if to_remove:
        st.session_state.staff_db = [
            s for s in st.session_state.staff_db if s["name"] != to_remove
        ]
        save_staff_data(st.session_state.staff_db)
        st.sidebar.warning(f"Removed {to_remove}")
        st.rerun()

  with st.sidebar.expander("💾 Backup / Export Data"):
    json_data = json.dumps(st.session_state.staff_db, indent=4)
    st.download_button(
        label="📥 Download Staff DB Backup",
        data=json_data,
        file_name="staff_db_backup.json",
        mime="application/json",
    )

  st.sidebar.markdown("---")

  col_left, col_right = st.columns([1, 1.2])

  with col_left:
    st.subheader("1. Availability Check")
    all_names = [s["name"] for s in st.session_state.staff_db]
    absent_staff = st.multiselect(
        "Select staff absent / on leave for next week:", options=all_names
    )

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
            st.session_state.task_targets[task_name_to_add] = 100.0
          st.session_state.active_tasks[task_name_to_add] = new_task_headcount
          st.success(f"Added task: {task_name_to_add}")
          st.rerun()

    st.markdown("**Adjust Required Headcount:**")

    updated_tasks = {}
    tasks_to_delete = {}

    for task_name, count in list(st.session_state.active_tasks.items()):
      c1, c2, c3 = st.columns([3, 1.5, 0.6])
      c1.markdown(f"**{task_name}**")
      new_cnt = c2.number_input(
          "Headcount",
          min_value=0,
          value=count,
          key=f"cnt_{task_name}",
          label_visibility="collapsed",
      )

      if c3.button("🗑️", key=f"del_{task_name}", type="tertiary"):
        tasks_to_delete[task_name] = True
      else:
        updated_tasks[task_name] = new_cnt

    if tasks_to_delete:
      for d_task in tasks_to_delete:
        if d_task in updated_tasks:
          del updated_tasks[d_task]
      st.session_state.active_tasks = updated_tasks
      st.rerun()

    st.session_state.active_tasks = updated_tasks

  task_requirements = {
      t: c for t, c in st.session_state.active_tasks.items() if c > 0
  }
  total_requested = sum(task_requirements.values())

  st.markdown("---")

  # --- ALLOCATION ENGINE WITH MATCH TRACKING ---
  available_pool = [
      s for s in st.session_state.staff_db if s["name"] not in absent_staff
  ]
  cat_priority = {"GG": 1, "TOTC": 2, "Leading Hand": 2, "Urson": 3}

  allocated_roster = {task: [] for task in task_requirements}


  def allocate_by_tier(tier_index, match_label):
    for task_name, req_count in task_requirements.items():
      while len(allocated_roster[task_name]) < req_count:
        assigned_flat = [
            m["person"] for mems in allocated_roster.values() for m in mems
        ]
        unassigned_pool = [p for p in available_pool if p not in assigned_flat]

        candidates_for_task = []
        for person in unassigned_pool:
          skills = person.get("skills", [])
          if len(skills) > tier_index and skills[tier_index] == task_name:
            def_t = st.session_state.task_targets.get(task_name, 100.0)
            t_perf = person.get("task_performance", {}).get(
                task_name, {"kpi": def_t, "quality": "👍", "notes": ""}
            )
            kpi_score = t_perf.get("kpi", def_t)
            qual_score = 0 if t_perf.get("quality", "👍") == "👍" else 1
            cat_rank = cat_priority.get(person["category"], 4)

            candidates_for_task.append({
                "person": person,
                "kpi": kpi_score,
                "quality": qual_score,
                "cat_rank": cat_rank,
            })

        if not candidates_for_task:
          break

        candidates_for_task.sort(
            key=lambda x: (x["cat_rank"], -x["kpi"], x["quality"])
        )
        best_cand = candidates_for_task[0]
        allocated_roster[task_name].append({
            "person": best_cand["person"],
            "match_type": match_label,
        })


  allocate_by_tier(0, "Primary")
  allocate_by_tier(1, "Secondary")
  allocate_by_tier(2, "Tertiary")

  for task_name, req_count in task_requirements.items():
    while len(allocated_roster[task_name]) < req_count:
      assigned_flat = [
          m["person"] for mems in allocated_roster.values() for m in mems
      ]
      unassigned_pool = [p for p in available_pool if p not in assigned_flat]

      if not unassigned_pool:
        break

      unassigned_pool.sort(key=lambda x: cat_priority.get(x["category"], 4))
      fallback_person = unassigned_pool[0]
      allocated_roster[task_name].append(
          {"person": fallback_person, "match_type": "No Match"}
      )

  assigned_staff_flat = [
      m["person"] for mems in allocated_roster.values() for m in mems
  ]
  unassigned_staff = [p for p in available_pool if p not in assigned_staff_flat]

  st.markdown(
      "**Skill Match Color Legend:** "
      "🟢 <span style='color:green; font-weight:600;'>Primary Skill</span>"
      " &nbsp;&nbsp;|&nbsp;&nbsp; "
      "🟡 <span style='color:#b8860b; font-weight:600;'>Secondary Skill</span>"
      " &nbsp;&nbsp;|&nbsp;&nbsp; "
      "⚫ <span style='color:black; font-weight:600;'>Tertiary Skill</span>"
      " &nbsp;&nbsp;|&nbsp;&nbsp; "
      "🔴 <span style='color:red; font-weight:600;'>No Matching Skillset</span>",
      unsafe_allow_html=True,
  )
  st.markdown("---")

  col1, col2 = st.columns([1, 1.2])

  with col1:
    st.markdown(
        f"### 📊 Labor Allocation Plan (Total Requested: {total_requested}"
        " Staff)"
    )
    for task, entries in allocated_roster.items():
      req_c = task_requirements[task]
      st.markdown(f"**{task} ({len(entries)} / {req_c})**")
      for item in entries:
        m = item["person"]
        m_type = item["match_type"]

        if m_type == "Primary":
          icon_badge = "🟢"
        elif m_type == "Secondary":
          icon_badge = "🟡"
        elif m_type == "Tertiary":
          icon_badge = "⚫"
        else:
          icon_badge = "🔴"

        t_note = (
            m.get("task_performance", {}).get(task, {}).get("notes", "")
        )
        note_str = f" (*{t_note}*)" if t_note else ""
        st.write(f"- **{m['name']}** [{m['category']}] — {icon_badge}{note_str}")
      st.markdown("---")

  with col2:
    st.markdown("### 📱 Copy-Paste Ready Lists")

    task_text_output = "GH3 - WEEKLY LABOR PLAN (BY TASK)\n"
    task_text_output += f"Total Staff Required: {total_requested}\n"
    task_text_output += "-----------------------------------\n\n"

    for task, entries in allocated_roster.items():
      task_text_output += f"*{task.upper()} ({len(entries)}/{task_requirements[task]})*\n"
      for idx, item in enumerate(entries, 1):
        m = item["person"]
        m_type = item["match_type"]
        
        if m_type == "Primary":
          dot_symbol = "🟢"
        elif m_type == "Secondary":
          dot_symbol = "🟡"
        elif m_type == "Tertiary":
          dot_symbol = "⚫"
        else:
          dot_symbol = "🔴"

        t_note = (
            m.get("task_performance", {}).get(task, {}).get("notes", "")
        )
        note = f" - {t_note}" if t_note else ""
        task_text_output += (
            f"{idx}. {m['name']} ({m['category']}) {dot_symbol}{note}\n"
        )
      task_text_output += "\n"

    if unassigned_staff:
      task_text_output += "*STANDBY / UNASSIGNED STAFF*\n"
      for u in unassigned_staff:
        task_text_output += f"- {u['name']} ({u['category']})\n"

    st.markdown("**1. Grouped by Task Heading:**")
    st.code(task_text_output, language="text")

    category_map = {"GG": [], "Leading Hand": [], "TOTC": [], "Urson": []}

    for task, entries in allocated_roster.items():
      for item in entries:
        m = item["person"]
        cat = m["category"]
        if cat not in category_map:
          category_map[cat] = []
        t_note = (
            m.get("task_performance", {}).get(task, {}).get("notes", "")
        )
        category_map[cat].append({
            "name": m["name"],
            "task": task,
            "match": item["match_type"],
            "notes": t_note,
        })

    cat_text_output = "GH3 - WEEKLY LABOR PLAN (BY CATEGORY)\n"
    cat_text_output += f"Total Staff Required: {total_requested}\n"
    cat_text_output += "-----------------------------------\n\n"

    cat_order = ["GG", "Leading Hand", "TOTC", "Urson"]
    for cat in cat_order:
      if cat in category_map and category_map[cat]:
        cat_members = category_map[cat]
        cat_text_output += f"*{cat.upper()} ({len(cat_members)})*\n"
        for idx, m in enumerate(cat_members, 1):
          note = f" - {m['notes']}" if m["notes"] else ""
          
          if m["match"] == "Primary":
            d_sym = "🟢"
          elif m["match"] == "Secondary":
            d_sym = "🟡"
          elif m["match"] == "Tertiary":
            d_sym = "⚫"
          else:
            d_sym = "🔴"

          cat_text_output += (
              f"{idx}. {m['name']} - {m['task']} {d_sym}{note}\n"
          )
        cat_text_output += "\n"

    if unassigned_staff:
      cat_text_output += "*STANDBY / UNASSIGNED STAFF*\n"
      for u in unassigned_staff:
        cat_text_output += f"- {u['name']} ({u['category']})\n"

    st.markdown("**2. Grouped by Employee Category:**")
    st.code(cat_text_output, language="text")

  if unassigned_staff:
    st.warning(
        f"⚠️ **{len(unassigned_staff)} Available Staff Not Allocated:** "
        + ", ".join([u["name"] for u in unassigned_staff])
    )


# ==========================================
# TAB 2: WEEKLY TASK-SPECIFIC KPI TRACKER
# ==========================================
with tab_kpi:
  st.subheader("⭐ Weekly Task-Specific KPI & Quality Evaluation")
  st.markdown(
      "Set individual KPI scores and quality ratings **per task** for each team"
      " member below."
  )

  selected_task_to_eval = st.selectbox(
      "Select Task to Evaluate / Update:",
      options=st.session_state.skills_list,
      key="eval_task_select",
  )
  target_val_for_task = st.session_state.task_targets.get(
      selected_task_to_eval, 100.0
  )
  st.info(
      f"🎯 Current Target KPI for **{selected_task_to_eval}**:"
      f" **{target_val_for_task}** (Adjustable in the sidebar)"
  )

  relevant_staff = [
      s
      for s in st.session_state.staff_db
      if selected_task_to_eval in s.get("skills", [])
  ]

  if not relevant_staff:
    st.warning(
        f"No staff currently trained in {selected_task_to_eval}. Go to sidebar"
        " 'Update / Train Staff Skills' to assign this skill."
    )
  else:
    with st.form(f"kpi_form_{selected_task_to_eval}"):
      h1, h2, h3, h4 = st.columns([1.5, 1.2, 1, 1.5])
      h1.markdown("**Staff Name**")
      h2.markdown(f"**KPI Score (Target: {target_val_for_task})**")
      h3.markdown("**Quality**")
      h4.markdown("**Task Notes / Excellence**")

      st.markdown("---")

      form_inputs = {}
      for person in relevant_staff:
        c1, c2, c3, c4 = st.columns([1.5, 1.2, 1, 1.5])

        c1.markdown(
            f"**{person['name']}** <br><small"
            f" style='color:gray;'>{person['category']}</small>",
            unsafe_allow_html=True,
        )

        p_perf = person.get("task_performance", {}).get(
            selected_task_to_eval,
            {"kpi": target_val_for_task, "quality": "👍", "notes": ""},
        )

        kpi_in = c2.number_input(
            "KPI",
            min_value=0.0,
            value=float(p_perf.get("kpi", target_val_for_task)),
            step=1.0,
            key=f"kpi_{person['name']}_{selected_task_to_eval}",
            label_visibility="collapsed",
        )
        qual_in = c3.selectbox(
            "Quality",
            ["👍", "👎"],
            index=0 if p_perf.get("quality", "👍") == "👍" else 1,
            key=f"qual_{person['name']}_{selected_task_to_eval}",
            label_visibility="collapsed",
        )
        note_in = c4.text_input(
            "Notes",
            value=p_perf.get("notes", ""),
            key=f"note_{person['name']}_{selected_task_to_eval}",
            label_visibility="collapsed",
            placeholder="e.g. Excellent speed",
        )

        form_inputs[person["name"]] = {
            "kpi": kpi_in,
            "quality": qual_in,
            "notes": note_in,
        }

      submit_task_kpi = st.form_submit_button(
          f"💾 Save Ratings for {selected_task_to_eval}", type="primary"
      )
      if submit_task_kpi:
        for person in st.session_state.staff_db:
          name = person["name"]
          if name in form_inputs:
            if "task_performance" not in person:
              person["task_performance"] = {}
            person["task_performance"][selected_task_to_eval] = form_inputs[name]

        save_staff_data(st.session_state.staff_db)
        st.success(
            f"Successfully updated KPI and Quality ratings for"
            f" {selected_task_to_eval}!"
        )
        st.rerun()


# ==========================================
# TAB 3: STAFF PROGRESS & SKILLS DIRECTORY
# ==========================================
with tab_progress:
  st.subheader("📈 Staff Skills Directory & Progress Overview")
  st.markdown(
      "Comprehensive view of all team members, certified skills, and performance"
      " records."
  )

  search_query = st.text_input("🔍 Search staff by name:", key="staff_search_progress")

  for person in st.session_state.staff_db:
    if not search_query or search_query.lower() in person["name"].lower():
      with st.expander(
          f"👤 **{person['name']}** — Category: `{person['category']}`"
      ):
        col_p1, col_p2 = st.columns([1, 1.5])

        with col_p1:
          st.markdown(
              "##### 🛠️ Certified Skills (Primary $\rightarrow$ Secondary"
              " $\rightarrow$ Tertiary)"
          )
          skills = person.get("skills", [])
          if skills:
            for idx, sk in enumerate(skills):
              tier_label = (
                  ["Primary", "Secondary", "Tertiary"][idx]
                  if idx < 3
                  else "Extra"
              )
              st.markdown(f"- ✅ **{tier_label}:** {sk}")
          else:
            st.markdown("_No skills assigned_")

        with col_p2:
          st.markdown("##### 📊 Task Progress & KPI Records")
          task_perf = person.get("task_performance", {})
          if task_perf:
            for t_name, metrics in task_perf.items():
              kpi = metrics.get("kpi", 100.0)
              qual = metrics.get("quality", "👍")
              notes = metrics.get("notes", "")
              note_text = f" | _Note: {notes}_" if notes else ""
              st.markdown(
                  f"- **{t_name}**: KPI **{kpi}** | Quality: {qual}{note_text}"
              )
          else:
            st.markdown("_No KPI records logged yet_")


# ==========================================
# TAB 4: LABOR PLANNING CALCULATOR
# ==========================================
with tab_calc:
  st.subheader("🌱 Labor Planning & Calculation Calculator")
  st.markdown(
      "Calculate total required labor hours and stem counts based on your"
      " glasshouse dimensions and task targets."
  )

  c_in1, c_in2, c_in3 = st.columns(3)

  with c_in1:
    total_area_ha = st.number_input(
        "Total Glasshouse Area (hectares)",
        min_value=0.1,
        value=5.0,
        step=0.5,
    )
    total_area_m2 = total_area_ha * 10000.0

  with c_in2:
    num_rows = st.number_input(
        "Number of Rows", min_value=1, value=260, step=5
    )
    plants_per_row = st.number_input(
        "Plant Density per Row", min_value=1, value=480, step=10
    )

  with c_in3:
    calc_task = st.selectbox(
        "Select Task for Calculation",
        options=st.session_state.skills_list,
        key="calc_task_select",
    )
    default_kpi_for_task = st.session_state.task_targets.get(calc_task, 65.0)
    target_kpi_rate = st.number_input(
        "Target KPI (Output per Hour)",
        min_value=1.0,
        value=float(default_kpi_for_task),
        step=5.0,
        key="calc_target_kpi_input",
    )

  # Calculations
  total_plants = num_rows * plants_per_row
  plant_density_m2 = (
      total_plants / total_area_m2 if total_area_m2 > 0 else 0.0
  )
  estimated_total_hours = (
      total_plants / target_kpi_rate if target_kpi_rate > 0 else 0
  )
  estimated_staff_needed_40h = estimated_total_hours / 40.0

  st.markdown("---")
  res1, res2, res3, res4 = st.columns(4)
  res1.metric("Total Plant / Stem Count", f"{total_plants:,.0f}")
  res2.metric("Plant Density", f"{plant_density_m2:.2f} plants/m²")
  res3.metric(
      "Total Estimated Labor Hours", f"{estimated_total_hours:,.1f} hrs"
  )
  res4.metric(
      "Staff Required (at 40 hrs/wk)", f"{estimated_staff_needed_40h:,.1f} workers"
  )
