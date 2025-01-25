import streamlit as st
import random
from datetime import datetime, timedelta



########## HEADER ##########
st.header("Date Practice!", divider="rainbow")



########## START SESSION STATE VARIABLES ##########
if "gameStarted" not in st.session_state:
    st.session_state.gameStarted = False
if "guessingStarted" not in st.session_state:
    st.session_state.guessingStarted = False

if "startDate" not in st.session_state:
    st.session_state.startDate = datetime(1900,1,1).date()
if "endDate" not in st.session_state:
    st.session_state.endDate = datetime(2100,1,1).date()
if "dateFormat" not in st.session_state:
    st.session_state.dateFormat = "MM/DD/YYYY"

if "totalCorrect" not in st.session_state:
    st.session_state.totalCorrect = 0
if "totalIncorrect" not in st.session_state:
    st.session_state.totalIncorrect = 0
if "totalGuesses" not in st.session_state:
    st.session_state.totalGuesses = 0
if "currentStreak" not in st.session_state:
    st.session_state.currentStreak = 0
if "longestStreak" not in st.session_state:
    st.session_state.longestStreak = 0

if "guessPercentage" not in st.session_state:
    st.session_state.guessPercentage = 0



########## DATE RANGE HEADER ##########
dateRangeSubheader = st.empty()



########## EXTRA OPTIONS EXPANDER ##########
with st.expander("Extra Date Options"):

    ########## FORMAT QUESTION ##########
    st.session_state.dateFormat = st.selectbox("Date Format", ["MM/DD/YYYY", "DD.MM.YYYY", "Month DD, YYYY", "DD Mo YYYY"])

    if st.session_state.dateFormat == "MM/DD/YYYY" or st.session_state.dateFormat == "Month DD, YYYY":
        calendarDateFormat = "MM/DD/YYYY"
    else:
        calendarDateFormat = "DD.MM.YYYY"
    


    ########## CUSTOM RANGE ##########
    st.divider()

    customRange = st.toggle("Custom date range?")

    if customRange == False:
        st.session_state.startDate = datetime(1900,1,1).date()
        st.session_state.endDate = datetime(2100,1,1).date()

    if customRange == True:
        st.session_state.startDate = st.date_input("Start of custom range", min_value=datetime(1600,1,1), max_value=datetime(2600,1,1), format=calendarDateFormat)
        st.session_state.endDate = st.date_input("End of custom range", min_value=st.session_state.startDate, max_value=datetime(2600,1,1), format=calendarDateFormat)



    ########## DATE RANGE HEADER ##########
    if st.session_state.dateFormat == "MM/DD/YYYY":
        dateRangeSubheader.subheader(f"Date Range: {st.session_state.startDate.strftime("%m/%d/%Y")} to {st.session_state.endDate.strftime("%m/%d/%Y")}")
    elif st.session_state.dateFormat == "DD.MM.YYYY":
        dateRangeSubheader.subheader(f"Date Range: {st.session_state.startDate.strftime("%d.%m.%Y")} to {st.session_state.endDate.strftime("%d.%m.%Y")}")
    elif st.session_state.dateFormat == "Month DD, YYYY":
        dateRangeSubheader.subheader(f"Date Range: {st.session_state.startDate.strftime("%B %d, %Y")} to {st.session_state.endDate.strftime("%B %d, %Y")}")
    elif st.session_state.dateFormat == "DD Mo YYYY":
        dateRangeSubheader.subheader(f"Date Range: {st.session_state.startDate.strftime("%d %b %Y")} to {st.session_state.endDate.strftime("%d %b %Y")}")





########## RANDOM DATE GENERATION ##########
def generate_random_date():
    randomDays = random.randint(0, (st.session_state.endDate - st.session_state.startDate).days)
    randomDate = st.session_state.startDate + timedelta(days=randomDays)
    return randomDate



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


########## ONCE GAME STARTED ##########
if st.session_state.gameStarted == True:
    st.write(st.session_state.correctDay)

    ########## QUESTION SELECTBOX ##########
    if st.session_state.dateFormat == "MM/DD/YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateUS}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    elif st.session_state.dateFormat == "DD.MM.YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateEU}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    elif st.session_state.dateFormat == "Month DD, YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateMonth}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    elif st.session_state.dateFormat == "DD Mo YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateMo}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))

    ########## GUESSING BUTTON ##########
    guessButton = st.button("Enter Guess")
    col1, col2 = st.columns(2)
    with col2:
        st.write("⠀")
    if guessButton == True:
        if dayGuess == st.session_state.correctDay:
            with col1:
                st.write("Correct!")

            st.session_state.totalCorrect += 1
            st.session_state.currentStreak += 1
            st.session_state.totalGuesses += 1

        else:
            with col1:
                st.write("Incorrect")

            st.session_state.totalIncorrect += 1
            st.session_state.currentStreak = 0
            st.session_state.totalGuesses += 1

        if st.session_state.currentStreak > st.session_state.longestStreak:
                st.session_state.longestStreak = st.session_state.currentStreak

        st.session_state.oldGuessPercentage = st.session_state.guessPercentage
        st.session_state.guessPercentage = 100*int(st.session_state.totalCorrect)/int(st.session_state.totalGuesses)



        st.session_state.guessingStarted = True


########## SCORE METRICS ##########
if st.session_state.guessingStarted == True:
    ### ANSWER METRICS ###
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Correct", value=st.session_state.totalCorrect)
    with col2:
        if st.session_state.totalGuesses < 2:
            st.session_state.guessPercentageDelta = ""
        else:
            st.session_state.guessPercentageDelta = f"{st.session_state.guessPercentage - st.session_state.oldGuessPercentage :.2f}%" 

        st.metric(label="Percent Correct Guesses", value= f"{st.session_state.guessPercentage:.2f}%", delta=st.session_state.guessPercentageDelta)
    with col3:
        st.metric(label="Current Streak", value=st.session_state.currentStreak)
    with col4:
        st.metric(label="Longest Streak", value=st.session_state.longestStreak)

    ### TIME METRICS ###
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Previous Answer Time", value="123", delta="+5", delta_color="inverse")
    with col2:
        st.metric(label="10-Answer Average Time", value="123", delta="+5", delta_color="inverse")
    with col3:
        st.metric(label="Fastest Time", value="12.25s")
    with col4:
        st.metric(label="Fastest 10-Answer Average", value="123")


#if guess percentage 0, delta = "" else delta = now-old


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
# Remove enter guess button when answered correctly
# Reset stats button?

###DONE###
# Answer checking system (use first [0:1] of the guess)
# Add preset time range(s), make custom just an option
# Generate new date button
# Use calendar input
