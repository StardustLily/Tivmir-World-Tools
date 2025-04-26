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
kenku_names = load_json("kenku_names.json")
# Consolidate name data into a dictionary
auran_gloss = load_json("auran_poetic_gloss.json")
aquan_gloss = load_json("aquan_poetic_gloss.json")
ignan_gloss = load_json("ignan_poetic_gloss.json")
terran_gloss = load_json("terran_poetic_gloss.json")
sylvan_gloss = load_json("sylvan_poetic_gloss.json")
lizardfolk_names = load_json("lizardfolk_names.json")
yuan_ti_names = load_json("yuan-ti_names.json")
goblin_names = load_json("goblin_names.json")
gnomish_gloss = load_json("gnomish_poetic_gloss.json")
halfling_gloss = load_json("halfling_poetic_gloss.json")
giant_gloss = load_json("giant_poetic_gloss.json")
bugbear_gloss = load_json("bugbear_poetic_gloss.json")
harengon_gloss = load_json("harengon_poetic_gloss.json")
leonin_gloss = load_json("leonin_poetic_gloss.json")
loxodon_gloss = load_json("loxodon_poetic_gloss.json")
aasimar_gloss = load_json("aasimar_poetic_gloss.json")
shifter_names = load_json("shifter_names.json")
githyanki_gloss = load_json("githyanki_poetic_gloss.json")
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
        "gloss": aquan_gloss},
    "sylvan": {
        "prefixes": load_json("sylvan_prefixes.json"),
        "middles": load_json("sylvan_middles.json"),
        "suffixes": load_json("sylvan_suffixes.json"),
        "gloss": sylvan_gloss},
    "gnomish": {
        "male_first": load_json("gnome_male_first.json"),
        "female_first": load_json("gnome_female_first.json"),
        "clans": load_json("gnome_clans.json"),
        "descriptors": load_json("gnome_descriptors.json"),
        "gloss": gnomish_gloss},
    "halfling": {
        "male_first": load_json("halfling_male_first.json"),
        "female_first": load_json("halfling_female_first.json"),
        "family": load_json("halfling_family.json"),
        "gloss": halfling_gloss},
    "goliath": {
        "given": load_json("goliath_given.json"),
        "titles": load_json("goliath_titles.json"),
        "gloss": giant_gloss},
    "minotaur": {
        "male_first": load_json("minotaur_male_first.json"),
        "female_first": load_json("minotaur_female_first.json"),
        "descriptors": load_json("minotaur_descriptors.json"),
        "gloss": giant_gloss},
    "bugbear": {
        "given": load_json("bugbear_given.json"),
        "epithets": load_json("bugbear_epithets.json"),
        "gloss": bugbear_gloss},
    "harengon": {
        "given": load_json("harengon_given.json"),
        "family": load_json("harengon_family.json"),
        "gloss": harengon_gloss},
    "leonin": {
        "male_first": load_json("leonin_male_first.json"),
        "female_first": load_json("leonin_female_first.json"),
        "pridenames": load_json("leonin_pridenames.json"),
        "gloss": leonin_gloss},
    "loxodon": {
        "male_first": load_json("loxodon_male_first.json"),
        "female_first": load_json("loxodon_female_first.json"),
        "herdnames": load_json("loxodon_herdnames.json"),
        "gloss": loxodon_gloss},
    "aasimar": {
        "prefixes": load_json("aasimar_base_prefixes.json"),
        "middles": load_json("aasimar_base_middles.json"),
        "suffixes": load_json("aasimar_base_suffixes.json"),
        "titles": load_json("aasimar_celestial_titles.json"),
        "gloss": aasimar_gloss},
    "githyanki": {
        "male_first": load_json("githyanki_male_first.json"),
        "female_first": load_json("githyanki_female_first.json"),
        "titles": load_json("githyanki_titles.json"),
        "gloss": githyanki_gloss}
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

