import json
import math
import os
import streamlit as st

# Page setup
st.set_page_config(
    page_title="GG Labor Roster Planner", page_icon="📋", layout="wide"
)

# File paths for persistent database & settings storage
DATA_FILE = "staff_db.json"
SETTINGS_FILE = "settings.json"


def load_settings():
  if os.path.exists(SETTINGS_FILE):
    try:
      with open(SETTINGS_FILE, "r") as f:
        return json.load(f)
    except Exception:
      return {}
  return {}


def save_settings(settings_dict):
  with open(SETTINGS_FILE, "w") as f:
    json.dump(settings_dict, f, indent=4)


# --- PREMIUM COMPACT MOBILE-FRIENDLY CSS STYLING ---
st.markdown(
    """
    <style>
    /* Main App Background & Typography */
    .stApp {
        background: linear-gradient(135deg, #E6EFE9 0%, #F4F8F5 40%, #E2ECE5 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 13.5px;
    }
    
    /* Compact Headings */
    h1 { font-size: 1.5rem !important; margin-bottom: 0.3rem !important; }
    h2 { font-size: 1.25rem !important; margin-top: 0.5rem !important; }
    h3 { font-size: 1.05rem !important; margin-top: 0.4rem !important; }

    /* Sidebar Styling */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #DCE7DF 0%, #E8F0EA 100%) !important;
        border-right: 1px solid rgba(46, 125, 50, 0.12) !important;
    }

    /* Card Containers for Main Columns (Compact Padding) */
    div[data-testid="stColumn"] {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 12px !important;
        padding: 0.6rem 0.8rem !important;
        box-shadow: 0 4px 16px rgba(27, 47, 33, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        margin-bottom: 0.5rem !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1px solid #D5E3D8 !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02) !important;
        margin-bottom: 0.5rem !important;
    }

    /* Form Inputs */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="base-input"] {
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #C5DACB !important;
    }

    /* Primary Buttons & Form Submit Buttons */
    .stButton > button[kind="primary"], .stFormSubmitButton > button {
        border-radius: 8px !important;
        background: linear-gradient(135deg, #2D6A4F 0%, #1B4332 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.35rem 0.9rem !important;
        box-shadow: 0 2px 8px rgba(45, 106, 79, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }

    /* Trash / Tertiary Action Buttons Styling */
    .stButton > button[kind="tertiary"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 1.1rem !important;
        padding: 0.1rem 0.3rem !important;
        color: #D32F2F !important;
        width: auto !important;
    }

    /* Code Output Box Styling */
    div[data-testid="stCodeBlock"] {
        border-radius: 10px !important;
        border: 1px solid #D1E0D5 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- LOAD PERSISTENT SETTINGS ---
saved_settings = load_settings()

# --- MASTER SKILLS & TARGET KPIS ---
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
  default_targets = {
      "Clip/Shoot & Pollination": 674.0,
      "De-leafing": 800.0,
      "Lowering": 1333.0,
      "Truss Pruning": 1200.0,
      "Truss Support": 1200.0,
      "Leading Hand": 100.0,
      "Others": 100.0,
  }
  st.session_state.task_targets = saved_settings.get(
      "task_targets", default_targets
  )

# Persistent Average KPIs dictionary loaded from settings
if "saved_avg_kpis" not in st.session_state:
  st.session_state.saved_avg_kpis = saved_settings.get("avg_kpis", {})

# Default Staff Data
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
            "Truss Support": {"kpi": 1200.0, "quality": "👍", "notes": ""},
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
            "Truss Support": {"kpi": 1200.0, "quality": "👍", "notes": ""},
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
            "Truss Support": {"kpi": 1200.0, "quality": "👍", "notes": ""},
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
        "name": "Tico",
        "category": "Leading Hand",
        "skills": ["Leading Hand"],
        "task_performance": {
            "Leading Hand": {"kpi": 100.0, "quality": "👍", "notes": ""}
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
            "Truss Support": {"kpi": 1200.0, "quality": "👍", "notes": ""},
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
            "Truss Support": {"kpi": 1200.0, "quality": "👍", "notes": ""},
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
            "Truss Support": {"kpi": 1200.0, "quality": "👍", "notes": ""},
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
            "Truss Support": {"kpi": 1200.0, "quality": "👍", "notes": ""},
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
            "Truss Support": {"kpi": 1200.0, "quality": "👍", "notes": ""},
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
            "Truss Support": {"kpi": 1200.0, "quality": "👍", "notes": ""},
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
            "Truss Support": {"kpi": 1200.0, "quality": "👍", "notes": ""},
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
  data = DEFAULT_STAFF_DB
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r") as f:
        data = json.load(f)
    except Exception:
      data = DEFAULT_STAFF_DB

  modified = False

  tico_found = False
  for person in data:
    if person.get("name") == "Tico":
      person["category"] = "Leading Hand"
      if "Leading Hand" not in person.get("skills", []):
        person["skills"] = ["Leading Hand"] + [
            s for s in person.get("skills", []) if s != "Leading Hand"
        ]
      tico_found = True
      modified = True
      break

  if not tico_found:
    data.append({
        "name": "Tico",
        "category": "Leading Hand",
        "skills": ["Leading Hand"],
        "task_performance": {
            "Leading Hand": {"kpi": 100.0, "quality": "👍", "notes": ""}
        },
    })
    modified = True

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
        default_t = st.session_state.get("task_targets", {}).get(sk, 100.0)
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


def save_staff_data(data):
  with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=4)


# Initialize Session State
if "staff_db" not in st.session_state:
  st.session_state.staff_db = load_and_sanitize_staff_data()

# Persistent Active Tasks loaded from settings.json
if "active_tasks" not in st.session_state:
  default_tasks = {
      "Leading Hand": 2,
      "Clip/Shoot & Pollination": 12,
      "De-leafing": 5,
      "Lowering": 4,
      "Truss Pruning": 3,
  }
  st.session_state.active_tasks = saved_settings.get("active_tasks", default_tasks)

# Calculator Session State Defaults
if "calc_plants_per_row" not in st.session_state:
  st.session_state.calc_plants_per_row = 480.0

total_gh_plants = 260 * st.session_state.calc_plants_per_row
plant_density_sqm = total_gh_plants / 50000.0

# Title
st.title("📋 GH3 Labor Planner")
st.markdown("---")

# --- GLOBAL ALLOCATION ENGINE WITH LEADING HAND RESTRICTION ---
absent_staff = st.session_state.get("absent_staff_input", [])
leading_hands_db_init = [
    s for s in st.session_state.staff_db if s["category"] == "Leading Hand"
]
lh_names_init = [lh["name"] for lh in leading_hands_db_init]
selected_leading_hands = st.session_state.get(
    "selected_leading_hands_filter", lh_names_init
)

# Eligible pool for regular tasks excludes Leading Hands
regular_available_pool = [
    s
    for s in st.session_state.staff_db
    if s["name"] not in absent_staff and s["category"] != "Leading Hand"
]
cat_priority = {"GG": 1, "TOTC": 2, "Urson": 3}
task_requirements = {
    t: c for t, c in st.session_state.active_tasks.items() if c > 0
}
total_requested = sum(task_requirements.values())

allocated_roster = {task: [] for task in task_requirements}


def allocate_by_tier(tier_index, match_label):
  for task_name, req_count in task_requirements.items():
    if task_name == "Leading Hand":
      continue  # Handled separately
    while len(allocated_roster[task_name]) < req_count:
      assigned_flat = [
          m["person"] for mems in allocated_roster.values() for m in mems
      ]
      unassigned_pool = [
          p for p in regular_available_pool if p not in assigned_flat
      ]

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

# Fallback for regular tasks
for task_name, req_count in task_requirements.items():
  if task_name == "Leading Hand":
    continue
  while len(allocated_roster[task_name]) < req_count:
    assigned_flat = [
        m["person"] for mems in allocated_roster.values() for m in mems
    ]
    unassigned_pool = [
        p for p in regular_available_pool if p not in assigned_flat
    ]

    if not unassigned_pool:
      break

    unassigned_pool.sort(key=lambda x: cat_priority.get(x["category"], 4))
    fallback_person = unassigned_pool[0]
    allocated_roster[task_name].append(
        {"person": fallback_person, "match_type": "No Match"}
    )

# Handle Leading Hand task allocation strictly
if "Leading Hand" in task_requirements:
  lh_req_count = task_requirements["Leading Hand"]
  active_lh_pool = [
      s
      for s in leading_hands_db_init
      if s["name"] not in absent_staff and s["name"] in selected_leading_hands
  ]
  for lh in active_lh_pool[:lh_req_count]:
    allocated_roster["Leading Hand"].append(
        {"person": lh, "match_type": "Primary"}
    )

# Determine Unassigned (Absent) vs Extra Available Staff (Not Required)
assigned_staff_flat = [
    m["person"] for mems in allocated_roster.values() for m in mems
]
absent_staff_records = [
    s for s in st.session_state.staff_db if s["name"] in absent_staff
]
extra_available_staff = [
    p
    for p in regular_available_pool + leading_hands_db_init
    if p not in assigned_staff_flat
    and p["name"] not in absent_staff
    and (
        p["category"] != "Leading Hand" or p["name"] in selected_leading_hands
    )
]


# --- 6 TABS ---
(
    tab_copy_lists,
    tab_planner,
    tab_smart_calc,
    tab_old_calc,
    tab_kpi,
    tab_progress,
) = st.tabs([
    "📱 Copy Lists",
    "📋 Roster & Allocation",
    "📊 Smart Headcount & Shift Hours",
    "🧮 Advanced Workload & Overtime Status",
    "⭐ Weekly KPI Tracker",
    "📈 Staff Progress & Skills",
])

# ==========================================
# TAB 1: COPY-PASTE READY LISTS (FIRST TAB)
# ==========================================
with tab_copy_lists:
  st.subheader("📱 Copy-Paste Ready Lists")
  st.markdown(
      f"**Total Staff Required:** `{total_requested}` workers across"
      f" `{len(task_requirements)}` tasks."
  )
  st.markdown("---")

  c_copy1, c_copy2 = st.columns(2)

  with c_copy1:
    st.markdown("**1. Grouped by Task Heading:**")
    task_text_output = "GH3 - WEEKLY LABOR PLAN (BY TASK)\n"
    task_text_output += f"Total Staff Required: {total_requested}\n"
    task_text_output += "-----------------------------------\n\n"

    for task, entries in allocated_roster.items():
      if not entries:
        continue
      task_text_output += (
          f"*{task.upper()} ({len(entries)}/{task_requirements.get(task, len(entries))})*\n"
      )
      for idx, item in enumerate(entries, 1):
        m = item["person"]
        t_note = (
            m.get("task_performance", {}).get(task, {}).get("notes", "")
        )
        note = f" - {t_note}" if t_note else ""
        task_text_output += f"{idx}. {m['name']} ({m['category']}){note}\n"
      task_text_output += "\n"

    if extra_available_staff:
      task_text_output += "*EXTRA AVAILABLE STAFF (NOT REQUIRED)*\n"
      for u in extra_available_staff:
        task_text_output += f"- {u['name']} ({u['category']})\n"
      task_text_output += "\n"

    if absent_staff_records:
      task_text_output += "*STANDBY / UNASSIGNED STAFF (ABSENT)*\n"
      for u in absent_staff_records:
        task_text_output += f"- {u['name']} ({u['category']})\n"

    st.code(task_text_output, language="text")

  with c_copy2:
    st.markdown("**2. Grouped by Employee Category:**")
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
          note = f" - {m['notes']}" if m['notes'] else ""
          cat_text_output += f"{idx}. {m['name']} - {m['task']}{note}\n"
        cat_text_output += "\n"

    if extra_available_staff:
      cat_text_output += "*EXTRA AVAILABLE STAFF (NOT REQUIRED)*\n"
      for u in extra_available_staff:
        cat_text_output += f"- {u['name']} ({u['category']})\n"
      cat_text_output += "\n"

    if absent_staff_records:
      cat_text_output += "*STANDBY / UNASSIGNED STAFF (ABSENT)*\n"
      for u in absent_staff_records:
        cat_text_output += f"- {u['name']} ({u['category']})\n"

    st.code(cat_text_output, language="text")


# ==========================================
# TAB 2: ROSTER PLANNER & STAFF CONTROLS
# ==========================================
with tab_planner:
  st.sidebar.header("⚙️ Roster Controls")

  with st.sidebar.expander("➕ Add Staff"):
    with st.form("add_staff_form", clear_on_submit=True):
      new_name = st.text_input("Name")
      new_cat = st.selectbox(
          "Category", ["GG", "TOTC", "Urson", "Leading Hand"]
      )

      opts = st.session_state.skills_list
      skill1 = st.selectbox("Primary Skill", opts)
      skill2 = st.selectbox("Secondary Skill", ["None"] + opts)
      skill3 = st.selectbox("Tertiary Skill", ["None"] + opts)

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

  with st.sidebar.expander("🎓 Update Skills", expanded=False):
    staff_names = [s["name"] for s in st.session_state.staff_db]
    selected_member_name = st.selectbox(
        "Select Member", options=[""] + staff_names, key="skill_select_member"
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
              "Primary", opts, index=opts.index(p_skill)
          )
          up_skill2 = st.selectbox(
              "Secondary",
              ["None"] + opts,
              index=(["None"] + opts).index(s_skill),
          )
          up_skill3 = st.selectbox(
              "Tertiary", ["None"] + opts, index=(["None"] + opts).index(t_skill)
          )

          submit_update = st.form_submit_button("Save Skills")
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
            st.sidebar.success("Updated!")
            st.rerun()

  with st.sidebar.expander("🎯 Target KPIs"):
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
    curr_settings = load_settings()
    curr_settings["task_targets"] = updated_targets
    save_settings(curr_settings)

  with st.sidebar.expander("🗑️ Remove Staff"):
    staff_names = [s["name"] for s in st.session_state.staff_db]
    to_remove = st.selectbox("Select Staff", options=[""] + staff_names)
    if st.button("Delete", type="primary"):
      if to_remove:
        st.session_state.staff_db = [
            s for s in st.session_state.staff_db if s["name"] != to_remove
        ]
        save_staff_data(st.session_state.staff_db)
        st.sidebar.warning(f"Removed {to_remove}")
        st.rerun()

  with st.sidebar.expander("💾 Backup DB"):
    json_data = json.dumps(st.session_state.staff_db, indent=4)
    st.download_button(
        label="📥 Download JSON",
        data=json_data,
        file_name="staff_db_backup.json",
        mime="application/json",
    )

  st.sidebar.markdown("---")

  col_ctrl1, col_ctrl2 = st.columns([1, 1.2])

  with col_ctrl1:
    st.subheader("1. Availability Check")
    all_names = [s["name"] for s in st.session_state.staff_db]
    absent_staff = st.multiselect(
        "Absent / Leave:", options=all_names, key="absent_staff_input"
    )

    leading_hands_db = [
        s for s in st.session_state.staff_db if s["category"] == "Leading Hand"
    ]
    lh_names = [lh["name"] for lh in leading_hands_db]
    st.markdown("---")
    st.subheader("⭐ Leading Hands")

    if "selected_leading_hands_filter" not in st.session_state:
      st.session_state["selected_leading_hands_filter"] = lh_names

    selected_leading_hands = st.multiselect(
        "Active Leading Hands:",
        options=lh_names,
        key="selected_leading_hands_filter",
    )

  with col_ctrl2:
    st.subheader("2. Task Headcounts")

    with st.expander("➕ Add Task Heading", expanded=False):
      task_add_options = st.session_state.skills_list + ["➕ Custom Task"]
      chosen_task_opt = st.selectbox("Task Name", task_add_options)
      task_name_to_add = chosen_task_opt
      if chosen_task_opt == "➕ Custom Task":
        custom_t_input = st.text_input("Type Name")
        if custom_t_input.strip():
          task_name_to_add = custom_t_input.strip()

      new_task_headcount = st.number_input("Headcount", min_value=1, value=4)
      if st.button("Add Task", type="primary"):
        if task_name_to_add and task_name_to_add != "➕ Custom Task":
          if task_name_to_add not in st.session_state.skills_list:
            st.session_state.skills_list.append(task_name_to_add)
            st.session_state.task_targets[task_name_to_add] = 100.0
          st.session_state.active_tasks[task_name_to_add] = new_task_headcount
          st.session_state[f"cnt_{task_name_to_add}"] = int(new_task_headcount)
          curr_sets = load_settings()
          curr_sets["active_tasks"] = st.session_state.active_tasks
          save_settings(curr_sets)
          st.rerun()

    st.markdown("**Adjust Headcounts:**")
    tasks_to_delete = []
    for task_name, count in list(st.session_state.active_tasks.items()):
      c_t1, c_t2, c_t3 = st.columns([3, 1.5, 0.6])
      c_t1.markdown(f"**{task_name}**")
      k = f"cnt_{task_name}"
      if k not in st.session_state:
        st.session_state[k] = int(count)

      def update_hc(t_name=task_name, key_name=k):
        val = int(st.session_state[key_name])
        st.session_state.active_tasks[t_name] = val
        curr_sets = load_settings()
        curr_sets["active_tasks"] = st.session_state.active_tasks
        save_settings(curr_sets)

      new_cnt = c_t2.number_input(
          "HC",
          min_value=0,
          step=1,
          key=k,
          on_change=update_hc,
          label_visibility="collapsed",
      )
      st.session_state.active_tasks[task_name] = int(new_cnt)

      if c_t3.button("🗑️", key=f"del_{task_name}", type="tertiary"):
        tasks_to_delete.append(task_name)

    if tasks_to_delete:
      for d_task in tasks_to_delete:
        if d_task in st.session_state.active_tasks:
          del st.session_state.active_tasks[d_task]
        if f"cnt_{d_task}" in st.session_state:
          del st.session_state[f"cnt_{d_task}"]
      curr_sets = load_settings()
      curr_sets["active_tasks"] = st.session_state.active_tasks
      save_settings(curr_sets)
      st.rerun()

  st.markdown("---")
  st.markdown(
      "**Skill Match Legend:** 🟢 `Primary` | 🟡 `Secondary` | ⚫ `Tertiary` |"
      " 🔴 `No Match`"
  )
  st.markdown("---")

  st.markdown(f"### 📊 Visual Labor Allocation Plan ({total_requested} Staff)")
  for task, entries in allocated_roster.items():
    req_c = task_requirements[task]
    st.markdown(f"**{task} ({len(entries)} / {req_c})**")
    for item in entries:
      m = item["person"]
      m_type = item["match_type"]
      icon_badge = (
          "🟢"
          if m_type == "Primary"
          else ("🟡" if m_type == "Secondary" else ("⚫" if m_type == "Tertiary" else "🔴"))
      )
      t_note = m.get("task_performance", {}).get(task, {}).get("notes", "")
      note_str = f" (*{t_note}*)" if t_note else ""
      st.write(f"- **{m['name']}** [{m['category']}] — {icon_badge}{note_str}")
    st.markdown("---")

  if extra_available_staff:
    st.info(
        f"💡 **Extra Available Staff (Not Required):** "
        + ", ".join([u["name"] for u in extra_available_staff])
    )
  if absent_staff_records:
    st.warning(
        f"⚠️ **Absent Staff:** "
        + ", ".join([u["name"] for u in absent_staff_records])
    )


# ==========================================
# TAB 3: SMART HEADCOUNT & SHIFT HOURS
# ==========================================
with tab_smart_calc:
  st.subheader("📊 Smart Headcount & Shift Hours")
  st.markdown(
      "Area is fixed at **5.0 ha (50,000 m²)** and Rows at **260**. Adjust"
      " **Plant Density per Row** below."
  )

  c_dim1, c_dim2, c_dim3 = st.columns(3)
  with c_dim1:
    st.markdown(
        "**Area (Constant)**<br><h3"
        " style='margin:0;color:#2D6A4F;'>5.0 ha</h3><small"
        " style='color:gray;'>50,000 m²</small>",
        unsafe_allow_html=True,
    )
  with c_dim2:
    st.markdown(
        "**Rows (Constant)**<br><h3"
        " style='margin:0;color:#2D6A4F;'>260 rows</h3>",
        unsafe_allow_html=True,
    )
  with c_dim3:
    st.session_state.calc_plants_per_row = st.number_input(
        "Plant Density per Row",
        min_value=1.0,
        value=float(st.session_state.calc_plants_per_row),
        step=10.0,
        key="smart_ppr_input",
    )

  total_gh_plants = 260 * st.session_state.calc_plants_per_row
  plant_density_sqm = total_gh_plants / 50000.0

  st.info(
      f"🌱 **Total Plants:** **{total_gh_plants:,.0f} plants** (260 rows ×"
      f" {st.session_state.calc_plants_per_row:,.1f} plants/row) &nbsp;|&nbsp;"
      f" 📐 **Density:** **{plant_density_sqm:,.2f} plants/m²**"
  )

  st.markdown("---")
  gh_crop_work_hrs_per_week = 7.35 * 5  # 36.75 hrs
  active_tasks_list = list(st.session_state.active_tasks.keys())

  st.markdown("### 📈 Staff Recommendations (Average KPI)")
  ash1, ash2, ash3, ash4 = st.columns([2, 1.2, 1.5, 1.5])
  ash1.markdown("**Task**")
  ash2.markdown("**Avg KPI**")
  ash3.markdown("**Exact HC**")
  ash4.markdown("**Rec. HC**")
  st.markdown("---")

  avg_kpi_calc_results = {}
  total_avg_rec_hc = 0
  total_avg_mh = 0.0

  clip_shoot_avg_rec = 0
  for task_name in active_tasks_list:
    if task_name == "Clip/Shoot & Pollination":
      avg_input_key = f"smart_avg_kpi_{task_name}"
      if avg_input_key not in st.session_state:
        default_avg = float(
            st.session_state.saved_avg_kpis.get(
                task_name,
                st.session_state.task_targets.get(task_name, 100.0),
            )
        )
        st.session_state[avg_input_key] = default_avg
      avg_kpi_val = float(st.session_state[avg_input_key])
      mh = total_gh_plants / avg_kpi_val if avg_kpi_val > 0 else 0
      exact_hc = (
          mh / gh_crop_work_hrs_per_week
          if gh_crop_work_hrs_per_week > 0
          else 0
      )
      clip_shoot_avg_rec = math.ceil(exact_hc)
      break

  for task_name in active_tasks_list:
    asc1, asc2, asc3, asc4 = st.columns([2, 1.2, 1.5, 1.5])
    asc1.markdown(f"**{task_name}**")

    if task_name in ["Leading Hand", "Others"]:
      current_val = float(st.session_state.active_tasks[task_name])
      asc2.markdown(
          f"<small style='color:gray;'>Fixed ({current_val})</small>",
          unsafe_allow_html=True,
      )
      mh = current_val * gh_crop_work_hrs_per_week
      exact_hc = current_val
      rec_hc = int(current_val)
      asc3.markdown(f"`{exact_hc:.2f}`")
      asc4.markdown(f"**{rec_hc}**")
    else:
      avg_input_key = f"smart_avg_kpi_{task_name}"
      if avg_input_key not in st.session_state:
        default_avg = float(
            st.session_state.saved_avg_kpis.get(
                task_name,
                st.session_state.task_targets.get(task_name, 100.0),
            )
        )
        st.session_state[avg_input_key] = default_avg


      def update_smart_avg(t_name=task_name, k=avg_input_key):
        val = float(st.session_state[k])
        st.session_state.saved_avg_kpis[t_name] = val
        curr_sets = load_settings()
        curr_sets["avg_kpis"] = st.session_state.saved_avg_kpis
        save_settings(curr_sets)


      avg_kpi_val = asc2.number_input(
          f"KPI {task_name}",
          min_value=1.0,
          value=float(st.session_state[avg_input_key]),
          step=10.0,
          key=avg_input_key,
          on_change=update_smart_avg,
          label_visibility="collapsed",
      )
      st.session_state.saved_avg_kpis[task_name] = avg_kpi_val

      mh = total_gh_plants / avg_kpi_val if avg_kpi_val > 0 else 0
      exact_hc = (
          mh / gh_crop_work_hrs_per_week
          if gh_crop_work_hrs_per_week > 0
          else 0
      )
      rec_hc = math.ceil(exact_hc)
      asc3.markdown(f"`{exact_hc:.2f}`")
      asc4.markdown(f"**{rec_hc}**")

    avg_kpi_calc_results[task_name] = {
        "exact": exact_hc,
        "recommended": rec_hc,
        "man_hours": mh,
    }
    total_avg_rec_hc += rec_hc
    total_avg_mh += mh

  # Pollination
  asc1_p, asc2_p, asc3_p, asc4_p = st.columns([2, 1.2, 1.5, 1.5])
  asc1_p.markdown("**Pollination**")
  asc2_p.markdown("`2500 (Fixed)`")
  poll_avg_hc = max(0, 12 - clip_shoot_avg_rec)
  poll_avg_mh = total_gh_plants / 2500.0
  asc3_p.markdown(f"`{float(poll_avg_hc):.2f}`")
  asc4_p.markdown(f"**{poll_avg_hc}**")
  total_avg_rec_hc += poll_avg_hc
  total_avg_mh += poll_avg_mh

  total_avg_hours = total_avg_rec_hc * 7.6 * 5
  st.markdown(
      f"""
        <div style="background: rgba(45,106,79,0.08); padding: 10px 14px; border-radius: 8px; border: 1px solid #C5DACB; margin-top: 8px; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 0.95rem; color: #1B4332;">
                <b>Total:</b> <b>{total_avg_rec_hc} Workers</b> | <b>{total_avg_mh:,.1f} Man-Hrs</b> | <b>{total_avg_hours:,.1f} Hrs</b>
            </p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  if st.button("🔄 Sync Average KPI Headcounts to Tab 2", type="primary"):
    for task_name, res in avg_kpi_calc_results.items():
      rec_val = 12 if task_name == "Clip/Shoot & Pollination" else int(res["recommended"])
      st.session_state.active_tasks[task_name] = rec_val
      if f"cnt_{task_name}" in st.session_state:
        del st.session_state[f"cnt_{task_name}"]
    curr_sets = load_settings()
    curr_sets["active_tasks"] = st.session_state.active_tasks
    save_settings(curr_sets)
    st.success("Synced successfully!")
    st.rerun()


# ==========================================
# TAB 4: ADVANCED WORKLOAD & OVERTIME STATUS
# ==========================================
with tab_old_calc:
  st.subheader("🧮 Workload & Overtime Status")

  c_ctrl1, c_ctrl2 = st.columns(2)
  with c_ctrl1:
    remaining_days = st.slider(
        "📅 Remaining Days",
        min_value=1.0,
        max_value=5.0,
        value=5.0,
        step=0.5,
        key="old_calc_rem_days",
    )
    max_allowed_hours = remaining_days * 8.0
  with c_ctrl2:
    st.markdown(
        f"**Setup:** `5 ha` × `260 rows` ×"
        f" `{st.session_state.calc_plants_per_row:.1f} pl/row`"
    )
    st.markdown(f"**Max limit:** `{max_allowed_hours:.1f} Hrs`")

  st.markdown("---")
  gh_crop_work_hrs_per_week = 36.75
  total_recommended_staff = sum(
      int(count) for count in st.session_state.active_tasks.values()
  )

  tasks_comparison_data = []
  for task_name, staff_qty in st.session_state.active_tasks.items():
    if task_name in ["Leading Hand", "Others"]:
      continue
    target_kpi = float(st.session_state.task_targets.get(task_name, 600.0))
    if task_name not in st.session_state.saved_avg_kpis:
      st.session_state.saved_avg_kpis[task_name] = target_kpi

    t_plants = total_gh_plants
    mh_target = t_plants / target_kpi if target_kpi > 0 else 0
    dur_target = mh_target / staff_qty if staff_qty > 0 else 0
    tasks_comparison_data.append({
        "name": task_name,
        "plants": t_plants,
        "staff": staff_qty,
        "target_kpi": target_kpi,
        "mh_target": mh_target,
        "dur_target": dur_target,
    })

  total_combined_avg_hours = 0.0
  active_support_tasks = [
      t
      for t in ["Leading Hand", "Others"]
      if t in st.session_state.active_tasks
      and int(st.session_state.active_tasks[t]) > 0
  ]

  st.markdown(
      '<div style="background-color: #FFFFFF; padding: 12px; border-radius: 10px; border: 1px solid #D5E3D8;">',
      unsafe_allow_html=True,
  )
  for task in tasks_comparison_data:
    input_key = f"unified_avg_kpi_{task['name']}"
    if input_key not in st.session_state:
      st.session_state[input_key] = float(
          st.session_state.saved_avg_kpis.get(task["name"], 100.0)
      )

    def update_unified_kpi(t_name=task["name"], k=input_key):
      val = float(st.session_state[k])
      st.session_state.saved_avg_kpis[t_name] = val
      curr_sets = load_settings()
      curr_sets["avg_kpis"] = st.session_state.saved_avg_kpis
      save_settings(curr_sets)

    is_clip_shoot = "clip/shoot" in task["name"].lower()
    limit_ref = (
        max_allowed_hours - ((9.0 / 5.0) * remaining_days)
        if is_clip_shoot
        else max_allowed_hours
    )

    c_n, c_s, c_k, c_h, c_st = st.columns([2.2, 1.0, 1.2, 1.4, 1.6])
    c_n.markdown(f"**{task['name']}**")
    c_s.markdown(f"`{task['staff']} S`")
    avg_kpi_val = c_k.number_input(
        "KPI",
        min_value=1.0,
        value=float(st.session_state[input_key]),
        step=10.0,
        key=input_key,
        on_change=update_unified_kpi,
        label_visibility="collapsed",
    )
    st.session_state.saved_avg_kpis[task["name"]] = avg_kpi_val

    mh_avg = task["plants"] / avg_kpi_val if avg_kpi_val > 0 else 0
    dur_avg = mh_avg / task["staff"] if task["staff"] > 0 else 0
    total_combined_avg_hours += mh_avg

    c_h.markdown(f"`{mh_avg:.1f}h` (`{dur_avg:.1f}h/w`)")
    if dur_avg > limit_ref:
      c_st.markdown(
          "<span style='color: #D32F2F;'>⚠️ Exceeds</span>",
          unsafe_allow_html=True,
      )
    else:
      c_st.markdown(
          "<span style='color: #1E7E34;'>✅ On Track</span>",
          unsafe_allow_html=True,
      )
    st.markdown(
        "<hr style='margin: 4px 0; border:0; border-top:1px solid"
        " #EAEFEA;'>",
        unsafe_allow_html=True,
    )

  for task_name in active_support_tasks:
    staff_qty = int(st.session_state.active_tasks[task_name])
    hours_per_worker = remaining_days * (gh_crop_work_hrs_per_week / 5.0)
    total_task_mh = staff_qty * hours_per_worker
    total_combined_avg_hours += total_task_mh

    c_n, c_s, c_k, c_h, c_st = st.columns([2.2, 1.0, 1.2, 1.4, 1.6])
    c_n.markdown(f"**{task_name}**")
    c_s.markdown(f"`{staff_qty} S`")
    c_k.markdown("<small>Fixed</small>", unsafe_allow_html=True)
    c_h.markdown(f"`{total_task_mh:.1f}h`")
    c_st.markdown(
        "<span style='color: #1E7E34;'>✅ Sched</span>", unsafe_allow_html=True
    )
    st.markdown(
        "<hr style='margin: 4px 0; border:0; border-top:1px solid"
        " #EAEFEA;'>",
        unsafe_allow_html=True,
    )

  st.markdown("</div>", unsafe_allow_html=True)

  coffee_break_hours = total_recommended_staff * 0.25 * remaining_days
  final_grand_total = total_combined_avg_hours + coffee_break_hours
  st.markdown(
      f"""
        <div style="background: linear-gradient(135deg, #2D6A4F 0%, #1B4332 100%); padding: 10px 14px; border-radius: 10px; color: #FFFFFF; margin-top: 10px;">
            <b>Grand Total:</b> {final_grand_total:,.2f} Man-Hours (Includes {coffee_break_hours:.1f}h breaks)
        </div>
        """,
      unsafe_allow_html=True,
  )


# ==========================================
# TAB 5: WEEKLY TASK-SPECIFIC KPI TRACKER
# ==========================================
with tab_kpi:
  st.subheader("⭐ Weekly KPI & Quality Evaluation")
  kpi_tasks_list = [
      t for t in st.session_state.skills_list if t != "Leading Hand"
  ]
  selected_task_to_eval = st.selectbox(
      "Select Task:", options=kpi_tasks_list, key="eval_task_select"
  )
  target_val_for_task = st.session_state.task_targets.get(
      selected_task_to_eval, 100.0
  )
  st.info(
      f"🎯 Target KPI for **{selected_task_to_eval}**: **{target_val_for_task}**"
  )

  relevant_staff = [
      s
      for s in st.session_state.staff_db
      if selected_task_to_eval in s.get("skills", [])
  ]

  if not relevant_staff:
    st.warning(f"No staff trained in {selected_task_to_eval}.")
  else:
    with st.form(f"kpi_form_{selected_task_to_eval}"):
      form_inputs = {}
      for person in relevant_staff:
        c1, c2, c3, c4 = st.columns([1.5, 1.2, 0.8, 1.5])
        c1.markdown(f"**{person['name']}**")
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
            "Q",
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
            placeholder="Notes",
        )
        form_inputs[person["name"]] = {
            "kpi": kpi_in,
            "quality": qual_in,
            "notes": note_in,
        }

      if st.form_submit_button(
          f"💾 Save Ratings for {selected_task_to_eval}", type="primary"
      ):
        for person in st.session_state.staff_db:
          name = person["name"]
          if name in form_inputs:
            if "task_performance" not in person:
              person["task_performance"] = {}
            person["task_performance"][selected_task_to_eval] = form_inputs[name]
        save_staff_data(st.session_state.staff_db)
        st.success("Saved successfully!")
        st.rerun()


# ==========================================
# TAB 6: STAFF PROGRESS & SKILLS DIRECTORY
# ==========================================
with tab_progress:
  st.subheader("📈 Staff Skills Directory")
  search_query = st.text_input("🔍 Search staff:", key="staff_search_progress")

  for person in st.session_state.staff_db:
    if not search_query or search_query.lower() in person["name"].lower():
      with st.expander(
          f"👤 **{person['name']}** (`{person['category']}`)"
      ):
        col_p1, col_p2 = st.columns([1, 1.5])
        with col_p1:
          st.markdown("##### 🛠️ Skills")
          for idx, sk in enumerate(person.get("skills", [])):
            st.markdown(f"- {sk}")
        with col_p2:
          st.markdown("##### 📊 KPI Records")
          for t_name, metrics in person.get("task_performance", {}).items():
            st.markdown(
                f"- **{t_name}**: KPI **{metrics.get('kpi', 100)}** |"
                f" {metrics.get('quality', '👍')}"
            )
