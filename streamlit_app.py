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

# === (Revised) Load Data ===
races = load_json("races.json")
npc_attributes = load_json("npc_attributes.json")
# Consolidate name data into a dictionary
auran_gloss = load_json("auran_poetic_gloss.json")
aquan_gloss = load_json("aquan_poetic_gloss.json")
ignan_gloss = load_json("ignan_poetic_gloss.json")
terran_gloss = load_json("terran_poetic_gloss.json")
name_data = {
    "tabaxi": {
        "prefixes": load_json("tabaxi_prefixes.json"),
        "middles": load_json("tabaxi_middles.json"),
        "suffixes": load_json("tabaxi_suffixes.json"),
        "gloss": load_json("tabaxi_poetic_gloss.json"),
        "clans": load_json("tabaxi_clans.json") # Specific to Tabaxi
    },
    "elf": {
        "prefixes": load_json("elven_prefixes.json"),
        "middles": load_json("elven_middles.json"),
        "suffixes": load_json("elven_suffixes.json"),
        "gloss": load_json("elven_poetic_gloss.json")
    },
    "common": { # For Human/Common names
        "first_names": load_json("common_first_names.json"),
        "surnames": load_json("common_surnames.json")
    },
    "orc": {
        "prefixes": load_json("orcish_prefixes.json"),
        "middles": load_json("orcish_middles.json"),
        "suffixes": load_json("orcish_suffixes.json"),
        "gloss": load_json("orcish_poetic_gloss.json"),
        "surnames": load_json("orcish_surnames.json") # Specific to Orc
    },
    "infernal": { # Using 'infernal' as the key for Tiefling
        "prefixes": load_json("infernal_prefixes.json"),
        "middles": load_json("infernal_middles.json"),
        "suffixes": load_json("infernal_suffixes.json"),
        "gloss": load_json("infernal_poetic_gloss.json"),
        "surnames": load_json("infernal_surnames.json")
    },
    "drow": {
        "prefixes": load_json("drow_prefixes.json"),
        "middles": load_json("drow_middles.json"),
        "suffixes": load_json("drow_suffixes.json"),
        "gloss": load_json("drow_poetic_gloss.json"),
        "surnames": load_json("drow_surnames.json")
    },
    "draconic": {
            "clans": load_json("draconic_clans.json"),
            "prefixes": load_json("draconic_prefixes.json"),
            "middles": load_json("draconic_middles.json"),
            "suffixes": load_json("draconic_suffixes.json"),
            "gloss": load_json("draconic_poetic_gloss.json")},
    "aarakocra": {
            "lineages": load_json("aarakocra_lineages.json"),
            "prefixes": load_json("aarakocra_prefixes.json"),
            "middles": load_json("aarakocra_middles.json"),
            "suffixes": load_json("aarakocra_suffixes.json"),
            "gloss": auran_gloss},
    "owlin": {
            "personal": load_json("owlin_personal.json"),
            "descriptors": load_json("owlin_descriptors.json"),
            "gloss": auran_gloss},
    "tortle": {
        "given": load_json("tortle_given.json"),
        "descriptors": load_json("tortle_descriptors.json"),
        "gloss": aquan_gloss},
    "triton": {
        "given": load_json("triton_given.json"),
        "markers": load_json("triton_markers.json"),
        "gloss": aquan_gloss},
    "ignan": {
        "prefixes": load_json("ignan_prefixes.json"),
        "middles": load_json("ignan_middles.json"),
        "suffixes": load_json("ignan_suffixes.json"),
        "gloss": ignan_gloss},
    "terran": {
        "prefixes": load_json("terran_prefixes.json"),
        "middles": load_json("terran_middles.json"),
        "suffixes": load_json("terran_suffixes.json"),
        "gloss": terran_gloss},
    "air_genasi": {
        "prefixes": load_json("air_genasi_prefixes.json"),
        "middles": load_json("air_genasi_middles.json"),
        "suffixes": load_json("air_genasi_suffixes.json"),
        "gloss": auran_gloss},
    "water_genasi": {
        "prefixes": load_json("water_genasi_prefixes.json"),
        "middles": load_json("water_genasi_middles.json"),
        "suffixes": load_json("water_genasi_suffixes.json"),
        "gloss": aquan_gloss}
}

# Emoji Icons (remains the same)
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

# === (Revised) Helper Functions for Name Generation ===

VOWELS = "aeiouyáéíóúàèìòùâêîôûäëïöü" # Define vowels (adjust if needed)

def _is_vowel(char):
  """Checks if a single character is a vowel (case-insensitive)."""
  return char.lower() in VOWELS

def _is_smooth_transition(prev_part_ends_vowel, current_part_starts_vowel):
  """Checks if joining two parts is phonetically smooth (avoids vowel+vowel or maybe consonant+consonant)."""
  # Simple: Avoid vowel + vowel. Could add consonant cluster checks later.
  return not (prev_part_ends_vowel and current_part_starts_vowel)

