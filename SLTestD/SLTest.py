import streamlit as st
import random
from datetime import datetime, timedelta


########## HEADER ##########
st.header("Date Practice!", divider="rainbow")



########## FORMAT QUESTION ##########
dateFormat = st.selectbox("Date Format", ["MM/DD/YYYY", "DD.MM.YYYY", "Month DD, YYYY", "DD Mo YYYY"])
#dateFormat = "MM/DD/YYYY"

if dateFormat == "MM/DD/YYYY" or dateFormat == "Month DD, YYYY":
    calendarDateFormat = "MM/DD/YYYY"
else:
    calendarDateFormat = "DD.MM.YYYY"



########## CUSTOM RANGE ##########
st.markdown('#####')

customRange = st.toggle("Custom date range?")

if customRange == False:
    startDate = datetime(1900,1,1).date()
    endDate = datetime(2100,1,1).date()

if customRange == True:
    startDate = st.date_input("Start of custom range", min_value=datetime(1600,1,1), max_value=datetime(2600,1,1), format=calendarDateFormat)
    endDate = st.date_input("End of custom range", min_value=startDate, max_value=datetime(2600,1,1), format=calendarDateFormat)



########## DATE RANGE HEADER ##########
if dateFormat == "MM/DD/YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%m/%d/%Y")} to {endDate.strftime("%m/%d/%Y")}")
elif dateFormat == "DD.MM.YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%d.%m.%Y")} to {endDate.strftime("%d.%m.%Y")}")
elif dateFormat == "Month DD, YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%B %d, %Y")} to {endDate.strftime("%B %d, %Y")}")
elif dateFormat == "DD Mo YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%d %b %Y")} to {endDate.strftime("%d %b %Y")}")



########## RANDOM DATE GENERATION ##########
def generate_random_date():
    randomDays = random.randint(0, (endDate - startDate).days)
    randomDate = startDate + timedelta(days=randomDays)
    return randomDate



########## START SESSION STATE VARIABLES ##########
if "gameStarted" not in st.session_state:
    st.session_state.gameStarted = False

if "totalCorrect" not in st.session_state:
    st.session_state.totalCorrect = 0



########## GENERATE DATE BUTTON ##########
st.markdown('#####')
generateButton = st.button("Generate a new random date")

if generateButton == True:
    randomDate = generate_random_date()
    st.session_state.correctDay = randomDate.strftime("%A")

    ########## SAVE DATE FORMATS ##########
    st.session_state.randomDateEU = randomDate.strftime("%d.%m.%Y")
    st.session_state.randomDateUS = randomDate.strftime("%m/%d/%Y")
    st.session_state.randomDateMonth = randomDate.strftime("%B %d, %Y")
    st.session_state.randomDateMo = randomDate.strftime("%d %b %Y")

    ########## FORMAT TENSES ##########
    if randomDate > datetime.now().date():
        st.session_state.tense1 = "will"
        st.session_state.tense2 = " be"
    if randomDate == datetime.now().date():
        st.session_state.tense1 = "is"
        st.session_state.tense2 = ""
    if randomDate < datetime.now().date():
        st.session_state.tense1 = "was"
        st.session_state.tense2 = ""


    st.session_state.gameStarted = True


#Give correct answer for testing
#st.write(st.session_state.correctDay)

########## DATE GUESSING ##########
if st.session_state.gameStarted == True:
    st.write(st.session_state.correctDay)

    ########## QUESTION SELECTBOX ##########
    if dateFormat == "MM/DD/YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateUS}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    elif dateFormat == "DD.MM.YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateEU}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    elif dateFormat == "Month DD, YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateMonth}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    elif dateFormat == "DD Mo YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateMo}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))

    ########## GUESSING BUTTON ##########
    guessButton = st.button("Enter Guess")
    if guessButton == True:
        if dayGuess == st.session_state.correctDay:
            st.write("Correct!")
            st.session_state.totalCorrect += 1
        else:
            st.write("Incorrect")



########## SCORE METRICS ##########

### ANSWER METRICS ###
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Correct", value=st.session_state.totalCorrect, delta="+1")
with col2:
    st.metric(label="Percent Correct Guesses", value="100%", delta="+0")
with col3:
    st.metric(label="Current Streak", value="4", delta="+1")
with col4:
    st.metric(label="Longest Streak", value="10", delta="", delta_color="off")

### TIME METRICS ###
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Previous Answer Time", value="123", delta="+5")
with col2:
    st.metric(label="10-Answer Average Time", value="123", delta="+5")
with col3:
    st.metric(label="Fastest Time", value="12.25s", delta="+5")
with col4:
    st.metric(label="Fastest 10-Answer Average", value="123", delta="+5")





########## TO DO ##########
# Option for auto-generate on correct guess
# timer
# Overall scorekeeping
# Intro and other explanation pages
# Link to numberphile video?
# Other practice: just doomsdays, 12s or 16s practice
# Check current date, write was if question date is in past or is if in present
# Add option to write dates in words?
# Add settings page with all of the options
# Add option to input answers differently

###DONE###
# Answer checking system (use first [0:1] of the guess)
# Add preset time range(s), make custom just an option
# Generate new date button
# Use calendar input
