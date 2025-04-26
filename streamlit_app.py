import streamlit as st
import random
import json
import os

# Set page config first!
st.set_page_config(page_title="Tivmir World Tools", layout="centered")

# === Load Data Functions ===
@st.cache_data #Caches JSON files
def load_json(filename):
    try:
        path = os.path.join("data", filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return [] if "list" in filename else {}

# === Load Data ===
races = load_json("races.json")
npc_attributes = load_json("npc_attributes.json")
tabaxi_prefixes = load_json("tabaxi_prefixes.json")
tabaxi_middles = load_json("tabaxi_middles.json")
tabaxi_suffixes = load_json("tabaxi_suffixes.json")
tabaxi_poetic_gloss = load_json("tabaxi_poetic_gloss.json")
tabaxi_clans = load_json("tabaxi_clans.json")
elven_prefixes = load_json("elven_prefixes.json")
elven_middles = load_json("elven_middles.json")
elven_suffixes = load_json("elven_suffixes.json")
elven_poetic_gloss = load_json("elven_poetic_gloss.json")

# === Emoji Icons ===
icons = {
    "Appearance": "👁️",
    "Worships": "🙏",
    "Quirk": "🎭",
    "Secret": "🔒",
    "Goal": "🎯",
    "Fear": "😨",
    "Profession": "🔮",
    "Ally": "🧡"
}

# === Helper Functions for Name Generation ===

VOWELS = "aeiouyáéíóúàèìòùâêîôûäëïöü" # Define vowels (adjust if needed)

def _is_vowel(char):
  """Checks if a single character is a vowel (case-insensitive)."""
  return char.lower() in VOWELS

# I might not need _is_vowel if I manually set flags in JSON,
# but it could be useful for auto-generating flags later.

def _is_smooth_transition(prev_part_ends_vowel, current_part_starts_vowel):
  """Checks if joining two parts is phonetically smooth (avoids vowel+vowel)."""
  # Returns True if it's NOT (vowel + vowel), False otherwise.
  return not (prev_part_ends_vowel and current_part_starts_vowel)

def _pick_smooth_part(part_list, prev_part_ends_vowel):
  """Picks a random part from the list, preferring smooth transitions."""
  if not part_list: # Handle empty list case
      st.warning("Attempted to pick from an empty name part list.")
      return None # Or return a default placeholder part

  # Find parts that start smoothly after the previous part
  smooth_options = [
      part for part in part_list
      if _is_smooth_transition(prev_part_ends_vowel, part["starts_vowel"])
  ]

  if smooth_options:
      # If smooth options exist, pick one randomly
      return random.choice(smooth_options)
  else:
      # Fallback: If NO smooth options exist (e.g., prev ends vowel, all options start vowel),
      # just pick any part randomly to avoid errors. The name might sound slightly less smooth.
      # st.info("Note: No perfectly smooth name transition found, choosing randomly.") # Optional debug info
      return random.choice(part_list)

def _generate_poetic_meaning(parts, poetic_gloss_dict):
    """Generates a poetic meaning string from chosen name parts and a gloss dictionary."""
    if not parts:
        return ""

    keywords = [p["meaning"].split("/")[0].strip() for p in parts] # Takes first meaning if '/' present
    glosses = [random.choice(poetic_gloss_dict.get(k, [k])) for k in keywords] # Gets poetic variations

    # Choose a template based on the number of parts/glosses
    if len(glosses) == 2:
        templates = [
            f"{glosses[0].title()} of {glosses[1]}",
            f"Bearer of {glosses[1]}, born of {glosses[0]}",
            f"A soul touched by {glosses[0]} and {glosses[1]}",
            f"Walker of {glosses[0]} and {glosses[1]}", # Added another option
            f"Voice of the {glosses[1]}, spirit of {glosses[0]}" # Added another option
        ]
    elif len(glosses) == 3:
         templates = [
            f"One who walks with {glosses[0]}, guided by {glosses[1]}, keeper of {glosses[2]}",
            f"A spirit shaped by {glosses[0]}, voice of {glosses[1]}, hand of {glosses[2]}",
            f"Child of {glosses[0]}, gifted by {glosses[1]}, soul of {glosses[2]}",
            f"{glosses[2].title()} made flesh, carved from {glosses[0]} and {glosses[1]}",
            f"Heart of {glosses[0]}, mind of {glosses[1]}, destiny of {glosses[2]}" # Added another option
         ]
    else: # Handle 1 part or other cases
         templates = [f"Embodiment of {glosses[0]}", f"Bearer of {glosses[0]}"]

    return random.choice(templates)

# === Generate NPC Function ===
def generate_npc():
    race = random.choice(races)
    npc_lines = [
        "💼 **Basic Info**",
        f"🧬 **Race:** {race['name']} ({race['rarity']})",
        f"🌍 **Region:** {race['region']}",
        f"📖 **Lore:** {race['description']}",
        "✶" * 25,
        "🎭 **Personality & Story**"
    ]

    for category, options in npc_attributes.items():
        clean_category = category.strip()
        icon = icons.get(clean_category, "•")
        choice = random.choice(options)
        npc_lines.append(f"{icon} **{clean_category}:** {choice}")

    return "\n\n".join(npc_lines)

# === Generate Tabaxi Name Function ===
def generate_tabaxi_name(selected_clan):
    # Ensure data lists are not empty
    if not tabaxi_prefixes or not tabaxi_suffixes:
         st.error("Tabaxi name parts data is missing or empty.")
         return "Error: Missing name data."
    # Check middles only if needed, but safer to check upfront
    if not tabaxi_middles:
         st.warning("Tabaxi middle name parts data is missing or empty.")
         # Decide how to handle: error out, or guarantee no middle part?
         # Let's guarantee no middle part if list is empty.
         # return "Error: Missing middle name data."


    use_middle = random.random() < 0.4 and bool(tabaxi_middles) # Only use middle if list exists
    parts = []

    # --- Choose Prefix ---
    prefix = random.choice(tabaxi_prefixes)
    parts.append(prefix)
    last_part_ends_vowel = prefix["ends_vowel"] # Get vowel status for next step

    # --- Choose Middle (Optional) ---
    if use_middle:
        # Pick middle part using smoothing logic
        middle = _pick_smooth_part(tabaxi_middles, last_part_ends_vowel)
        if middle: # Check if _pick_smooth_part returned a part
             parts.append(middle)
             last_part_ends_vowel = middle["ends_vowel"] # Update vowel status

    # --- Choose Suffix ---
    # Pick suffix part using smoothing logic based on the LAST chosen part (prefix or middle)
    suffix = _pick_smooth_part(tabaxi_suffixes, last_part_ends_vowel)
    if suffix:
        parts.append(suffix)

    # --- Assemble Name & Meanings ---
    full_name = "".join(p["text"] for p in parts)
    meaning_lines = [f"- **{p['text']}** = {p['meaning']}" for p in parts]

    # --- Poetic Meaning ---
    # Call the helper function
    poetic = _generate_poetic_meaning(parts, tabaxi_poetic_gloss)

    # --- Clan Info ---
    clan_info = next((c for c in tabaxi_clans if c["name"] == selected_clan), None)
    if clan_info:
        clan_desc = (
            f"\n\n🏡 **Clan:** {clan_info['name']}\n\n"
            f"• **Region:** {clan_info['region']}\n\n"
            f"• **Traits:** {clan_info['traits']}\n\n"
            f"• **Twist:** {clan_info['twist']}"
        )
    else:
        clan_desc = ""

    # --- Return Formatted Output ---
    return (
        f"🐾 **Name:** {full_name}\n\n"
        + "\n\n".join(meaning_lines)
        + f"\n\n➔ **Poetic Meaning:** {poetic}{clan_desc}"
    )

# === Generate Elven Name Function ===
def generate_elven_name():
    # Ensure data lists are not empty
    if not elven_prefixes or not elven_suffixes:
         st.error("Elven name parts data is missing or empty.")
         return "Error: Missing name data."
    if not elven_middles:
         st.warning("Elven middle name parts data is missing or empty.")

    use_middle = random.random() < 0.4 and bool(elven_middles) # Only use middle if list exists
    parts = []

    # --- Choose Prefix ---
    prefix = random.choice(elven_prefixes)
    parts.append(prefix)
    last_part_ends_vowel = prefix["ends_vowel"]

    # --- Choose Middle (Optional) ---
    if use_middle:
        middle = _pick_smooth_part(elven_middles, last_part_ends_vowel)
        if middle:
            parts.append(middle)
            last_part_ends_vowel = middle["ends_vowel"]

    # --- Choose Suffix ---
    suffix = _pick_smooth_part(elven_suffixes, last_part_ends_vowel)
    if suffix:
        parts.append(suffix)

    # --- Assemble Name & Meanings ---
    full_name = "".join(p["text"] for p in parts)
    meaning_lines = [f"- **{p['text']}** = {p['meaning']}" for p in parts]

    # --- Poetic Meaning ---
    poetic = _generate_poetic_meaning(parts, elven_poetic_gloss)

    # --- Return Formatted Output ---
    return (
        f"🌿 **Name:** {full_name}\n\n" +
        "\n".join(meaning_lines) + # Keep single newline for bullet list
        f"\n\n➔ **Poetic Meaning:** {poetic}"
    )


# === UI ===
st.title("🌸 Tivmir World Tools")

# Initialize session state variables if they don't exist
if 'npc_output' not in st.session_state:
    st.session_state.npc_output = ""
if 'name_output' not in st.session_state:
    st.session_state.name_output = ""
# (Initialize others as needed, e.g., for selected clan state if desired)

tabs = st.tabs(["🌿 NPC Generator", "🔤 Name Generator"])

with tabs[0]:
    st.header("🌿 NPC Generator")
    if st.button("Generate NPC", key="npc_button"):
        # Store result in session state
        st.session_state.npc_output = generate_npc()

    # Always display from session state
    if st.session_state.npc_output:
        st.markdown("---") # Optional separator
        st.markdown(st.session_state.npc_output)


with tabs[1]:
    st.header("🔤 Name Generator")
    race = st.selectbox("Choose a race:", ["Elven", "Tabaxi"], key="name_race")

    if race == "Tabaxi":
        clan_names = [clan["name"] for clan in tabaxi_clans]
        selected_clan = st.selectbox("Choose a Tabaxi clan:", clan_names, key="tabaxi_clan")
        if st.button("Generate Tabaxi Name", key="tabaxi_name_button"):
            # Store result
            st.session_state.name_output = generate_tabaxi_name(selected_clan)
    else: # Elven
        if st.button("Generate Elven Name", key="elven_name_button"):
            # Store result
            st.session_state.name_output = generate_elven_name()

    # Always display name output from session state
    if st.session_state.name_output:
        st.markdown("---") # Optional separator
        st.markdown(st.session_state.name_output)