import streamlit as st
import os
st.set_page_config(page_title="Tivmir World Tools", layout="centered")
# Import necessary data and TOP-LEVEL generator functions
from data_loader import name_data, races, calendar_data, npc_attributes, icons, deities
from npc_generator import generate_npc
# --- ADD Calendar Imports ---
from calendar_tracker import (
    initialize_calendar_state,
    get_current_date_string,
    advance_day,
    advance_week,
    advance_month
)
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
    generate_common_name # Used for Human
)

# --- Define the Name Generator Map ---
# Maps Race Name -> { func: generator_function, needs_gender: bool, needs_clan: bool, needs_element: bool }
# Use generate_common_name for Human
# Use None for func if special handling is needed (like Genasi composite)
NAME_GENERATOR_MAP = {
    "Elf": {"func": generate_elven_name, "needs_gender": False},
    "Eladrin": {"func": generate_eladrin_name, "needs_gender": False},
    "Tabaxi": {"func": generate_tabaxi_name, "needs_gender": False, "needs_clan": True},
    "Human": {"func": generate_common_name, "needs_gender": True},
    "Halfling": {"func": generate_halfling_name, "needs_gender": True},
    "Orc": {"func": generate_orc_name, "needs_gender": True},
    "Tiefling": {"func": generate_infernal_name, "needs_gender": True},
    "Drow": {"func": generate_drow_name, "needs_gender": True},
    "Dragonborn": {"func": generate_dragonborn_name, "needs_gender": False},
    "Aarakocra": {"func": generate_aarakocra_name, "needs_gender": True},
    "Owlin": {"func": generate_owlin_name, "needs_gender": False},
    "Tortle": {"func": generate_tortle_name, "needs_gender": True},
    "Triton": {"func": generate_triton_name, "needs_gender": False},
    "Genasi": {"func": None, "needs_gender": False, "needs_element": True}, # Special case
    "Kenku": {"func": generate_kenku_name, "needs_gender": False},
    "Lizardfolk": {"func": generate_lizardfolk_name, "needs_gender": False},
    "Yuan-Ti": {"func": generate_yuan_ti_name, "needs_gender": False},
    "Goblin": {"func": generate_goblin_name, "needs_gender": False},
    "Bugbear": {"func": generate_bugbear_name, "needs_gender": False},
    "Gnome": {"func": generate_gnome_name, "needs_gender": True},
    "Goliath": {"func": generate_goliath_name, "needs_gender": False},
    "Minotaur": {"func": generate_minotaur_name, "needs_gender": True},
    "Harengon": {"func": generate_harengon_name, "needs_gender": False},
    "Leonin": {"func": generate_leonin_name, "needs_gender": True},
    "Loxodon": {"func": generate_loxodon_name, "needs_gender": True},
    "Aasimar": {"func": generate_aasimar_name, "needs_gender": False},
    "Shifter": {"func": generate_shifter_name, "needs_gender": False},
    "Githyanki": {"func": generate_githyanki_name, "needs_gender": True},
}

# === Pre-process Races for UI ===
# Group races by rarity and sort alphabetically
RACES_BY_RARITY = {
    "Common": [],
    "Uncommon": [],
    "Rare": [],
    "Very Rare": []
}
ALL_RACE_NAMES_SORTED = []

if races and isinstance(races, list):
    all_names = []
    for race_info in races:
        if isinstance(race_info, dict) and "name" in race_info and "rarity" in race_info:
            name = race_info["name"]
            rarity = race_info["rarity"]
            if rarity in RACES_BY_RARITY:
                RACES_BY_RARITY[rarity].append(name)
            else:
                st.warning(f"Race '{name}' has unknown rarity '{rarity}'.") # Handle unexpected rarity
            all_names.append(name)
        else:
            st.warning(f"Skipping invalid race entry in races.json: {race_info}")

    # Sort lists alphabetically
    for rarity_key in RACES_BY_RARITY:
        RACES_BY_RARITY[rarity_key].sort()
    ALL_RACE_NAMES_SORTED = sorted(all_names)
else:
    st.error("Failed to load or process race data for UI.")
    # Provide fallback race list if needed, or handle error state
    ALL_RACE_NAMES_SORTED = list(NAME_GENERATOR_MAP.keys()).sort()

# === UI ===
st.title("🌸 Tivmir World Tools")

# === Initialize Session State ===
# NPC & Name Output
if 'npc_output' not in st.session_state: st.session_state.npc_output = ""
if 'name_output' not in st.session_state: st.session_state.name_output = ""
# Name Gen UI State
if 'selected_rarity' not in st.session_state: st.session_state.selected_rarity = "Common"
if 'name_race' not in st.session_state: st.session_state.name_race = None
# --- ADD Calendar State Initialization ---
# Call this only once per session start
initialize_calendar_state(start_year=1478, start_month_index=0, start_day=1)