# === NEW Helper Function for Gnome Names ===
def _generate_gnome_name_data(race_data, gender="Any"):
    """
    Internal helper for Gnome names (Given + Clan + Optional Descriptor).
    Accepts the gnomish data dictionary and gender.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    male_first = race_data.get("male_first")
    female_first = race_data.get("female_first")
    clans = race_data.get("clans")
    descriptors = race_data.get("descriptors")
    gloss = race_data.get("gloss")

    if not male_first or not female_first or not clans or not descriptors or not gloss:
        error_msg = "Missing core Gnomish data (first names, clans, descriptors, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Gendered) ---
    given_part = None
    if gender == "Male":
        given_part = random.choice(male_first)
    elif gender == "Female":
        given_part = random.choice(female_first)
    else: # Gender is "Any"
        # Randomly pick Male or Female list, then pick a name
        chosen_list = random.choice([male_first, female_first])
        given_part = random.choice(chosen_list)

    if not given_part: # Should not happen if lists aren't empty
         error_msg = "Failed to select Gnomish given name."; st.error(error_msg)
         result["error"] = error_msg; return result

    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
    all_parts = [given_dict]

    # --- Select Clan Name (Unisex) ---
    clan_part = random.choice(clans)
    clan_dict = {"text": clan_part["text"], "meaning": clan_part.get("meaning", "N/A")}
    all_parts.append(clan_dict)

    # --- Select Optional Descriptor (Unisex) ---
    descriptor_dict = None
    use_descriptor = random.random() < 0.5 # 50% chance of having a descriptor
    if use_descriptor:
        descriptor_part = random.choice(descriptors)
        descriptor_dict = {"text": descriptor_part["text"], "meaning": descriptor_part.get("meaning", "N/A")}
        all_parts.append(descriptor_dict)

    # --- Combine into Full Name (Space separated) ---
    name_components = [p["text"] for p in all_parts]
    full_name = " ".join(name_components)
    result["name"] = full_name
    result["parts"] = all_parts

    # --- Generate Poetic Meaning (based on all selected parts) ---
    result["poetic"] = _generate_poetic_meaning(all_parts, gloss)

    return result

# === NEW Helper Function for Halfling Names ===
def _generate_halfling_name_data(race_data, gender="Any"):
    """
    Internal helper for Halfling names (Given + Family Name structure).
    Accepts the halfling data dictionary and gender.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    male_first = race_data.get("male_first")
    female_first = race_data.get("female_first")
    family_names = race_data.get("family")
    gloss = race_data.get("gloss")

    if not male_first or not female_first or not family_names or not gloss:
        error_msg = "Missing core Halfling data (first names, family names, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Gendered) ---
    given_part = None
    if gender == "Male":
        given_part = random.choice(male_first)
    elif gender == "Female":
        given_part = random.choice(female_first)
    else: # Gender is "Any"
        chosen_list = random.choice([male_first, female_first])
        given_part = random.choice(chosen_list)

    if not given_part:
         error_msg = "Failed to select Halfling given name."; st.error(error_msg)
         result["error"] = error_msg; return result

    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
    all_parts = [given_dict]

    # --- Select Family Name (Unisex) ---
    family_part = random.choice(family_names)
    family_dict = {"text": family_part["text"], "meaning": family_part.get("meaning", "N/A")}
    all_parts.append(family_dict)

    # --- Combine into Full Name (Space separated) ---
    full_name = f"{given_dict['text']} {family_dict['text']}"
    result["name"] = full_name
    result["parts"] = all_parts

    # --- Generate Poetic Meaning (based on all parts) ---
    # Poetic meaning might focus more on the family name for flavor
    result["poetic"] = _generate_poetic_meaning(all_parts, gloss)

    return result

# === NEW Helper Function for Goliath Names ===
def _generate_goliath_name_data(race_data):
    """
    Internal helper for Goliath names (Given + Title/Descriptor structure).
    Accepts the goliath data dictionary. Names are Unisex.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    given_names = race_data.get("given")
    titles = race_data.get("titles")
    gloss = race_data.get("gloss")

    if not given_names or not titles or not gloss:
        error_msg = "Missing core Goliath data (given, titles, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Unisex) ---
    given_part = random.choice(given_names)
    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}

    # --- Select Title/Descriptor (Unisex) ---
    title_part = random.choice(titles)
    title_dict = {"text": title_part["text"], "meaning": title_part.get("meaning", "N/A")}

    all_parts = [given_dict, title_dict]

    # --- Combine into Full Name (with space) ---
    full_name = f"{given_dict['text']} {title_dict['text']}"
    result["name"] = full_name
    result["parts"] = all_parts

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts, gloss)

    return result

# === NEW Helper Function for Minotaur Names ===
def _generate_minotaur_name_data(race_data, gender="Any"):
    """
    Internal helper for Minotaur names (Given + Descriptor/Epithet).
    Accepts the minotaur data dictionary and gender.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    male_first = race_data.get("male_first")
    female_first = race_data.get("female_first")
    descriptors = race_data.get("descriptors")
    gloss = race_data.get("gloss")

    if not male_first or not female_first or not descriptors or not gloss:
        error_msg = "Missing core Minotaur data (first names, descriptors, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Gendered) ---
    given_part = None
    if gender == "Male":
        given_part = random.choice(male_first)
    elif gender == "Female":
        given_part = random.choice(female_first)
    else: # Gender is "Any"
        chosen_list = random.choice([male_first, female_first])
        given_part = random.choice(chosen_list)

    if not given_part:
         error_msg = "Failed to select Minotaur given name."; st.error(error_msg)
         result["error"] = error_msg; return result

    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}

    # --- Select Descriptor/Epithet (Unisex) ---
    descriptor_part = random.choice(descriptors)
    descriptor_dict = {"text": descriptor_part["text"], "meaning": descriptor_part.get("meaning", "N/A")}

    all_parts = [given_dict, descriptor_dict]

    # --- Combine into Full Name (with space) ---
    full_name = f"{given_dict['text']} {descriptor_dict['text']}"
    result["name"] = full_name
    result["parts"] = all_parts

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts, gloss)

    return result

