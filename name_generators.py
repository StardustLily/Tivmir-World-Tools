import random
import streamlit as st
# Import data and core helpers from other modules
# Assuming files are in the same directory, use relative imports
# If in subdirectories, adjust paths accordingly (e.g., from ..data_loader import ...)
from data_loader import name_data, kenku_names, lizardfolk_names, yuan_ti_names, goblin_names, shifter_names
from name_helpers import _assemble_name_parts, _generate_poetic_meaning

# === Specific Helper Functions (Moved Here) ===

def _generate_structured_name_data(race_data, gender="Any"):
    """
    Internal helper to generate name components for structured names (P+M+S +/- S).
    Accepts a dictionary containing the specific race's data.
    Returns a dictionary containing 'name', 'parts', 'poetic', 'error'.
    """
    result = {"name": None, "parts": [], "poetic": "", "error": None}
    if not race_data or not isinstance(race_data, dict):
        result["error"] = "Invalid race data provided to structured name helper."; st.error(result["error"]); return result

    prefixes = race_data.get("prefixes")
    middles = race_data.get("middles")
    suffixes = race_data.get("suffixes")
    gloss = race_data.get("gloss")
    surnames = race_data.get("surnames")

    if not prefixes or not suffixes or not gloss:
        error_msg = "Missing core name data (prefixes, suffixes, or gloss) for this race."
        st.error(error_msg); result["error"] = error_msg; return result

    parts = _assemble_name_parts(prefixes, middles or [], suffixes, gender_filter=gender)
    if not parts:
        error_msg = "Failed to assemble name parts."; st.warning(error_msg); result["error"] = error_msg; return result

    result["parts"] = list(parts) # Ensure it's a mutable list copy
    first_name = "".join(p["text"] for p in parts)

    surname = ""
    surname_part = None
    if surnames and isinstance(surnames, list) and surnames: # Check if list exists and is not empty
        try:
             surname_entry = random.choice(surnames)
             surname = surname_entry["text"]
             surname_part = {"text": surname, "meaning": surname_entry.get('meaning', 'N/A')}
             full_name = f"{first_name} {surname}"
        except (IndexError, KeyError) as e:
             st.warning(f"Error selecting surname, skipping: {e}")
             full_name = first_name # Fallback
    else:
        full_name = first_name

    result["name"] = full_name
    result["poetic"] = _generate_poetic_meaning(parts, gloss) # Poetic meaning from P+M+S parts only

    if surname_part:
        result["parts"].append(surname_part) # Add surname details after poetic meaning

    return result

def _generate_dragonborn_name_data(race_data):
    result = {"name": None, "parts": [], "poetic": "", "error": None}
    if not race_data or not isinstance(race_data, dict):
        result["error"] = "Invalid race data provided to Dragonborn helper."; st.error(result["error"]); return result
    clans = race_data.get("clans"); prefixes = race_data.get("prefixes")
    middles = race_data.get("middles"); suffixes = race_data.get("suffixes")
    gloss = race_data.get("gloss")
    if not clans or not prefixes or not suffixes or not gloss:
        error_msg = "Missing core Draconic data."; st.error(error_msg); result["error"] = error_msg; return result

    try:
        clan_part = random.choice(clans)
        clan_dict = {"text": clan_part["text"], "meaning": clan_part.get("meaning", "N/A")}
        all_parts_for_meaning = [clan_dict]
        personal_parts = _assemble_name_parts(prefixes, middles or [], suffixes, gender_filter="Any")
        if not personal_parts:
            error_msg = "Failed to assemble Draconic personal name parts."; st.warning(error_msg); result["error"] = error_msg
            result["name"] = clan_dict["text"] + "-k-[Error]"; result["parts"] = [clan_dict]; return result
        personal_name_str = "".join(p["text"] for p in personal_parts)
        all_parts_for_meaning.extend(personal_parts)
        full_name = f"{clan_dict['text']}-k-{personal_name_str}"
        result["name"] = full_name
        result["parts"] = all_parts_for_meaning
        result["poetic"] = _generate_poetic_meaning(all_parts_for_meaning, gloss)
    except Exception as e:
         st.error(f"Error generating Dragonborn name: {e}"); result["error"] = str(e)
    return result

