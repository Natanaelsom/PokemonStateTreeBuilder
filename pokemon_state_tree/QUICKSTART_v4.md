# Quick Start Guide - v4.0

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

Or directly:
```bash
python gui.py
```

## Features Overview

### 1. Trainer Management

**Selecting a Trainer:**
- Go to "Tree Editor" tab
- Use the **Trainer** dropdown at the top
- Click "Next Trainer" to auto-navigate to the next non-defeated trainer

**Marking Trainer Status:**
- Select a trainer from dropdown
- Click **"Mark Defeated"** to mark as defeated
- Click **"Mark Skipped"** to mark as skipped
- Status appears in dropdown: `Trainer Name [DEFEATED]` or `Trainer Name [SKIPPED]`

### 2. Editing States

**Add/Remove States:**
- Click **"Next Turn"** to add a new state
- Click **"Add Possibility"** to add alternative battle paths
- Click **"Remove"** to delete current state

**Edit State Properties:**
- **Name:** Enter state name and click "Update"
- **Type:** Select "single" or "double" battle
- **Weather:** Choose weather effect (None, Rain, Sandstorm, etc.)

### 3. Pokémon Selection

**For Player Pokémon (Self/Self2):**
- Select tab "Self" or "Self2"
- Search/select Pokémon from your Box
- Only Pokémon in your Box appear

**For Enemy Pokémon (Enemy/Enemy2):**
- Select tab "Enemy" or "Enemy2"
- Search/select Pokémon from the selected trainer's team
- List updates automatically when you switch trainers

### 4. Visual Tree

- Central canvas shows your state tree graphically
- Click on states to select and edit them
- Scroll or use scrollbars to navigate

### 5. Transitions

- Bottom panel shows transitions from current state
- Manage which states connect together

---

## Keyboard Navigation

| Action | Key |
|--------|-----|
| Next Turn | Click button or Alt+N |
| Add Possibility | Click button or Alt+A |
| Remove State | Click button or Alt+R |
| Next Trainer | Click button or Alt+T |
| Mark Defeated | Click button or Alt+D |
| Mark Skipped | Click button or Alt+S |

---

## Data Files

### Test Data
- `test_box.json` - Sample Box with 10 Pokémon
- `test_enemy_library.json` - Sample Trainers (Brock, Misty, Cynthia, Lance)

### Generating New Test Data
```bash
python setup_test_data.py
```

This generates fresh test data in JSON format.

---

## Tab Navigation

### Tree Editor
- Main editing interface for states
- Trainer selector at top
- Visual tree in center
- Pokémon editor and transitions below

### Box (Allies)
- Manage your team of Pokémon
- Add/remove/view Box Pokémon

### Enemy Library
- Manage opponent trainers
- View trainer teams
- Add/edit/remove trainers

---

## Tips & Tricks

1. **Smart Navigation:** Use "Next Trainer" to cycle through non-defeated trainers automatically

2. **Status Tracking:** Mark trainers as you battle them - status displays in dropdown

3. **Quick Pokémon Selection:** SearchableCombobox filters as you type

4. **Dual Battles:** Select "double" battle type to edit Self2 and Enemy2 slots

5. **Trainer Teams:** Only show relevant Pokémon for each trainer when editing

---

## Troubleshooting

**"No trainers in dropdown"**
- Go to "Enemy Library" tab
- Add trainers to the library first
- Return to "Tree Editor"

**"Pokémon not showing in selection"**
- For Self/Self2: Make sure Pokémon are in Box (Enemy Library tab)
- For Enemy: Make sure selected trainer has Pokémon

**"Trainer marked as defeated but still appears"**
- This is correct - defeated trainers remain in list but marked as [DEFEATED]
- Use "Next Trainer" to skip them automatically

---

## Project Structure

```
pokemon_state_tree/
├── gui.py                    # Main GUI application
├── main.py                   # Entry point
├── state.py                  # State logic
├── pokemon.py                # Pokémon class
├── library.py                # Box/Trainer management
├── state_tree.py             # Tree structure
├── transition.py             # Transitions
├── custom_widgets.py         # Tkinter widgets
├── visualizer.py             # Canvas rendering
├── pokemon_data.py           # Pokémon database
├── pokemon_parser.py         # Data parsing
├── requirements.txt          # Dependencies
├── setup_test_data.py        # Test data generator
├── README.md                 # Full documentation
├── START_HERE.md             # Getting started
└── test_*.json               # Sample data
```

---

## Version Info

- **Version:** 4.0
- **Python:** 3.7+
- **GUI Framework:** Tkinter
- **Status:** Production Ready
- **Last Updated:** December 2024

---

## Support & Documentation

- Full documentation: See [README.md](README.md)
- Getting started: See [START_HERE.md](START_HERE.md)
- Implementation details: See [IMPLEMENTATION_REPORT_v4.md](IMPLEMENTATION_REPORT_v4.md)
- Completion summary: See [V4_COMPLETION_SUMMARY.md](V4_COMPLETION_SUMMARY.md)

---

**Enjoy building your Pokémon battle state trees! 🎮**