# === NEW Helper Function for Bugbear Names ===
def _generate_bugbear_name_data(race_data):
    """
    Internal helper for Bugbear names (Given + Epithet structure).
    Accepts the bugbear data dictionary. Names are Unisex.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    given_names = race_data.get("given")
    epithets = race_data.get("epithets")
    gloss = race_data.get("gloss")

    if not given_names or not epithets or not gloss:
        error_msg = "Missing core Bugbear data (given, epithets, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Unisex) ---
    given_part = random.choice(given_names)
    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}

    # --- Select Epithet (Unisex) ---
    epithet_part = random.choice(epithets)
    epithet_dict = {"text": epithet_part["text"], "meaning": epithet_part.get("meaning", "N/A")}

    all_parts = [given_dict, epithet_dict]

    # --- Combine into Full Name (with space) ---
    full_name = f"{given_dict['text']} {epithet_dict['text']}"
    result["name"] = full_name
    result["parts"] = all_parts

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts, gloss)

    return result

# === NEW Helper Function for Harengon Names ===
def _generate_harengon_name_data(race_data):
    """
    Internal helper for Harengon names (Given + Family/Burrow structure).
    Accepts the harengon data dictionary. Names are Unisex.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    given_names = race_data.get("given")
    family_names = race_data.get("family")
    gloss = race_data.get("gloss")

    if not given_names or not family_names or not gloss:
        error_msg = "Missing core Harengon data (given, family, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Unisex) ---
    given_part = random.choice(given_names)
    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}

    # --- Select Family/Burrow Name (Unisex) ---
    family_part = random.choice(family_names)
    family_dict = {"text": family_part["text"], "meaning": family_part.get("meaning", "N/A")}

    all_parts = [given_dict, family_dict]

    # --- Combine into Full Name (with space) ---
    full_name = f"{given_dict['text']} {family_dict['text']}"
    result["name"] = full_name
    result["parts"] = all_parts

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts, gloss)

    return result

