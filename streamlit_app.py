import streamlit as st
# Import necessary data and TOP-LEVEL generator functions
from data_loader import name_data # Keep name_data for Tabaxi clan lookup
from npc_generator import generate_npc
# Import all the generate_X_name functions needed by the UI buttons
# (Ensure ALL needed functions are listed here)
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

# Set page config first!
st.set_page_config(page_title="Tivmir World Tools", layout="centered")

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
# Make sure all races from race_options are keys in the map above

# === UI ===
st.title("🌸 Tivmir World Tools")

# Initialize session state variables if they don't exist
if 'npc_output' not in st.session_state:
    st.session_state.npc_output = ""
if 'name_output' not in st.session_state:
    st.session_state.name_output = ""
# Keep track of selected race for the name generator tab
if 'name_race' not in st.session_state:
     st.session_state.name_race = list(NAME_GENERATOR_MAP.keys())[0] # Default to first race


tabs = st.tabs(["🌿 NPC Generator", "🔤 Name Generator"])

# --- NPC Generator Tab ---
with tabs[0]:
    st.header("🌿 NPC Generator")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Generate NPC", key="npc_button"):
             st.session_state.npc_output = generate_npc() # Call imported function
    with col2:
        if st.button("Clear Output", key="npc_clear"):
            st.session_state.npc_output = ""

    # Display NPC output
    if st.session_state.npc_output:
        st.markdown("---")
    with st.container(border=True):
         if st.session_state.npc_output and "Error:" in st.session_state.npc_output:
              st.error(st.session_state.npc_output)
         elif st.session_state.npc_output:
              st.markdown(st.session_state.npc_output)
         else:
              st.markdown("*Click 'Generate NPC' to create a character...*")

# --- Refactored Name Generator Tab ---
with tabs[1]:
    st.header("🔤 Name Generator")

    # Use the keys from the map as options
    race_options = list(NAME_GENERATOR_MAP.keys())
    # Use session state for the selectbox value persistence
    st.selectbox(
        "Choose a race:",
        race_options,
        key="name_race" # Use session state key
    )
    # Get the current selected race from session state
    race = st.session_state.name_race

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
            # The actual function call is handled below for Genasi

        if race_config.get("needs_clan"): # Special case for Tabaxi
            tabaxi_data = name_data.get("tabaxi", {})
            clan_list = tabaxi_data.get("clans", [])
            if clan_list and isinstance(clan_list, list):
                 clan_names = [c["name"] for c in clan_list if isinstance(c, dict) and "name" in c]
                 if clan_names:
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


    # Display Name Generator output (Remains the same)
    if st.session_state.name_output:
        st.markdown("---")
        if "Error:" in st.session_state.name_output:
            st.error(st.session_state.name_output)
        else:
            st.markdown(st.session_state.name_output)