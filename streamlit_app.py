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
common_first_names = load_json("common_first_names.json")
common_surnames = load_json("common_surnames.json")
orcish_prefixes = load_json("orcish_prefixes.json")
orcish_middles = load_json("orcish_middles.json")
orcish_suffixes = load_json("orcish_suffixes.json")
orcish_poetic_gloss = load_json("orcish_poetic_gloss.json")
orcish_surnames = load_json("orcish_surnames.json")
infernal_prefixes = load_json("infernal_prefixes.json")
infernal_middles = load_json("infernal_middles.json")
infernal_suffixes = load_json("infernal_suffixes.json")
infernal_poetic_gloss = load_json("infernal_poetic_gloss.json")

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
def _assemble_name_parts(prefixes, middles, suffixes, gender_filter="Any"): # Add gender_filter
    """Internal logic to select name parts using smoothing. Returns list of chosen parts."""
    if not prefixes or not suffixes: return []
    if not middles: middles_list = []
    else: middles_list = middles

    use_middle = random.random() < 0.3 and bool(middles_list)
    chosen_parts = []

    # --- Prefix Selection (Could add gender filtering here too if desired later) ---
    prefix = random.choice(prefixes)
    chosen_parts.append(prefix)
    last_part_ends_vowel = prefix["ends_vowel"]
    last_part_text = prefix["text"]

    # --- Middle Selection (No gender filtering applied here currently) ---
    if use_middle:
        middle = _pick_smooth_part(middles_list, last_part_ends_vowel)
        if middle:
            # Simple repeat check
            if len(last_part_text) > 1 and len(middle["text"]) > 1 and \
               last_part_text.endswith(middle["text"][0]):
                middle = _pick_smooth_part(middles_list, last_part_ends_vowel)

            if middle:
                chosen_parts.append(middle)
                last_part_ends_vowel = middle["ends_vowel"]
                last_part_text = middle["text"]

    # --- Suffix Selection with Gender Filtering ---
    suffix_options = suffixes # Start with all suffixes
    if gender_filter != "Any":
        # Filter based on gender, always including Unisex
        suffix_options = [
            s for s in suffixes
            if s.get("gender") == gender_filter or s.get("gender") == "Unisex"
        ]
        if not suffix_options: # Fallback if no matching gendered suffixes found
            st.warning(f"No specific {gender_filter} or Unisex suffixes found, using any.")
            suffix_options = suffixes # Use all suffixes as fallback

    if not suffix_options: # Check if list became empty (shouldn't if fallback works)
        st.error("Suffix options list is empty after filtering.")
        return chosen_parts # Return parts assembled so far

    suffix = _pick_smooth_part(suffix_options, last_part_ends_vowel)
    if suffix:
        # Simple repeat check
        if len(last_part_text) > 1 and len(suffix["text"]) > 1 and \
           last_part_text.endswith(suffix["text"][0]):
            suffix = _pick_smooth_part(suffix_options, last_part_ends_vowel) # Try again on filtered list

        if suffix:
            chosen_parts.append(suffix)

    return chosen_parts # Return the list of chosen part dictionaries

