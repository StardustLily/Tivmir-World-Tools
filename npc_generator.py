import random
import streamlit as st
# Import necessary data and generator functions
from data_loader import races, npc_attributes, name_data, icons, kenku_names, lizardfolk_names, yuan_ti_names, goblin_names, shifter_names
# Import the specific helper functions needed by generate_npc
# Note: It's generally cleaner if generate_npc calls the main generate_X_name wrappers,
# but based on current structure, it calls helpers directly. Let's keep that for now.
# If refactoring further (Step 2), we'd change this.
from name_generators import (
    _generate_structured_name_data, _get_common_name_string,
    _generate_dragonborn_name_data, _generate_aarakocra_name_data,
    _generate_owlin_name_data, _generate_tortle_name_data,
    _generate_triton_name_data, _generate_gnome_name_data,
    _generate_halfling_name_data, _generate_goliath_name_data,
    _generate_minotaur_name_data, _generate_bugbear_name_data,
    _generate_harengon_name_data, _generate_leonin_name_data,
    _generate_loxodon_name_data, _generate_aasimar_name_data,
    _generate_githyanki_name_data
)


def generate_npc():
    """Generates a full NPC description string."""
    if not races or not isinstance(races, list):
        st.error("Race data is missing or invalid.")
        return "Error: Missing race data."
    if not npc_attributes or not isinstance(npc_attributes, dict):
        st.error("NPC attributes data is missing or invalid.")
        return "Error: Missing attribute data."

    # --- Select Race ---
    try:
        race_data = random.choice(races)
        if not isinstance(race_data, dict) or 'name' not in race_data:
             st.error("Invalid race entry selected."); return "Error: Invalid race data format."
        race_name = race_data['name']
    except IndexError:
         st.error("Races list is empty."); return "Error: No races available."
    except Exception as e:
         st.error(f"Error selecting race: {e}"); return "Error during race selection."


    npc_name = f"Unnamed {race_name}" # Default placeholder
    clan_name = None # Initialize clan_name
    npc_gender = "Any" # Default gender for NPC gen

    # --- Generate Name based on Race ---
    name_data_result = None # To store results from helpers
    try:
        # --- Handle name generation based on race_name ---
        if race_name == "Elf":
            race_key = "elf"
            if race_key in name_data: name_data_result = _generate_structured_name_data(name_data[race_key], npc_gender)
            else: npc_name = f"[{race_name} Name Data Missing] {race_name}"
        elif race_name == "Tabaxi":
            race_key = "tabaxi"
            if race_key in name_data:
                name_data_result = _generate_structured_name_data(name_data[race_key], npc_gender)
                if name_data_result and not name_data_result["error"]:
                     npc_first_name = name_data_result["name"]
                     clan_list = name_data[race_key].get("clans", [])
                     if clan_list: clan_entry = random.choice(clan_list); clan_name = clan_entry['name']; npc_name = f"{npc_first_name} of the {clan_name} Clan"
                     else: npc_name = f"{npc_first_name} [Clan Data Missing]"; clan_name = "[Clan Data Missing]"
                else: npc_name = f"[{race_name} Name Error] {race_name}" # Error from helper
            else: npc_name = f"[{race_name} Name Data Missing] {race_name}"
            # Skip setting npc_name directly from name_data_result here as it's handled above
            name_data_result = None # Prevent reprocessing below
        elif race_name == "Human":
            npc_name = _get_common_name_string(gender_filter=npc_gender)
        elif race_name == "Half-Elf":
            chosen_style = random.choice(["Elven", "Common"])
            if chosen_style == "Elven":
                race_key = "elf"
                if race_key in name_data: name_data_result = _generate_structured_name_data(name_data[race_key], npc_gender)
                else: npc_name = f"[Elven Name Data Missing] Half-Elf"
            else: npc_name = _get_common_name_string(gender_filter=npc_gender)
        elif race_name == "Orc":
             race_key = "orc"; name_data_result = _generate_structured_name_data(name_data.get(race_key, {}), npc_gender)
        elif race_name == "Half-Orc":
             chosen_style = random.choice(["Orc", "Common"])
             if chosen_style == "Orc":
                 race_key = "orc"; name_data_result = _generate_structured_name_data(name_data.get(race_key, {}), npc_gender)
             else: npc_name = _get_common_name_string(gender_filter=npc_gender)
        elif race_name == "Tiefling":
              race_key = "infernal"; name_data_result = _generate_structured_name_data(name_data.get(race_key, {}), npc_gender)
        elif race_name == "Drow":
              race_key = "drow"; name_data_result = _generate_structured_name_data(name_data.get(race_key, {}), npc_gender)
        elif race_name == "Dragonborn":
              race_key = "draconic"; name_data_result = _generate_dragonborn_name_data(name_data.get(race_key, {}))
        elif race_name == "Aarakocra":
              race_key = "aarakocra"; name_data_result = _generate_aarakocra_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Owlin":
              race_key = "owlin"; name_data_result = _generate_owlin_name_data(name_data.get(race_key, {}))
        elif race_name == "Tortle":
              race_key = "tortle"; name_data_result = _generate_tortle_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Triton":
              race_key = "triton"; name_data_result = _generate_triton_name_data(name_data.get(race_key, {}))
        elif race_name == "Fire Genasi":
              race_key = "ignan"; name_data_result = _generate_structured_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Earth Genasi":
              race_key = "terran"; name_data_result = _generate_structured_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Air Genasi":
              race_key = "air_genasi"; name_data_result = _generate_structured_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Water Genasi":
              race_key = "water_genasi"; name_data_result = _generate_structured_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Eladrin":
              race_key = "sylvan"; name_data_result = _generate_structured_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Kenku":
              if kenku_names: name_entry = random.choice(kenku_names); npc_name = name_entry.get('text', '[Name Error]')
              else: npc_name = f"[{race_name} Name Data Missing] {race_name}"
        elif race_name == "Lizardfolk":
              if lizardfolk_names: name_entry = random.choice(lizardfolk_names); npc_name = name_entry.get('text', '[Name Error]')
              else: npc_name = f"[{race_name} Name Data Missing] {race_name}"
        elif race_name == "Yuan-Ti":
              if yuan_ti_names: name_entry = random.choice(yuan_ti_names); npc_name = name_entry.get('text', '[Name Error]')
              else: npc_name = f"[{race_name} Name Data Missing] {race_name}"
        elif race_name == "Goblin":
              if goblin_names: name_entry = random.choice(goblin_names); npc_name = name_entry.get('text', '[Name Error]')
              else: npc_name = f"[{race_name} Name Data Missing] {race_name}"
        elif race_name == "Gnome":
               race_key = "gnomish"; name_data_result = _generate_gnome_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Halfling":
               race_key = "halfling"; name_data_result = _generate_halfling_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Goliath":
               race_key = "goliath"; name_data_result = _generate_goliath_name_data(name_data.get(race_key, {}))
        elif race_name == "Minotaur":
               race_key = "minotaur"; name_data_result = _generate_minotaur_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Bugbear":
               race_key = "bugbear"; name_data_result = _generate_bugbear_name_data(name_data.get(race_key, {}))
        elif race_name == "Harengon":
               race_key = "harengon"; name_data_result = _generate_harengon_name_data(name_data.get(race_key, {}))
        elif race_name == "Leonin":
               race_key = "leonin"; name_data_result = _generate_leonin_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Loxodon":
               race_key = "loxodon"; name_data_result = _generate_loxodon_name_data(name_data.get(race_key, {}), gender="Any")
        elif race_name == "Aasimar":
               race_key = "aasimar"; name_data_result = _generate_aasimar_name_data(name_data.get(race_key, {}))
        elif race_name == "Shifter":
               if shifter_names: name_entry = random.choice(shifter_names); npc_name = name_entry.get('text', '[Name Error]')
               else: npc_name = f"[{race_name} Name Data Missing] {race_name}"
        elif race_name == "Githyanki":
                race_key = "githyanki"; name_data_result = _generate_githyanki_name_data(name_data.get(race_key, {}), gender="Any")
        # --- ADD more races here ---
        else:
             # Fallback for races not explicitly handled by specific generators
             st.warning(f"No specific name generator found for {race_name}. Using default.")
             # Optionally try a common name as a fallback?
             # npc_name = _get_common_name_string(gender_filter=npc_gender)


        # Process result if a helper function was called
        if name_data_result:
            if not name_data_result.get("error") and name_data_result.get("name"):
                npc_name = name_data_result["name"]
            else:
                # Construct more specific error message if helper failed
                error_detail = name_data_result.get("error", "Unknown error")
                npc_name = f"[{race_name} Name Error: {error_detail}] {race_name}"

    except Exception as e:
         # Catch any unexpected error during name generation phase
         st.error(f"Unexpected error generating name for {race_name}: {e}")
         npc_name = f"[{race_name} Name Error] {race_name}" # Fallback name


    # --- Assemble NPC Output ---
    npc_lines = [f"👤 **Name:** {npc_name}"]

    # Add Clan details if applicable
    if race_name == "Tabaxi" and clan_name and clan_name != "[Clan Data Missing]":
         npc_lines.append(f"🏡 **Clan:** {clan_name}")

    # Basic Info
    npc_lines.extend([
        "---", "💼 **Basic Info**",
        f"🧬 **Race:** {race_name} ({race_data.get('rarity', 'N/A')})",
        f"🌍 **Region:** {race_data.get('region', 'N/A')}",
        f"📖 **Lore:** {race_data.get('description', 'N/A')}",
        "✶" * 25, "🎭 **Personality & Story**"
    ])

    # Attributes
    if isinstance(npc_attributes, dict):
        for category, options in npc_attributes.items():
            if not options or not isinstance(options, list): continue
            try:
                clean_category = category.strip()
                icon = icons.get(clean_category, "•")
                choice = random.choice(options)
                npc_lines.append(f"{icon} **{clean_category}:** {choice}")
            except IndexError:
                 st.warning(f"Attribute list for '{category}' is empty.")
            except Exception as e:
                 st.error(f"Error processing attribute '{category}': {e}")
    else:
         st.warning("NPC attributes data is not in the expected dictionary format.")


    return "\n\n".join(npc_lines)