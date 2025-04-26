import random
import streamlit as st

VOWELS = "aeiouyáéíóúàèìòùâêîôûäëïöü" # Define vowels (adjust if needed)

def _is_vowel(char):
    """Checks if a single character is a vowel (case-insensitive)."""
    return char.lower() in VOWELS

def _is_smooth_transition(prev_part_ends_vowel, current_part_starts_vowel):
    """Checks if joining two parts is phonetically smooth (avoids vowel+vowel)."""
    # Simple: Avoid vowel + vowel. Could add consonant cluster checks later.
    return not (prev_part_ends_vowel and current_part_starts_vowel)

def _pick_smooth_part(part_list, prev_part_ends_vowel):
    """Picks a random part from the list, preferring smooth transitions."""
    if not part_list:
        # This warning might appear often if middles are optional and empty
        # st.warning("Attempted to pick from an empty name part list.")
        return None

    # Check if parts have the required 'starts_vowel' key
    if not all("starts_vowel" in part for part in part_list if isinstance(part, dict)):
         st.error("Some parts in list lack 'starts_vowel' key.")
         return random.choice(part_list) # Fallback

    smooth_options = [
        part for part in part_list
        if isinstance(part, dict) and _is_smooth_transition(prev_part_ends_vowel, part.get("starts_vowel", False))
    ]

    if smooth_options:
        return random.choice(smooth_options)
    else:
        # Fallback: pick any part if no smooth options exist
        return random.choice(part_list)

def _assemble_name_parts(prefixes, middles, suffixes, gender_filter="Any"):
    """Internal logic to select name parts using smoothing. Returns list of chosen parts."""
    # Ensure input lists contain valid data
    if not prefixes or not isinstance(prefixes, list) or not all(isinstance(p, dict) for p in prefixes):
        st.error("Invalid or empty prefixes list provided to _assemble_name_parts.")
        return []
    if not suffixes or not isinstance(suffixes, list) or not all(isinstance(s, dict) for s in suffixes):
        st.error("Invalid or empty suffixes list provided to _assemble_name_parts.")
        return []
    if middles and (not isinstance(middles, list) or not all(isinstance(m, dict) for m in middles)):
        st.warning("Invalid middles list provided to _assemble_name_parts; ignoring middles.")
        middles = []


    middles_list = middles or [] # Ensure middles_list is always a list

    # Check for required keys early
    if not all("text" in p and "ends_vowel" in p for p in prefixes):
        st.error("Prefix parts are missing required 'text' or 'ends_vowel' keys.")
        return []
    if middles_list and not all("text" in m and "ends_vowel" in m and "starts_vowel" in m for m in middles_list):
        st.error("Middle parts are missing required keys ('text', 'ends_vowel', 'starts_vowel').")
        # Decide how to handle: return error or proceed without middles? Let's proceed without.
        middles_list = []
    if not all("text" in s and "starts_vowel" in s and ("gender" in s or gender_filter == "Any") for s in suffixes):
         # Allow missing 'gender' if filter is 'Any', otherwise require it
         requires_gender = gender_filter != "Any"
         for s in suffixes:
             if requires_gender and "gender" not in s:
                 st.error(f"Suffix '{s.get('text')}' missing required 'gender' key for filtering.")
                 # return [] # Option: fail hard
             if "text" not in s or "starts_vowel" not in s:
                  st.error(f"Suffix '{s.get('text', '[Missing Text]')}' missing required 'text' or 'starts_vowel' key.")
                  # return [] # Option: fail hard
         # If we didn't fail hard, proceed carefully, but warn
         st.warning("Some suffix parts missing required keys, results may be unpredictable.")


    use_middle = random.random() < 0.3 and bool(middles_list)
    chosen_parts = []

    # --- Prefix Selection ---
    try:
        prefix = random.choice(prefixes)
        chosen_parts.append(prefix)
        last_part_ends_vowel = prefix["ends_vowel"]
        last_part_text = prefix["text"]
    except (IndexError, KeyError) as e:
        st.error(f"Error selecting prefix: {e}")
        return []


    # --- Middle Selection ---
    if use_middle:
        try:
            middle = _pick_smooth_part(middles_list, last_part_ends_vowel)
            if middle:
                # Optional: More robust repeat check could go here
                chosen_parts.append(middle)
                last_part_ends_vowel = middle["ends_vowel"]
                last_part_text = middle["text"]
        except (IndexError, KeyError) as e:
            st.warning(f"Error selecting middle part, skipping: {e}")
            # Continue without middle part


    # --- Suffix Selection with Gender Filtering ---
    try:
        suffix_options = list(suffixes) # Create a copy
        if gender_filter != "Any":
            # Filter based on gender, always including Unisex
            filtered_options = [
                s for s in suffix_options
                if s.get("gender") == gender_filter or s.get("gender") == "Unisex"
            ]
            if not filtered_options and suffix_options: # Fallback only if filtering resulted in empty list but original had options
                st.warning(f"No specific {gender_filter} or Unisex suffixes found, using any.")
                # Keep suffix_options as the original full list
            elif filtered_options:
                 suffix_options = filtered_options # Use the filtered list

        if not suffix_options:
            st.error("Suffix options list is empty after filtering (and fallback). Cannot select suffix.")
            return chosen_parts # Return what we have so far

        suffix = _pick_smooth_part(suffix_options, last_part_ends_vowel)
        if suffix:
            # Optional: More robust repeat check
            chosen_parts.append(suffix)
        else:
             st.warning("Could not pick a suitable suffix.")

    except (IndexError, KeyError) as e:
        st.error(f"Error selecting suffix: {e}")
        # Return parts assembled so far

    return chosen_parts


def _generate_poetic_meaning(parts, poetic_gloss_dict):
    """Generates a poetic meaning string from chosen name parts and a gloss dictionary."""
    if not parts or not isinstance(parts, list):
        return "Invalid parts list for poetic meaning."
    if not poetic_gloss_dict or not isinstance(poetic_gloss_dict, dict):
        return "Poetic gloss data missing or invalid."

    # Ensure parts are dictionaries with 'meaning' key
    valid_parts = [p for p in parts if isinstance(p, dict) and "meaning" in p]
    if not valid_parts:
         return "No parts with meanings found."

    # Extract primary meaning keyword for lookup
    keywords = [p["meaning"].split("/")[0].strip().lower() for p in valid_parts] # Use lower for lookup consistency
    if not keywords:
        return "Could not determine meaning keywords."

    # Get random poetic gloss for each keyword
    glosses = []
    for k in keywords:
        options = poetic_gloss_dict.get(k)
        # If direct key match fails, try matching keys in the gloss dict case-insensitively
        if not options:
             insensitive_match = [key for key in poetic_gloss_dict if key.lower() == k]
             if insensitive_match:
                 options = poetic_gloss_dict.get(insensitive_match[0])

        # If still no options, use the keyword itself, capitalized
        if not options or not isinstance(options, list) or not options:
             glosses.append(k.capitalize())
        else:
             glosses.append(random.choice(options))


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
         if num_glosses > 0:
             all_but_last = ", ".join(glosses[:-1])
             last = glosses[-1]
             templates = [f"One connected to {all_but_last}, and {last}"]
         else:
             return "Meaning generation failed (no glosses)."

    # Ensure templates list is not empty before choosing
    return random.choice(templates) if templates else "Could not generate poetic meaning."