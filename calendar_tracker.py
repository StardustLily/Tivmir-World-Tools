import streamlit as st
from data_loader import calendar_data # Import the loaded data

# --- Calendar Constants ---
MONTHS = calendar_data.get("months", [])
YEAR_SUFFIX = calendar_data.get("year_suffix", "LD")
DAYS_IN_MONTH = {month["name"]: month["days"] for month in MONTHS}
MONTH_NAMES = [month["name"] for month in MONTHS]

# --- Session State Initialization ---
def initialize_calendar_state(start_year=1478, start_month_index=0, start_day=1):
    """Initializes the calendar date in session state if not already present."""
    if 'current_year' not in st.session_state:
        st.session_state.current_year = start_year
    if 'current_month_index' not in st.session_state:
        st.session_state.current_month_index = start_month_index # Index (0-11)
    if 'current_day' not in st.session_state:
        st.session_state.current_day = start_day

# --- Core Logic Functions ---
def get_current_date_string():
    """Formats the current date from session state into a string."""
    if not MONTH_NAMES: return "Error: Calendar not loaded"
    try:
        year = st.session_state.current_year
        month_index = st.session_state.current_month_index
        day = st.session_state.current_day
        month_name = MONTH_NAMES[month_index]
        return f"{month_name} {day}, {year} {YEAR_SUFFIX}"
    except (KeyError, IndexError, TypeError) as e:
        st.error(f"Error retrieving date state: {e}")
        return "Error: Date State Invalid"
    except Exception as e:
        st.error(f"Unexpected error formatting date: {e}")
        return "Error: Date Format Error"


def advance_day(days_to_advance=1):
    """Advances the date in session state by a number of days."""
    if not MONTH_NAMES or not DAYS_IN_MONTH:
        st.error("Cannot advance day: Calendar data not loaded.")
        return

    try:
        current_day = st.session_state.current_day
        current_month_index = st.session_state.current_month_index
        current_year = st.session_state.current_year

        for _ in range(days_to_advance):
            month_name = MONTH_NAMES[current_month_index]
            days_in_current_month = DAYS_IN_MONTH[month_name]
            # TODO: Add leap year logic here if desired later

            current_day += 1
            if current_day > days_in_current_month:
                current_day = 1 # Reset to first day
                current_month_index += 1 # Advance month
                if current_month_index >= len(MONTH_NAMES):
                    current_month_index = 0 # Reset to first month
                    current_year += 1 # Advance year

        # Update session state
        st.session_state.current_day = current_day
        st.session_state.current_month_index = current_month_index
        st.session_state.current_year = current_year

    except (KeyError, IndexError, TypeError) as e:
        st.error(f"Error advancing date state: {e}")
    except Exception as e:
        st.error(f"Unexpected error advancing date: {e}")

# --- Optional Convenience Functions ---
def advance_week():
    """Advances the date by 7 days."""
    advance_day(7)

def advance_month():
     """Advances the date to the 1st of the next month."""
     if not MONTH_NAMES or not DAYS_IN_MONTH:
        st.error("Cannot advance month: Calendar data not loaded.")
        return
     try:
        current_month_index = st.session_state.current_month_index
        current_year = st.session_state.current_year

        next_month_index = current_month_index + 1
        next_year = current_year
        if next_month_index >= len(MONTH_NAMES):
            next_month_index = 0
            next_year += 1

        # Update session state
        st.session_state.current_day = 1
        st.session_state.current_month_index = next_month_index
        st.session_state.current_year = next_year
     except (KeyError, IndexError, TypeError) as e:
        st.error(f"Error advancing month state: {e}")
     except Exception as e:
        st.error(f"Unexpected error advancing month: {e}")