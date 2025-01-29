import streamlit as st
import random
from datetime import datetime, timedelta
from collections import deque



########## HEADER ##########
st.header("Date Practice!", divider="rainbow")

########## START SESSION STATE VARIABLES ##########
if True:
    if "gameStarted" not in st.session_state:
        st.session_state.gameStarted = False
    if "guessingStarted" not in st.session_state:
        st.session_state.guessingStarted = False
    st.session_state.prevAnsCorrect = False
    if "guessButtonDisabled" not in st.session_state:
        st.session_state.guessButtonDisabled = False

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
    if "oldAnswerTime" not in st.session_state:
        st.session_state.oldAnswerTime = ""
    if "guessPercentage" not in st.session_state:
        st.session_state.guessPercentage = 0
    if "fastestTime" not in st.session_state:
        st.session_state.fastestTime = ""
    if "ansTimesList" not in st.session_state:
        st.session_state.ansTimesList = deque(maxlen=4)
    if "fourAnsAvgList" not in st.session_state:
        st.session_state.fourAnsAvgList = deque(maxlen=2)



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



    ########## AUTO REGENERATE ON CORRECT ANSWER ##########
    autoRegen = st.toggle("Automatically generate new date on correct answer?")
    


########## RANDOM DATE GENERATION ##########
def generate_random_date():
    randomDays = random.randint(0, (st.session_state.endDate - st.session_state.startDate).days)
    randomDate = st.session_state.startDate + timedelta(days=randomDays)
    return randomDate



########## GENERATE DATE BUTTON ##########
st.markdown('#####')
generateButton = st.button("Generate a new random date")

def generateButtonPressed():
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

    ########## START TIMER ##########
    st.session_state.timerStart = datetime.now().time().hour*3600 + datetime.now().time().minute * 60 + datetime.now().time().second + datetime.now().time().microsecond / 1000000
    st.session_state.gameStarted = True

    ########## RESET ALREADY GUESSED STATUS ##########
    st.session_state.guessButtonDisabled = False

    st.session_state.prevAnsCorrect = False

if generateButton == True:
    generateButtonPressed()

#Give correct answer for testing
#st.write(st.session_state.correctDay)


########## ONCE GAME STARTED ##########
if st.session_state.gameStarted == True:
    st.write(st.session_state.correctDay)

    ########## QUESTION SELECTBOX ##########
    daysOfWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

    
    if st.session_state.dateFormat == "MM/DD/YYYY":
            dayGuess = st.pills(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateUS}{st.session_state.tense2}?",(daysOfWeek))
    elif st.session_state.dateFormat == "DD.MM.YYYY":
        dayGuess = st.pills(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateEU}{st.session_state.tense2}?",(daysOfWeek))
    elif st.session_state.dateFormat == "Month DD, YYYY":
        dayGuess = st.pills(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateMonth}{st.session_state.tense2}?",(daysOfWeek))
    elif st.session_state.dateFormat == "DD Mo YYYY":
        dayGuess = st.pills(f"What day of the week {st.session_state.tense1} {st.session_state.randomDateMo}{st.session_state.tense2}?",(daysOfWeek))


    ########## GUESSING BUTTON ##########
    guessButton = st.button("Enter Guess", disabled=st.session_state.guessButtonDisabled)
    feedbackCol1, invCol2 = st.columns(2)
    with invCol2:
        st.write("⠀")
    if guessButton == True:   
        if dayGuess == st.session_state.correctDay:
            with feedbackCol1:
                st.write("Correct!")
  
            ##### UPDATE SCORE METRIC VALUES #####
            st.session_state.totalCorrect += 1
            st.session_state.currentStreak += 1
            st.session_state.totalGuesses += 1

            ##### UPDATE TIME METRIC VALUES #####
            st.session_state.timerEnd = datetime.now().time().hour*3600 + datetime.now().time().minute * 60 + datetime.now().time().second + datetime.now().time().microsecond / 1000000
            st.session_state.answerTime = st.session_state.timerEnd-st.session_state.timerStart

            st.session_state.ansTimesList.append(st.session_state.answerTime)
            st.session_state.fourAnsAvg = sum(st.session_state.ansTimesList)/4
            st.session_state.fourAnsAvgList.append(st.session_state.fourAnsAvg)

            if st.session_state.totalCorrect > 1:
                st.session_state.answerTimeDelta = f"{st.session_state.answerTime - st.session_state.oldAnswerTime:.2f}s"

            st.session_state.answerTimeStr = f"{st.session_state.answerTime:.2f}s"
            st.session_state.oldAnswerTime = st.session_state.answerTime

            ########## MARK ALREADY GUESSED ##########
            st.session_state.guessButtonDisabled = True

            st.session_state.prevAnsCorrect = True
            

        else:
            with feedbackCol1:
                st.write("Incorrect")

            st.session_state.totalIncorrect += 1
            st.session_state.currentStreak = 0
            st.session_state.totalGuesses += 1


        if st.session_state.currentStreak > st.session_state.longestStreak:
            st.session_state.longestStreak = st.session_state.currentStreak
        if st.session_state.totalCorrect > 0:
            if st.session_state.fastestTime == "":
                st.session_state.fastestTime = st.session_state.answerTime
            elif st.session_state.answerTime < st.session_state.fastestTime:
                st.session_state.fastestTime = st.session_state.answerTime
            st.session_state.fastestTimeStr = f"{st.session_state.fastestTime:.2f}s"
        else:
            st.session_state.fastestTimeStr = "N/A"        

        st.session_state.oldGuessPercentage = st.session_state.guessPercentage
        st.session_state.guessPercentage = 100*int(st.session_state.totalCorrect)/int(st.session_state.totalGuesses)


        st.session_state.guessingStarted = True