def _generate_aarakocra_name_data(race_data, gender="Any"):
    result = {"name": None, "parts": [], "poetic": "", "error": None}
    if not race_data or not isinstance(race_data, dict):
         result["error"] = "Invalid race data provided to Aarakocra helper."; st.error(result["error"]); return result
    lineages = race_data.get("lineages"); prefixes = race_data.get("prefixes")
    middles = race_data.get("middles"); suffixes = race_data.get("suffixes")
    gloss = race_data.get("gloss")
    if not lineages or not prefixes or not suffixes or not gloss:
        error_msg = "Missing core Aarakocra data."; st.error(error_msg); result["error"] = error_msg; return result

    try:
        lineage_part = random.choice(lineages)
        lineage_dict = {"text": lineage_part["text"], "meaning": lineage_part.get("meaning", "N/A")}
        all_parts_for_meaning = [lineage_dict]
        personal_parts = _assemble_name_parts(prefixes, middles or [], suffixes, gender_filter=gender)
        if not personal_parts:
            error_msg = "Failed to assemble Aarakocra personal parts."; st.warning(error_msg); result["error"] = error_msg
            result["name"] = lineage_dict["text"] + " [Error]"; result["parts"] = [lineage_dict]; return result
        personal_name_str = "".join(p["text"] for p in personal_parts)
        all_parts_for_meaning.extend(personal_parts)
        full_name = f"{lineage_dict['text']} {personal_name_str}"
        result["name"] = full_name
        result["parts"] = all_parts_for_meaning
        result["poetic"] = _generate_poetic_meaning(all_parts_for_meaning, gloss)
    except Exception as e:
         st.error(f"Error generating Aarakocra name: {e}"); result["error"] = str(e)
    return result

def _generate_owlin_name_data(race_data):
    result = {"name": None, "parts": [], "poetic": "", "error": None}
    if not race_data or not isinstance(race_data, dict):
         result["error"] = "Invalid race data provided to Owlin helper."; st.error(result["error"]); return result
    personal_roots = race_data.get("personal"); descriptors = race_data.get("descriptors")
    gloss = race_data.get("gloss")
    if not personal_roots or not descriptors or not gloss:
        error_msg = "Missing core Owlin data."; st.error(error_msg); result["error"] = error_msg; return result

    try:
        personal_part = random.choice(personal_roots)
        personal_dict = {"text": personal_part["text"], "meaning": personal_part.get("meaning", "N/A")}
        descriptor_part = random.choice(descriptors)
        descriptor_dict = {"text": descriptor_part["text"], "meaning": descriptor_part.get("meaning", "N/A")}
        all_parts_for_meaning = [personal_dict, descriptor_dict]
        full_name = f"{personal_dict['text']}{descriptor_dict['text']}" # Combined
        result["name"] = full_name
        result["parts"] = all_parts_for_meaning
        result["poetic"] = _generate_poetic_meaning(all_parts_for_meaning, gloss)
    except Exception as e:
         st.error(f"Error generating Owlin name: {e}"); result["error"] = str(e)
    return result

def _generate_tortle_name_data(race_data, gender="Any"):
    result = {"name": None, "parts": [], "poetic": "", "error": None}
    if not race_data or not isinstance(race_data, dict):
         result["error"] = "Invalid race data provided to Tortle helper."; st.error(result["error"]); return result
    given_names = race_data.get("given"); descriptors = race_data.get("descriptors")
    gloss = race_data.get("gloss")
    if not given_names or not descriptors or not gloss:
        error_msg = "Missing core Tortle data."; st.error(error_msg); result["error"] = error_msg; return result

    try:
        given_part = random.choice(given_names)
        given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
        all_parts_for_meaning = [given_dict]
        descriptor_options = descriptors
        if gender != "Any":
            filtered_options = [d for d in descriptors if d.get("gender") == gender or d.get("gender") == "Unisex"]
            if filtered_options: descriptor_options = filtered_options
            else: st.warning(f"No specific {gender} Tortle descriptors found, using any.")
        if not descriptor_options:
            error_msg = "Tortle descriptor options list empty."; st.error(error_msg); result["error"] = error_msg
            result["name"] = given_dict["text"] + " [Error]"; result["parts"] = [given_dict]; return result
        descriptor_part = random.choice(descriptor_options)
        descriptor_dict = {"text": descriptor_part["text"], "meaning": descriptor_part.get("meaning", "N/A")}
        all_parts_for_meaning.append(descriptor_dict)
        full_name = f"{given_dict['text']} {descriptor_dict['text']}"
        result["name"] = full_name
        result["parts"] = all_parts_for_meaning
        result["poetic"] = _generate_poetic_meaning(all_parts_for_meaning, gloss)
    except Exception as e:
        st.error(f"Error generating Tortle name: {e}"); result["error"] = str(e)
    return result

def _generate_triton_name_data(race_data):
    result = {"name": None, "parts": [], "poetic": "", "error": None}
    if not race_data or not isinstance(race_data, dict):
        result["error"] = "Invalid race data provided to Triton helper."; st.error(result["error"]); return result
    given_names = race_data.get("given"); markers = race_data.get("markers")
    gloss = race_data.get("gloss")
    if not given_names or not markers or not gloss:
        error_msg = "Missing core Triton data."; st.error(error_msg); result["error"] = error_msg; return result

    try:
        given_part = random.choice(given_names)
        given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
        marker_part = random.choice(markers)
        marker_dict = {"text": marker_part["text"], "meaning": marker_part.get("meaning", "N/A")}
        all_parts_for_meaning = [given_dict, marker_dict]
        full_name = f"{given_dict['text']}-{marker_dict['text']}" # Hyphenated
        result["name"] = full_name
        result["parts"] = all_parts_for_meaning
        result["poetic"] = _generate_poetic_meaning(all_parts_for_meaning, gloss)
    except Exception as e:
         st.error(f"Error generating Triton name: {e}"); result["error"] = str(e)
    return result

