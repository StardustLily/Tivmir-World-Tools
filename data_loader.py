import streamlit as st
import json
import os

# === Load Data Functions ===
@st.cache_data # Caches JSON files
def load_json(filename):
    """Loads a JSON file from the 'data' subdirectory."""
    try:
        path = os.path.join("data", filename)
        # Ensure the path uses forward slashes for compatibility, though os.path.join should handle it
        path = path.replace("\\", "/")
        st.info(f"Attempting to load: {path}") # Debugging print
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        st.info(f"Successfully loaded: {filename}") # Debugging print
        return data
    except FileNotFoundError:
        st.error(f"Error loading {filename}: File not found at {path}")
        return [] if "names" in filename or "clans" in filename or "given" in filename or "family" in filename or "personal" in filename else {} # More robust default based on expected type
    except json.JSONDecodeError:
        st.error(f"Error loading {filename}: File is not valid JSON.")
        return [] if "names" in filename or "clans" in filename or "given" in filename or "family" in filename or "personal" in filename else {}
    except Exception as e:
        st.error(f"An unexpected error occurred loading {filename}: {e}")
        return [] if "names" in filename or "clans" in filename or "given" in filename or "family" in filename or "personal" in filename else {}

# === Load Base Data ===
races = load_json("races.json")
npc_attributes = load_json("npc_attributes.json")

# === Load Calendar Data ===  # ADD THIS SECTION
calendar_data = load_json("tivmir_calendar.json")
if not calendar_data or "months" not in calendar_data:
     st.error("Failed to load valid calendar data! Tracker will not work.")
     calendar_data = {"months": [], "year_suffix": "ERR"}

# === Load Single Name Lists ===
kenku_names = load_json("kenku_names.json")
lizardfolk_names = load_json("lizardfolk_names.json")
yuan_ti_names = load_json("yuan-ti_names.json")
goblin_names = load_json("goblin_names.json")
shifter_names = load_json("shifter_names.json")

# === Load Shared Gloss Files ===
# Note: Ensure these files exist and are valid JSON
auran_gloss = load_json("auran_poetic_gloss.json")
aquan_gloss = load_json("aquan_poetic_gloss.json")
ignan_gloss = load_json("ignan_poetic_gloss.json")
terran_gloss = load_json("terran_poetic_gloss.json")
sylvan_gloss = load_json("sylvan_poetic_gloss.json")
gnomish_gloss = load_json("gnomish_poetic_gloss.json")
halfling_gloss = load_json("halfling_poetic_gloss.json")
giant_gloss = load_json("giant_poetic_gloss.json")
bugbear_gloss = load_json("bugbear_poetic_gloss.json")
harengon_gloss = load_json("harengon_poetic_gloss.json")
leonin_gloss = load_json("leonin_poetic_gloss.json")
loxodon_gloss = load_json("loxodon_poetic_gloss.json")
aasimar_gloss = load_json("aasimar_poetic_gloss.json")
githyanki_gloss = load_json("githyanki_poetic_gloss.json")
tabaxi_gloss = load_json("tabaxi_poetic_gloss.json") # Added missing gloss loads
elven_gloss = load_json("elven_poetic_gloss.json")
orc_gloss = load_json("orcish_poetic_gloss.json")
infernal_gloss = load_json("infernal_poetic_gloss.json")
drow_gloss = load_json("drow_poetic_gloss.json")
draconic_gloss = load_json("draconic_poetic_gloss.json")