def _pick_smooth_part(part_list, prev_part_ends_vowel):
  """Picks a random part from the list, preferring smooth transitions."""
  if not part_list:
      st.warning("Attempted to pick from an empty name part list.")
      return None

  smooth_options = [
      part for part in part_list
      if _is_smooth_transition(prev_part_ends_vowel, part["starts_vowel"])
  ]

  if smooth_options:
      return random.choice(smooth_options)
  else:
      # Fallback: pick any part if no smooth options exist
      return random.choice(part_list)

def _generate_poetic_meaning(parts, poetic_gloss_dict):
    """Generates a poetic meaning string from chosen name parts and a gloss dictionary."""
    if not parts or not poetic_gloss_dict:
        return "No poetic meaning available." # Return informative string

    # Extract primary meaning keyword for lookup
    keywords = [p.get("meaning", "").split("/")[0].strip() for p in parts if p.get("meaning")]
    if not keywords:
        return "Could not determine meaning keywords." # Handle case where parts have no meaning

    # Get random poetic gloss for each keyword
    glosses = [random.choice(poetic_gloss_dict.get(k, [k.capitalize()])) for k in keywords] # Fallback to capitalized keyword

    num_glosses = len(glosses)
    templates = []

    # Choose a template based on the number of parts/glosses
    if num_glosses == 1:
        templates = [
            f"Embodiment of {glosses[0]}",
            f"Bearer of {glosses[0]}",
            f"A soul defined by {glosses[0]}",
        ]
    elif num_glosses == 2:
        templates = [
            f"{glosses[0].title()} of {glosses[1]}",
            f"Bearer of {glosses[1]}, born of {glosses[0]}",
            f"A soul touched by {glosses[0]} and {glosses[1]}",
            f"Walker between {glosses[0]} and {glosses[1]}",
            f"Voice of the {glosses[1]}, spirit of {glosses[0]}"
        ]
    elif num_glosses == 3:
         templates = [
            f"One who walks with {glosses[0]}, guided by {glosses[1]}, keeper of {glosses[2]}",
            f"A spirit shaped by {glosses[0]}, voice of {glosses[1]}, hand of {glosses[2]}",
            f"Child of {glosses[0]}, gifted by {glosses[1]}, soul of {glosses[2]}",
            f"{glosses[2].title()} made flesh, carved from {glosses[0]} and {glosses[1]}",
            f"Heart of {glosses[0]}, mind of {glosses[1]}, destiny of {glosses[2]}"
         ]
    else: # Fallback for 4 or more parts - simple conjunction
         # Join all but the last with commas, then add "and" before the last one.
         if num_glosses > 0:
             all_but_last = ", ".join(glosses[:-1])
             last = glosses[-1]
             templates = [f"One connected to {all_but_last}, and {last}"]
         else: # Should not happen if checks above work, but safety
             return "Meaning generation failed."

    return random.choice(templates) if templates else "Could not generate poetic meaning."

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

