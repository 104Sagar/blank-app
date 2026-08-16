import json
import math
import os
import streamlit as st
from datetime import datetime

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
    /* Main App Background & Typography (Slightly Darker Sage Gradient) */
    .stApp {
        background: linear-gradient(135deg, #C2D6C6 0%, #D6E3D8 40%, #B8CDBC 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 13px;
    }
    
    /* Compact Headings */
    h1 { font-size: 1.4rem !important; margin-bottom: 0.2rem !important; }
    h2 { font-size: 1.15rem !important; margin-top: 0.4rem !important; }
    h3 { font-size: 1.0rem !important; margin-top: 0.3rem !important; }

    /* Force Streamlit Columns to Stay Side-by-Side on Mobile (Prevent Stacking) */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0.4rem !important;
        align-items: center !important;
    }
    div[data-testid="stColumn"] {
        flex: 1 1 0% !important;
        min-width: 0 !important;
        padding: 0.1rem 0.2rem !important;
        background: rgba(255, 255, 255, 0.92) !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(27, 47, 33, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.95) !important;
        margin-bottom: 0.3rem !important;
    }

    /* Sidebar Styling */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #C4D3C7 0%, #D0DEC5 100%) !important;
        border-right: 1px solid rgba(46, 125, 50, 0.18) !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #B5CBC0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        margin-bottom: 0.4rem !important;
    }

    /* Form Inputs */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="base-input"] {
        border-radius: 6px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #A8C2B3 !important;
        font-size: 12.5px !important;
    }

    /* Primary Buttons & Form Submit Buttons */
    .stButton > button[kind="primary"], .stFormSubmitButton > button {
        border-radius: 6px !important;
        background: linear-gradient(135deg, #2D6A4F 0%, #1B4332 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.3rem 0.8rem !important;
        box-shadow: 0 2px 6px rgba(45, 106, 79, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }

    /* Trash / Tertiary Action Buttons Styling */
    .stButton > button[kind="tertiary"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 1.0rem !important;
        padding: 0.1rem 0.2rem !important;
        color: #D32F2F !important;
        width: auto !important;
    }

    /* Code Output Box Styling */
    div[data-testid="stCodeBlock"] {
        border-radius: 8px !important;
        border: 1px solid #A8C2B3 !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02) !important;
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

# Persistent Per-Task Row Progress loaded from settings
if "task_row_progress" not in st.session_state:
  st.session_state.task_row_progress = saved_settings.get(
      "task_row_progress", {}
  )

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
            "Truss Pruning": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Truss Support": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
                "history": [],
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
            "Truss Pruning": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Truss Support": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
                "history": [],
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
            "Truss Pruning": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Truss Support": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
        },
    },
    {
        "name": "Rebecca",
        "category": "Leading Hand",
        "skills": ["Leading Hand"],
        "task_performance": {
            "Leading Hand": {
                "kpi": 100.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            }
        },
    },
    {
        "name": "Rene",
        "category": "Leading Hand",
        "skills": ["Leading Hand", "Others"],
        "task_performance": {
            "Leading Hand": {
                "kpi": 100.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Others": {
                "kpi": 100.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
        },
    },
    {
        "name": "Tico",
        "category": "Leading Hand",
        "skills": ["Leading Hand"],
        "task_performance": {
            "Leading Hand": {
                "kpi": 100.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            }
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
                "history": [],
            },
            "Truss Support": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
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
                "history": [],
            },
            "De-leafing": {
                "kpi": 800.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
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
                "history": [],
            },
            "Truss Pruning": {
                "kpi": 90.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
        },
    },
    {
        "name": "Dan",
        "category": "TOTC",
        "skills": ["De-leafing", "Lowering"],
        "task_performance": {
            "De-leafing": {
                "kpi": 800.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Lowering": {
                "kpi": 1333.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
        },
    },
    {
        "name": "Will",
        "category": "TOTC",
        "skills": ["De-leafing", "Truss Support"],
        "task_performance": {
            "De-leafing": {
                "kpi": 800.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Truss Support": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
        },
    },
    {
        "name": "Terry",
        "category": "TOTC",
        "skills": ["Others", "De-leafing"],
        "task_performance": {
            "Others": {
                "kpi": 100.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "De-leafing": {
                "kpi": 800.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
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
                "history": [],
            },
            "De-leafing": {
                "kpi": 800.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
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
                "history": [],
            },
            "Truss Support": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
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
                "history": [],
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
                "history": [],
            },
            "Lowering": {
                "kpi": 1333.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
        },
    },
    {
        "name": "Rosyfa",
        "category": "Urson",
        "skills": ["Truss Pruning", "Truss Support"],
        "task_performance": {
            "Truss Pruning": {
                "kpi": 95.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Truss Support": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
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
                "history": [],
            },
            "Others": {
                "kpi": 100.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
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
                "history": [],
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
                "history": [],
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
                "history": [],
            }
        },
    },
    {
        "name": "Dhia",
        "category": "Urson",
        "skills": ["De-leafing", "Truss Pruning"],
        "task_performance": {
            "De-leafing": {
                "kpi": 800.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Truss Pruning": {
                "kpi": 90.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
        },
    },
    {
        "name": "Cassy",
        "category": "Urson",
        "skills": ["De-leafing"],
        "task_performance": {
            "De-leafing": {
                "kpi": 800.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            }
        },
    },
    {
        "name": "Erica",
        "category": "Urson",
        "skills": ["De-leafing", "Truss Support"],
        "task_performance": {
            "De-leafing": {
                "kpi": 800.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Truss Support": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
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
            "Truss Pruning": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Truss Support": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
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
            "Truss Pruning": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Clip/Shoot & Pollination": {
                "kpi": 674.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
            "Truss Support": {
                "kpi": 1200.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
        },
    },
    {
        "name": "Panyawat",
        "category": "Urson",
        "skills": ["Others"],
        "task_performance": {
            "Others": {
                "kpi": 100.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            }
        },
    },
    {
        "name": "AkashDeep",
        "category": "Urson",
        "skills": ["Others"],
        "task_performance": {
            "Others": {
                "kpi": 100.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            }
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
            "Leading Hand": {
                "kpi": 100.0,
                "quality": "👍",
                "notes": "",
                "history": [],
            }
        },
    })
    modified = True

  for person in data:
    if "task_performance" not in person:
      person["task_performance"] = {}
      modified = True

    for sk, perf in person["task_performance"].items():
      if "history" not in perf:
        perf["history"] = []
        modified = True

    skills = person.get("skills", [])
    for sk in skills:
      if sk not in person["task_performance"]:
        default_t = st.session_state.get("task_targets", {}).get(sk, 100.0)
        person["task_performance"][sk] = {
            "kpi": default_t,
            "quality": "👍",
            "notes": "",
            "history": [],
        }
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
      continue
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
              task_name,
              {"kpi": def_t, "quality": "👍", "notes": "", "history": []},
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


# --- 7 TABS ---
(
    tab_copy_lists,
    tab_planner,
    tab_smart_calc,
    tab_old_calc,
    tab_kpi,
    tab_progress,
    tab_row_tracker,
) = st.tabs([
    "📱 Copy Lists",
    "📋 Roster & Allocation",
    "📊 Smart Headcount & Shift Hours",
    "🧮 Workload & Status",
    "⭐ Weekly KPI Tracker",
    "📈 Staff Progress & Trends",
    "📌 Row Progress",
])

# ==========================================
# TAB 1: COPY-PASTE READY LISTS
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

    st.code(cat_text_output, language="text")

  st.markdown("---")

  st.markdown("**3. Standby, Unassigned & Extra Staff Lists:**")
  unassigned_text_output = "GH3 - STANDBY & UNASSIGNED STAFF\n"
  unassigned_text_output += "-----------------------------------\n\n"

  if extra_available_staff:
    unassigned_text_output += "*EXTRA AVAILABLE STAFF (NOT REQUIRED)*\n"
    for idx, u in enumerate(extra_available_staff, 1):
      unassigned_text_output += f"{idx}. {u['name']} ({u['category']})\n"
    unassigned_text_output += "\n"

  if absent_staff_records:
    unassigned_text_output += "*ABSENT / ON LEAVE*\n"
    for idx, u in enumerate(absent_staff_records, 1):
      unassigned_text_output += f"{idx}. {u['name']} ({u['category']})\n"

  if not extra_available_staff and not absent_staff_records:
    unassigned_text_output += "None\n"

  st.code(unassigned_text_output, language="text")


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
          t_perf[sk] = {
              "kpi": def_t,
              "quality": "👍",
              "notes": "",
              "history": [],
          }

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
                    "history": [],
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

  # ==========================================
  # SECTION 1: STAFF RECOMMENDATIONS (AVERAGE KPI)
  # ==========================================
  st.markdown("### 📈 Staff Recommendations (Based on Average KPI)")
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

  # Pollination (Average KPI - factored for 3x a week)
  asc1_p, asc2_p, asc3_p, asc4_p = st.columns([2, 1.2, 1.5, 1.5])
  asc1_p.markdown("**Pollination (3x/wk)**")
  asc2_p.markdown("`2500 (Fixed)`")
  poll_avg_hc = max(0, 12 - clip_shoot_avg_rec)
  poll_avg_mh = (total_gh_plants / 2500.0) * 3
  asc3_p.markdown(f"`{float(poll_avg_hc):.2f}`")
  asc4_p.markdown(f"**{poll_avg_hc}**")
  total_avg_rec_hc += poll_avg_hc
  total_avg_mh += poll_avg_mh

  total_avg_hours = total_avg_rec_hc * 7.6 * 5
  st.markdown(
      f"""
        <div style="background: rgba(45,106,79,0.08); padding: 10px 14px; border-radius: 8px; border: 1px solid #C5DACB; margin-top: 8px; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 0.95rem; color: #1B4332;">
                <b>Average Total:</b> <b>{total_avg_rec_hc} Workers</b> | <b>{total_avg_mh:,.1f} Man-Hrs</b>
            </p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  st.markdown("---")

  # ==========================================
  # SECTION 2: STAFF RECOMMENDATIONS (TARGET KPI)
  # ==========================================
  st.markdown("### 🎯 Staff Recommendations (Based on Target KPI)")
  sh1, sh2, sh3, sh4 = st.columns([2, 1.2, 1.5, 1.5])
  sh1.markdown("**Task**")
  sh2.markdown("**Target KPI**")
  sh3.markdown("**Exact HC**")
  sh4.markdown("**Rec. HC**")
  st.markdown("---")

  target_kpi_calc_results = {}
  total_target_rec_hc = 0
  total_target_mh = 0.0

  clip_shoot_target_rec = 0
  for task_name in active_tasks_list:
    if task_name == "Clip/Shoot & Pollination":
      default_target = float(
          st.session_state.task_targets.get(task_name, 100.0)
      )
      mh = total_gh_plants / default_target if default_target > 0 else 0
      exact_hc = (
          mh / gh_crop_work_hrs_per_week
          if gh_crop_work_hrs_per_week > 0
          else 0
      )
      clip_shoot_target_rec = math.ceil(exact_hc)
      break

  for task_name in active_tasks_list:
    sc1, sc2, sc3, sc4 = st.columns([2, 1.2, 1.5, 1.5])
    sc1.markdown(f"**{task_name}**")

    if task_name in ["Leading Hand", "Others"]:
      current_val = float(st.session_state.active_tasks[task_name])
      sc2.markdown(
          f"<small style='color:gray;'>Fixed ({current_val})</small>",
          unsafe_allow_html=True,
      )
      mh = current_val * gh_crop_work_hrs_per_week
      exact_hc = current_val
      rec_hc = int(current_val)
      sc3.markdown(f"`{exact_hc:.2f}`")
      sc4.markdown(f"**{rec_hc}**")
    else:
      default_target = float(
          st.session_state.task_targets.get(task_name, 100.0)
      )
      target_kpi_input = sc2.number_input(
          f"Target {task_name}",
          min_value=1.0,
          value=default_target,
          step=10.0,
          key=f"smart_target_kpi_{task_name}",
          label_visibility="collapsed",
      )
      st.session_state.task_targets[task_name] = target_kpi_input

      mh = total_gh_plants / target_kpi_input if target_kpi_input > 0 else 0
      exact_hc = (
          mh / gh_crop_work_hrs_per_week
          if gh_crop_work_hrs_per_week > 0
          else 0
      )
      rec_hc = math.ceil(exact_hc)
      sc3.markdown(f"`{exact_hc:.2f}`")
      sc4.markdown(f"**{rec_hc}**")

    target_kpi_calc_results[task_name] = {
        "exact": exact_hc,
        "recommended": rec_hc,
        "man_hours": mh,
    }
    total_target_rec_hc += rec_hc
    total_target_mh += mh

  # Pollination (Target KPI - factored for 3x a week)
  sc1_p, sc2_p, sc3_p, sc4_p = st.columns([2, 1.2, 1.5, 1.5])
  sc1_p.markdown("**Pollination (3x/wk)**")
  sc2_p.markdown("`2500 (Fixed)`")
  poll_target_hc = max(0, 12 - clip_shoot_target_rec)
  poll_target_mh = (total_gh_plants / 2500.0) * 3
  sc3_p.markdown(f"`{float(poll_target_hc):.2f}`")
  sc4_p.markdown(f"**{poll_target_hc}**")
  total_target_rec_hc += poll_target_hc
  total_target_mh += poll_target_mh

  total_target_hours = total_target_rec_hc * 7.6 * 5
  st.markdown(
      f"""
        <div style="background: rgba(45,106,79,0.08); padding: 10px 14px; border-radius: 8px; border: 1px solid #C5DACB; margin-top: 8px; margin-bottom: 15px;">
            <p style="margin: 0; font-size: 0.95rem; color: #1B4332;">
                <b>Target Total:</b> <b>{total_target_rec_hc} Workers</b> | <b>{total_target_mh:,.1f} Man-Hrs</b>
            </p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  st.markdown("---")

  if st.button("🔄 Sync Average KPI Headcounts to Tab 2", type="primary"):
    for task_name, res in avg_kpi_calc_results.items():
      rec_val = (
          12
          if task_name == "Clip/Shoot & Pollination"
          else int(res["recommended"])
      )
      st.session_state.active_tasks[task_name] = rec_val
      if f"cnt_{task_name}" in st.session_state:
        del st.session_state[f"cnt_{task_name}"]
    curr_sets = load_settings()
    curr_sets["active_tasks"] = st.session_state.active_tasks
    save_settings(curr_sets)
    st.success("Synced successfully!")
    st.rerun()


# ==========================================
# TAB 4: WORKLOAD & STATUS
# ==========================================
with tab_old_calc:
  st.subheader("🧮 Workload & Overtime Status Dashboard")
  st.markdown(
      "Review the comprehensive workload, total man-hours, and weekly pace"
      " per worker across all active tasks."
  )

  c_ctrl1, c_ctrl2 = st.columns(2)
  with c_ctrl1:
    remaining_days = st.slider(
        "📅 Remaining Days in Week",
        min_value=1.0,
        max_value=5.0,
        value=5.0,
        step=0.5,
        key="old_calc_rem_days",
    )
    max_allowed_hours = remaining_days * 8.0
  with c_ctrl2:
    st.markdown(
        f"**Greenhouse Setup:** `5 ha` (50,000 m²) | `260 rows` ×"
        f" `{st.session_state.calc_plants_per_row:.1f} pl/row`"
    )
    st.markdown(f"**Max Weekly Reference Limit:** `{max_allowed_hours:.1f}h`")

  st.markdown("---")
  gh_crop_work_hrs_per_week = 36.75
  total_recommended_staff = sum(
      int(count) for count in st.session_state.active_tasks.values()
  )
  total_combined_avg_hours = 0.0

  # Render task-specific cards
  for task_name, staff_qty in st.session_state.active_tasks.items():
    if staff_qty <= 0:
      continue

    is_support = task_name in ["Leading Hand", "Others"]

    if is_support:
      hours_per_worker = remaining_days * (gh_crop_work_hrs_per_week / 5.0)
      task_mh = staff_qty * hours_per_worker
      dur_avg = hours_per_worker
      kpi_display = "Fixed Support Allocation"
      status_badge = (
          "<span style='color: #1E7E34; background: rgba(30,126,52,0.1); padding:"
          " 2px 8px; border-radius: 4px; font-weight: 600;'>✅ Scheduled"
          " Support</span>"
      )
    else:
      kpi_val = float(
          st.session_state.saved_avg_kpis.get(
              task_name, st.session_state.task_targets.get(task_name, 600.0)
          )
      )
      task_mh = total_gh_plants / kpi_val if kpi_val > 0 else 0

      kpi_display = f"KPI Rate: {kpi_val:,.1f} plants/worker/day"
      dur_avg = task_mh / staff_qty if staff_qty > 0 else 0

      # Compare against standard maximum allowed hours without arbitrary deductions
      limit_ref = max_allowed_hours

      if dur_avg > limit_ref:
        status_badge = (
            "<span style='color: #D32F2F; background:"
            " rgba(211,47,47,0.1); padding: 2px 8px; border-radius: 4px;"
            " font-weight: 600;'>⚠️ Exceeds Limit</span>"
        )
      else:
        status_badge = (
            "<span style='color: #1E7E34; background:"
            " rgba(30,126,52,0.1); padding: 2px 8px; border-radius: 4px;"
            " font-weight: 600;'>✅ On Track</span>"
        )

    total_combined_avg_hours += task_mh

    st.markdown(
        f"""
        <div style="background: #FFFFFF; padding: 14px 18px; border-radius: 10px; border: 1px solid #B5CBC0; box-shadow: 0 2px 6px rgba(0,0,0,0.02); margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h4 style="margin: 0; color: #1B4332; font-size: 1.1rem;">📋 {task_name}</h4>
                <span style="background: rgba(45,106,79,0.1); color: #2D6A4F; padding: 3px 10px; border-radius: 6px; font-weight: 600; font-size: 0.85rem;">{staff_qty} Workers Assigned</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; color: #333; border-top: 1px solid #EAEFEA; padding-top: 8px; flex-wrap: wrap; gap: 8px;">
                <div><b>{kpi_display}</b></div>
                <div>Total Man-Hours: <b>{task_mh:,.1f}h</b></div>
                <div>Weekly Pace: <b>{dur_avg:,.1f}h / worker</b></div>
                <div>Status: {status_badge}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  coffee_break_hours = total_recommended_staff * 0.25 * remaining_days
  final_grand_total = total_combined_avg_hours + coffee_break_hours

  st.markdown(
      f"""
        <div style="background: linear-gradient(135deg, #2D6A4F 0%, #1B4332 100%); padding: 12px 18px; border-radius: 10px; color: #FFFFFF; margin-top: 15px; display: flex; justify-content: space-between; align-items: center;">
            <div><b>Grand Total Workload:</b> {final_grand_total:,.2f} Man-Hours</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Includes {coffee_break_hours:.1f}h coffee breaks</div>
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
            {
                "kpi": target_val_for_task,
                "quality": "👍",
                "notes": "",
                "history": [],
            },
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
        current_date_str = datetime.now().strftime("%d %b %Y")
        for person in st.session_state.staff_db:
          name = person["name"]
          if name in form_inputs:
            if "task_performance" not in person:
              person["task_performance"] = {}
            if selected_task_to_eval not in person["task_performance"]:
              person["task_performance"][selected_task_to_eval] = {
                  "history": []
              }

            old_perf = person["task_performance"][selected_task_to_eval]
            old_kpi = old_perf.get("kpi")
            old_qual = old_perf.get("quality")

            history_list = old_perf.get("history", [])
            if old_kpi is not None:
              history_list.append({
                  "date": current_date_str,
                  "kpi": old_kpi,
                  "quality": old_qual,
              })

            new_data = form_inputs[name]
            new_data["history"] = history_list
            person["task_performance"][selected_task_to_eval] = new_data

        save_staff_data(st.session_state.staff_db)
        st.success(
            "Saved successfully! Historical KPI trends updated automatically."
        )
        st.rerun()


# ==========================================
# TAB 6: STAFF PROGRESS & HISTORICAL TRENDS
# ==========================================
with tab_progress:
  st.subheader("📈 Staff Skills & Historical KPI Trends")
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
          st.markdown("##### 📊 Current KPI & Historical Trends")
          chart_data = {}
          for t_name, metrics in person.get("task_performance", {}).items():
            current_kpi = metrics.get("kpi", 100)
            current_qual = metrics.get("quality", "👍")
            st.markdown(
                f"- **{t_name}**: Current KPI **{current_kpi}** |"
                f" {current_qual}"
            )

            history = metrics.get("history", [])
            chart_data[t_name] = current_kpi

            if history:
              history_str = ", ".join([
                  f"{h['date']}: {h['kpi']} ({h['quality']})" for h in history
              ])
              st.markdown(
                  f"&nbsp;&nbsp;&nbsp;&nbsp;<small"
                  f" style='color:gray;'>History: {history_str}</small>"
              )
            else:
              st.markdown(
                  "&nbsp;&nbsp;&nbsp;&nbsp;<small"
                  " style='color:gray;'>History: No prior weekly logs"
                  " yet</small>"
              )

          if chart_data:
            st.markdown(
                "<small style='color:#2D6A4F; font-weight:600;'>KPI Bar"
                " Summary:</small>",
                unsafe_allow_html=True,
            )
            st.bar_chart(chart_data)


# ==========================================
# TAB 7: TASK-SPECIFIC ROW PROGRESS TRACKER
# ==========================================
with tab_row_tracker:
  st.subheader("📌 Task-Specific Greenhouse Row Progress Tracker")
  st.markdown(
      "Track completed rows independently per task, along with estimated"
      " remaining work hours based on remaining rows."
  )

  active_tasks_list = list(st.session_state.active_tasks.keys())
  for t_name in active_tasks_list:
    if t_name not in st.session_state.task_row_progress:
      st.session_state.task_row_progress[t_name] = 0

  for task_name in active_tasks_list:
    current_task_completed = st.session_state.task_row_progress.get(
        task_name, 0
    )

    # Calculate total man-hours required for this task based on current KPI
    if task_name in ["Leading Hand", "Others"]:
      task_total_mh = float(st.session_state.active_tasks.get(task_name, 2)) * 36.75
    else:
      kpi_val = float(
          st.session_state.saved_avg_kpis.get(
              task_name, st.session_state.task_targets.get(task_name, 600.0)
          )
      )
      task_total_mh = total_gh_plants / kpi_val if kpi_val > 0 else 0.0

    remaining_rows_count = 260 - current_task_completed
    remaining_work_hours = (remaining_rows_count / 260.0) * task_total_mh

    st.markdown(
        f"<div style='background: #FFFFFF; padding: 14px 18px; border-radius: 10px; border: 1px solid #B5CBC0; box-shadow: 0 2px 6px rgba(0,0,0,0.02); margin-bottom: 15px;'>"
        f"<h4 style='margin: 0 0 8px 0; color: #1B4332;'>📋 {task_name}</h4>",
        unsafe_allow_html=True,
    )

    c_b1, c_b2, c_b3, c_b4 = st.columns(4)
    if c_b1.button("➕ 10 Rows", key=f"p10_{task_name}"):
      st.session_state.task_row_progress[task_name] = min(
          260, current_task_completed + 10
      )
      save_settings({
          "completed_rows_count": saved_settings.get(
              "completed_rows_count", 0
          ),
          "active_tasks": st.session_state.active_tasks,
          "task_targets": st.session_state.task_targets,
          "avg_kpis": st.session_state.saved_avg_kpis,
          "task_row_progress": st.session_state.task_row_progress,
      })
      st.rerun()

    if c_b2.button("➕ 50 Rows", key=f"p50_{task_name}"):
      st.session_state.task_row_progress[task_name] = min(
          260, current_task_completed + 50
      )
      save_settings({
          "completed_rows_count": saved_settings.get(
              "completed_rows_count", 0
          ),
          "active_tasks": st.session_state.active_tasks,
          "task_targets": st.session_state.task_targets,
          "avg_kpis": st.session_state.saved_avg_kpis,
          "task_row_progress": st.session_state.task_row_progress,
      })
      st.rerun()

    if c_b3.button("Reset", key=f"preset_{task_name}"):
      st.session_state.task_row_progress[task_name] = 0
      save_settings({
          "completed_rows_count": saved_settings.get(
              "completed_rows_count", 0
          ),
          "active_tasks": st.session_state.active_tasks,
          "task_targets": st.session_state.task_targets,
          "avg_kpis": st.session_state.saved_avg_kpis,
          "task_row_progress": st.session_state.task_row_progress,
      })
      st.rerun()

    if c_b4.button("Complete All", key=f"pall_{task_name}"):
      st.session_state.task_row_progress[task_name] = 260
      save_settings({
          "completed_rows_count": saved_settings.get(
              "completed_rows_count", 0
          ),
          "active_tasks": st.session_state.active_tasks,
          "task_targets": st.session_state.task_targets,
          "avg_kpis": st.session_state.saved_avg_kpis,
          "task_row_progress": st.session_state.task_row_progress,
      })
      st.rerun()

    def update_task_slider(t=task_name):
      curr_sets = load_settings()
      if "task_row_progress" not in curr_sets:
        curr_sets["task_row_progress"] = {}
      curr_sets["task_row_progress"][t] = st.session_state[f"slider_{t}"]
      save_settings(curr_sets)

    slider_val = st.slider(
        f"Rows Completed for {task_name}:",
        min_value=0,
        max_value=260,
        value=int(current_task_completed),
        step=1,
        key=f"slider_{task_name}",
        on_change=update_task_slider,
    )
    st.session_state.task_row_progress[task_name] = slider_val

    pct = (slider_val / 260.0) * 100.0
    st.markdown(
        f"<p style='margin: 4px 0 0 0; color: #333; font-size: 0.9rem;'>"
        f"Progress: <b>{slider_val} / 260 rows</b> ({pct:.1f}% completed) &nbsp;|&nbsp; "
        f"Remaining Rows: <b>{remaining_rows_count} rows</b> &nbsp;|&nbsp; "
        f"Est. Remaining Work: <b style='color:#2D6A4F;'>{remaining_work_hours:,.1f}h</b>"
        f"</p>",
        unsafe_allow_html=True,
    )
    st.progress(slider_val / 260.0)
    st.markdown("</div>", unsafe_allow_html=True)