# === NEW Generalized Helper for Structured Names ===
def _generate_structured_name_data(race_key, gender="Any"):
    """
    Internal helper to generate name components for structured names (Elf, Orc, Infernal, Tabaxi).
    Returns a dictionary containing 'name', 'parts', 'poetic', 'error' (if any).
    """
    prefixes, middles, suffixes, gloss, surnames = None, None, None, None, None
    error_msg = None
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    # --- Map race_key to data variables ---
    # (This mapping is needed because we haven't done the data restructure yet)
    if race_key == "elf":
        if all([elven_prefixes, elven_middles, elven_suffixes, elven_poetic_gloss]):
            prefixes, middles, suffixes, gloss = elven_prefixes, elven_middles, elven_suffixes, elven_poetic_gloss
        else: error_msg = "Missing required Elven data."
    elif race_key == "orc":
         if all([orcish_prefixes, orcish_middles, orcish_suffixes, orcish_poetic_gloss, orcish_surnames]):
            prefixes, middles, suffixes, gloss, surnames = orcish_prefixes, orcish_middles, orcish_suffixes, orcish_poetic_gloss, orcish_surnames
         else: error_msg = "Missing required Orcish data."
    elif race_key == "infernal":
         if all([infernal_prefixes, infernal_middles, infernal_suffixes, infernal_poetic_gloss]):
             prefixes, middles, suffixes, gloss = infernal_prefixes, infernal_middles, infernal_suffixes, infernal_poetic_gloss
         else: error_msg = "Missing required Infernal data."
    elif race_key == "tabaxi":
        if all([tabaxi_prefixes, tabaxi_middles, tabaxi_suffixes, tabaxi_poetic_gloss]):
            prefixes, middles, suffixes, gloss = tabaxi_prefixes, tabaxi_middles, tabaxi_suffixes, tabaxi_poetic_gloss
        else: error_msg = "Missing required Tabaxi data."
    else:
        error_msg = f"Unknown race key for structured name: {race_key}"

    if error_msg:
        st.error(error_msg)
        result["error"] = error_msg
        return result # Return early with error

    # --- Assemble Parts ---
    parts = _assemble_name_parts(prefixes, middles, suffixes, gender_filter=gender)
    if not parts:
        error_msg = f"Failed to assemble {race_key.capitalize()} name parts."
        st.warning(error_msg)
        result["error"] = error_msg
        return result # Return early

    result["parts"] = parts
    first_name = "".join(p["text"] for p in parts) # First name generated from parts

    # --- Handle Surnames (Orcish) ---
    surname = ""
    surname_part = None # Store surname details if applicable
    if race_key == "orc" and surnames:
        surname_entry = random.choice(surnames)
        surname = surname_entry["text"]
        # Create a pseudo-part for the surname to store its meaning
        surname_part = {"text": surname, "meaning": surname_entry.get('meaning', 'N/A')}
        full_name = f"{first_name} {surname}"
    else:
        full_name = first_name # Most races just use the generated name

    result["name"] = full_name

    # --- Poetic Meaning (based on generated parts, excluding surname for Orcs) ---
    result["poetic"] = _generate_poetic_meaning(parts, gloss) # Pass the correct gloss

    # Add surname part to parts list *after* poetic meaning generation if applicable
    if surname_part:
        result["parts"].append(surname_part)

    return result # Return dictionary with name, parts, poetic meaning, and potential error