tabs = st.tabs(["🌿 NPC Generator", "🔤 Name Generator", "📅 Calendar", "🌌 Lore"])

# --- NPC Generator Tab (Remains the same) ---
with tabs[0]:
    st.header("🌿 NPC Generator")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Generate NPC", key="npc_button"):
             st.session_state.npc_output = generate_npc()
    with col2:
        if st.button("Clear Output", key="npc_clear"):
            st.session_state.npc_output = ""

    if st.session_state.npc_output: st.markdown("---")
    with st.container(border=True):
         if st.session_state.npc_output and "Error:" in st.session_state.npc_output: st.error(st.session_state.npc_output)
         elif st.session_state.npc_output: st.markdown(st.session_state.npc_output)
         else: st.markdown("*Click 'Generate NPC' to create a character...*")


# --- Name Generator Tab with Rarity Selection ---
with tabs[1]:
    st.header("🔤 Name Generator")

    # Define rarity order + Add "All" option
    rarity_options = ["All"] + list(RACES_BY_RARITY.keys())

    # Callback to reset race when rarity changes
    def rarity_changed():
        st.session_state.name_race = None # Reset race selection

    # Rarity Selection
    st.selectbox(
        "Filter by Rarity:",
        rarity_options,
        key="selected_rarity",
        on_change=rarity_changed # Call the reset function when rarity changes
    )
    selected_rarity = st.session_state.selected_rarity

    # Determine race options based on selected rarity
    current_race_options = []
    if selected_rarity == "All":
        current_race_options = ALL_RACE_NAMES_SORTED
    elif selected_rarity in RACES_BY_RARITY:
        current_race_options = RACES_BY_RARITY[selected_rarity]

    # Race Selection (conditional based on rarity having races)
    if current_race_options:
        # Set default index for race selectbox if resetting or first load
        race_key = "name_race"
        current_race_value = st.session_state.get(race_key, None)
        default_index = 0
        if current_race_value not in current_race_options:
            st.session_state[race_key] = current_race_options[0] # Set to first in new list
        else:
            try:
                default_index = current_race_options.index(current_race_value)
            except ValueError: # Should not happen if value is in options
                 st.session_state[race_key] = current_race_options[0]

        st.selectbox(
             "Choose a race:",
             current_race_options,
             key=race_key, # Use session state key
             index=default_index # Set default index
         )
        # Get the current selected race from session state AFTER the selectbox is drawn
        race = st.session_state.name_race
    else:
        st.warning(f"No races found for rarity '{selected_rarity}'.")
        race = None # No race selected

    # --- Dynamic Widget Display and Generation Logic (using Dictionary Dispatch) ---
    if race: # Only proceed if a race is selected
        race_config = NAME_GENERATOR_MAP.get(race)

        # Store widget values temporarily
        selected_gender = "Any"
        selected_element = None
        selected_clan = None
        kwargs_for_func = {} # Arguments to pass to the generator function

        if race_config:
            # --- Display relevant widgets ---
            if race_config.get("needs_gender"):
                selected_gender = st.radio(
                    "Select Gender:", ["Any", "Male", "Female"],
                    key=f"{race}_gender_ng", # Unique key per race for name gen tab
                    horizontal=True
                )
                kwargs_for_func["gender"] = selected_gender

            if race_config.get("needs_element"): # Special case for Genasi
                selected_element = st.radio(
                    "Select Element:", ["Air", "Water", "Fire", "Earth"],
                    key=f"{race}_element_ng",
                    horizontal=True
                )
                # Function call handled below

            if race_config.get("needs_clan"): # Special case for Tabaxi
                tabaxi_data = name_data.get("tabaxi", {})
                clan_list = tabaxi_data.get("clans", [])
                if clan_list and isinstance(clan_list, list):
                     clan_names = [c["name"] for c in clan_list if isinstance(c, dict) and "name" in c]
                     if clan_names:
                         # Sort clan names alphabetically
                         clan_names.sort()
                         selected_clan = st.selectbox("Choose a Tabaxi clan:", clan_names, key="tabaxi_clan_ng")
                         kwargs_for_func["selected_clan"] = selected_clan # Pass clan name
                     else: st.warning("No valid clan names found.")
                else: st.warning("Tabaxi clan data not found or invalid.")

            # --- Generate Button and Function Call ---
            generate_button = st.button(f"Generate {race} Name", key=f"{race}_button_ng")

            if generate_button:
                generator_func = race_config["func"]

                if race == "Genasi": # Handle Genasi separately
                    if selected_element == "Air": st.session_state.name_output = generate_air_genasi_name()
                    elif selected_element == "Water": st.session_state.name_output = generate_water_genasi_name()
                    elif selected_element == "Fire": st.session_state.name_output = generate_fire_genasi_name()
                    elif selected_element == "Earth": st.session_state.name_output = generate_earth_genasi_name()
                elif race == "Tabaxi": # Handle Tabaxi separately
                     if selected_clan:
                         st.session_state.name_output = generator_func(selected_clan)
                     else:
                          st.warning("Please select a Tabaxi clan.")
                          st.session_state.name_output = "" # Clear output if no clan
                elif generator_func: # Handle all other standard races
                    try:
                        st.session_state.name_output = generator_func(**kwargs_for_func)
                    except Exception as e:
                        st.error(f"Error calling {generator_func.__name__}: {e}")
                        st.session_state.name_output = "Error generating name."
                else:
                     st.warning(f"No generator function configured for {race}.")
                     st.session_state.name_output = "" # Clear output

        else:
            st.write(f"Configuration missing for race: {race}") # Should not happen if map is complete
    else:
        # Optionally display a message if no race is selected (e.g., rarity filter yields no results)
        if selected_rarity != "All":
             st.markdown("*Select a race from the list above.*")
        else:
             st.markdown("*Select a race.*") # Should only happen if initial load fails


    # Display Name Generator output (Remains the same)
    if st.session_state.name_output:
        st.markdown("---")
        if "Error:" in st.session_state.name_output:
            st.error(st.session_state.name_output)
        else:
            st.markdown(st.session_state.name_output)