# === (Revised) Generalized Helper for Structured Names ===
def _generate_structured_name_data(race_data, gender="Any"): # Accepts the race's data dict
    """
    Internal helper to generate name components for structured names (Elf, Orc, Infernal, Tabaxi).
    Accepts a dictionary containing the specific race's data ('prefixes', 'middles', etc.).
    Returns a dictionary containing 'name', 'parts', 'poetic', 'error' (if any).
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    # --- Access data directly from the passed dictionary ---
    prefixes = race_data.get("prefixes")
    middles = race_data.get("middles") # Might be missing for some future structures
    suffixes = race_data.get("suffixes")
    gloss = race_data.get("gloss")
    surnames = race_data.get("surnames") # Only present for Orcs currently

    # --- Basic Data Validation ---
    if not prefixes or not suffixes or not gloss:
        error_msg = "Missing core name data (prefixes, suffixes, or gloss) for this race."
        st.error(error_msg)
        result["error"] = error_msg
        return result

    # --- Assemble Parts ---
    # Handle potentially missing middles list gracefully
    parts = _assemble_name_parts(prefixes, middles or [], suffixes, gender_filter=gender)
    if not parts:
        error_msg = f"Failed to assemble name parts."
        st.warning(error_msg)
        result["error"] = error_msg
        return result

    result["parts"] = parts
    first_name = "".join(p["text"] for p in parts)

    # --- Handle Surnames ---
    surname = ""
    surname_part = None
    if surnames: # Check if surname list exists for this race
        surname_entry = random.choice(surnames)
        surname = surname_entry["text"]
        surname_part = {"text": surname, "meaning": surname_entry.get('meaning', 'N/A')}
        full_name = f"{first_name} {surname}"
    else:
        full_name = first_name

    result["name"] = full_name

    # --- Poetic Meaning (use the correct gloss dict) ---
    # Ensure _generate_poetic_meaning is called *after* potential surname handling
    # but *before* adding surname_part to result["parts"] if you only want poetic meaning for generated parts.
    result["poetic"] = _generate_poetic_meaning(parts, gloss) # Pass the specific gloss dict

    if surname_part:
        result["parts"].append(surname_part) # Add surname details for display

    return result # Return early with error

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

# === NEW Helper Function for Dragonborn Names ===
def _generate_dragonborn_name_data(race_data):
    """
    Internal helper to generate Dragonborn names (ClanName-k-PersonalName structure).
    Accepts the draconic data dictionary.
    Returns a dictionary containing 'name', 'parts', 'poetic', 'error'.
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    # --- Access data directly ---
    clans = race_data.get("clans")
    prefixes = race_data.get("prefixes")
    middles = race_data.get("middles") # Might be missing
    suffixes = race_data.get("suffixes")
    gloss = race_data.get("gloss")

    # --- Basic Data Validation ---
    if not clans or not prefixes or not suffixes or not gloss:
        error_msg = "Missing core Draconic data (clans, prefixes, suffixes, or gloss)."
        st.error(error_msg)
        result["error"] = error_msg
        return result

    # --- Select Clan Name ---
    clan_part = random.choice(clans)
    # Create a part dictionary for the clan name
    clan_dict = {"text": clan_part["text"], "meaning": clan_part.get("meaning", "N/A")}
    all_parts_for_meaning = [clan_dict] # Start list for poetic meaning

    # --- Assemble Personal Name Parts (using existing helper) ---
    # Dragonborn names are unisex, so use "Any" filter
    personal_parts = _assemble_name_parts(prefixes, middles or [], suffixes, gender_filter="Any")
    if not personal_parts:
        error_msg = "Failed to assemble Draconic personal name parts."
        st.warning(error_msg)
        result["error"] = error_msg
        # Still return the clan name at least
        result["name"] = clan_dict["text"] + "-k-[Error]"
        result["parts"] = [clan_dict]
        return result

    personal_name_str = "".join(p["text"] for p in personal_parts)
    all_parts_for_meaning.extend(personal_parts) # Add personal parts for gloss lookup

    # --- Combine into Full Name ---
    full_name = f"{clan_dict['text']}-k-{personal_name_str}"
    result["name"] = full_name
    result["parts"] = all_parts_for_meaning # Store clan + personal parts

    # --- Generate Poetic Meaning (based on clan + personal parts) ---
    result["poetic"] = _generate_poetic_meaning(all_parts_for_meaning, gloss)

    return result

# === NEW Helper Function for Aarakocra Names ===
def _generate_aarakocra_name_data(race_data, gender="Any"):
    """
    Internal helper for Aarakocra names (Lineage + Personal(P+M+S) structure).
    Accepts the aarakocra data dictionary and gender.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    lineages = race_data.get("lineages")
    prefixes = race_data.get("prefixes")
    middles = race_data.get("middles")
    suffixes = race_data.get("suffixes")
    gloss = race_data.get("gloss")

    if not lineages or not prefixes or not suffixes or not gloss:
        error_msg = "Missing core Aarakocra data (lineages, prefixes, suffixes, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Lineage Name ---
    lineage_part = random.choice(lineages)
    lineage_dict = {"text": lineage_part["text"], "meaning": lineage_part.get("meaning", "N/A")}
    all_parts_for_meaning = [lineage_dict]

    # --- Assemble Personal Name Parts ---
    personal_parts = _assemble_name_parts(prefixes, middles or [], suffixes, gender_filter=gender)
    if not personal_parts:
        error_msg = "Failed to assemble Aarakocra personal name parts."
        st.warning(error_msg); result["error"] = error_msg
        result["name"] = lineage_dict["text"] + " [Error]"
        result["parts"] = [lineage_dict]; return result

    personal_name_str = "".join(p["text"] for p in personal_parts)
    all_parts_for_meaning.extend(personal_parts)

    # --- Combine into Full Name ---
    full_name = f"{lineage_dict['text']} {personal_name_str}" # Space between lineage and personal
    result["name"] = full_name
    result["parts"] = all_parts_for_meaning

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts_for_meaning, gloss)

    return result

# === NEW Helper Function for Owlin Names ===
def _generate_owlin_name_data(race_data):
    """
    Internal helper for Owlin names (Personal + Descriptor structure).
    Accepts the owlin data dictionary. Gender is always Unisex.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    personal_roots = race_data.get("personal")
    descriptors = race_data.get("descriptors")
    gloss = race_data.get("gloss")

    if not personal_roots or not descriptors or not gloss:
        error_msg = "Missing core Owlin data (personal, descriptors, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Personal Name Root ---
    personal_part = random.choice(personal_roots)
    personal_dict = {"text": personal_part["text"], "meaning": personal_part.get("meaning", "N/A")}

    # --- Select Descriptor ---
    descriptor_part = random.choice(descriptors)
    descriptor_dict = {"text": descriptor_part["text"], "meaning": descriptor_part.get("meaning", "N/A")}

    all_parts_for_meaning = [personal_dict, descriptor_dict]

    # --- Combine into Full Name ---
    full_name = f"{personal_dict['text']}{descriptor_dict['text']}" # Combine directly, no space? Or add space? Let's add space.
    full_name = f"{personal_dict['text']}{descriptor_dict['text']}"
    result["name"] = full_name
    result["parts"] = all_parts_for_meaning

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts_for_meaning, gloss)

    return result