# === Consolidate Structured Name Data ===
# Added checks for gloss files before assigning
name_data = {
    "tabaxi": {
        "prefixes": load_json("tabaxi_prefixes.json"),
        "middles": load_json("tabaxi_middles.json"),
        "suffixes": load_json("tabaxi_suffixes.json"),
        "gloss": tabaxi_gloss if tabaxi_gloss else {}, # Use loaded gloss or empty dict
        "clans": load_json("tabaxi_clans.json")
    },
    "elf": {
        "prefixes": load_json("elven_prefixes.json"),
        "middles": load_json("elven_middles.json"),
        "suffixes": load_json("elven_suffixes.json"),
        "gloss": elven_gloss if elven_gloss else {}
    },
    "common": { # For Human/Common names
        "first_names": load_json("common_first_names.json"),
        "surnames": load_json("common_surnames.json")
        # No gloss needed for common typically
    },
    "orc": {
        "prefixes": load_json("orcish_prefixes.json"),
        "middles": load_json("orcish_middles.json"),
        "suffixes": load_json("orcish_suffixes.json"),
        "gloss": orc_gloss if orc_gloss else {},
        "surnames": load_json("orcish_surnames.json")
    },
    "infernal": { # Using 'infernal' as the key for Tiefling
        "prefixes": load_json("infernal_prefixes.json"),
        "middles": load_json("infernal_middles.json"),
        "suffixes": load_json("infernal_suffixes.json"),
        "gloss": infernal_gloss if infernal_gloss else {},
        "surnames": load_json("infernal_surnames.json")
    },
    "drow": {
        "prefixes": load_json("drow_prefixes.json"),
        "middles": load_json("drow_middles.json"),
        "suffixes": load_json("drow_suffixes.json"),
        "gloss": drow_gloss if drow_gloss else {},
        "surnames": load_json("drow_surnames.json")
    },
    "draconic": { # Dragonborn
        "clans": load_json("draconic_clans.json"),
        "prefixes": load_json("draconic_prefixes.json"),
        "middles": load_json("draconic_middles.json"),
        "suffixes": load_json("draconic_suffixes.json"),
        "gloss": draconic_gloss if draconic_gloss else {}
    },
    "aarakocra": {
        "lineages": load_json("aarakocra_lineages.json"),
        "prefixes": load_json("aarakocra_prefixes.json"),
        "middles": load_json("aarakocra_middles.json"),
        "suffixes": load_json("aarakocra_suffixes.json"),
        "gloss": auran_gloss if auran_gloss else {}
    },
    "owlin": {
        "personal": load_json("owlin_personal.json"),
        "descriptors": load_json("owlin_descriptors.json"),
        "gloss": auran_gloss if auran_gloss else {}
    },
    "tortle": {
        "given": load_json("tortle_given.json"),
        "descriptors": load_json("tortle_descriptors.json"),
        "gloss": aquan_gloss if aquan_gloss else {}
    },
    "triton": {
        "given": load_json("triton_given.json"),
        "markers": load_json("triton_markers.json"),
        "gloss": aquan_gloss if aquan_gloss else {}
    },
    "ignan": { # Fire Genasi
        "prefixes": load_json("ignan_prefixes.json"),
        "middles": load_json("ignan_middles.json"),
        "suffixes": load_json("ignan_suffixes.json"),
        "gloss": ignan_gloss if ignan_gloss else {}
    },
    "terran": { # Earth Genasi
        "prefixes": load_json("terran_prefixes.json"),
        "middles": load_json("terran_middles.json"),
        "suffixes": load_json("terran_suffixes.json"),
        "gloss": terran_gloss if terran_gloss else {}
    },
    "air_genasi": {
        "prefixes": load_json("air_genasi_prefixes.json"),
        "middles": load_json("air_genasi_middles.json"),
        "suffixes": load_json("air_genasi_suffixes.json"),
        "gloss": auran_gloss if auran_gloss else {}
    },
    "water_genasi": {
        "prefixes": load_json("water_genasi_prefixes.json"),
        "middles": load_json("water_genasi_middles.json"),
        "suffixes": load_json("water_genasi_suffixes.json"),
        "gloss": aquan_gloss if aquan_gloss else {}
    },
    "sylvan": { # Eladrin
        "prefixes": load_json("sylvan_prefixes.json"),
        "middles": load_json("sylvan_middles.json"),
        "suffixes": load_json("sylvan_suffixes.json"),
        "gloss": sylvan_gloss if sylvan_gloss else {}
    },
    "gnomish": {
        "male_first": load_json("gnome_male_first.json"),
        "female_first": load_json("gnome_female_first.json"),
        "clans": load_json("gnome_clans.json"),
        "descriptors": load_json("gnome_descriptors.json"),
        "gloss": gnomish_gloss if gnomish_gloss else {}
    },
    "halfling": {
        "male_first": load_json("halfling_male_first.json"),
        "female_first": load_json("halfling_female_first.json"),
        "family": load_json("halfling_family.json"),
        "gloss": halfling_gloss if halfling_gloss else {}
    },
    "goliath": {
        "given": load_json("goliath_given.json"),
        "titles": load_json("goliath_titles.json"),
        "gloss": giant_gloss if giant_gloss else {}
    },
    "minotaur": {
        "male_first": load_json("minotaur_male_first.json"),
        "female_first": load_json("minotaur_female_first.json"),
        "descriptors": load_json("minotaur_descriptors.json"),
        "gloss": giant_gloss if giant_gloss else {}
    },
    "bugbear": {
        "given": load_json("bugbear_given.json"),
        "epithets": load_json("bugbear_epithets.json"),
        "gloss": bugbear_gloss if bugbear_gloss else {}
    },
    "harengon": {
        "given": load_json("harengon_given.json"),
        "family": load_json("harengon_family.json"),
        "gloss": harengon_gloss if harengon_gloss else {}
    },
    "leonin": {
        "male_first": load_json("leonin_male_first.json"),
        "female_first": load_json("leonin_female_first.json"),
        "pridenames": load_json("leonin_pridenames.json"),
        "gloss": leonin_gloss if leonin_gloss else {}
    },
    "loxodon": {
        "male_first": load_json("loxodon_male_first.json"),
        "female_first": load_json("loxodon_female_first.json"),
        "herdnames": load_json("loxodon_herdnames.json"),
        "gloss": loxodon_gloss if loxodon_gloss else {}
    },
    "aasimar": {
        "prefixes": load_json("aasimar_base_prefixes.json"),
        "middles": load_json("aasimar_base_middles.json"),
        "suffixes": load_json("aasimar_base_suffixes.json"),
        "titles": load_json("aasimar_celestial_titles.json"),
        "gloss": aasimar_gloss if aasimar_gloss else {}
    },
    "githyanki": {
        "male_first": load_json("githyanki_male_first.json"),
        "female_first": load_json("githyanki_female_first.json"),
        "titles": load_json("githyanki_titles.json"),
        "gloss": githyanki_gloss if githyanki_gloss else {}
    }
}


# Emoji Icons
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