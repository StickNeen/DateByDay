import streamlit as st
import random
from datetime import datetime, timedelta

#Header
st.header("Date Practice!", divider="rainbow")

dateFormat = st.radio("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "Month/DD/YYYY", "DD/Month/YYYY"])

if dateFormat == "MM/DD/YYYY" or dateFormat == "Month/DD/YYYY":
    calendarDateFormat = "MM/DD/YYYY"
else:
    calendarDateFormat = "DD/MM/YYYY"


st.markdown('#####')
#Chose the date range of guesses
customRange = st.toggle("Custom date range?")

if customRange == False:
    startDate = datetime(1900,1,1)
    endDate = datetime(2100,1,1)

if customRange == True:
    startDate = st.date_input("Start of custom range", min_value=datetime(1600,1,1), max_value=datetime(2600,1,1), format=calendarDateFormat)
    endDate = st.date_input("End of custom range", min_value=startDate, max_value=datetime(2600,1,1), format=calendarDateFormat)


if dateFormat == "MM/DD/YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%m/%d/%Y")} to {endDate.strftime("%m/%d/%Y")}")
elif dateFormat == "DD/MM/YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%d/%m/%Y")} to {endDate.strftime("%d/%m/%Y")}")
elif dateFormat == "Month/DD/YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%B/%d/%Y")} to {endDate.strftime("%B/%d/%Y")}")
elif dateFormat == "DD/Month/YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%d/%B/%Y")} to {endDate.strftime("%d/%B/%Y")}")


#Generate the random date
def generate_random_date():

    randomDays = random.randint(0, (endDate - startDate).days)
    randomDate = startDate + timedelta(days=randomDays)
    return randomDate


#Add space after date range
st.markdown('#####')


generateButton = st.button("Generate a new random date")



if 'randomDate' not in st.session_state:
        st.session_state.randomDate = ""
if 'correctDay' not in st.session_state:
    st.session_state.correctDay = ""
if 'dateGenerated' not in st.session_state:
        st.session_state.dateGenerated = False
if 'randomDateEU' not in st.session_state:
        st.session_state.randomDateEU = ""
if 'randomDateUS' not in st.session_state:
        st.session_state.randomDateUS = ""
if 'gameStarted' not in st.session_state:
        st.session_state.gameStarted = False


if generateButton == True:
    randomDate = generate_random_date()
    st.session_state.correctDay = randomDate.strftime("%A")

    st.session_state.randomDateEU = randomDate.strftime("%d/%m/%Y")
    st.session_state.randomDateUS = randomDate.strftime("%m/%d/%Y")

    st.session_state.randomDate = str(randomDate)

    st.session_state.dateGenerated = True
    st.session_state.gameStarted = True


#Give correct answer for testing
#st.write(st.session_state.correctDay)

if st.session_state.gameStarted == True:
#   dayGuess = st.text_input(f"What day of the week was {randomDate[0:10]}? (YYYY-MM-DD)")
    if dateFormat == "MM/DD/YYYY":
        dayGuess = st.selectbox(f"What day of the week was {st.session_state.randomDateUS}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    elif dateFormat == "DD/MM/YYYY":
        dayGuess = st.selectbox(f"What day of the week was {st.session_state.randomDateEU}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))


    guessButton = st.button("Enter Guess")
    if guessButton == True:
        if dayGuess == st.session_state.correctDay:
            st.write("Correct!")
        else:
            st.write("Incorrect")

#Write all saved variables for debugging
#st.write(f"RandomDate: {st.session_state.randomDate}")
#st.write(f"CorrectDay: {st.session_state.correctDay}")
#st.write(f"dateGenerated: {st.session_state.dateGenerated}")
#st.write(f"gameStarted: {st.session_state.gameStarted}")

###TO DO
# Answer checking system (use first [0:1] of the guess)
# Add preset time range(s), make custom just an option
# Generate new date button
# Option for auto-generate on correct guess
# Use calendar input
# Intro and other explanation pages
# Link to numberphile video?
# Other practice: just doomsdays, 12s or 16s practice
# Check current date, write was if question date is in past or is if in present
# Overall scorekeeping
# Add option to write dates in words?