# === NEW Helper Function for Tortle Names ===
def _generate_tortle_name_data(race_data, gender="Any"):
    """
    Internal helper for Tortle names (Given + Descriptor structure).
    Accepts the tortle data dictionary and gender.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    given_names = race_data.get("given")
    descriptors = race_data.get("descriptors")
    gloss = race_data.get("gloss")

    if not given_names or not descriptors or not gloss:
        error_msg = "Missing core Tortle data (given, descriptors, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Unisex) ---
    given_part = random.choice(given_names)
    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
    all_parts_for_meaning = [given_dict]

    # --- Select Descriptor (Filtered by Gender) ---
    descriptor_options = descriptors
    if gender != "Any":
        # Filter based on gender, always including Unisex
        filtered_options = [
            d for d in descriptors
            if d.get("gender") == gender or d.get("gender") == "Unisex"
        ]
        if filtered_options:
            descriptor_options = filtered_options
        else:
            st.warning(f"No specific {gender} or Unisex Tortle descriptors found, using any.")
            # Fallback to all descriptors

    if not descriptor_options:
         error_msg = "Tortle descriptor options list is empty after filtering."
         st.error(error_msg); result["error"] = error_msg
         result["name"] = given_dict["text"] + " [Error]"
         result["parts"] = [given_dict]; return result

    descriptor_part = random.choice(descriptor_options)
    descriptor_dict = {"text": descriptor_part["text"], "meaning": descriptor_part.get("meaning", "N/A")}
    all_parts_for_meaning.append(descriptor_dict)

    # --- Combine into Full Name (with space) ---
    full_name = f"{given_dict['text']} {descriptor_dict['text']}"
    result["name"] = full_name
    result["parts"] = all_parts_for_meaning

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts_for_meaning, gloss)

    return result

# === NEW Helper Function for Triton Names ===
def _generate_triton_name_data(race_data):
    """
    Internal helper for Triton names (Given + -Marker structure).
    Accepts the triton data dictionary. Gender is always Unisex.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    given_names = race_data.get("given")
    markers = race_data.get("markers")
    gloss = race_data.get("gloss")

    if not given_names or not markers or not gloss:
        error_msg = "Missing core Triton data (given, markers, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Unisex) ---
    given_part = random.choice(given_names)
    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}

    # --- Select Marker (Unisex) ---
    marker_part = random.choice(markers)
    marker_dict = {"text": marker_part["text"], "meaning": marker_part.get("meaning", "N/A")}

    all_parts_for_meaning = [given_dict, marker_dict]

    # --- Combine into Full Name (with hyphen?) ---
    # Let's use a hyphen to visually separate the marker
    full_name = f"{given_dict['text']}-{marker_dict['text']}"
    result["name"] = full_name
    # Add marker text to parts list for display of meanings
    result["parts"] = all_parts_for_meaning

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts_for_meaning, gloss)

    return result