st.divider()

########## SCORE METRICS ##########
if st.session_state.guessingStarted == True:
    ### ANSWER METRICS ###
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="Total Correct", value=st.session_state.totalCorrect)
    with col2:
        st.metric(label="Total Guesses", value=st.session_state.totalGuesses)
    with col3:
        if st.session_state.totalCorrect < 1:
            st.session_state.guessPercentageDelta = ""
        elif f"{st.session_state.guessPercentage:.1f}" == f"{st.session_state.oldGuessPercentage:.1f}":
            st.session_state.guessPercentageDelta = ""
        else:
            st.session_state.guessPercentageDelta = f"{st.session_state.guessPercentage - st.session_state.oldGuessPercentage :.1f}%" 
        st.metric(label="Percent Accuracy", value= f"{st.session_state.guessPercentage:.1f}%", delta=st.session_state.guessPercentageDelta)
    with col4:
        st.metric(label="Current Streak", value=st.session_state.currentStreak)
    with col5:
        st.metric(label="Longest Streak", value=st.session_state.longestStreak)

    ### TIME METRICS ###
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.session_state.totalCorrect < 2:
            st.session_state.answerTimeDelta = ""
        if st.session_state.totalCorrect == 0:
            st.session_state.answerTimeStr = "N/A"

        st.metric(label="Answer Time", value=st.session_state.answerTimeStr, delta=st.session_state.answerTimeDelta, delta_color="inverse")

    with col2:
        if len(st.session_state.ansTimesList) < 4:
            st.session_state.fourAnsAvgStr = "N/A"
        else:
            st.session_state.fourAnsAvgStr = f"{st.session_state.fourAnsAvg:.2f}s"

        if st.session_state.totalCorrect < 5:
            st.session_state.fourAnsAvgDelta = ""
        else:
            st.session_state.fourAnsAvgDelta = f"{st.session_state.fourAnsAvgList[1] - st.session_state.fourAnsAvgList[0]:.2f}s"
        
        st.metric(label="4-Answer Avg Time", value=st.session_state.fourAnsAvgStr, delta=st.session_state.fourAnsAvgDelta, delta_color= "inverse")
    with col3:
        st.metric(label="Fastest Time", value=st.session_state.fastestTimeStr)
    with col4:
        st.metric(label="Fastest 4-Answer Avg", value="123")
    with col5:
        st.metric(label="Overall Avg Time", value= "12s", delta="")


########## AUTOMATICALLY GENERATE NEW DATE ##########

if st.session_state.prevAnsCorrect == True:
    if autoRegen == True:
        generateButtonPressed()
    st.rerun()






########## TO DO ##########
# timer
# Overall scorekeeping
# Intro and other explanation pages
# Link to numberphile video?
# Other practice: just doomsdays, 12s or 16s practice
# Reset stats button?
# Think about making delta answer time not appear when 0?
# Better message to tell when correct (use same thing as date range header)
# Redo all deltas with deques

###DONE###
# Answer checking system (use first [0:1] of the guess)
# Add preset time range(s), make custom just an option
# Generate new date button
# Use calendar input
# Option for auto-generate on correct guess
# Check current date, write was if question date is in past or is if in present
# Add option to write dates in words?
# Add settings page with all of the options
# Remove enter guess button when answered correctly
# Add if precent accuracy is unchanged, delta doesnt appear
# Disable button when already guessed