# === NEW Helper Function for Leonin Names ===
def _generate_leonin_name_data(race_data, gender="Any"):
    """
    Internal helper for Leonin names (Given + Pride Name structure).
    Accepts the leonin data dictionary and gender.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    male_first = race_data.get("male_first")
    female_first = race_data.get("female_first")
    pride_names = race_data.get("pridenames")
    gloss = race_data.get("gloss")

    if not male_first or not female_first or not pride_names or not gloss:
        error_msg = "Missing core Leonin data (first names, pride names, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Gendered) ---
    given_part = None
    if gender == "Male":
        given_part = random.choice(male_first)
    elif gender == "Female":
        given_part = random.choice(female_first)
    else: # Gender is "Any"
        chosen_list = random.choice([male_first, female_first])
        given_part = random.choice(chosen_list)

    if not given_part:
         error_msg = "Failed to select Leonin given name."; st.error(error_msg)
         result["error"] = error_msg; return result

    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
    all_parts = [given_dict]

    # --- Select Pride Name (Unisex) ---
    pride_part = random.choice(pride_names)
    pride_dict = {"text": pride_part["text"], "meaning": pride_part.get("meaning", "N/A")}
    all_parts.append(pride_dict)

    # --- Combine into Full Name (with space) ---
    full_name = f"{given_dict['text']} {pride_dict['text']}"
    result["name"] = full_name
    result["parts"] = all_parts

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts, gloss)

    return result

# === NEW Helper Function for Loxodon Names ===
def _generate_loxodon_name_data(race_data, gender="Any"):
    """
    Internal helper for Loxodon names (Given + Herd Name structure).
    Accepts the loxodon data dictionary and gender.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    male_first = race_data.get("male_first")
    female_first = race_data.get("female_first")
    herd_names = race_data.get("herdnames")
    gloss = race_data.get("gloss")

    if not male_first or not female_first or not herd_names or not gloss:
        error_msg = "Missing core Loxodon data (first names, herd names, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Gendered) ---
    given_part = None
    if gender == "Male":
        given_part = random.choice(male_first)
    elif gender == "Female":
        given_part = random.choice(female_first)
    else: # Gender is "Any"
        chosen_list = random.choice([male_first, female_first])
        given_part = random.choice(chosen_list)

    if not given_part:
         error_msg = "Failed to select Loxodon given name."; st.error(error_msg)
         result["error"] = error_msg; return result

    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
    all_parts = [given_dict]

    # --- Select Herd Name (Unisex) ---
    herd_part = random.choice(herd_names)
    herd_dict = {"text": herd_part["text"], "meaning": herd_part.get("meaning", "N/A")}
    all_parts.append(herd_dict)

    # --- Combine into Full Name (with space) ---
    full_name = f"{given_dict['text']} {herd_dict['text']}"
    result["name"] = full_name
    result["parts"] = all_parts

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts, gloss)

    return result