def _generate_gnome_name_data(race_data, gender="Any"):
    result = {"name": None, "parts": [], "poetic": "", "error": None}
    if not race_data or not isinstance(race_data, dict):
         result["error"] = "Invalid race data provided to Gnome helper."; st.error(result["error"]); return result
    male_first = race_data.get("male_first"); female_first = race_data.get("female_first")
    clans = race_data.get("clans"); descriptors = race_data.get("descriptors")
    gloss = race_data.get("gloss")
    if not male_first or not female_first or not clans or not descriptors or not gloss:
        error_msg = "Missing core Gnomish data."; st.error(error_msg); result["error"] = error_msg; return result

    try:
        given_part = None
        if gender == "Male": given_part = random.choice(male_first)
        elif gender == "Female": given_part = random.choice(female_first)
        else: chosen_list = random.choice([male_first, female_first]); given_part = random.choice(chosen_list)
        if not given_part: raise ValueError("Empty given name list for Gnome")
        given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
        all_parts = [given_dict]
        clan_part = random.choice(clans)
        clan_dict = {"text": clan_part["text"], "meaning": clan_part.get("meaning", "N/A")}
        all_parts.append(clan_dict)
        use_descriptor = random.random() < 0.5
        if use_descriptor:
            descriptor_part = random.choice(descriptors)
            descriptor_dict = {"text": descriptor_part["text"], "meaning": descriptor_part.get("meaning", "N/A")}
            all_parts.append(descriptor_dict)
        name_components = [p["text"] for p in all_parts]
        full_name = " ".join(name_components)
        result["name"] = full_name
        result["parts"] = all_parts
        result["poetic"] = _generate_poetic_meaning(all_parts, gloss)
    except Exception as e:
        st.error(f"Error generating Gnome name: {e}"); result["error"] = str(e)
    return result

def _generate_halfling_name_data(race_data, gender="Any"):
    result = {"name": None, "parts": [], "poetic": "", "error": None}
    if not race_data or not isinstance(race_data, dict):
        result["error"] = "Invalid race data provided to Halfling helper."; st.error(result["error"]); return result
    male_first = race_data.get("male_first"); female_first = race_data.get("female_first")
    family_names = race_data.get("family"); gloss = race_data.get("gloss")
    if not male_first or not female_first or not family_names or not gloss:
        error_msg = "Missing core Halfling data."; st.error(error_msg); result["error"] = error_msg; return result

    try:
        given_part = None
        if gender == "Male": given_part = random.choice(male_first)
        elif gender == "Female": given_part = random.choice(female_first)
        else: chosen_list = random.choice([male_first, female_first]); given_part = random.choice(chosen_list)
        if not given_part: raise ValueError("Empty given name list for Halfling")
        given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
        all_parts = [given_dict]
        family_part = random.choice(family_names)
        family_dict = {"text": family_part["text"], "meaning": family_part.get("meaning", "N/A")}
        all_parts.append(family_dict)
        full_name = f"{given_dict['text']} {family_dict['text']}"
        result["name"] = full_name
        result["parts"] = all_parts
        result["poetic"] = _generate_poetic_meaning(all_parts, gloss)
    except Exception as e:
        st.error(f"Error generating Halfling name: {e}"); result["error"] = str(e)
    return result

def _generate_goliath_name_data(race_data):
     result = {"name": None, "parts": [], "poetic": "", "error": None}
     if not race_data or not isinstance(race_data, dict):
         result["error"] = "Invalid race data provided to Goliath helper."; st.error(result["error"]); return result
     given_names = race_data.get("given"); titles = race_data.get("titles")
     gloss = race_data.get("gloss")
     if not given_names or not titles or not gloss:
         error_msg = "Missing core Goliath data."; st.error(error_msg); result["error"] = error_msg; return result

     try:
        given_part = random.choice(given_names)
        given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
        title_part = random.choice(titles)
        title_dict = {"text": title_part["text"], "meaning": title_part.get("meaning", "N/A")}
        all_parts = [given_dict, title_dict]
        full_name = f"{given_dict['text']} {title_dict['text']}"
        result["name"] = full_name
        result["parts"] = all_parts
        result["poetic"] = _generate_poetic_meaning(all_parts, gloss)
     except Exception as e:
        st.error(f"Error generating Goliath name: {e}"); result["error"] = str(e)
     return result