# --- ADD Calendar Tracker Tab ---
with tabs[2]:
    st.header("📅 Tivmir Calendar Tracker")

    # Display current date
    st.subheader("Current Date:")
    st.markdown(f"## {get_current_date_string()}") # Display formatted date prominently

    st.markdown("---") # Separator

    # Buttons to advance time
    st.subheader("Advance Time:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Advance 1 Day", key="adv_day_1"):
            advance_day(1)
            st.rerun() # Rerun script immediately to show updated date
    with col2:
        if st.button("Advance 1 Week", key="adv_week"):
            advance_week()
            st.rerun()
    with col3:
        if st.button("Advance 1 Month", key="adv_month"):
            advance_month()
            st.rerun()

# --- ADD Lore / Deity Browser Tab ---
with tabs[3]: # Index 3 corresponds to the 4th tab, "🌌 Lore"
    st.header("🌌 Tivmir Pantheon")

    if not deities:
        st.warning("Deity information could not be loaded.")
    else:
        # Option to show all or a random deity
        display_mode = st.radio(
            "Display:",
            ["Browse All", "Random Deity"],
            key="lore_display_mode",
            horizontal=True
        )

        st.markdown("---")

        # --- Helper function to display deity info (including image) ---
        def display_deity_info(deity_data):
            if not deity_data:
                st.error("No deity data provided.")
                return

            st.markdown(f"### {deity_data.get('name', '')} - _{deity_data.get('title', '')}_")

            # --- Image Handling ---
            symbol_filename = deity_data.get('symbol_image')
            symbol_text = deity_data.get('symbol', 'N/A')
            image_path = None
            if symbol_filename:
                # Assume images are in an 'images' folder at the root
                image_path = os.path.join("images", symbol_filename)

            if image_path and os.path.exists(image_path):
                st.image(image_path, caption=f"Symbol: {symbol_text}", width=100) # Adjust width as needed
            else:
                st.markdown(f"**Symbol:** {symbol_text}")
                if symbol_filename: # Add a note if image was expected but not found
                     st.caption(f"(Image '{symbol_filename}' not found)")
            # --- End Image Handling ---

            st.markdown(f"**Domains:** {', '.join(deity_data.get('domains', ['N/A']))}")
            st.markdown("---")
            st.markdown(f"**Dogma:**")
            st.markdown(f"> {deity_data.get('dogma', 'N/A')}")
        # --- End Helper Function ---


        if display_mode == "Browse All":
            st.subheader("Browse Deities")

            deity_names = sorted([d.get("name", "Unknown Deity") for d in deities]) # Sort names
            selected_deity_name = st.selectbox("Select a Deity:", deity_names)
            selected_deity = next((d for d in deities if d.get("name") == selected_deity_name), None)

            if selected_deity:
                display_deity_info(selected_deity) # Use the helper function
            else:
                st.error("Could not find details for the selected deity.")

        elif display_mode == "Random Deity":
            st.subheader("Random Deity")
            import random

            # Initialize or get new random deity
            if 'random_deity' not in st.session_state or st.button("Show Another Random Deity", key="lore_random_button"):
                if deities:
                    st.session_state.random_deity = random.choice(deities)
                else:
                    st.session_state.random_deity = None
                    st.warning("Cannot select random deity, data missing.")

            # Display the random deity info using the helper function
            if st.session_state.get('random_deity'):
                display_deity_info(st.session_state.random_deity)
            else:
                 st.info("Click 'Show Another Random Deity' or select 'Browse All'.")