# === NEW Helper Function for Aasimar Names ===
def _generate_aasimar_name_data(race_data):
    """
    Internal helper for Aasimar names (Base P+M+S + Optional Title).
    Accepts the aasimar data dictionary. Names are Unisex.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    prefixes = race_data.get("prefixes")
    middles = race_data.get("middles")
    suffixes = race_data.get("suffixes")
    titles = race_data.get("titles")
    gloss = race_data.get("gloss")

    if not prefixes or not suffixes or not titles or not gloss: # Middles are optional
        error_msg = "Missing core Aasimar data (prefixes, suffixes, titles, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Assemble Base Name Parts (Unisex) ---
    base_parts = _assemble_name_parts(prefixes, middles or [], suffixes, gender_filter="Any")
    if not base_parts:
        error_msg = "Failed to assemble Aasimar base name parts."
        st.warning(error_msg); result["error"] = error_msg
        result["name"] = "[Base Name Error]"
        return result

    base_name_str = "".join(p["text"] for p in base_parts)
    all_parts = base_parts # Start list for display & gloss

    # --- Select Optional Title (Unisex) ---
    title_dict = None
    full_name = base_name_str # Default to just base name
    use_title = random.random() < 0.4 # 40% chance of having a title
    if use_title and titles:
        title_part = random.choice(titles)
        title_dict = {"text": title_part["text"], "meaning": title_part.get("meaning", "N/A")}
        all_parts.append(title_dict)
        full_name = f"{base_name_str} {title_dict['text']}" # Add title with space

    result["name"] = full_name
    result["parts"] = all_parts

    # --- Generate Poetic Meaning (based on all selected parts) ---
    result["poetic"] = _generate_poetic_meaning(all_parts, gloss)

    return result

# === NEW Helper Function for Githyanki Names ===
def _generate_githyanki_name_data(race_data, gender="Any"):
    """
    Internal helper for Githyanki names (Given + Title structure).
    Accepts the githyanki data dictionary and gender.
    Returns {'name':..., 'parts':..., 'poetic':..., 'error':...}
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}

    male_first = race_data.get("male_first")
    female_first = race_data.get("female_first")
    titles = race_data.get("titles")
    gloss = race_data.get("gloss")

    if not male_first or not female_first or not titles or not gloss:
        error_msg = "Missing core Githyanki data (first names, titles, or gloss)."
        st.error(error_msg); result["error"] = error_msg; return result

    # --- Select Given Name (Gendered) ---
    given_part = None
    if gender == "Male":
        given_part = random.choice(male_first)
    elif gender == "Female":
        given_part = random.choice(female_first)
    else: # Gender is "Any"
        chosen_list = random.choice([male_first, female_first])
        given_part = random.choice(chosen_list)

    if not given_part:
         error_msg = "Failed to select Githyanki given name."; st.error(error_msg)
         result["error"] = error_msg; return result

    given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
    all_parts = [given_dict]

    # --- Select Title (Unisex) ---
    title_part = random.choice(titles)
    title_dict = {"text": title_part["text"], "meaning": title_part.get("meaning", "N/A")}
    all_parts.append(title_dict)

    # --- Combine into Full Name (with space) ---
    full_name = f"{given_dict['text']} {title_dict['text']}"
    result["name"] = full_name
    result["parts"] = all_parts

    # --- Generate Poetic Meaning ---
    result["poetic"] = _generate_poetic_meaning(all_parts, gloss)

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

    elif race_name == "Eladrin":
        race_key = "sylvan" # Use the Sylvan data key
        if race_key in name_data:
            # Use standard helper, gender="Any" for unisex names
            name_data_result = _generate_structured_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Single P+M+S name result
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Kenku":
        if kenku_names: # Check if the list was loaded
             # generate_kenku_name now returns the formatted string, we need just the name text
             name_entry = random.choice(kenku_names)
             npc_name = name_entry.get('text', '[Name Error]')
        else:
            npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Lizardfolk":
        if lizardfolk_names: # Check if the list was loaded
             name_entry = random.choice(lizardfolk_names)
             npc_name = name_entry.get('text', '[Name Error]')
        else:
            npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Yuan-ti":
        if yuan_ti_names: # Check if the list was loaded
             name_entry = random.choice(yuan_ti_names)
             npc_name = name_entry.get('text', '[Name Error]')
        else:
            npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Goblin":
        if goblin_names: # Check if the list was loaded
             name_entry = random.choice(goblin_names)
             npc_name = name_entry.get('text', '[Name Error]')
        else:
            npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Gnome":
        race_key = "gnomish"
        if race_key in name_data:
            # Use "Any" gender for NPC gen default (helper function handles random M/F pick)
            name_data_result = _generate_gnome_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Full G+C+D name
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Halfling":
        race_key = "halfling"
        if race_key in name_data:
            # Use "Any" gender for NPC gen default (helper handles random M/F pick)
            name_data_result = _generate_halfling_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Given + Family name
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Goliath":
        race_key = "goliath"
        if race_key in name_data:
            # Goliath names are unisex
            name_data_result = _generate_goliath_name_data(name_data[race_key])
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Given + Title
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Minotaur":
        race_key = "minotaur"
        if race_key in name_data:
            # Use "Any" gender for NPC gen default
            name_data_result = _generate_minotaur_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Given + Descriptor
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Bugbear":
        race_key = "bugbear"
        if race_key in name_data:
            # Bugbear names are unisex
            name_data_result = _generate_bugbear_name_data(name_data[race_key])
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Given + Epithet
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Harengon":
        race_key = "harengon"
        if race_key in name_data:
            # Harengon names are unisex
            name_data_result = _generate_harengon_name_data(name_data[race_key])
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Given + Family name
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Leonin":
        race_key = "leonin"
        if race_key in name_data:
            # Use "Any" gender for NPC gen default
            name_data_result = _generate_leonin_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Given + Pride Name
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Loxodon":
        race_key = "loxodon"
        if race_key in name_data:
            # Use "Any" gender for NPC gen default
            name_data_result = _generate_loxodon_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Given + Herd Name
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Aasimar":
        race_key = "aasimar"
        if race_key in name_data:
            # Aasimar names are unisex
            name_data_result = _generate_aasimar_name_data(name_data[race_key])
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Base + Optional Title
            else:
                npc_name = f"[{race_name} Name Error] {race_name}"
        else:
           npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Shifter":
        if shifter_names: # Check if the list was loaded
             name_entry = random.choice(shifter_names)
             npc_name = name_entry.get('text', '[Name Error]')
        else:
            npc_name = f"[{race_name} Name Data Missing] {race_name}"

    elif race_name == "Githyanki":
        race_key = "githyanki"
        if race_key in name_data:
            # Use "Any" gender for NPC gen default
            name_data_result = _generate_githyanki_name_data(name_data[race_key], gender="Any")
            if not name_data_result["error"] and name_data_result["name"]:
                npc_name = name_data_result["name"] # Given + Title
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

