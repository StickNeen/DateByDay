import streamlit as st
import random
from datetime import datetime, timedelta


#Header
st.header("Date Practice!", divider="rainbow")

dateFormat = st.selectbox("Date Format", ["MM/DD/YYYY", "DD.MM.YYYY", "Month DD, YYYY", "DD Mo YYYY"])
#dateFormat = "MM/DD/YYYY"

if dateFormat == "MM/DD/YYYY" or dateFormat == "Month DD, YYYY":
    calendarDateFormat = "MM/DD/YYYY"
else:
    calendarDateFormat = "DD.MM.YYYY"


st.markdown('#####')
#Chose the date range of guesses
customRange = st.toggle("Custom date range?")

if customRange == False:
    startDate = datetime(1900,1,1).date()
    endDate = datetime(2100,1,1).date()

if customRange == True:
    startDate = st.date_input("Start of custom range", min_value=datetime(1600,1,1), max_value=datetime(2600,1,1), format=calendarDateFormat)
    endDate = st.date_input("End of custom range", min_value=startDate, max_value=datetime(2600,1,1), format=calendarDateFormat)


if dateFormat == "MM/DD/YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%m/%d/%Y")} to {endDate.strftime("%m/%d/%Y")}")
elif dateFormat == "DD.MM.YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%d.%m.%Y")} to {endDate.strftime("%d.%m.%Y")}")
elif dateFormat == "Month DD, YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%B %d, %Y")} to {endDate.strftime("%B %d, %Y")}")
elif dateFormat == "DD Mo YYYY":
    st.subheader(f"Date Range: {startDate.strftime("%d %b %Y")} to {endDate.strftime("%d %b %Y")}")


#Generate the random date
def generate_random_date():

    randomDays = random.randint(0, (endDate - startDate).days)
    randomDate = startDate + timedelta(days=randomDays)
    return randomDate


#Add space after date range
st.markdown('#####')


generateButton = st.button("Generate a new random date")




#if 'correctDay' not in st.session_state:
#    st.session_state.correctDay = ""
#if 'randomDateEU' not in st.session_state:
#        st.session_state.randomDateEU = ""
#if 'randomDateUS' not in st.session_state:
#        st.session_state.randomDateUS = ""
#if 'randomDateMonth' not in st.session_state:
#        st.session_state.randomDateMonth = ""
#if 'randomDateMo' not in st.session_state:
#        st.session_state.randomDateMo = ""
#if 'tense1' not in st.session_state:
#        st.session_state.tense1 = ""
#if 'tense2' not in st.session_state:
#        st.session_state.tense2 = ""

if 'gameStarted' not in st.session_state:
        st.session_state.gameStarted = False


if generateButton == True:
    randomDate = generate_random_date()
    st.session_state.correctDay = randomDate.strftime("%A")

    ###Save Date Formats###
    st.session_state.randomDateEU = randomDate.strftime("%d.%m.%Y")
    st.session_state.randomDateUS = randomDate.strftime("%m/%d/%Y")
    st.session_state.randomDateMonth = randomDate.strftime("%B %d, %Y")
    st.session_state.randomDateMo = randomDate.strftime("%d %b %Y")

    ###Tense Formatting###
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

if st.session_state.gameStarted == True:

    if dateFormat == "MM/DD/YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateUS}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    elif dateFormat == "DD.MM.YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateEU}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    elif dateFormat == "Month DD, YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateMonth}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))
    elif dateFormat == "DD Mo YYYY":
        dayGuess = st.selectbox(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateMo}{st.session_state.tense2}?",("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))

    ###Guessing Button###
    guessButton = st.button("Enter Guess")
    if guessButton == True:
        if dayGuess == st.session_state.correctDay:
            st.write("Correct!")
        else:
            st.write("Incorrect")



col1, col2, col3, col4 = st.columns(4)

# Place st.metric in each column
with col1:
    st.metric(label="Metric 1", value="123", delta="+5")
    
with col2:
    st.metric(label="Metric 2", value="456", delta="-2")
    
with col3:
    st.metric(label="Metric 3", value="789", delta="+10", delta_color="off")


###TO DO###
# Option for auto-generate on correct guess
# timer
# Overall scorekeeping
# Intro and other explanation pages
# Link to numberphile video?
# Other practice: just doomsdays, 12s or 16s practice
# Check current date, write was if question date is in past or is if in present
# Add option to write dates in words?

###DONE###
# Answer checking system (use first [0:1] of the guess)
# Add preset time range(s), make custom just an option
# Generate new date button
# Use calendar input