# Helper specifically for Common names (returns only string)
# Add gender_filter parameter
def _get_common_name_string(gender_filter="Any"):
    """Generates a Common first name + surname string, optionally filtered by gender."""
    if not common_first_names or not common_surnames:
        return "[Common Name Data Missing]"

    # --- Filter first names based on gender ---
    possible_first_names = common_first_names
    if gender_filter != "Any":
        # Select names matching the filter OR Unisex names
        filtered_names = [
            name_entry for name_entry in common_first_names
            if name_entry.get("gender") == gender_filter or name_entry.get("gender") == "Unisex"
        ]
        if filtered_names: # Only use filter if results were found
            possible_first_names = filtered_names
        else:
            st.warning(f"No '{gender_filter}' or 'Unisex' first names found, using any.")
            # Fallback to using all names if filter yields no results
    # --- End Filtering ---

    if not possible_first_names: # Should not happen if fallback works, but safety check
        return "[Error: No suitable first names]"

    first_name_entry = random.choice(possible_first_names)
    surname_entry = random.choice(common_surnames) # Surnames are not filtered by gender here

    return f"{first_name_entry['text']} {surname_entry['text']}"

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
    npc_name = f"Unnamed {race_name}" # Default placeholder
    clan_name = None # Initialize clan_name

    # --- Generate Name based on Race ---
    # Use default "Any" gender for NPC generation for simplicity for now
    # (Could add gender selection to NPC gen later if desired)
    npc_gender = "Any"

    if race_name == "Elf":
        # Call the simplified wrapper which uses the helper
        name_data = _generate_structured_name_data("elf", npc_gender)
        if not name_data["error"] and name_data["name"]:
            npc_name = name_data["name"]
        else:
            npc_name = f"[{race_name} Name Error] {race_name}"

    elif race_name == "Tabaxi":
        # Get name part using the helper
        name_data = _generate_structured_name_data("tabaxi", npc_gender)
        if not name_data["error"] and name_data["name"]:
            npc_first_name = name_data["name"]
        else:
            npc_first_name = f"[{race_name} Name Error]"

        # Assign Clan Name (Logic remains similar)
        if tabaxi_clans:
             clan_entry = random.choice(tabaxi_clans)
             clan_name = clan_entry['name'] # Store for details output
             npc_name = f"{npc_first_name} of the {clan_name} Clan" # Construct display name
        else:
             npc_name = f"{npc_first_name} [Clan Data Missing]"
             clan_name = "[Clan Data Missing]" # Placeholder

    elif race_name == "Human":
        # Common name logic remains the same
        if common_first_names and common_surnames:
             npc_name = _get_common_name_string(gender_filter=npc_gender)
        else: npc_name = f"[Common Name Data Missing] {race_name}"

    elif race_name == "Half-Elf":
        # Logic remains the same, but internal calls are now simpler
        chosen_style = random.choice(["Elven", "Common"])
        if chosen_style == "Elven":
            name_data = _generate_structured_name_data("elf", npc_gender) # Use helper via race key
            if not name_data["error"] and name_data["name"]: npc_name = name_data["name"]
            else: npc_name = f"[Elven Name Error] Half-Elf"
        else: # Common style
            if common_first_names and common_surnames: npc_name = _get_common_name_string(gender_filter=npc_gender)
            else: npc_name = f"[Common Name Data Missing] Half-Elf"

    elif race_name == "Orc":
        # Use helper via race key
        name_data = _generate_structured_name_data("orc", npc_gender)
        if not name_data["error"] and name_data["name"]:
            npc_name = name_data["name"] # Helper now includes surname
        else:
             npc_name = f"[{race_name} Name Error] {race_name}"

    elif race_name == "Half-Orc":
        # Logic remains the same, calls are simpler
        chosen_style = random.choice(["Orc", "Common"])
        if chosen_style == "Orc":
             name_data = _generate_structured_name_data("orc", npc_gender) # Use helper via race key
             if not name_data["error"] and name_data["name"]: npc_name = name_data["name"]
             else: npc_name = f"[Orcish Name Error] Half-Orc"
        else: # Common style
             if common_first_names and common_surnames: npc_name = _get_common_name_string(gender_filter=npc_gender)
             else: npc_name = f"[Common Name Data Missing] Half-Orc"

    elif race_name == "Tiefling":
         # Use helper via race key
         name_data = _generate_structured_name_data("infernal", npc_gender)
         if not name_data["error"] and name_data["name"]:
             npc_name = name_data["name"]
         else:
             npc_name = f"[{race_name} Name Error] {race_name}"

    # --- Add more elif blocks here for future races using _generate_structured_name_data ---

    # --- Assemble NPC Output ---
    npc_lines = [f"👤 **Name:** {npc_name}"]

    # Add Clan details if applicable (logic remains the same)
    if race_name == "Tabaxi" and clan_name and clan_name != "[Clan Data Missing]":
         npc_lines.append(f"🏡 **Clan:** {clan_name}")

    # Add Separator and Basic Info Header (logic remains the same)
    npc_lines.extend([
        "---",
        "💼 **Basic Info**",
        f"🧬 **Race:** {race_name} ({race_data.get('rarity', 'N/A')})",
        f"🌍 **Region:** {race_data.get('region', 'N/A')}",
        f"📖 **Lore:** {race_data.get('description', 'N/A')}",
        "✶" * 25,
        "🎭 **Personality & Story**"
    ])

    # Add attributes (logic remains the same)
    for category, options in npc_attributes.items():
        if not options: continue
        clean_category = category.strip()
        icon = icons.get(clean_category, "•")
        choice = random.choice(options)
        npc_lines.append(f"{icon} **{clean_category}:** {choice}")

    return "\n\n".join(npc_lines) # Use double newline for better spacing

# === (Revised) Generate Tabaxi Name Function ===
def generate_tabaxi_name(selected_clan): # Tabaxi doesn't use gender filter currently
    # Check clan data exists (specific to Tabaxi)
    if not tabaxi_clans:
         st.error("Missing required Tabaxi clan data.")
         return "Error: Missing clan data."

    # Use helper for name generation part
    data = _generate_structured_name_data("tabaxi", gender="Any") # Pass "Any" gender
    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Tabaxi name is just the generated part
    full_name = data["name"]
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    poetic = data["poetic"]

    # Clan Info (remains the same logic as before)
    clan_info = next((c for c in tabaxi_clans if c["name"] == selected_clan), None)
    clan_desc = ""
    if clan_info:
        clan_desc = (
            f"\n\n🏡 **Clan:** {clan_info['name']}\n\n"
            f"• **Region:** {clan_info['region']}\n\n"
            f"• **Traits:** {clan_info['traits']}\n\n"
            f"• **Twist:** {clan_info['twist']}"
        )
    else:
        st.warning(f"Could not find details for clan: {selected_clan}")
        clan_desc = f"\n\n🏡 **Clan:** {selected_clan} (Details not found)"


    # Return Formatted Output
    return (
        f"🐾 **Name:** {full_name}\n\n" # Note: Tabaxi names might not include "of the X clan" directly here
        + "\n".join(meaning_lines)
        + f"\n\n➔ **Poetic Meaning:** {poetic}{clan_desc}"
    )

# === (Revised) Generate Elven Name Function ===
def generate_elven_name(gender="Any"): # Added gender default
    data = _generate_structured_name_data("elf", gender) # Use helper
    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently." # Safety check

    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    return (
        f"🌿 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **Poetic Meaning:** {data['poetic']}"
    )

