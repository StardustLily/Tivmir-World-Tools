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

# === (Revised) Internal Helper Functions for Name Assembly ===
def _assemble_name_parts(prefixes, middles, suffixes):
    """Internal logic to select name parts using smoothing. Returns list of chosen parts."""
    if not prefixes or not suffixes: return [] # Return empty list on error
    if not middles: middles_list = [] # Handle empty list
    else: middles_list = middles

    use_middle = random.random() < 0.4 and bool(middles_list)
    chosen_parts = []

    prefix = random.choice(prefixes)
    chosen_parts.append(prefix)
    last_part_ends_vowel = prefix["ends_vowel"]

    if use_middle:
        middle = _pick_smooth_part(middles_list, last_part_ends_vowel)
        if middle:
            chosen_parts.append(middle)
            last_part_ends_vowel = middle["ends_vowel"]

    suffix = _pick_smooth_part(suffixes, last_part_ends_vowel)
    if suffix:
        chosen_parts.append(suffix)

    return chosen_parts # Return the list of chosen part dictionaries

# We no longer need separate _get_elven_name_string, etc. We use _assemble_name_parts

# === (Revised) Generate NPC Function ===
def generate_npc():
    if not races:
        st.error("Race data is missing or empty.")
        return "Error: Missing race data."
    if not npc_attributes:
        st.error("NPC attributes data is missing or empty.")
        return "Error: Missing attribute data."

    # --- Select Race ---
    race_data = random.choice(races)
    race_name = race_data['name']

    # --- Generate Name based on Race ---
    npc_name = f"Unnamed {race_name}" # Default placeholder
    generated_parts = [] # Store parts if generated

    if race_name == "Elven":
        if all([elven_prefixes, elven_middles, elven_suffixes]): # Check data exists
             generated_parts = _assemble_name_parts(elven_prefixes, elven_middles, elven_suffixes)
             if generated_parts: npc_name = "".join(p["text"] for p in generated_parts)
        else: npc_name = f"[Elven Name Data Missing] {race_name}"

    elif race_name == "Tabaxi":
        if all([tabaxi_prefixes, tabaxi_middles, tabaxi_suffixes]): # Check data exists
             generated_parts = _assemble_name_parts(tabaxi_prefixes, tabaxi_middles, tabaxi_suffixes)
             if generated_parts: npc_name = "".join(p["text"] for p in generated_parts)
        else: npc_name = f"[Tabaxi Name Data Missing] {race_name}"

    # --- Add more elif blocks here for future races ---
    # elif race_name == "Dwarf":
    #     if all ([dwarf_prefixes, ...]): # Load dwarf data first
    #          generated_parts = _assemble_name_parts(dwarf_prefixes, ...)
    #          if generated_parts: npc_name = "".join(p["text"] for p in generated_parts)
    #     else: npc_name = f"[Dwarf Name Data Missing] {race_name}"


    # --- Assemble NPC Output ---
    npc_lines = [
        f"👤 **Name:** {npc_name}", # Add the name here!
        "---", # Separator
        "💼 **Basic Info**",
        f"🧬 **Race:** {race_name} ({race_data.get('rarity', 'N/A')})", # Use .get for safety
        f"🌍 **Region:** {race_data.get('region', 'N/A')}",
        f"📖 **Lore:** {race_data.get('description', 'N/A')}",
        "✶" * 25,
        "🎭 **Personality & Story**"
    ]

    # Add attributes
    for category, options in npc_attributes.items():
        if not options: continue # Skip empty attribute lists
        clean_category = category.strip()
        icon = icons.get(clean_category, "•")
        choice = random.choice(options)
        npc_lines.append(f"{icon} **{clean_category}:** {choice}")

    return "\n\n".join(npc_lines)

# === (Revised) Generate Tabaxi Name Function ===
def generate_tabaxi_name(selected_clan):
    # Check data (can be done inside _assemble_name_parts too)
    if not all([tabaxi_prefixes, tabaxi_middles, tabaxi_suffixes, tabaxi_poetic_gloss, tabaxi_clans]):
         st.error("Missing required Tabaxi data.")
         return "Error: Missing data."

    # Assemble the parts using the helper
    parts = _assemble_name_parts(tabaxi_prefixes, tabaxi_middles, tabaxi_suffixes)
    if not parts: return "Error: Failed to assemble name parts." # Check if assembly worked

    full_name = "".join(p["text"] for p in parts)
    meaning_lines = [f"- **{p['text']}** = {p['meaning']}" for p in parts]

    # Poetic Meaning (using existing helper)
    poetic = _generate_poetic_meaning(parts, tabaxi_poetic_gloss)

    # Clan Info (remains the same)
    clan_info = next((c for c in tabaxi_clans if c["name"] == selected_clan), None)
    clan_desc = ""
    if clan_info:
        clan_desc = (
            f"\n\n🏡 **Clan:** {clan_info['name']}\n\n"
            f"• **Region:** {clan_info['region']}\n\n"
            f"• **Traits:** {clan_info['traits']}\n\n"
            f"• **Twist:** {clan_info['twist']}"
        )

    # Return Formatted Output
    return (
        f"🐾 **Name:** {full_name}\n\n"
        + "\n\n".join(meaning_lines)
        + f"\n\n➔ **Poetic Meaning:** {poetic}{clan_desc}"
    )

# === (Revised) Generate Elven Name Function ===
def generate_elven_name():
    if not all([elven_prefixes, elven_middles, elven_suffixes, elven_poetic_gloss]):
         st.error("Missing required Elven data.")
         return "Error: Missing data."

    # Assemble the parts using the helper
    parts = _assemble_name_parts(elven_prefixes, elven_middles, elven_suffixes)
    if not parts: return "Error: Failed to assemble name parts."

    full_name = "".join(p["text"] for p in parts)
    meaning_lines = [f"- **{p['text']}** = {p['meaning']}" for p in parts]

    # Poetic Meaning (using existing helper)
    poetic = _generate_poetic_meaning(parts, elven_poetic_gloss)

    # Return Formatted Output
    return (
        f"🌿 **Name:** {full_name}\n\n" +
        "\n".join(meaning_lines) + # Single newline for bullet points
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