# === (Corrected) Generate NPC Function ===
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

    # Use default "Any" gender for NPC generation for simplicity for now
    npc_gender = "Any"

    # --- Generate Name based on Race (Using Correct Data Structure) ---

    if race_name == "Elf":
        race_key = "elf"
        if race_key in name_data:
            # *** FIX: Pass the dictionary name_data[race_key] ***
            name_data_result = _generate_structured_name_data(name_data[race_key], npc_gender)
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"]
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
             npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Tabaxi":
        race_key = "tabaxi"
        if race_key in name_data:
            # *** FIX: Pass the dictionary name_data[race_key] ***
            name_data_result = _generate_structured_name_data(name_data[race_key], npc_gender)
            if not name_data_result["error"] and name_data_result["name"]:
                npc_first_name = name_data_result["name"]
            else:
                npc_first_name = f"[{race_name} Name Error]"

            # Assign Clan Name (Access clans via name_data)
            clan_list = name_data[race_key].get("clans", [])
            if clan_list:
                 clan_entry = random.choice(clan_list)
                 clan_name = clan_entry['name'] # Store for details output
                 npc_name = f"{npc_first_name} of the {clan_name} Clan" # Construct display name
            else:
                 npc_name = f"{npc_first_name} [Clan Data Missing]"
                 clan_name = "[Clan Data Missing]" # Placeholder
        else:
            npc_name = f"[{race_name} Name Data Missing] {race_name}"


    elif race_name == "Human":
        # Common name logic (already updated to use name_data)
        npc_name = _get_common_name_string(gender_filter=npc_gender)


    elif race_name == "Half-Elf":
        chosen_style = random.choice(["Elven", "Common"])
        if chosen_style == "Elven":
            race_key = "elf"
            if race_key in name_data:
                 # *** FIX: Pass the dictionary name_data[race_key] ***
                name_data_result = _generate_structured_name_data(name_data[race_key], npc_gender)
                if not name_data_result["error"] and name_data_result["name"]: npc_name = name_data_result["name"]
                else: npc_name = f"[Elven Name Error] Half-Elf"
            else:
                 npc_name = f"[Elven Name Data Missing] Half-Elf"
        else: # Common style
            npc_name = _get_common_name_string(gender_filter=npc_gender)


    elif race_name == "Orc":
        race_key = "orc"
        if race_key in name_data:
            # *** FIX: Pass the dictionary name_data[race_key] ***
            name_data_result = _generate_structured_name_data(name_data[race_key], npc_gender)
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Helper now includes surname
            else:
                 npc_name = f"[{race_name} Name Error] {race_name}"
        else:
            npc_name = f"[{race_name} Name Data Missing] {race_name}"


    elif race_name == "Half-Orc":
        chosen_style = random.choice(["Orc", "Common"])
        if chosen_style == "Orc":
             race_key = "orc"
             if race_key in name_data:
                 # *** FIX: Pass the dictionary name_data[race_key] ***
                 name_data_result = _generate_structured_name_data(name_data[race_key], npc_gender)
                 if not name_data_result["error"] and name_data_result["name"]: npc_name = name_data_result["name"]
                 else: npc_name = f"[Orcish Name Error] Half-Orc"
             else:
                 npc_name = f"[Orcish Name Data Missing] Half-Orc"
        else: # Common style
             npc_name = _get_common_name_string(gender_filter=npc_gender)


    elif race_name == "Tiefling":
         race_key = "infernal" # Key used in name_data
         if race_key in name_data:
             # *** FIX: Pass the dictionary name_data[race_key] ***
             name_data_result = _generate_structured_name_data(name_data[race_key], npc_gender)
             if not name_data_result["error"] and name_data_result["name"]:
                 npc_name = name_data_result["name"] # Includes surname now
             else:
                 npc_name = f"[{race_name} Name Error] {race_name}"
         else:
            npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Drow":
        race_key = "drow"
        if race_key in name_data:
            # Pass the Drow sub-dictionary
            name_data_result = _generate_structured_name_data(name_data[race_key], npc_gender)
            if not name_data_result["error"] and name_data_result["name"]:
                # Drow names don't have separate surnames in this setup
                npc_name = name_data_result["name"]
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Dragonborn":
        race_key = "draconic"
        if race_key in name_data:
            # Call the new Dragonborn helper
            name_data_result = _generate_dragonborn_name_data(name_data[race_key])
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"]
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Aarakocra":
        race_key = "aarakocra"
        if race_key in name_data:
            # Use "Any" gender for NPC gen default
            name_data_result = _generate_aarakocra_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"]
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Owlin":
        race_key = "owlin"
        if race_key in name_data:
            # Owlin names are unisex, no gender needed
            name_data_result = _generate_owlin_name_data(name_data[race_key])
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"]
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Tortle":
        race_key = "tortle"
        if race_key in name_data:
            # Use "Any" gender for NPC gen default
            name_data_result = _generate_tortle_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"]
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Triton":
        race_key = "triton"
        if race_key in name_data:
            # Triton names are unisex
            name_data_result = _generate_triton_name_data(name_data[race_key])
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"]
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Fire Genasi":
        race_key = "ignan"
        if race_key in name_data:
            # Use standard helper, gender="Any" for unisex names
            name_data_result = _generate_structured_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Single name result
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Earth Genasi":
        race_key = "terran"
        if race_key in name_data:
            # Use standard helper, gender="Any" for unisex names
            name_data_result = _generate_structured_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Single name result
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Air Genasi":
        race_key = "air_genasi"
        if race_key in name_data:
            # Use standard helper, gender="Any" for unisex names
            name_data_result = _generate_structured_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Single name result
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Water Genasi":
        race_key = "water_genasi"
        if race_key in name_data:
            # Use standard helper, gender="Any" for unisex names
            name_data_result = _generate_structured_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Single name result
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    # --- Add more elif blocks here for future races ---

    # --- Assemble NPC Output --- (Rest of the function remains the same)
    npc_lines = [f"👤 **Name:** {npc_name}"]

    if race_name == "Tabaxi" and clan_name and clan_name != "[Clan Data Missing]":
         npc_lines.append(f"🏡 **Clan:** {clan_name}")

    npc_lines.extend([
        "---",
        "💼 **Basic Info**",
        f"🧬 **Race:** {race_name} ({race_data.get('rarity', 'N/A')})",
        f"🌍 **Region:** {race_data.get('region', 'N/A')}",
        f"📖 **Lore:** {race_data.get('description', 'N/A')}",
        "✶" * 25,
        "🎭 **Personality & Story**"
    ])

    for category, options in npc_attributes.items():
        if not options: continue
        clean_category = category.strip()
        icon = icons.get(clean_category, "•")
        choice = random.choice(options)
        npc_lines.append(f"{icon} **{clean_category}:** {choice}")

    return "\n\n".join(npc_lines) # Use double newline for better spacing

