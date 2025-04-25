import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Windows 8.1+ DPI awareness
except Exception:
    pass

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import random
import json
import os

class TivmirApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self._ELVEN_PREFIXES = self._load_elven_data("elven_prefixes.json")
        self._ELVEN_MIDDLES = self._load_elven_data("elven_middles.json")
        self._ELVEN_SUFFIXES = self._load_elven_data("elven_suffixes.json")
        self._ELVEN_POETIC_GLOSS = self._load_elven_data("elven_poetic_gloss.json")
        self._TABAXI_CLANS = self._load_tabaxi_clans()
        self._RACES = self._load_races()
        self._NPC_ATTRIBUTES = self._load_npc_attributes()

        self.title("🌸 Tivmir World Tools")
        self.geometry("1150x950")
        self.configure(bg="#f5f0ff")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook.Tab", padding=[12, 6], font=('Segoe UI', 11, 'bold'))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        npc_tab = self.build_npc_tab(notebook)
        name_tab = self.build_name_tab(notebook)

        notebook.add(npc_tab, text="🧝 NPC Generator")
        notebook.add(name_tab, text="🔤 Name Generator")

    def build_npc_tab(self, parent):
        frame = tk.Frame(parent, bg="#ece4f8")

        self.npc_output = tk.Text(
            frame, height=15, width=72, wrap=tk.WORD, font=("Segoe UI", 11),
            fg="#2b2d42", bg="#fdfcff", padx=10, pady=10, relief=tk.FLAT
        )
        self.npc_output.pack(pady=(20, 10))

        self.npc_output.tag_configure("category_bold", font=("Segoe UI", 11, "bold"))
        self.npc_output.tag_configure("header", font=("Segoe UI", 12, "bold"), spacing3=6)

        generate_button = tk.Button(
            frame, text="Generate NPC", font=("Segoe UI", 11, "bold"),
            bg="#9d4edd", fg="white", padx=10, pady=6,
            command=self.generate_npc
        )
        generate_button.pack(pady=(0, 10))

        return frame

    def generate_npc(self):
        race = random.choice(self._RACES)
        
        self.npc_output.config(state=tk.NORMAL)
        self.npc_output.delete("1.0", tk.END)

        # Header: Race Details
        self.npc_output.insert(tk.END, "📛 Basic Info\n", "header")
        self.npc_output.insert(tk.END, f"🧬 Race: ", "category_bold")
        self.npc_output.insert(tk.END, f"{race['name']} ({race['rarity']})\n")
        self.npc_output.insert(tk.END, f"🌍 Region: ", "category_bold")
        self.npc_output.insert(tk.END, f"{race['region']}\n")
        self.npc_output.insert(tk.END, f"📖 Lore: ", "category_bold")
        self.npc_output.insert(tk.END, f"{race['description']}\n")
        self.npc_output.insert(tk.END, "✦" * 25 + "\n")

        # Header: Personality and Details
        self.npc_output.insert(tk.END, "🎭 Personality & Story\n", "header")

        icons = {
            "Appearance": "👁",
            "Worships": "🙏",
            "Quirk": "🎭",
            "Secret": "🔒",
            "Goal": "🎯",
            "Fear": "😨",
            "Profession": "🔮",
            "Ally": "🤝"
        }

        for category, options in self._NPC_ATTRIBUTES.items():
            clean_category = category.strip()
            icon = icons.get(clean_category, "•")
            choice = random.choice(options)
            self.npc_output.insert(tk.END, f"{icon}\u200A{clean_category}: ", "category_bold")
            self.npc_output.insert(tk.END, f"{choice}\n")

        self.npc_output.config(state=tk.DISABLED)

    def _write_category(self, label, options):
        choice = random.choice(options)
        self.npc_output.insert(tk.END, f"{label}: ", "category")
        self.npc_output.insert(tk.END, choice + "\n")

    def build_name_tab(self, parent):
        frame = tk.Frame(parent, bg="#ece4f8")

        # Dropdown for race selection
        race_label = tk.Label(frame, text="Select Race:", bg="#ece4f8", font=("Segoe UI", 11))
        race_label.pack(pady=(20, 0))

        self.race_var = tk.StringVar(value="Elven")
        race_selector = ttk.Combobox(frame, textvariable=self.race_var, values=["Elven", "Tabaxi"], state="readonly", font=("Segoe UI", 11))
        race_selector.pack(pady=(0, 10))
        race_selector.bind("<<ComboboxSelected>>", self.toggle_clan_dropdown)

        # Clan dropdown (initially hidden)
        self.clan_label = tk.Label(frame, text="Select Clan:", bg="#ece4f8", font=("Segoe UI", 11))
        self.clan_dropdown = ttk.Combobox(frame, state="readonly", font=("Segoe UI", 11))
        self.clan_label.pack_forget()
        self.clan_dropdown.pack_forget()

        # Output text area
        self.name_output = tk.Text(frame, height=15, width=60, wrap=tk.WORD, font=("Segoe UI", 11), bg="#fdfcff")
        self.name_output.pack(pady=(10, 10))

        # Generate button
        generate_button = tk.Button(
            frame, text="Generate Name", font=("Segoe UI", 11, "bold"),
            bg="#9d4edd", fg="white", padx=10, pady=6,
            command=self.generate_name
        )
        generate_button.pack(pady=(0, 10))

        return frame

    def toggle_clan_dropdown(self, event=None):
        if self.race_var.get() == "Tabaxi":
            self.clan_label.pack(pady=(0, 2))
            self.clan_dropdown.pack(pady=(0, 10))
            self.clan_dropdown["values"] = [clan["name"] for clan in self._TABAXI_CLANS]
            self.clan_dropdown.current(0)
        else:
            self.clan_label.pack_forget()
            self.clan_dropdown.pack_forget()

    def generate_name(self):
        selected_race = self.race_var.get()
        if selected_race == "Elven":
            name = self.generate_elven_name()
        elif selected_race == "Tabaxi":
            name = self.generate_tabaxi_name()
        else:
            name = f"⚠️ Unknown race selected: {selected_race}"

        self.name_output.delete("1.0", tk.END)
        self.name_output.insert(tk.END, name)

    def _load_tabaxi_clans(self):
        try:
            path = os.path.join(os.path.dirname(__file__), "data", "tabaxi_clans.json")
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading Tabaxi clans: {e}")
            return []

    def _load_elven_data(self, filename):
        try:
            path = os.path.join(os.path.dirname(__file__), "data", filename)
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return []

    def _load_races(self):
        try:
            path = os.path.join(os.path.dirname(__file__), "data", "races.json")
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading races: {e}")
            return []

    def _load_npc_attributes(self):
        try:
            path = os.path.join(os.path.dirname(__file__), "data", "npc_attributes.json")
            with open(path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                return {k.strip(): v for k, v in raw_data.items()}
        except Exception as e:
            print(f"Error loading NPC attributes: {e}")
            return {}

    # === Internal Helpers ===
    def _is_smooth(self, a_ev, b_sv):
        return not (a_ev and b_sv)

    def _pick_smooth(self, parts, prev_ev):
        return random.choice([
            p for p in parts if self._is_smooth(prev_ev, p["starts_vowel"])
        ]) or random.choice(parts)

    def _generate_poetic_line(self, parts, gloss_dict):
        keywords = [p["meaning"].split("/")[0].strip() for p in parts]
        glosses = [random.choice(gloss_dict.get(k, [k])) for k in keywords]
        return random.choice([
            f"{glosses[0].title()} of {glosses[1]}",
            f"Bearer of {glosses[1]}, born of {glosses[0]}",
            f"A soul touched by {glosses[0]} and {glosses[1]}"
        ]) if len(glosses) == 2 else random.choice([
            f"One who walks with {glosses[0]}, guided by {glosses[1]}, keeper of {glosses[2]}",
            f"A spirit shaped by {glosses[0]}, voice of {glosses[1]}, hand of {glosses[2]}",
        ])

    # === Name Generator ===
    def generate_elven_name(self):
        use_middle = random.random() < 0.4
        prefix = random.choice(self._ELVEN_PREFIXES)
        parts = [prefix]

        if use_middle:
            middle = self._pick_smooth(self._ELVEN_MIDDLES, prefix["ends_vowel"])
            suffix = self._pick_smooth(self._ELVEN_SUFFIXES, middle["ends_vowel"])
            parts += [middle, suffix]
        else:
            suffix = self._pick_smooth(self._ELVEN_SUFFIXES, prefix["ends_vowel"])
            parts += [suffix]

        full_name = "".join(p["text"] for p in parts)
        meaning_lines = [f"• {p['text']} = {p['meaning']}" for p in parts]
        poetic = self._generate_poetic_line(parts, self._ELVEN_POETIC_GLOSS)
        extra = "\n📝 " + random.choice([
            f"Known among the Twilight Courts as “{full_name[-5:]} the Quiet Bloom.”",
            f"A name whispered in forest prayers during equinox.",
            f"Traditionally given to artists born beneath moonlight.",
            f"Once sung by dream-priests of the Vale in mourning rites.",
            f"Believed to bring luck in journeys across misted rivers.",
        ]) if random.random() < 0.4 else ""

        return f"🌿 Name: {full_name}\n\n" + "\n".join(meaning_lines) + f"\n\n➤ Poetic Meaning: {poetic}{extra}"
        if extra_note:
            output += extra_note
        return output

    def generate_tabaxi_name(self):
        tabaxi_prefixes = [
            {"text": "Zaha", "meaning": "desert / endurance"},
            {"text": "Teli", "meaning": "wind / voice"},
            {"text": "Ranu", "meaning": "snow / peace"},
            {"text": "Ashi", "meaning": "flame / spark"},
            {"text": "Xira", "meaning": "cunning / watchful"},
            {"text": "Nalu", "meaning": "moon / cycle"},
            {"text": "Kael", "meaning": "noble / fierce"},
            {"text": "Jako", "meaning": "hunter / heir"},
        ]

        tabaxi_middles = [
            {"text": "rren", "meaning": "strength"},
            {"text": "mari", "meaning": "grace / gift"},
            {"text": "luz", "meaning": "light"},
            {"text": "zako", "meaning": "whisper / stealth"},
            {"text": "mena", "meaning": "trade / wealth"},
            {"text": "halo", "meaning": "aura / guide"},
        ]

        tabaxi_suffixes = [
            {"text": "ara", "meaning": "essence / soul"},
            {"text": "len", "meaning": "frost / clarity"},
            {"text": "ion", "meaning": "sun / pride"},
            {"text": "ira", "meaning": "wisdom / age"},
            {"text": "oné", "meaning": "blessed"},
            {"text": "anir", "meaning": "breath / spirit"},
        ]

        tabaxi_gloss = {
            "desert": ["sun-worn", "enduring flame", "dune-born"],
            "wind": ["whisper", "sky singer", "traveler's breath"],
            "snow": ["frost-born", "quiet one", "crystal soul"],
            "flame": ["spark", "ember heart", "wildfire"],
            "cunning": ["sharp eye", "quick paw", "shadowstep"],
            "moon": ["moonlit soul", "cycle-weaver", "tidebound"],
            "noble": ["high-born", "graced", "lion-blooded"],
            "hunter": ["pathfinder", "arrow soul", "stalker's grace"],
            "strength": ["unyielding", "pillar", "twinfang"],
            "grace": ["glimmer", "gifted step", "soft song"],
            "light": ["radiance", "gleam", "morning gaze"],
            "whisper": ["hushed tone", "veilvoice", "shade-singer"],
            "trade": ["coinwise", "goldtongue", "market-wise"],
            "aura": ["guide", "haloed one", "presence"],
            "essence": ["true self", "heart", "core"],
            "frost": ["sharp air", "still touch", "ice-born"],
            "sun": ["goldflame", "bright roar", "dawnfire"],
            "wisdom": ["sage-borne", "old knowing", "spirit-thought"],
            "blessed": ["favored one", "spirit-kissed", "light-touched"],
            "breath": ["lifebreath", "soft wind", "sigh of stars"]
        }

        def generate_poetic(parts):
            keywords = [p["meaning"].split("/")[0].strip() for p in parts]
            glosses = [random.choice(tabaxi_gloss.get(k, [k])) for k in keywords]
            if len(glosses) == 2:
                lines = [
                    f"{glosses[0].title()} of {glosses[1]}",
                    f"Voice of the {glosses[1]}, born of {glosses[0]}",
                    f"{glosses[0].title()} soul, touched by {glosses[1]}",
                ]
            else:
                lines = [
                    f"One who walks with {glosses[0]}, gifted by {glosses[1]}, soul of {glosses[2]}",
                    f"Child of {glosses[0]} and {glosses[1]}, spirit of {glosses[2]}",
                    f"{glosses[2].title()} made flesh, carved from {glosses[0]} and {glosses[1]}",
                ]
            return random.choice(lines)

        use_middle = random.random() < 0.4
        prefix = random.choice(tabaxi_prefixes)

        if use_middle:
            middle = random.choice(tabaxi_middles)
            suffix = random.choice(tabaxi_suffixes)
            full_name = prefix["text"] + middle["text"] + suffix["text"]
            parts = [prefix, middle, suffix]
        else:
            suffix = random.choice(tabaxi_suffixes)
            full_name = prefix["text"] + suffix["text"]
            parts = [prefix, suffix]

        meaning_lines = [f"• {p['text']} = {p['meaning']}" for p in parts]
        poetic_translation = generate_poetic(parts)
        # 🧩 Get selected clan and its data
        selected_clan_name = self.clan_dropdown.get()
        clan_data = next((c for c in self._TABAXI_CLANS if c["name"] == selected_clan_name), None)

        clan_block = ""
        if clan_data:
            clan_block = f"\n\n🏛 Clan: {clan_data['name']}\n" \
                         f"• Meaning: {clan_data['meaning']}\n" \
                         f"• Region: {clan_data['region']}\n" \
                         f"• Traits: {clan_data['traits']}\n" \
                         f"• Twist: {clan_data['twist']}"

        return f"🐾 Name: {full_name}\n\n" + "\n".join(meaning_lines) + f"\n\n➤ Poetic Meaning: {poetic_translation}{clan_block}"
    
        return output


if __name__ == "__main__":
    app = TivmirApp()
    app.mainloop()