def _generate_minotaur_name_data(race_data, gender="Any"):
     result = {"name": None, "parts": [], "poetic": "", "error": None}
     if not race_data or not isinstance(race_data, dict):
          result["error"] = "Invalid race data provided to Minotaur helper."; st.error(result["error"]); return result
     male_first = race_data.get("male_first"); female_first = race_data.get("female_first")
     descriptors = race_data.get("descriptors"); gloss = race_data.get("gloss")
     if not male_first or not female_first or not descriptors or not gloss:
         error_msg = "Missing core Minotaur data."; st.error(error_msg); result["error"] = error_msg; return result

     try:
        given_part = None
        if gender == "Male": given_part = random.choice(male_first)
        elif gender == "Female": given_part = random.choice(female_first)
        else: chosen_list = random.choice([male_first, female_first]); given_part = random.choice(chosen_list)
        if not given_part: raise ValueError("Empty given name list for Minotaur")
        given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
        descriptor_part = random.choice(descriptors)
        descriptor_dict = {"text": descriptor_part["text"], "meaning": descriptor_part.get("meaning", "N/A")}
        all_parts = [given_dict, descriptor_dict]
        full_name = f"{given_dict['text']} {descriptor_dict['text']}"
        result["name"] = full_name
        result["parts"] = all_parts
        result["poetic"] = _generate_poetic_meaning(all_parts, gloss)
     except Exception as e:
         st.error(f"Error generating Minotaur name: {e}"); result["error"] = str(e)
     return result

def _generate_bugbear_name_data(race_data):
      result = {"name": None, "parts": [], "poetic": "", "error": None}
      if not race_data or not isinstance(race_data, dict):
           result["error"] = "Invalid race data provided to Bugbear helper."; st.error(result["error"]); return result
      given_names = race_data.get("given"); epithets = race_data.get("epithets")
      gloss = race_data.get("gloss")
      if not given_names or not epithets or not gloss:
          error_msg = "Missing core Bugbear data."; st.error(error_msg); result["error"] = error_msg; return result

      try:
         given_part = random.choice(given_names)
         given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
         epithet_part = random.choice(epithets)
         epithet_dict = {"text": epithet_part["text"], "meaning": epithet_part.get("meaning", "N/A")}
         all_parts = [given_dict, epithet_dict]
         full_name = f"{given_dict['text']} {epithet_dict['text']}"
         result["name"] = full_name
         result["parts"] = all_parts
         result["poetic"] = _generate_poetic_meaning(all_parts, gloss)
      except Exception as e:
         st.error(f"Error generating Bugbear name: {e}"); result["error"] = str(e)
      return result

def _generate_harengon_name_data(race_data):
       result = {"name": None, "parts": [], "poetic": "", "error": None}
       if not race_data or not isinstance(race_data, dict):
            result["error"] = "Invalid race data provided to Harengon helper."; st.error(result["error"]); return result
       given_names = race_data.get("given"); family_names = race_data.get("family")
       gloss = race_data.get("gloss")
       if not given_names or not family_names or not gloss:
           error_msg = "Missing core Harengon data."; st.error(error_msg); result["error"] = error_msg; return result

       try:
          given_part = random.choice(given_names)
          given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
          family_part = random.choice(family_names)
          family_dict = {"text": family_part["text"], "meaning": family_part.get("meaning", "N/A")}
          all_parts = [given_dict, family_dict]
          full_name = f"{given_dict['text']} {family_dict['text']}"
          result["name"] = full_name
          result["parts"] = all_parts
          result["poetic"] = _generate_poetic_meaning(all_parts, gloss)
       except Exception as e:
           st.error(f"Error generating Harengon name: {e}"); result["error"] = str(e)
       return result

def _generate_leonin_name_data(race_data, gender="Any"):
        result = {"name": None, "parts": [], "poetic": "", "error": None}
        if not race_data or not isinstance(race_data, dict):
             result["error"] = "Invalid race data provided to Leonin helper."; st.error(result["error"]); return result
        male_first = race_data.get("male_first"); female_first = race_data.get("female_first")
        pride_names = race_data.get("pridenames"); gloss = race_data.get("gloss")
        if not male_first or not female_first or not pride_names or not gloss:
            error_msg = "Missing core Leonin data."; st.error(error_msg); result["error"] = error_msg; return result

        try:
           given_part = None
           if gender == "Male": given_part = random.choice(male_first)
           elif gender == "Female": given_part = random.choice(female_first)
           else: chosen_list = random.choice([male_first, female_first]); given_part = random.choice(chosen_list)
           if not given_part: raise ValueError("Empty given name list for Leonin")
           given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
           all_parts = [given_dict]
           pride_part = random.choice(pride_names)
           pride_dict = {"text": pride_part["text"], "meaning": pride_part.get("meaning", "N/A")}
           all_parts.append(pride_dict)
           full_name = f"{given_dict['text']} {pride_dict['text']}"
           result["name"] = full_name
           result["parts"] = all_parts
           result["poetic"] = _generate_poetic_meaning(all_parts, gloss)
        except Exception as e:
           st.error(f"Error generating Leonin name: {e}"); result["error"] = str(e)
        return result