# === (Revised Wrappers using name_data) ===

def generate_elven_name(gender="Any"):
    race_key = "elf"
    if race_key not in name_data: return "Error: Elven name data not loaded."
    data = _generate_structured_name_data(name_data[race_key], gender) # Pass sub-dictionary
    # ... (rest of the function formatting remains the same) ...
    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    return (
        f"🌿 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **Poetic Meaning:** {data['poetic']}"
    )


def generate_orc_name(gender="Any"):
    race_key = "orc"
    if race_key not in name_data: return "Error: Orcish name data not loaded."
    data = _generate_structured_name_data(name_data[race_key], gender) # Pass sub-dictionary
    # ... (rest of the function formatting remains the same) ...
    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    return (
        f"⚙️ **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **Poetic Meaning (First Name):** {data['poetic']}"
    )

# === (Revised) Generate Infernal Name Function ===
def generate_infernal_name(gender="Any"):
    race_key = "infernal"
    if race_key not in name_data: return "Error: Infernal name data not loaded."
    # Pass the sub-dictionary to the helper
    data = _generate_structured_name_data(name_data[race_key], gender)

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines will include surname meaning if present, as helper adds it to 'parts'
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    # Clarify that poetic meaning applies to the name generated from parts (first name)
    poetic_label = "Poetic Meaning (First Name):" if len(data["parts"]) > 1 and any(p for p in data["parts"] if p.get("text") == data["name"].split(" ")[-1]) else "Poetic Meaning:" # Crude check if surname seems present

    return (
        f"🔥 **Name:** {data['name']}\n\n" + # Full name includes surname now
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

def generate_tabaxi_name(selected_clan):
    race_key = "tabaxi"
    if race_key not in name_data: return "Error: Tabaxi name data not loaded."
    # Check specific clan data (still needed separately)
    if "clans" not in name_data[race_key] or not name_data[race_key]["clans"]:
         st.error("Missing required Tabaxi clan data.")
         return "Error: Missing clan data."

    data = _generate_structured_name_data(name_data[race_key], gender="Any") # Pass sub-dictionary
    # ... (rest of the function formatting remains the same) ...
    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    full_name = data["name"]
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    poetic = data["poetic"]

    # Clan Info (Access clans via name_data)
    clan_list = name_data[race_key]["clans"]
    clan_info = next((c for c in clan_list if c["name"] == selected_clan), None)
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

    return (
        f"🐾 **Name:** {full_name}\n\n"
        + "\n".join(meaning_lines)
        + f"\n\n➔ **Poetic Meaning:** {poetic}{clan_desc}"
    )

def generate_drow_name(gender="Any"):
    """Generates a Drow name with meanings for the Name Generator tab."""
    race_key = "drow"
    if race_key not in name_data: return "Error: Drow name data not loaded."
    # Pass the Drow sub-dictionary to the helper
    data = _generate_structured_name_data(name_data[race_key], gender)

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines will include surname (House Name) meaning, as helper adds it to 'parts'
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    # Clarify that poetic meaning applies to the first name parts
    # Use a slightly more robust check for surname presence
    is_surname_present = len(data["parts"]) > 1 and "surnames" in name_data.get(race_key, {})
    poetic_label = "Poetic Meaning (First Name):" if is_surname_present else "Poetic Meaning:"

    # Use a spider emoji for Drow
    return (
        f"🕷️ **Name:** {data['name']}\n\n" + # Full name includes House Name now
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Dragonborn Name Function ===
def generate_dragonborn_name(): # No gender parameter needed
    """Generates a Dragonborn name with meanings for the Name Generator tab."""
    race_key = "draconic"
    if race_key not in name_data: return "Error: Draconic name data not loaded."
    # Pass the Draconic sub-dictionary to the new helper
    data = _generate_dragonborn_name_data(name_data[race_key])

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include clan + personal parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    # Poetic meaning applies to the whole name construct
    poetic_label = "Poetic Meaning:"

    # Use a dragon emoji
    return (
        f"🐉 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Aarakocra Name Function ===
def generate_aarakocra_name(gender="Any"):
    """Generates an Aarakocra name with meanings for the Name Generator tab."""
    race_key = "aarakocra"
    if race_key not in name_data: return "Error: Aarakocra name data not loaded."
    # Pass the Aarakocra sub-dictionary and gender to the helper
    data = _generate_aarakocra_name_data(name_data[race_key], gender)

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include lineage + personal parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    # Poetic meaning applies to the whole name construct
    poetic_label = "Poetic Meaning:"

    # Use a bird emoji?
    return (
        f"🐦 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Owlin Name Function ===
def generate_owlin_name(): # No gender parameter
    """Generates an Owlin name with meanings for the Name Generator tab."""
    race_key = "owlin"
    if race_key not in name_data: return "Error: Owlin name data not loaded."
    # Pass the Owlin sub-dictionary to the helper
    data = _generate_owlin_name_data(name_data[race_key])

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include personal + descriptor parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    # Poetic meaning applies to the whole name construct
    poetic_label = "Poetic Meaning:"

    # Use an owl emoji?
    return (
        f"🦉 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Tortle Name Function ===
def generate_tortle_name(gender="Any"):
    """Generates a Tortle name with meanings for the Name Generator tab."""
    race_key = "tortle"
    if race_key not in name_data: return "Error: Tortle name data not loaded."
    # Pass the Tortle sub-dictionary and gender to the helper
    data = _generate_tortle_name_data(name_data[race_key], gender)

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include given + descriptor parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    # Poetic meaning applies to the whole name
    poetic_label = "Poetic Meaning:"

    # Use a turtle emoji
    return (
        f"🐢 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Triton Name Function ===
def generate_triton_name(): # No gender parameter
    """Generates a Triton name with meanings for the Name Generator tab."""
    race_key = "triton"
    if race_key not in name_data: return "Error: Triton name data not loaded."
    # Pass the Triton sub-dictionary to the helper
    data = _generate_triton_name_data(name_data[race_key])

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include given + marker parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    # Poetic meaning applies to the whole name
    poetic_label = "Poetic Meaning:"

    # Use a trident emoji?
    return (
        f"🔱 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Fire Genasi Name Function ===
def generate_fire_genasi_name(): # Unisex, no gender parameter
    """Generates a Fire Genasi name with meanings for the Name Generator tab."""
    race_key = "ignan" # Use the Ignan data key
    if race_key not in name_data: return "Error: Ignan (Fire Genasi) name data not loaded."

    # Use the standard helper - it handles P+M+S combination into one name
    # Pass "Any" gender since all Ignan parts are Unisex
    data = _generate_structured_name_data(name_data[race_key], gender="Any")

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include P+M+S parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    poetic_label = "Poetic Meaning:"

    # Use a fire emoji
    return (
        f"🔥 **Name:** {data['name']}\n\n" + # Helper already provides combined name
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Earth Genasi Name Function ===
def generate_earth_genasi_name(): # Unisex, no gender parameter
    """Generates an Earth Genasi name with meanings for the Name Generator tab."""
    race_key = "terran" # Use the Terran data key
    if race_key not in name_data: return "Error: Terran (Earth Genasi) name data not loaded."

    # Use the standard helper
    data = _generate_structured_name_data(name_data[race_key], gender="Any")

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    poetic_label = "Poetic Meaning:"

    # Use a mountain or rock emoji
    return (
        f"⛰️ **Name:** {data['name']}\n\n" + # Helper already provides combined name
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Air Genasi Name Function ===
def generate_air_genasi_name(): # Unisex
    """Generates an Air Genasi name with meanings for the Name Generator tab."""
    race_key = "air_genasi"
    if race_key not in name_data: return "Error: Air Genasi name data not loaded."

    # Use the standard helper; gender="Any" for unisex names
    data = _generate_structured_name_data(name_data[race_key], gender="Any")

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    poetic_label = "Poetic Meaning:"

    # Use a wind emoji
    return (
        f"💨 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Water Genasi Name Function ===
def generate_water_genasi_name(): # Unisex
    """Generates a Water Genasi name with meanings for the Name Generator tab."""
    race_key = "water_genasi"
    if race_key not in name_data: return "Error: Water Genasi name data not loaded."

    # Use the standard helper; gender="Any" for unisex names
    data = _generate_structured_name_data(name_data[race_key], gender="Any")

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    poetic_label = "Poetic Meaning:"

    # Use a water drop emoji
    return (
        f"💧 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# IMPORTANT: Also update generate_npc where it calls _generate_structured_name_data directly for Half-Elves/Half-Orcs
# Example for Half-Elf (Elven style):
# Replace:
# name_data_result = _generate_structured_name_data("elf", npc_gender)
# With:
# if "elf" in name_data:
#     name_data_result = _generate_structured_name_data(name_data["elf"], npc_gender)
# else:
#     name_data_result = {"error": "Elven name data not loaded."}

# Do similarly for Half-Orc (Orc Style).
# Calls to _get_common_name_string also need updating to use name_data['common']

# Revised _get_common_name_string:
def _get_common_name_string(gender_filter="Any"):
    """Generates a Common first name + surname string, optionally filtered by gender."""
    if "common" not in name_data or "first_names" not in name_data["common"] or "surnames" not in name_data["common"]:
        st.error("Common name data missing or incomplete.")
        return "[Common Name Data Missing]"

    common_first_names = name_data["common"]["first_names"]
    common_surnames = name_data["common"]["surnames"]

    # --- Filter first names based on gender --- (Logic remains the same)
    possible_first_names = common_first_names
    if gender_filter != "Any":
        filtered_names = [
            name_entry for name_entry in common_first_names
            if name_entry.get("gender") == gender_filter or name_entry.get("gender") == "Unisex"
        ]
        if filtered_names:
            possible_first_names = filtered_names
        else:
            st.warning(f"No '{gender_filter}' or 'Unisex' first names found, using any.")

    if not possible_first_names:
        return "[Error: No suitable first names]"
    # --- End Filtering ---

    first_name_entry = random.choice(possible_first_names)
    surname_entry = random.choice(common_surnames)

    return f"{first_name_entry['text']} {surname_entry['text']}"

# And update generate_common_name similarly:
def generate_common_name(gender="Any"): # Add gender parameter
    """Generates a Common name with meanings for the Name Generator tab."""
    if "common" not in name_data or "first_names" not in name_data["common"] or "surnames" not in name_data["common"]:
        st.error("Missing required Common name data.")
        return "Error: Missing data."

    common_first_names = name_data["common"]["first_names"]
    common_surnames = name_data["common"]["surnames"]
    # --- Filtering logic copied from _get_common_name_string ---
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
    surname_entry = random.choice(common_surnames)
    # ... rest of formatting logic remains the same ...
    full_name = f"{first_name_entry['text']} {surname_entry['text']}"
    meaning_lines = []
    meaning_lines.append(f"- **{first_name_entry['text']}** = {first_name_entry.get('meaning', 'N/A')}")
    if 'meaning' in surname_entry:
         meaning_lines.append(f"- **{surname_entry['text']}** = {surname_entry['meaning']}")
    else:
         meaning_lines.append(f"- **{surname_entry['text']}**")
    return (
        f"👤 **Name:** {full_name}\n\n" +
        "\n".join(meaning_lines) +
        ""
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
    race = st.selectbox(
        "Choose a race:",
        ["Elf", "Tabaxi", "Human", "Orc", "Tiefling", "Drow", "Dragonborn",
        "Aarakocra", "Owlin", "Tortle", "Triton", "Genasi"],
        key="name_race"
    )
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
        # --- ADD Gender selection HERE for Tieflings ---
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="tiefling_gender_radio", # Use unique key
            horizontal=True
        )
        # --- End ADD ---
        if st.button("Generate Infernal Name", key="tiefling_name_button"):
             # --- Pass the selected gender ---
             st.session_state.name_output = generate_infernal_name(gender=gender)

    elif race == "Drow":
        # Gender selection shown HERE for Drow
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="drow_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Drow Name", key="drow_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_drow_name(gender=gender)

    elif race == "Dragonborn":
        # NO gender selection needed for Dragonborn
        if st.button("Generate Dragonborn Name", key="dragonborn_name_button"):
             # Call the function without gender
             st.session_state.name_output = generate_dragonborn_name()

    elif race == "Aarakocra":
        # Gender selection needed for Aarakocra
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="aarakocra_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Aarakocra Name", key="aarakocra_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_aarakocra_name(gender=gender)

    elif race == "Owlin":
        # NO gender selection needed for Owlin
        if st.button("Generate Owlin Name", key="owlin_name_button"):
             # Call the function without gender
             st.session_state.name_output = generate_owlin_name()

    elif race == "Tortle":
        # Gender selection needed for Tortle
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="tortle_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Tortle Name", key="tortle_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_tortle_name(gender=gender)

    elif race == "Triton":
        # NO gender selection needed for Triton
        if st.button("Generate Triton Name", key="triton_name_button"):
             # Call the function without gender
             st.session_state.name_output = generate_triton_name()

    elif race == "Genasi":
        st.markdown("---") # Optional separator
        # Add secondary selection for element type
        element = st.radio(
            "Select Element:",
            ["Air", "Water", "Fire", "Earth"],
            key="genasi_element_radio",
            horizontal=True
        )

        # Single button for all Genasi types
        if st.button("Generate Genasi Name", key="genasi_name_button"):
            # Call the correct function based on the selected element
            if element == "Air":
                st.session_state.name_output = generate_air_genasi_name()
            elif element == "Water":
                st.session_state.name_output = generate_water_genasi_name()
            elif element == "Fire":
                st.session_state.name_output = generate_fire_genasi_name()
            elif element == "Earth":
                st.session_state.name_output = generate_earth_genasi_name()

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