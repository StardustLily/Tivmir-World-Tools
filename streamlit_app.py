# streamlit_app.py
import streamlit as st
# Import necessary data and TOP-LEVEL generator functions
from data_loader import name_data # Keep name_data for Tabaxi clan lookup? Or pass it? Pass it maybe.
# Let's try importing only the necessary top-level things
from data_loader import icons # icons are used directly in UI? No, only NPC gen. Remove import.
# We need the list of race options for the selectbox
from data_loader import name_data # Need this to get keys for options, and Tabaxi clans
from npc_generator import generate_npc
# Import all the generate_X_name functions needed by the UI buttons
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
    generate_common_name
)

# Set page config first!
st.set_page_config(page_title="Tivmir World Tools", layout="centered")

# === UI ===
st.title("🌸 Tivmir World Tools")

# Initialize session state variables if they don't exist
if 'npc_output' not in st.session_state:
    st.session_state.npc_output = ""
if 'name_output' not in st.session_state:
    st.session_state.name_output = ""

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

# --- Name Generator Tab ---
with tabs[1]:
    st.header("🔤 Name Generator")

    # Define race options (can keep manual list for order/display)
    race_options = ["Elf", "Eladrin", "Tabaxi", "Human", "Halfling", "Orc",
                    "Tiefling", "Drow", "Dragonborn", "Aarakocra", "Owlin",
                    "Tortle", "Triton", "Genasi", "Kenku", "Lizardfolk",
                    "Yuan-Ti", "Goblin", "Bugbear", "Gnome", "Goliath",
                    "Minotaur", "Harengon", "Leonin", "Loxodon",
                    "Aasimar", "Shifter", "Githyanki"]
    race = st.selectbox("Choose a race:", race_options, key="name_race")

    # UI Blocks for each race - simplified, calling imported functions
    if race == "Tabaxi":
        tabaxi_data = name_data.get("tabaxi", {})
        clan_list = tabaxi_data.get("clans", [])
        if clan_list and isinstance(clan_list, list):
             clan_names = [c["name"] for c in clan_list if isinstance(c, dict) and "name" in c]
             if clan_names:
                 selected_clan = st.selectbox("Choose a Tabaxi clan:", clan_names, key="tabaxi_clan")
                 if st.button("Generate Tabaxi Name", key="tabaxi_name_button"):
                     st.session_state.name_output = generate_tabaxi_name(selected_clan) # Imported func
             else: st.warning("No valid clan names found.")
        else: st.warning("Tabaxi clan data not found or invalid.")

    elif race == "Human":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="human_gender", horizontal=True)
        if st.button("Generate Common Name", key="common_name_button"): st.session_state.name_output = generate_common_name(gender=gender) # Imported func

    elif race == "Halfling":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="halfling_gender", horizontal=True)
        if st.button("Generate Halfling Name", key="halfling_name_button"): st.session_state.name_output = generate_halfling_name(gender=gender) # Imported func

    elif race == "Orc":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="orc_gender", horizontal=True)
        if st.button("Generate Orcish Name", key="orc_name_button"): st.session_state.name_output = generate_orc_name(gender=gender) # Imported func

    elif race == "Tiefling":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="tiefling_gender", horizontal=True)
        if st.button("Generate Infernal Name", key="tiefling_name_button"): st.session_state.name_output = generate_infernal_name(gender=gender) # Imported func

    elif race == "Drow":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="drow_gender", horizontal=True)
        if st.button("Generate Drow Name", key="drow_name_button"): st.session_state.name_output = generate_drow_name(gender=gender) # Imported func

    elif race == "Dragonborn":
        if st.button("Generate Dragonborn Name", key="dragonborn_name_button"): st.session_state.name_output = generate_dragonborn_name() # Imported func

    elif race == "Aarakocra":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="aarakocra_gender", horizontal=True)
        if st.button("Generate Aarakocra Name", key="aarakocra_name_button"): st.session_state.name_output = generate_aarakocra_name(gender=gender) # Imported func

    elif race == "Owlin":
        if st.button("Generate Owlin Name", key="owlin_name_button"): st.session_state.name_output = generate_owlin_name() # Imported func

    elif race == "Tortle":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="tortle_gender", horizontal=True)
        if st.button("Generate Tortle Name", key="tortle_name_button"): st.session_state.name_output = generate_tortle_name(gender=gender) # Imported func

    elif race == "Triton":
        if st.button("Generate Triton Name", key="triton_name_button"): st.session_state.name_output = generate_triton_name() # Imported func

    elif race == "Genasi":
        st.markdown("---")
        element = st.radio("Select Element:", ["Air", "Water", "Fire", "Earth"], key="genasi_element", horizontal=True)
        if st.button("Generate Genasi Name", key="genasi_name_button"):
            if element == "Air": st.session_state.name_output = generate_air_genasi_name() # Imported func
            elif element == "Water": st.session_state.name_output = generate_water_genasi_name() # Imported func
            elif element == "Fire": st.session_state.name_output = generate_fire_genasi_name() # Imported func
            elif element == "Earth": st.session_state.name_output = generate_earth_genasi_name() # Imported func

    elif race == "Kenku":
        if st.button("Generate Kenku Name", key="kenku_name_button"): st.session_state.name_output = generate_kenku_name() # Imported func

    elif race == "Lizardfolk":
        if st.button("Generate Lizardfolk Name", key="lizardfolk_name_button"): st.session_state.name_output = generate_lizardfolk_name() # Imported func

    elif race == "Yuan-Ti":
        if st.button("Generate Yuan-Ti Name", key="yuan_ti_name_button"): st.session_state.name_output = generate_yuan_ti_name() # Imported func

    elif race == "Goblin":
        if st.button("Generate Goblin Name", key="goblin_name_button"): st.session_state.name_output = generate_goblin_name() # Imported func

    elif race == "Bugbear":
        if st.button("Generate Bugbear Name", key="bugbear_name_button"): st.session_state.name_output = generate_bugbear_name() # Imported func

    elif race == "Gnome":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="gnome_gender", horizontal=True)
        if st.button("Generate Gnome Name", key="gnome_name_button"): st.session_state.name_output = generate_gnome_name(gender=gender) # Imported func

    elif race == "Harengon":
        if st.button("Generate Harengon Name", key="harengon_name_button"): st.session_state.name_output = generate_harengon_name() # Imported func

    elif race == "Leonin":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="leonin_gender", horizontal=True)
        if st.button("Generate Leonin Name", key="leonin_name_button"): st.session_state.name_output = generate_leonin_name(gender=gender) # Imported func

    elif race == "Loxodon":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="loxodon_gender", horizontal=True)
        if st.button("Generate Loxodon Name", key="loxodon_name_button"): st.session_state.name_output = generate_loxodon_name(gender=gender) # Imported func

    elif race == "Githyanki":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="githyanki_gender", horizontal=True)
        if st.button("Generate Githyanki Name", key="githyanki_name_button"): st.session_state.name_output = generate_githyanki_name(gender=gender) # Imported func

    elif race == "Aasimar":
        if st.button("Generate Aasimar Name", key="aasimar_name_button"): st.session_state.name_output = generate_aasimar_name() # Imported func

    elif race == "Shifter":
        if st.button("Generate Shifter Name", key="shifter_name_button"): st.session_state.name_output = generate_shifter_name() # Imported func

    elif race == "Eladrin":
        if st.button("Generate Eladrin Name", key="eladrin_name_button"): st.session_state.name_output = generate_eladrin_name() # Imported func

    elif race == "Goliath":
        if st.button("Generate Goliath Name", key="goliath_name_button"): st.session_state.name_output = generate_goliath_name() # Imported func

    elif race == "Minotaur":
        gender = st.radio("Select Gender:", ["Any", "Male", "Female"], key="minotaur_gender", horizontal=True)
        if st.button("Generate Minotaur Name", key="minotaur_name_button"): st.session_state.name_output = generate_minotaur_name(gender=gender) # Imported func

    elif race == "Elf":
        if st.button("Generate Elven Name", key="elven_name_button"): st.session_state.name_output = generate_elven_name() # Imported func

    else:
        st.write(f"Select a race to generate a name.") # Fallback


    # Display Name Generator output
    if st.session_state.name_output:
        st.markdown("---")
        if "Error:" in st.session_state.name_output:
            st.error(st.session_state.name_output)
        else:
            st.markdown(st.session_state.name_output)