def _generate_loxodon_name_data(race_data, gender="Any"):
         result = {"name": None, "parts": [], "poetic": "", "error": None}
         if not race_data or not isinstance(race_data, dict):
              result["error"] = "Invalid race data provided to Loxodon helper."; st.error(result["error"]); return result
         male_first = race_data.get("male_first"); female_first = race_data.get("female_first")
         herd_names = race_data.get("herdnames"); gloss = race_data.get("gloss")
         if not male_first or not female_first or not herd_names or not gloss:
             error_msg = "Missing core Loxodon data."; st.error(error_msg); result["error"] = error_msg; return result

         try:
            given_part = None
            if gender == "Male": given_part = random.choice(male_first)
            elif gender == "Female": given_part = random.choice(female_first)
            else: chosen_list = random.choice([male_first, female_first]); given_part = random.choice(chosen_list)
            if not given_part: raise ValueError("Empty given name list for Loxodon")
            given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
            all_parts = [given_dict]
            herd_part = random.choice(herd_names)
            herd_dict = {"text": herd_part["text"], "meaning": herd_part.get("meaning", "N/A")}
            all_parts.append(herd_dict)
            full_name = f"{given_dict['text']} {herd_dict['text']}"
            result["name"] = full_name
            result["parts"] = all_parts
            result["poetic"] = _generate_poetic_meaning(all_parts, gloss)
         except Exception as e:
            st.error(f"Error generating Loxodon name: {e}"); result["error"] = str(e)
         return result

def _generate_aasimar_name_data(race_data):
          result = {"name": None, "parts": [], "poetic": "", "error": None}
          if not race_data or not isinstance(race_data, dict):
               result["error"] = "Invalid race data provided to Aasimar helper."; st.error(result["error"]); return result
          prefixes = race_data.get("prefixes"); middles = race_data.get("middles")
          suffixes = race_data.get("suffixes"); titles = race_data.get("titles")
          gloss = race_data.get("gloss")
          if not prefixes or not suffixes or not titles or not gloss: # Middles optional
              error_msg = "Missing core Aasimar data."; st.error(error_msg); result["error"] = error_msg; return result

          try:
             base_parts = _assemble_name_parts(prefixes, middles or [], suffixes, gender_filter="Any")
             if not base_parts:
                 error_msg = "Failed to assemble Aasimar base parts."; st.warning(error_msg); result["error"] = error_msg
                 result["name"] = "[Base Name Error]"; return result
             base_name_str = "".join(p["text"] for p in base_parts)
             all_parts = list(base_parts)
             full_name = base_name_str
             use_title = random.random() < 0.4
             if use_title and titles:
                 title_part = random.choice(titles)
                 title_dict = {"text": title_part["text"], "meaning": title_part.get("meaning", "N/A")}
                 all_parts.append(title_dict)
                 full_name = f"{base_name_str} {title_dict['text']}"
             result["name"] = full_name
             result["parts"] = all_parts
             result["poetic"] = _generate_poetic_meaning(all_parts, gloss)
          except Exception as e:
             st.error(f"Error generating Aasimar name: {e}"); result["error"] = str(e)
          return result

def _generate_githyanki_name_data(race_data, gender="Any"):
           result = {"name": None, "parts": [], "poetic": "", "error": None}
           if not race_data or not isinstance(race_data, dict):
                result["error"] = "Invalid race data provided to Githyanki helper."; st.error(result["error"]); return result
           male_first = race_data.get("male_first"); female_first = race_data.get("female_first")
           titles = race_data.get("titles"); gloss = race_data.get("gloss")
           if not male_first or not female_first or not titles or not gloss:
               error_msg = "Missing core Githyanki data."; st.error(error_msg); result["error"] = error_msg; return result

           try:
              given_part = None
              if gender == "Male": given_part = random.choice(male_first)
              elif gender == "Female": given_part = random.choice(female_first)
              else: chosen_list = random.choice([male_first, female_first]); given_part = random.choice(chosen_list)
              if not given_part: raise ValueError("Empty given name list for Githyanki")
              given_dict = {"text": given_part["text"], "meaning": given_part.get("meaning", "N/A")}
              all_parts = [given_dict]
              title_part = random.choice(titles)
              title_dict = {"text": title_part["text"], "meaning": title_part.get("meaning", "N/A")}
              all_parts.append(title_dict)
              full_name = f"{given_dict['text']} {title_dict['text']}"
              result["name"] = full_name
              result["parts"] = all_parts
              result["poetic"] = _generate_poetic_meaning(all_parts, gloss)
           except Exception as e:
               st.error(f"Error generating Githyanki name: {e}"); result["error"] = str(e)
           return result


# === Wrapper Functions (Public Interface) ===

def generate_elven_name(gender="Any"):
     race_key = "elf"
     if race_key not in name_data: return "Error: Elven name data not loaded."
     data = _generate_structured_name_data(name_data[race_key], gender)
     if data["error"]: return f"Error: {data['error']}"
     if not data["name"]: return "Error: Name generation failed silently."
     meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
     return (f"🌿 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **Poetic Meaning:** {data['poetic']}")

