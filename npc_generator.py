import random
import streamlit as st
import re # Import regular expressions for parsing

# Import necessary data
# Import TOP-LEVEL generator functions ONLY
from data_loader import races, npc_attributes, icons, name_data # name_data needed for Tabaxi clan lookup
from name_generators import (
    generate_elven_name, generate_orc_name, generate_infernal_name,
    generate_tabaxi_name, generate_drow_name, generate_dragonborn_name,
    generate_aarakocra_name, generate_owlin_name, generate_tortle_name,
    generate_triton_name, generate_fire_genasi_name, generate_earth_genasi_name,
    generate_air_genasi_name, generate_water_genasi_name, generate_eladrin_name,
    generate_kenku_name, generate_lizardfolk_name, generate_yuan_ti_name,
    generate_goblin_name, generate_gnome_name, generate_halfling_name,
    generate_goliath_name, generate_minotaur_name, generate_bugbear_name,
    generate_harengon_name, generate_leonin_name, generate_loxodon_name,
    generate_aasimar_name, generate_shifter_name, generate_githyanki_name,
    generate_common_name # Keep this for Human, Half-Elf, Half-Orc common style
)

# --- Helper function to parse name from Markdown ---
def _parse_name_from_markdown(markdown_string, race_name_for_error="Unknown"):
    """Extracts the name after ':** ' from the markdown string."""
    if not isinstance(markdown_string, str) or "Error:" in markdown_string:
        return f"[{race_name_for_error} Name Error]" # Return error if input is bad

    # Regex to find ': ** ' followed by the name until the end of the line or newline
    # Handles potential variations in emoji/bolding
    match = re.search(r":\s*\**\s*(.*?)\s*(\\n|\n|$)", markdown_string)
    if match:
        return match.group(1).strip()
    else:
        # Fallback if regex fails (maybe log this)
        st.warning(f"Could not parse name using regex from: {markdown_string}")
        # Simple split as fallback, might be fragile
        parts = markdown_string.split(":**")
        if len(parts) > 1:
             return parts[1].split("\\n")[0].strip()
        return f"[{race_name_for_error} Parse Error]"


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

    # --- Generate Name based on Race using Top-Level Functions ---
    try:
        name_markdown = "" # Store the markdown output from generator functions

        # Create a mapping similar to the UI, but simpler for NPC gen
        # We only need the function, and maybe gender arg if applicable
        # Note: 'Any' gender is often the default in the functions themselves now
        NPC_NAME_FUNC_MAP = {
            "Elf": generate_elven_name,
            "Eladrin": generate_eladrin_name,
            "Tabaxi": generate_tabaxi_name, # Requires special handling for clan
            "Human": generate_common_name,
            "Halfling": generate_halfling_name,
            "Orc": generate_orc_name,
            "Tiefling": generate_infernal_name,
            "Drow": generate_drow_name,
            "Dragonborn": generate_dragonborn_name,
            "Aarakocra": generate_aarakocra_name,
            "Owlin": generate_owlin_name,
            "Tortle": generate_tortle_name,
            "Triton": generate_triton_name,
            # Genasi needs special handling
            "Kenku": generate_kenku_name,
            "Lizardfolk": generate_lizardfolk_name,
            "Yuan-ti": generate_yuan_ti_name,
            "Goblin": generate_goblin_name,
            "Bugbear": generate_bugbear_name,
            "Gnome": generate_gnome_name,
            "Goliath": generate_goliath_name,
            "Minotaur": generate_minotaur_name,
            "Harengon": generate_harengon_name,
            "Leonin": generate_leonin_name,
            "Loxodon": generate_loxodon_name,
            "Aasimar": generate_aasimar_name,
            "Shifter": generate_shifter_name,
            "Githyanki": generate_githyanki_name,
        }

        # Handle races requiring gender choice (can set npc_gender if needed later)
        races_needing_gender = ["Human", "Halfling", "Orc", "Tiefling", "Drow",
                                "Aarakocra", "Tortle", "Gnome", "Minotaur",
                                "Leonin", "Loxodon", "Githyanki"]

        if race_name == "Half-Elf":
            chosen_style = random.choice(["Elven", "Common"])
            if chosen_style == "Elven":
                name_markdown = generate_elven_name() # gender="Any" is default
            else:
                name_markdown = generate_common_name(gender=npc_gender)
        elif race_name == "Half-Orc":
            chosen_style = random.choice(["Orc", "Common"])
            if chosen_style == "Orc":
                name_markdown = generate_orc_name(gender=npc_gender)
            else:
                name_markdown = generate_common_name(gender=npc_gender)
        elif race_name == "Fire Genasi": name_markdown = generate_fire_genasi_name()
        elif race_name == "Earth Genasi": name_markdown = generate_earth_genasi_name()
        elif race_name == "Air Genasi": name_markdown = generate_air_genasi_name()
        elif race_name == "Water Genasi": name_markdown = generate_water_genasi_name()
        elif race_name == "Tabaxi":
             # Need to pick a random clan for NPC gen
             tabaxi_data = name_data.get("tabaxi", {})
             clan_list = tabaxi_data.get("clans", [])
             if clan_list and isinstance(clan_list, list):
                  valid_clans = [c for c in clan_list if isinstance(c, dict) and "name" in c]
                  if valid_clans:
                      selected_clan_info = random.choice(valid_clans)
                      selected_clan_name = selected_clan_info['name']
                      name_markdown = generate_tabaxi_name(selected_clan_name)
                      # Store clan name for output section
                      clan_name = selected_clan_name
                  else: name_markdown = "Error: No valid Tabaxi clans found."
             else: name_markdown = "Error: Tabaxi clan data missing/invalid."
        elif race_name in NPC_NAME_FUNC_MAP:
             generator_func = NPC_NAME_FUNC_MAP[race_name]
             if race_name in races_needing_gender:
                  name_markdown = generator_func(gender=npc_gender)
             else:
                  name_markdown = generator_func() # Call without gender
        else:
             # Fallback for races not explicitly handled
             st.warning(f"No specific name generator mapped for {race_name} in NPC gen. Trying Common.")
             name_markdown = generate_common_name(gender=npc_gender)

        # --- Parse the name from the markdown ---
        npc_name = _parse_name_from_markdown(name_markdown, race_name)
        # Special case: If Tabaxi name includes clan, remove it for the npc_name variable
        if race_name == "Tabaxi" and " of the " in npc_name:
            npc_name = npc_name.split(" of the ")[0]


    except Exception as e:
         # Catch any unexpected error during name generation phase
         st.error(f"Unexpected error generating name for {race_name}: {e}")
         # Ensure npc_name has a fallback value even after error
         if npc_name.startswith("Unnamed"): # Only overwrite if it's still the default
             npc_name = f"[{race_name} Name Error]"


    # --- Assemble NPC Output ---
    npc_lines = [f"👤 **Name:** {npc_name}"] # Use the parsed name

    # Add Clan details if applicable (using clan_name variable set during Tabaxi generation)
    if race_name == "Tabaxi" and clan_name:
         npc_lines.append(f"🏡 **Clan:** {clan_name}")

    # Basic Info (remains the same)
    npc_lines.extend([
        "---", "💼 **Basic Info**",
        f"🧬 **Race:** {race_name} ({race_data.get('rarity', 'N/A')})",
        f"🌍 **Region:** {race_data.get('region', 'N/A')}",
        f"📖 **Lore:** {race_data.get('description', 'N/A')}",
        "✶" * 25, "🎭 **Personality & Story**"
    ])

    # Attributes (remains the same)
    if isinstance(npc_attributes, dict):
        # Shuffle categories for variety if desired
        categories = list(npc_attributes.keys())
        random.shuffle(categories)
        for category in categories:
            options = npc_attributes[category]
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