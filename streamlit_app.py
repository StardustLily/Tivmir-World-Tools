import streamlit as st
import random
import json
import os

# Set page config first!
st.set_page_config(page_title="Tivmir World Tools", layout="centered")

# === Load Data Functions ===
def load_json(filename):
    try:
        path = os.path.join("data", filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return [] if "list" in filename else {}

# === Load Data ===
races = load_json("races.json")
npc_attributes = load_json("npc_attributes.json")
tabaxi_prefixes = load_json("tabaxi_prefixes.json")
tabaxi_middles = load_json("tabaxi_middles.json")
tabaxi_suffixes = load_json("tabaxi_suffixes.json")
tabaxi_clans = load_json("tabaxi_clans.json")
elven_prefixes = load_json("elven_prefixes.json")
elven_middles = load_json("elven_middles.json")
elven_suffixes = load_json("elven_suffixes.json")
elven_poetic_gloss = load_json("elven_poetic_gloss.json")

# === Emoji Icons ===
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

# === Generate NPC Function ===
def generate_npc():
    race = random.choice(races)
    npc_lines = [
        "💼 **Basic Info**",
        f"🧬 **Race:** {race['name']} ({race['rarity']})",
        f"🌍 **Region:** {race['region']}",
        f"📖 **Lore:** {race['description']}",
        "✶" * 25,
        "🎭 **Personality & Story**"
    ]

    for category, options in npc_attributes.items():
        clean_category = category.strip()
        icon = icons.get(clean_category, "•")
        choice = random.choice(options)
        npc_lines.append(f"{icon} **{clean_category}:** {choice}")

    return "\n\n".join(npc_lines)

# === Generate Tabaxi Name Function ===
def generate_tabaxi_name(selected_clan):
    use_middle = random.random() < 0.4
    parts = []

    prefix = random.choice(tabaxi_prefixes)
    parts.append(prefix)

    if use_middle:
        middle = random.choice(tabaxi_middles)
        parts.append(middle)

    suffix = random.choice(tabaxi_suffixes)
    parts.append(suffix)

    full_name = "".join(p["text"] for p in parts)

    meaning_lines = [f"• {p['text']} = {p['meaning']}" for p in parts]

    poetic = random.choice([
        f"Voice of the dunes, child of the stars.",
        f"Shadowstep on silent paws.",
        f"Born under a moon that never wanes."
    ])

    clan_info = next((c for c in tabaxi_clans if c["name"] == selected_clan), None)
    if clan_info:
        clan_desc = (
            f"\n\n🏡 **Clan:** {clan_info['name']}\n\n"
            f"• **Region:** {clan_info['region']}\n\n"
            f"• **Traits:** {clan_info['traits']}\n\n"
            f"• **Twist:** {clan_info['twist']}"
        )
    else:
        clan_desc = ""

    return (
        f"🐾 **Name:** {full_name}\n\n"
        + "\n\n".join(meaning_lines)
        + f"\n\n➔ **Poetic Meaning:** {poetic}{clan_desc}"
    )

# === Generate Elven Name Function ===
def generate_elven_name():
    use_middle = random.random() < 0.4
    prefix = random.choice(elven_prefixes)
    parts = [prefix]

    if use_middle:
        middle = random.choice(elven_middles)
        suffix = random.choice(elven_suffixes)
        parts += [middle, suffix]
    else:
        suffix = random.choice(elven_suffixes)
        parts += [suffix]

    full_name = "".join(p["text"] for p in parts)

    # Make the breakdown a proper separate list
    meanings = [f"- **{p['text']}** = {p['meaning']}" for p in parts]

    # Poetic generation
    keywords = [p["meaning"].split("/")[0].strip() for p in parts]
    glosses = [random.choice(elven_poetic_gloss.get(k, [k])) for k in keywords]

    if len(glosses) == 2:
        poetic = random.choice([
            f"{glosses[0].title()} of {glosses[1]}",
            f"Bearer of {glosses[1]}, born of {glosses[0]}",
            f"A soul touched by {glosses[0]} and {glosses[1]}"
        ])
    else:
        poetic = random.choice([
            f"One who walks with {glosses[0]}, guided by {glosses[1]}, keeper of {glosses[2]}",
            f"A spirit shaped by {glosses[0]}, voice of {glosses[1]}, hand of {glosses[2]}"
        ])

    return (
        f"🌿 **Name:** {full_name}\n\n" +
        "\n".join(meanings) +  # <--- now each syllable part is properly bullet-pointed
        f"\n\n➔ **Poetic Meaning:** {poetic}"
    )


# === UI ===
st.title("🌸 Tivmir World Tools")
tabs = st.tabs(["🌿 NPC Generator", "🔤 Name Generator"])

with tabs[0]:
    st.header("🌿 NPC Generator")
    if st.button("Generate NPC", key="npc_button"):
        st.markdown(generate_npc())

with tabs[1]:
    st.header("🔤 Name Generator")
    race = st.selectbox("Choose a race:", ["Elven", "Tabaxi"], key="name_race")
    if race == "Tabaxi":
        clan_names = [clan["name"] for clan in tabaxi_clans]
        selected_clan = st.selectbox("Choose a Tabaxi clan:", clan_names, key="tabaxi_clan")
        if st.button("Generate Tabaxi Name", key="tabaxi_name_button"):
            st.markdown(generate_tabaxi_name(selected_clan))
    else:
        if st.button("Generate Elven Name", key="elven_name_button"):
            st.markdown(generate_elven_name())