def generate_orc_name(gender="Any"):
      race_key = "orc"
      if race_key not in name_data: return "Error: Orcish name data not loaded."
      data = _generate_structured_name_data(name_data[race_key], gender)
      if data["error"]: return f"Error: {data['error']}"
      if not data["name"]: return "Error: Name generation failed silently."
      meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
      return (f"⚙️ **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **Poetic Meaning (First Name):** {data['poetic']}")

def generate_infernal_name(gender="Any"):
       race_key = "infernal"
       if race_key not in name_data: return "Error: Infernal name data not loaded."
       data = _generate_structured_name_data(name_data[race_key], gender)
       if data["error"]: return f"Error: {data['error']}"
       if not data["name"]: return "Error: Name generation failed silently."
       meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
       is_surname_present = len(data["parts"]) > 1 and "surnames" in name_data.get(race_key, {}) and any(p["text"] == data["name"].split(" ")[-1] for p in data["parts"] if p["text"] == data["name"].split(" ")[-1]) # Check if last part matches surname meaning
       poetic_label = "Poetic Meaning (First Name):" if is_surname_present else "Poetic Meaning:"
       return (f"🔥 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_tabaxi_name(selected_clan):
        race_key = "tabaxi"
        if race_key not in name_data: return "Error: Tabaxi name data not loaded."
        if "clans" not in name_data[race_key] or not name_data[race_key]["clans"]:
             st.error("Missing required Tabaxi clan data.")
             return "Error: Missing clan data."
        data = _generate_structured_name_data(name_data[race_key], gender="Any")
        if data["error"]: return f"Error: {data['error']}"
        if not data["name"]: return "Error: Name generation failed silently."
        full_name = data["name"]; meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]; poetic = data["poetic"]
        clan_list = name_data[race_key]["clans"]
        clan_info = next((c for c in clan_list if c["name"] == selected_clan), None)
        clan_desc = ""
        if clan_info:
            clan_desc = (f"\n\n🏡 **Clan:** {clan_info['name']}\n\n" + f"• **Region:** {clan_info['region']}\n\n" + f"• **Traits:** {clan_info['traits']}\n\n" + f"• **Twist:** {clan_info['twist']}")
        else:
            st.warning(f"Could not find details for clan: {selected_clan}")
            clan_desc = f"\n\n🏡 **Clan:** {selected_clan} (Details not found)"
        return (f"🐾 **Name:** {full_name}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **Poetic Meaning:** {poetic}{clan_desc}")