# === Generate Eladrin Name Function ===
def generate_eladrin_name(): # Unisex
    """Generates an Eladrin name with meanings for the Name Generator tab."""
    race_key = "sylvan" # Use the Sylvan data key
    if race_key not in name_data: return "Error: Sylvan (Eladrin) name data not loaded."

    # Use the standard helper; gender="Any" for unisex names
    data = _generate_structured_name_data(name_data[race_key], gender="Any")

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    poetic_label = "Poetic Meaning:"

    # Use a sparkle or leaf emoji?
    return (
        f"✨ **Name:** {data['name']}\n\n" + # Helper already provides combined name
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Kenku Name Function ===
def generate_kenku_name():
    """Generates a Kenku name for the Name Generator tab."""
    if not kenku_names: # Check if data loaded correctly
        st.error("Kenku name data is missing or empty.")
        return "Error: Missing Kenku data."

    # Select a random name entry
    name_entry = random.choice(kenku_names)
    name_text = name_entry.get('text', '[Name Error]')
    name_meaning = name_entry.get('meaning', 'No description available.')

    # Return a simple formatted string directly
    # Using a black bird emoji
    return (
        f"🐦‍⬛ **Name:** {name_text}\n\n"
        f"*{name_meaning}*" # Add the meaning/description in italics
    )

# === Generate Lizardfolk Name Function ===
def generate_lizardfolk_name():
    """Generates a Lizardfolk name for the Name Generator tab."""
    if not lizardfolk_names: # Check if data loaded correctly
        st.error("Lizardfolk name data is missing or empty.")
        return "Error: Missing Lizardfolk data."

    name_entry = random.choice(lizardfolk_names)
    name_text = name_entry.get('text', '[Name Error]')
    name_meaning = name_entry.get('meaning', 'No description available.')

    # Using a lizard emoji
    return (
        f"🦎 **Name:** {name_text}\n\n"
        f"*{name_meaning}*" # Add the meaning/description in italics
    )

# === Generate Yuan-Ti Name Function ===
def generate_yuan_ti_name():
    """Generates a Yuan-Ti name for the Name Generator tab."""
    if not yuan_ti_names: # Check if data loaded correctly
        st.error("Yuan-Ti name data is missing or empty.")
        return "Error: Missing Yuan-Ti data."

    name_entry = random.choice(yuan_ti_names)
    name_text = name_entry.get('text', '[Name Error]')
    name_meaning = name_entry.get('meaning', 'Derived from Draconic/Ignan roots.') # Simplified meaning

    # Using a snake emoji
    return (
        f"🐍 **Name:** {name_text}\n\n"
        # Optionally add meaning back if desired: f"*{name_meaning}*"
    )

# === Generate Goblin Name Function ===
def generate_goblin_name():
    """Generates a Goblin name for the Name Generator tab."""
    if not goblin_names: # Check if data loaded correctly
        st.error("Goblin name data is missing or empty.")
        return "Error: Missing Goblin data."

    name_entry = random.choice(goblin_names)
    name_text = name_entry.get('text', '[Name Error]')
    name_meaning = name_entry.get('meaning', 'No description available.')

    # Using a goblin emoji
    return (
        f"👺 **Name:** {name_text}\n\n"
        f"*{name_meaning}*" # Add the meaning/description in italics
    )

# === Generate Gnome Name Function ===
def generate_gnome_name(gender="Any"):
    """Generates a Gnome name with meanings for the Name Generator tab."""
    race_key = "gnomish"
    if race_key not in name_data: return "Error: Gnomish name data not loaded."
    # Pass the Gnomish sub-dictionary and gender to the new helper
    data = _generate_gnome_name_data(name_data[race_key], gender)

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include all parts (Given, Clan, Optional Descriptor)
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    # Poetic meaning applies to the whole name construct
    poetic_label = "Poetic Meaning:"

    # Use a mushroom or generic fantasy emoji?
    return (
        f"🍄 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Halfling Name Function ===
def generate_halfling_name(gender="Any"):
    """Generates a Halfling name with meanings for the Name Generator tab."""
    race_key = "halfling"
    if race_key not in name_data: return "Error: Halfling name data not loaded."
    # Pass the Halfling sub-dictionary and gender to the new helper
    data = _generate_halfling_name_data(name_data[race_key], gender)

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include Given + Family parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    poetic_label = "Poetic Meaning:"

    # Use a simple person or maybe home emoji?
    return (
        f"🧑‍🌾 **Name:** {data['name']}\n\n" + # Or 🏠
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Goliath Name Function ===
def generate_goliath_name(): # Unisex
    """Generates a Goliath name with meanings for the Name Generator tab."""
    race_key = "goliath"
    if race_key not in name_data: return "Error: Goliath name data not loaded."
    # Pass the Goliath sub-dictionary to the helper
    data = _generate_goliath_name_data(name_data[race_key])

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    poetic_label = "Poetic Meaning:"

    # Use a mountain or stone emoji?
    return (
        f"🗿 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Minotaur Name Function ===
def generate_minotaur_name(gender="Any"):
    """Generates a Minotaur name with meanings for the Name Generator tab."""
    race_key = "minotaur"
    if race_key not in name_data: return "Error: Minotaur name data not loaded."
    # Pass the Minotaur sub-dictionary and gender to the helper
    data = _generate_minotaur_name_data(name_data[race_key], gender)

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    poetic_label = "Poetic Meaning:"

    # Use a bull emoji?
    return (
        f"🐂 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Bugbear Name Function ===
def generate_bugbear_name(): # Unisex
    """Generates a Bugbear name with meanings for the Name Generator tab."""
    race_key = "bugbear"
    if race_key not in name_data: return "Error: Bugbear name data not loaded."
    # Pass the Bugbear sub-dictionary to the new helper
    data = _generate_bugbear_name_data(name_data[race_key])

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include Given + Epithet parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    poetic_label = "Poetic Meaning:"

    # Use a bear emoji?
    return (
        f"🐻 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Harengon Name Function ===
def generate_harengon_name(): # Unisex
    """Generates a Harengon name with meanings for the Name Generator tab."""
    race_key = "harengon"
    if race_key not in name_data: return "Error: Harengon name data not loaded."
    # Pass the Harengon sub-dictionary to the new helper
    data = _generate_harengon_name_data(name_data[race_key])

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include Given + Family parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    poetic_label = "Poetic Meaning:"

    # Use a rabbit emoji?
    return (
        f"🐇 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Leonin Name Function ===
def generate_leonin_name(gender="Any"):
    """Generates a Leonin name with meanings for the Name Generator tab."""
    race_key = "leonin"
    if race_key not in name_data: return "Error: Leonin name data not loaded."
    # Pass the Leonin sub-dictionary and gender to the new helper
    data = _generate_leonin_name_data(name_data[race_key], gender)

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include Given + Pride Name parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    poetic_label = "Poetic Meaning:"

    # Use a lion emoji
    return (
        f"🦁 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Loxodon Name Function ===
def generate_loxodon_name(gender="Any"):
    """Generates a Loxodon name with meanings for the Name Generator tab."""
    race_key = "loxodon"
    if race_key not in name_data: return "Error: Loxodon name data not loaded."
    # Pass the Loxodon sub-dictionary and gender to the new helper
    data = _generate_loxodon_name_data(name_data[race_key], gender)

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include Given + Herd Name parts
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    poetic_label = "Poetic Meaning:"

    # Use an elephant emoji
    return (
        f"🐘 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Aasimar Name Function ===
def generate_aasimar_name(): # Unisex
    """Generates an Aasimar name with meanings for the Name Generator tab."""
    race_key = "aasimar"
    if race_key not in name_data: return "Error: Aasimar name data not loaded."
    # Pass the Aasimar sub-dictionary to the new helper
    data = _generate_aasimar_name_data(name_data[race_key])

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # Meaning lines include base parts + optional title
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]

    poetic_label = "Poetic Meaning:"

    # Use an angel or sparkle emoji?
    return (
        f"😇 **Name:** {data['name']}\n\n" +
        "\n".join(meaning_lines) +
        f"\n\n➔ **{poetic_label}** {data['poetic']}"
    )

# === Generate Shifter Name Function ===
def generate_shifter_name():
    """Generates a Shifter name for the Name Generator tab."""
    if not shifter_names: # Check if data loaded correctly
        st.error("Shifter name data is missing or empty.")
        return "Error: Missing Shifter data."

    name_entry = random.choice(shifter_names)
    name_text = name_entry.get('text', '[Name Error]')
    name_meaning = name_entry.get('meaning', 'No description available.')

    # Using a wolf emoji?
    return (
        f"🐺 **Name:** {name_text}\n\n"
        f"*{name_meaning}*" # Add the meaning/description in italics
    )

# === (Revised) Generate Githyanki Name Function ===
def generate_githyanki_name(gender="Any"):
    """Generates a Githyanki name with meanings for the Name Generator tab."""
    race_key = "githyanki"
    if race_key not in name_data: return "Error: Githyanki name data not loaded."
    # Pass the Githyanki sub-dictionary and gender to the new helper
    data = _generate_githyanki_name_data(name_data[race_key], gender)

    if data["error"]: return f"Error: {data['error']}"
    if not data["name"]: return "Error: Name generation failed silently."

    # --- FIX: Explicitly build the output string components ---
    name_line = f"⚔️ **Name:** {data['name']}"
    # Create the block of meaning lines
    meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
    meanings_block = "\n".join(meaning_lines)
    # Determine the poetic label
    poetic_label = "Poetic Meaning:" # Githyanki names are Given + Title, so poetic meaning applies to both parts together

    poetic_line = f"➔ **{poetic_label}** {data['poetic']}"

    # Combine components with double newlines for spacing
    return f"{name_line}\n\n{meanings_block}\n\n{poetic_line}"

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
    race_options = ["Elf", "Eladrin", "Tabaxi", "Human", "Halfling", "Orc",
                    "Tiefling", "Drow", "Dragonborn", "Aarakocra", "Owlin",
                    "Tortle", "Triton", "Genasi", "Kenku", "Lizardfolk",
                    "Yuan-Ti", "Goblin", "Bugbear", "Gnome", "Goliath",
                    "Minotaur", "Harengon", "Leonin", "Loxodon",
                    "Aasimar", "Shifter", "Githyanki"]
    race = st.selectbox(
        "Choose a race:",
        race_options,
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

    elif race == "Halfling":
        # Gender selection needed for Halfling
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="halfling_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Halfling Name", key="halfling_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_halfling_name(gender=gender)

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

    elif race == "Kenku":
        # NO gender selection needed
        if st.button("Generate Kenku Name", key="kenku_name_button"):
             # The function returns the fully formatted string
             st.session_state.name_output = generate_kenku_name()

    elif race == "Lizardfolk":
        # NO gender selection needed
        if st.button("Generate Lizardfolk Name", key="lizardfolk_name_button"):
             st.session_state.name_output = generate_lizardfolk_name()

    elif race == "Yuan-Ti":
        # NO gender selection needed
        if st.button("Generate Yuan-Ti Name", key="yuan_ti_name_button"):
             st.session_state.name_output = generate_yuan_ti_name()

    elif race == "Goblin":
        # NO gender selection needed
        if st.button("Generate Goblin Name", key="goblin_name_button"):
             st.session_state.name_output = generate_goblin_name()

    elif race == "Bugbear":
        # NO gender selection needed
        if st.button("Generate Bugbear Name", key="bugbear_name_button"):
             st.session_state.name_output = generate_bugbear_name()

    elif race == "Gnome":
        # Gender selection needed for Gnome
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="gnome_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Gnome Name", key="gnome_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_gnome_name(gender=gender)

    elif race == "Harengon":
        # NO gender selection needed
        if st.button("Generate Harengon Name", key="harengon_name_button"):
             st.session_state.name_output = generate_harengon_name()

    elif race == "Leonin":
        # Gender selection needed for Leonin
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="leonin_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Leonin Name", key="leonin_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_leonin_name(gender=gender)

    elif race == "Loxodon":
        # Gender selection needed for Loxodon
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="loxodon_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Loxodon Name", key="loxodon_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_loxodon_name(gender=gender)

    elif race == "Githyanki":
        # Gender selection needed for Githyanki
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="githyanki_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Githyanki Name", key="githyanki_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_githyanki_name(gender=gender)

    elif race == "Aasimar":
        # NO gender selection needed
        if st.button("Generate Aasimar Name", key="aasimar_name_button"):
             st.session_state.name_output = generate_aasimar_name()

    elif race == "Shifter":
        # NO gender selection needed
        if st.button("Generate Shifter Name", key="shifter_name_button"):
             st.session_state.name_output = generate_shifter_name()

    elif race == "Eladrin":
        # NO gender selection needed
        if st.button("Generate Eladrin Name", key="eladrin_name_button"):
             st.session_state.name_output = generate_eladrin_name()

    elif race == "Goliath":
        # NO gender selection needed
        if st.button("Generate Goliath Name", key="goliath_name_button"):
             st.session_state.name_output = generate_goliath_name()

    elif race == "Minotaur":
        # Gender selection needed for Minotaur
        gender = st.radio(
            "Select Gender:", ["Any", "Male", "Female"],
            key="minotaur_gender_radio", # Use unique key
            horizontal=True
        )
        if st.button("Generate Minotaur Name", key="minotaur_name_button"):
             # Pass the selected gender
             st.session_state.name_output = generate_minotaur_name(gender=gender)

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