# === Generate Common Name Function (for Name Generator Tab) ===
def generate_common_name(gender="Any"): # Add gender parameter
    """Generates a Common name with meanings for the Name Generator tab."""
    if not common_first_names or not common_surnames:
        st.error("Missing required Common name data.")
        return "Error: Missing data."

    # --- Filter first names based on gender ---
    possible_first_names = common_first_names
    if gender != "Any":
        filtered_names = [
            name_entry for name_entry in common_first_names
            if name_entry.get("gender") == gender or name_entry.get("gender") == "Unisex"
        ]
        if filtered_names:
            possible_first_names = filtered_names
        else:
            st.warning(f"No '{gender}' or 'Unisex' first names found, using any.")
            # Fallback to using all names

    if not possible_first_names:
        return "[Error: No suitable first names]"
    # --- End Filtering ---

    first_name_entry = random.choice(possible_first_names)
    # Choose surname (no gender filter applied)
    surname_entry = random.choice(common_surnames)

    full_name = f"{first_name_entry['text']} {surname_entry['text']}"

    # Prepare meaning lines (remains the same)
    meaning_lines = []
    meaning_lines.append(f"- **{first_name_entry['text']}** = {first_name_entry.get('meaning', 'N/A')}")
    if 'meaning' in surname_entry:
         meaning_lines.append(f"- **{surname_entry['text']}** = {surname_entry['meaning']}")
    else:
         meaning_lines.append(f"- **{surname_entry['text']}**")

    return (
        f"👤 **Name:** {full_name}\n\n" +
        "\n".join(meaning_lines) +
        #f"\n\n📜 **Notes:** {flavor_text}"
        ""
    )

# === (Revised) Generate Orcish Name Function ===
def generate_orc_name(gender="Any"):
    data = _generate_structured_name_data("orc", gender) # Use helper
    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include surname meaning because helper adds it to 'parts'
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    # Note: Poetic meaning from helper applies only to the first name parts
    return (
        f"⚙️ **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **Poetic Meaning (First Name):** {data['poetic']}"
    )

# === (Revised) Generate Infernal Name Function ===
def generate_infernal_name(gender="Any"):
    data = _generate_structured_name_data("infernal", gender) # Use helper
    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    return (
        f"🔥 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **Poetic Meaning:** {data['poetic']}"
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
    col1, col2 = st.columns([1, 1]) # Put buttons side-by-side
    with col1:
        if st.button("Generate NPC", key="npc_button"):
            st.session_state.npc_output = generate_npc()
    with col2:
        # Add this button
        if st.button("Clear Output", key="npc_clear"):
            st.session_state.npc_output = "" # Clear the state

    # Always display from session state
    if st.session_state.npc_output:
        st.markdown("---")
    with st.container(border=True):
        st.markdown(st.session_state.npc_output)

# --- Start Corrected Name Generator Tab UI ---
with tabs[1]:
    st.header("🔤 Name Generator")
    # Race selection stays at the top
    race = st.selectbox("Choose a race:", ["Elf", "Tabaxi", "Human", "Orc", "Tiefling"], key="name_race") # Added Tiefling based on previous steps

    # --- Gender selection is now INSIDE the relevant blocks ---

    if race == "Tabaxi":
        # NO gender selection shown here
        clan_names = [clan["name"] for clan in tabaxi_clans]
        selected_clan = st.selectbox("Choose a Tabaxi clan:", clan_names, key="tabaxi_clan")
        if st.button("Generate Tabaxi Name", key="tabaxi_name_button"):
            # Call WITHOUT gender argument (it defaults to "Any" inside the function if needed)
            st.session_state.name_output = generate_tabaxi_name(selected_clan)

    elif race == "Human":
        # Gender selection shown HERE for Humans
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="human_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Common Name", key="common_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_common_name(gender=gender)

    elif race == "Orc":
        # Gender selection shown HERE for Orcs
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="orc_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Orcish Name", key="orc_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_orc_name(gender=gender)

    elif race == "Tiefling":
        # NO gender selection shown here
        if st.button("Generate Infernal Name", key="tiefling_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_infernal_name()

    # Use elif for Elf now, not else, to be specific
    elif race == "Elf":
        # NO gender selection shown here
        if st.button("Generate Elven Name", key="elven_name_button"):
            # Call WITHOUT gender argument (it defaults to "Any" inside the function if needed)
            st.session_state.name_output = generate_elven_name()

    else:
        # Handle any unexpected race selection, maybe display a message
        st.write(f"Select a race to generate a name.")


    # Always display name output from session state (this part remains the same)
    if st.session_state.name_output:
        st.markdown("---") # Optional separator
        st.markdown(st.session_state.name_output)