def generate_drow_name(gender="Any"):
         race_key = "drow"
         if race_key not in name_data: return "Error: Drow name data not loaded."
         data = _generate_structured_name_data(name_data[race_key], gender)
         if data["error"]: return f"Error: {data['error']}"
         if not data["name"]: return "Error: Name generation failed silently."
         meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
         is_surname_present = len(data["parts"]) > 1 and "surnames" in name_data.get(race_key, {}) and any(p["text"] == data["name"].split(" ")[-1] for p in data["parts"] if p["text"] == data["name"].split(" ")[-1])
         poetic_label = "Poetic Meaning (First Name):" if is_surname_present else "Poetic Meaning:"
         return (f"🕷️ **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_dragonborn_name():
          race_key = "draconic"
          if race_key not in name_data: return "Error: Draconic name data not loaded."
          data = _generate_dragonborn_name_data(name_data[race_key])
          if data["error"]: return f"Error: {data['error']}"
          if not data["name"]: return "Error: Name generation failed silently."
          meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
          poetic_label = "Poetic Meaning:"
          return (f"🐉 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_aarakocra_name(gender="Any"):
           race_key = "aarakocra"
           if race_key not in name_data: return "Error: Aarakocra name data not loaded."
           data = _generate_aarakocra_name_data(name_data[race_key], gender)
           if data["error"]: return f"Error: {data['error']}"
           if not data["name"]: return "Error: Name generation failed silently."
           meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
           poetic_label = "Poetic Meaning:"
           return (f"🐦 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_owlin_name():
            race_key = "owlin"
            if race_key not in name_data: return "Error: Owlin name data not loaded."
            data = _generate_owlin_name_data(name_data[race_key])
            if data["error"]: return f"Error: {data['error']}"
            if not data["name"]: return "Error: Name generation failed silently."
            meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
            poetic_label = "Poetic Meaning:"
            return (f"🦉 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_tortle_name(gender="Any"):
             race_key = "tortle"
             if race_key not in name_data: return "Error: Tortle name data not loaded."
             data = _generate_tortle_name_data(name_data[race_key], gender)
             if data["error"]: return f"Error: {data['error']}"
             if not data["name"]: return "Error: Name generation failed silently."
             meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
             poetic_label = "Poetic Meaning:"
             return (f"🐢 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_triton_name():
              race_key = "triton"
              if race_key not in name_data: return "Error: Triton name data not loaded."
              data = _generate_triton_name_data(name_data[race_key])
              if data["error"]: return f"Error: {data['error']}"
              if not data["name"]: return "Error: Name generation failed silently."
              meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
              poetic_label = "Poetic Meaning:"
              return (f"🔱 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_fire_genasi_name():
               race_key = "ignan"
               if race_key not in name_data: return "Error: Ignan (Fire Genasi) name data not loaded."
               data = _generate_structured_name_data(name_data[race_key], gender="Any")
               if data["error"]: return f"Error: {data['error']}"
               if not data["name"]: return "Error: Name generation failed silently."
               meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
               poetic_label = "Poetic Meaning:"
               return (f"🔥 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_earth_genasi_name():
                race_key = "terran"
                if race_key not in name_data: return "Error: Terran (Earth Genasi) name data not loaded."
                data = _generate_structured_name_data(name_data[race_key], gender="Any")
                if data["error"]: return f"Error: {data['error']}"
                if not data["name"]: return "Error: Name generation failed silently."
                meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                poetic_label = "Poetic Meaning:"
                return (f"⛰️ **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_air_genasi_name():
                 race_key = "air_genasi"
                 if race_key not in name_data: return "Error: Air Genasi name data not loaded."
                 data = _generate_structured_name_data(name_data[race_key], gender="Any")
                 if data["error"]: return f"Error: {data['error']}"
                 if not data["name"]: return "Error: Name generation failed silently."
                 meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                 poetic_label = "Poetic Meaning:"
                 return (f"💨 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_water_genasi_name():
                  race_key = "water_genasi"
                  if race_key not in name_data: return "Error: Water Genasi name data not loaded."
                  data = _generate_structured_name_data(name_data[race_key], gender="Any")
                  if data["error"]: return f"Error: {data['error']}"
                  if not data["name"]: return "Error: Name generation failed silently."
                  meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                  poetic_label = "Poetic Meaning:"
                  return (f"💧 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_eladrin_name():
                   race_key = "sylvan"
                   if race_key not in name_data: return "Error: Sylvan (Eladrin) name data not loaded."
                   data = _generate_structured_name_data(name_data[race_key], gender="Any")
                   if data["error"]: return f"Error: {data['error']}"
                   if not data["name"]: return "Error: Name generation failed silently."
                   meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                   poetic_label = "Poetic Meaning:"
                   return (f"✨ **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_kenku_name():
                    if not kenku_names: st.error("Kenku name data missing."); return "Error: Missing Kenku data."
                    name_entry = random.choice(kenku_names)
                    name_text = name_entry.get('text', '[Name Error]')
                    name_meaning = name_entry.get('meaning', 'No description available.')
                    return (f"🐦‍⬛ **Name:** {name_text}\n\n" + f"*{name_meaning}*")

def generate_lizardfolk_name():
                     if not lizardfolk_names: st.error("Lizardfolk name data missing."); return "Error: Missing Lizardfolk data."
                     name_entry = random.choice(lizardfolk_names)
                     name_text = name_entry.get('text', '[Name Error]')
                     name_meaning = name_entry.get('meaning', 'No description available.')
                     return (f"🦎 **Name:** {name_text}\n\n" + f"*{name_meaning}*")

def generate_yuan_ti_name():
                      if not yuan_ti_names: st.error("Yuan-Ti name data missing."); return "Error: Missing Yuan-Ti data."
                      name_entry = random.choice(yuan_ti_names)
                      name_text = name_entry.get('text', '[Name Error]')
                      name_meaning = name_entry.get('meaning', 'Derived from Draconic/Ignan roots.')
                      return (f"🐍 **Name:** {name_text}\n\n" + f"*{name_meaning}*") # Simplified meaning display

def generate_goblin_name():
                       if not goblin_names: st.error("Goblin name data missing."); return "Error: Missing Goblin data."
                       name_entry = random.choice(goblin_names)
                       name_text = name_entry.get('text', '[Name Error]')
                       name_meaning = name_entry.get('meaning', 'No description available.')
                       return (f"👺 **Name:** {name_text}\n\n" + f"*{name_meaning}*")

def generate_gnome_name(gender="Any"):
                        race_key = "gnomish"
                        if race_key not in name_data: return "Error: Gnomish name data not loaded."
                        data = _generate_gnome_name_data(name_data[race_key], gender)
                        if data["error"]: return f"Error: {data['error']}"
                        if not data["name"]: return "Error: Name generation failed silently."
                        meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                        poetic_label = "Poetic Meaning:"
                        return (f"🍄 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_halfling_name(gender="Any"):
                         race_key = "halfling"
                         if race_key not in name_data: return "Error: Halfling name data not loaded."
                         data = _generate_halfling_name_data(name_data[race_key], gender)
                         if data["error"]: return f"Error: {data['error']}"
                         if not data["name"]: return "Error: Name generation failed silently."
                         meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                         poetic_label = "Poetic Meaning:"
                         return (f"🧑‍🌾 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_goliath_name():
                          race_key = "goliath"
                          if race_key not in name_data: return "Error: Goliath name data not loaded."
                          data = _generate_goliath_name_data(name_data[race_key])
                          if data["error"]: return f"Error: {data['error']}"
                          if not data["name"]: return "Error: Name generation failed silently."
                          meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                          poetic_label = "Poetic Meaning:"
                          return (f"🗿 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_minotaur_name(gender="Any"):
                           race_key = "minotaur"
                           if race_key not in name_data: return "Error: Minotaur name data not loaded."
                           data = _generate_minotaur_name_data(name_data[race_key], gender)
                           if data["error"]: return f"Error: {data['error']}"
                           if not data["name"]: return "Error: Name generation failed silently."
                           meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                           poetic_label = "Poetic Meaning:"
                           return (f"🐂 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_bugbear_name():
                            race_key = "bugbear"
                            if race_key not in name_data: return "Error: Bugbear name data not loaded."
                            data = _generate_bugbear_name_data(name_data[race_key])
                            if data["error"]: return f"Error: {data['error']}"
                            if not data["name"]: return "Error: Name generation failed silently."
                            meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                            poetic_label = "Poetic Meaning:"
                            return (f"🐻 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_harengon_name():
                             race_key = "harengon"
                             if race_key not in name_data: return "Error: Harengon name data not loaded."
                             data = _generate_harengon_name_data(name_data[race_key])
                             if data["error"]: return f"Error: {data['error']}"
                             if not data["name"]: return "Error: Name generation failed silently."
                             meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                             poetic_label = "Poetic Meaning:"
                             return (f"🐇 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_leonin_name(gender="Any"):
                              race_key = "leonin"
                              if race_key not in name_data: return "Error: Leonin name data not loaded."
                              data = _generate_leonin_name_data(name_data[race_key], gender)
                              if data["error"]: return f"Error: {data['error']}"
                              if not data["name"]: return "Error: Name generation failed silently."
                              meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                              poetic_label = "Poetic Meaning:"
                              return (f"🦁 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_loxodon_name(gender="Any"):
                               race_key = "loxodon"
                               if race_key not in name_data: return "Error: Loxodon name data not loaded."
                               data = _generate_loxodon_name_data(name_data[race_key], gender)
                               if data["error"]: return f"Error: {data['error']}"
                               if not data["name"]: return "Error: Name generation failed silently."
                               meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                               poetic_label = "Poetic Meaning:"
                               return (f"🐘 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_aasimar_name():
                                race_key = "aasimar"
                                if race_key not in name_data: return "Error: Aasimar name data not loaded."
                                data = _generate_aasimar_name_data(name_data[race_key])
                                if data["error"]: return f"Error: {data['error']}"
                                if not data["name"]: return "Error: Name generation failed silently."
                                meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                                poetic_label = "Poetic Meaning:"
                                return (f"😇 **Name:** {data['name']}\n\n" + "\n".join(meaning_lines) + f"\n\n➔ **{poetic_label}** {data['poetic']}")

def generate_shifter_name():
                                 if not shifter_names: st.error("Shifter name data missing."); return "Error: Missing Shifter data."
                                 name_entry = random.choice(shifter_names)
                                 name_text = name_entry.get('text', '[Name Error]')
                                 name_meaning = name_entry.get('meaning', 'No description available.')
                                 return (f"🐺 **Name:** {name_text}\n\n" + f"*{name_meaning}*")

def generate_githyanki_name(gender="Any"):
                                  race_key = "githyanki"
                                  if race_key not in name_data: return "Error: Githyanki name data not loaded."
                                  data = _generate_githyanki_name_data(name_data[race_key], gender)
                                  if data["error"]: return f"Error: {data['error']}"
                                  if not data["name"]: return "Error: Name generation failed silently."
                                  name_line = f"⚔️ **Name:** {data['name']}"
                                  meaning_lines = [f"- **{p['text']}** = {p.get('meaning', 'N/A')}" for p in data["parts"]]
                                  meanings_block = "\n".join(meaning_lines)
                                  poetic_label = "Poetic Meaning:"
                                  poetic_line = f"➔ **{poetic_label}** {data['poetic']}"
                                  return f"{name_line}\n\n{meanings_block}\n\n{poetic_line}"

# And update generate_common_name similarly:
def generate_common_name(gender="Any"): # Add gender parameter
    """Generates a Common name with meanings for the Name Generator tab."""
    if "common" not in name_data or "first_names" not in name_data["common"] or "surnames" not in name_data["common"]:
        st.error("Missing required Common name data.")
        return "Error: Missing data."

    common_first_names = name_data["common"]["first_names"]
    common_surnames = name_data["common"]["surnames"]
    # --- Filtering logic copied from generate_common_name ---
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
        "")

# Initialize session state variables if they don't exist
if 'npc_output' not in st.session_state:
    st.session_state.npc_output = ""
if 'name_output' not in st.session_state:
    st.session_state.name_output = ""
# (Initialize others as needed, e.g., for selected clan state if desired)

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