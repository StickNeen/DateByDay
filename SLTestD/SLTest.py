import streamlit as st
import random
from datetime import datetime, timedelta
from collections import deque
import pandas as pd



########## TABS ##########

dateGuessingTab, howToTab = st.tabs(["Weekday Guessing", "How To?"])


with dateGuessingTab:

    ########## HEADER ##########
    st.header("Guess the Day of the Week!", divider="rainbow")

    ########## START SESSION STATE VARIABLES ##########
    if True:
        if "gameStarted" not in st.session_state:
            st.session_state.gameStarted = False
        if "guessingStarted" not in st.session_state:
            st.session_state.guessingStarted = False
        st.session_state.prevAnsCorrect = False
        if "guessButtonDisabled" not in st.session_state:
            st.session_state.guessButtonDisabled = False
        if "resetStatsButton" not in st.session_state:
            st.session_state.resetStatsButton = False
        if "resetGuessesButton" not in st.session_state:
            st.session_state.resetGuessesButton = False

        if "startDate" not in st.session_state:
            st.session_state.startDate = datetime(1900,1,1).date()
        if "endDate" not in st.session_state:
            st.session_state.endDate = datetime(2100,1,1).date()
        if "dateFormat" not in st.session_state:
            st.session_state.dateFormat = "MM/DD/YYYY"
        if "feedbackTextStr" not in st.session_state:
            st.session_state.feedbackTextStr = ""

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
        if "fastestFourAnsAvg" not in st.session_state:
            st.session_state.fastestFourAnsAvg = ""
        if "ansTimesList" not in st.session_state:
            st.session_state.ansTimesList = deque(maxlen=5)
        if "fourAnsAvgList" not in st.session_state:
            st.session_state.fourAnsAvgList = deque(maxlen=2)
        if "allTimesList" not in st.session_state:
            st.session_state.allTimesList = []
        if "allTimeAvgList" not in st.session_state:
            st.session_state.allTimeAvgList = deque(maxlen=2)

        if "pastDatesGenerated" not in st.session_state:
            st.session_state.pastDatesGenerated = []
        if "pastCorrectGuesses" not in st.session_state:
            st.session_state.pastCorrectGuesses = []
        if "pastCorrectDays" not in st.session_state:
            st.session_state.pastCorrectDays = []
        if "pastDaysGuessed" not in st.session_state:
            st.session_state.pastDaysGuessed = []
        if "pastGuessTimes" not in st.session_state:
            st.session_state.pastGuessTimes = []
        if "IBpastDatesGenerated" not in st.session_state:
            st.session_state.IBpastDatesGenerated = []
        if "IBpastCorrectGuesses" not in st.session_state:
            st.session_state.IBpastCorrectGuesses = []
        if "IBpastCorrectDays" not in st.session_state:
            st.session_state.IBpastCorrectDays = []
        if "IBpastDaysGuessed" not in st.session_state:
            st.session_state.IBpastDaysGuessed = []
        if "IBpastGuessTimes" not in st.session_state:
            st.session_state.IBpastGuessTimes = []
        


    ########## SECRET ANSWER PHASES ##########
    secretPhrases = ["psst... the answer is", "a little bird told me that it's", 
            "I have a hunch that the answer is", "don't tell anyone, but the answer is", 
            "I have the inside scoop: it's", "I've got a feeling it's", 
            "if I were you, I'd bet on", "rumor has it that the answer is",
            "shhhhh... don't let anyone else know that it's", "between you and me, the answer is",
            "here's a little secret: it's", "I know the answer... it's", 
            "I happen to know that it's", "you didn't hear it from me, but the answer is", 
            "I'm not saying it's a guarantee, but I'm pretty sure the answer is", 
            "in case you were wondering, it's", "you didn't get this from me, but I think it's"]






    ########## EXTRA OPTIONS EXPANDER ##########
    with st.popover("Options"):

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
            st.session_state.dateRangeStr = f"Date Range: {st.session_state.startDate.strftime("%m/%d/%Y")} to {st.session_state.endDate.strftime("%m/%d/%Y")}"
        elif st.session_state.dateFormat == "DD.MM.YYYY":
            st.session_state.dateRangeStr = f"Date Range: {st.session_state.startDate.strftime("%d.%m.%Y")} to {st.session_state.endDate.strftime("%d.%m.%Y")}"
        elif st.session_state.dateFormat == "Month DD, YYYY":
            st.session_state.dateRangeStr = f"Date Range: {st.session_state.startDate.strftime("%B %d, %Y")} to {st.session_state.endDate.strftime("%B %d, %Y")}"
        elif st.session_state.dateFormat == "DD Mo YYYY":
            st.session_state.dateRangeStr = f"Date Range: {st.session_state.startDate.strftime("%d %b %Y")} to {st.session_state.endDate.strftime("%d %b %Y")}"



        ########## AUTO REGENERATE ON CORRECT ANSWER ##########
        autoRegen = st.toggle("Automatically generate new date on correct answer?")


        ########## SHOW ANSWER TOGGLE ##########
        st.session_state.showAnswerToggle = st.toggle("Show the answer? (This is cheating... but feel free!)")




    ########## DATE RANGE HEADER ##########
    dateRangeSubheader = st.empty()
    dateRangeSubheader.subheader(st.session_state.dateRangeStr)




    ########## RANDOM DATE GENERATION ##########
    def generate_random_date():
        randomDays = random.randint(0, (st.session_state.endDate - st.session_state.startDate).days)
        randomDate = st.session_state.startDate + timedelta(days=randomDays)
        return randomDate



    ########### UPDATE DATA FRAME ##########
    def updateDataFrame():
        st.session_state.pastDatesGenerated = st.session_state.IBpastDatesGenerated + st.session_state.pastDatesGenerated
        st.session_state.pastCorrectGuesses = st.session_state.IBpastCorrectGuesses + st.session_state.pastCorrectGuesses
        st.session_state.pastCorrectDays = st.session_state.IBpastCorrectDays + st.session_state.pastCorrectDays
        st.session_state.pastDaysGuessed = st.session_state.IBpastDaysGuessed + st.session_state.pastDaysGuessed
        st.session_state.pastGuessTimes = st.session_state.IBpastGuessTimes + st.session_state.pastGuessTimes
        st.session_state.IBpastDatesGenerated = []
        st.session_state.IBpastCorrectGuesses = []
        st.session_state.IBpastCorrectDays = []
        st.session_state.IBpastDaysGuessed = []
        st.session_state.IBpastGuessTimes = []
        



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

        ########## PICK ANSWER PHRASE ##########
        st.session_state.chosenSecretPhrase = random.choice(secretPhrases)

        ########## START TIMER ##########
        st.session_state.timerStart = datetime.now().time().hour*3600 + datetime.now().time().minute * 60 + datetime.now().time().second + datetime.now().time().microsecond / 1000000
        st.session_state.gameStarted = True

        ########## RESET ALREADY GUESSED STATUS ##########
        st.session_state.guessButtonDisabled = False
        st.session_state.prevAnsCorrect = False

        st.session_state.feedbackTextStr = ""

        ########## UPDATE TOTAL GUESSES LIST ##########
        updateDataFrame()


    if generateButton == True:
        generateButtonPressed()

    #Give correct answer for testing
    #st.write(st.session_state.correctDay)





    ########## SET FEEDBACK IF PILLS CHANGE ##########
    def onPillChange():
        if st.session_state.feedbackTextStr == "<h3 style='color: red;'>Incorrect</h3>":
            st.session_state.feedbackTextStr = ""





    ########## ONCE GAME STARTED ##########
    if st.session_state.gameStarted == True:
        
        if st.session_state.showAnswerToggle == True:    
            st.write(f"({st.session_state.chosenSecretPhrase} <span style='color: red;'>{st.session_state.correctDay}</span>)", unsafe_allow_html=True) 
            

        ########## QUESTION SELECTBOX ##########
        daysOfWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

        
        if st.session_state.dateFormat == "MM/DD/YYYY":
            st.write(f"##### What day of the week {st.session_state.tense1} <span style='color: red;'>{st.session_state.randomDateUS}</span>{st.session_state.tense2}?", unsafe_allow_html= True)
        elif st.session_state.dateFormat == "DD.MM.YYYY":
            st.write(f"##### What day of the week {st.session_state.tense1} <span style='color: red;'>{st.session_state.randomDateEU}</span>{st.session_state.tense2}?", unsafe_allow_html= True)
        elif st.session_state.dateFormat == "Month DD, YYYY":
            st.write(f"##### What day of the week {st.session_state.tense1} <span style='color: red;'>{st.session_state.randomDateMonth}</span>{st.session_state.tense2}?", unsafe_allow_html= True)
        elif st.session_state.dateFormat == "DD Mo YYYY":
            st.write(f"##### What day of the week {st.session_state.tense1} <span style='color: red;'>{st.session_state.randomDateMo}</span>{st.session_state.tense2}?", unsafe_allow_html= True)

        dayGuess = st.pills("",(daysOfWeek), key= "inputPill", on_change=onPillChange)
        st.write("")
        st.write("")

        ########## GUESSING BUTTON ##########
        guessButton = st.button("Enter Guess", disabled=st.session_state.guessButtonDisabled)
        feedbackCol1, invCol2 = st.columns(2)
        #with invCol2:
        #    st.write("⠀")
        if guessButton == True:
            if dayGuess == None:
                st.session_state.feedbackTextStr = "<h3 style='color: grey;'>Pick a weekday to guess</h3>"
            
            else: 
                if dayGuess == st.session_state.correctDay:
                    st.session_state.feedbackTextStr = "<h3 style='color: green;'>Correct!⠀:D</h3>"
        
                    ##### UPDATE SCORE METRIC VALUES #####
                    st.session_state.totalCorrect += 1
                    st.session_state.currentStreak += 1
                    st.session_state.totalGuesses += 1

                    ##### UPDATE TIME METRIC VALUES #####
                    st.session_state.timerEnd = datetime.now().time().hour*3600 + datetime.now().time().minute * 60 + datetime.now().time().second + datetime.now().time().microsecond / 1000000
                    st.session_state.answerTime = st.session_state.timerEnd-st.session_state.timerStart

                    st.session_state.ansTimesList.append(st.session_state.answerTime)
                    st.session_state.fourAnsAvg = sum(st.session_state.ansTimesList)/len(st.session_state.ansTimesList)
                    st.session_state.fourAnsAvgList.append(st.session_state.fourAnsAvg)

                    st.session_state.allTimesList.append(st.session_state.answerTime)
                    st.session_state.allTimeAvg = sum(st.session_state.allTimesList)/len(st.session_state.allTimesList)
                    st.session_state.allTimeAvgList.append(st.session_state.allTimeAvg)

                    if st.session_state.totalCorrect > 1:
                        if f"{st.session_state.answerTime - st.session_state.oldAnswerTime:.2f}s" != "0.00s":
                            st.session_state.answerTimeDelta = f"{st.session_state.answerTime - st.session_state.oldAnswerTime:.2f}s"
                        else:
                            st.session_state.answerTimeDelta = ""
                    else:
                        st.session_state.answerTimeDelta = ""

                    st.session_state.answerTimeStr = f"{st.session_state.answerTime:.2f}s"
                    st.session_state.oldAnswerTime = st.session_state.answerTime

                    ########## MARK ALREADY GUESSED ##########
                    st.session_state.guessButtonDisabled = True

                    st.session_state.prevAnsCorrect = True


                else:
                    st.session_state.feedbackTextStr = "<h3 style='color: red;'>Incorrect⠀:(</h3>"

                    st.session_state.totalIncorrect += 1
                    st.session_state.currentStreak = 0
                    st.session_state.totalGuesses += 1


                if st.session_state.currentStreak > st.session_state.longestStreak:
                    st.session_state.longestStreak = st.session_state.currentStreak

                
                if st.session_state.totalCorrect > 4:
                    if st.session_state.fastestFourAnsAvg == "":
                        st.session_state.fastestFourAnsAvg = st.session_state.fourAnsAvg
                    elif st.session_state.fourAnsAvg < st.session_state.fastestFourAnsAvg:
                        st.session_state.fastestFourAnsAvg = st.session_state.fourAnsAvg
                    st.session_state.fastestFourAnsAvgStr = f"{st.session_state.fastestFourAnsAvg:.2f}s"
                else:
                    st.session_state.fastestFourAnsAvgStr = "N/A"

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



                if st.session_state.dateFormat == "MM/DD/YYYY":
                    st.session_state.IBpastDatesGenerated.insert(0, st.session_state.randomDateUS)
                elif st.session_state.dateFormat == "DD.MM.YYYY":
                    st.session_state.IBpastDatesGenerated.insert(0, st.session_state.randomDateEU)
                elif st.session_state.dateFormat == "Month DD, YYYY":
                    st.session_state.IBpastDatesGenerated.insert(0, st.session_state.randomDateMonth)
                elif st.session_state.dateFormat == "DD Mo YYYY":
                    st.session_state.IBpastDatesGenerated.insert(0, st.session_state.randomDateMo)

                if st.session_state.prevAnsCorrect:
                    st.session_state.IBpastCorrectGuesses.insert(0, "Correct")
                else:
                    st.session_state.IBpastCorrectGuesses.insert(0, "Incorrect")
            
                st.session_state.IBpastCorrectDays.insert(0, st.session_state.correctDay)
                st.session_state.IBpastDaysGuessed.insert(0, dayGuess)

                guessTimeEnd = datetime.now().time().hour*3600 + datetime.now().time().minute * 60 + datetime.now().time().second + datetime.now().time().microsecond / 1000000
                guessTime = guessTimeEnd-st.session_state.timerStart
                

                st.session_state.IBpastGuessTimes.insert(0, f"{guessTime:.2f} seconds")

                if st.session_state.prevAnsCorrect:
                    updateDataFrame()


                st.session_state.guessingStarted = True


        st.markdown(st.session_state.feedbackTextStr, unsafe_allow_html=True)

        st.divider()







        ########## SCORE METRICS ##########
        if st.session_state.guessingStarted == True:
            showMetrics = st.toggle("Show score metrics")
            if showMetrics:
                ### ANSWER METRICS ###
                st.write("### Score Metrics")
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
                    if st.session_state.totalCorrect == 0:
                        st.session_state.answerTimeStr = "N/A"
                    if st.session_state.totalCorrect < 2:
                        st.session_state.answerTimeDelta = ""

                    st.metric(label="Answer Time", value=st.session_state.answerTimeStr, delta=st.session_state.answerTimeDelta, delta_color="inverse")

                with col2:
                    if len(st.session_state.ansTimesList) < 5:
                        st.session_state.fourAnsAvgStr = "N/A"
                    else:
                        st.session_state.fourAnsAvgStr = f"{st.session_state.fourAnsAvg:.2f}s"

                    if st.session_state.totalCorrect < 6:
                        st.session_state.fourAnsAvgDelta = ""
                    elif f"{st.session_state.fourAnsAvgList[1] - st.session_state.fourAnsAvgList[0]:.2f}s" == "0.00s":
                        st.session_state.fourAnsAvgDelta = ""
                    else:
                        st.session_state.fourAnsAvgDelta = f"{st.session_state.fourAnsAvgList[1] - st.session_state.fourAnsAvgList[0]:.2f}s"
                    
                    st.metric(label="5-Answer Avg Time", value=st.session_state.fourAnsAvgStr, delta=st.session_state.fourAnsAvgDelta, delta_color= "inverse")
                with col3:
                    st.metric(label="Fastest Time", value=st.session_state.fastestTimeStr)
                with col4:
                    st.metric(label="Fastest 5-Answer Avg", value=st.session_state.fastestFourAnsAvgStr)
                with col5:
                    if st.session_state.totalCorrect == 0:
                        st.session_state.allTimeAvgStr = "N/A"
                    else:
                        st.session_state.allTimeAvgStr = f"{st.session_state.allTimeAvg:.2f}s"

                    if st.session_state.totalCorrect < 2:
                        st.session_state.allTimeAvgDelta = ""
                    elif f"{st.session_state.allTimeAvgList[1] - st.session_state.allTimeAvgList[0]:.2f}s" == "0.00s":
                        st.session_state.allTimeAvgDelta = ""
                    else:
                        st.session_state.allTimeAvgDelta = f"{st.session_state.allTimeAvgList[1] - st.session_state.allTimeAvgList[0]:.2f}s"

                    st.metric(label="Overall Avg Time", value= st.session_state.allTimeAvgStr, delta=st.session_state.allTimeAvgDelta, delta_color= "inverse")

                ########## RESET STATS BUTTON ##########

                def resetStats():
                    st.session_state.totalCorrect = 0
                    st.session_state.totalIncorrect = 0
                    st.session_state.totalGuesses = 0
                    st.session_state.currentStreak = 0
                    st.session_state.longestStreak = 0
                    st.session_state.oldAnswerTime = ""
                    st.session_state.guessPercentage = 0
                    st.session_state.fastestTime = ""
                    st.session_state.fastestFourAnsAvg = ""
                    st.session_state.ansTimesList = deque(maxlen=5)
                    st.session_state.fourAnsAvg = 0
                    st.session_state.fourAnsAvgList = deque(maxlen=2)
                    st.session_state.allTimesList = []
                    st.session_state.allTimeAvgList = deque(maxlen=2)
                    st.session_state.fastestFourAnsAvgStr = "N/A"
                    st.session_state.fastestTimeStr = "N/A"

                st.session_state.resetStatsButton = st.button("Reset Stats")
                if st.session_state.resetStatsButton == True:
                    resetStats()

            ########## PAST GUESSES ##########
            pastGuessesData = {
                "Date": st.session_state.pastDatesGenerated,
                "Correct?": st.session_state.pastCorrectGuesses,
                "Correct Weekday": st.session_state.pastCorrectDays,
                "Your Guess": st.session_state.pastDaysGuessed,
                "Time": st.session_state.pastGuessTimes
            }

            pastGuessesDataFrame = pd.DataFrame(pastGuessesData)

            def colorCell(val):
                if val == "Correct":
                    return 'background-color: #93c47d; color: black'
                elif val == "Incorrect":
                    return 'background-color: #e06666; color: black'

            formattedPGDF = pastGuessesDataFrame.style.applymap(colorCell, subset=["Correct?"])

            showTable = st.toggle("Show past guesses")
            if showTable == True:
                st.write("### Past Guesses")
                st.dataframe(formattedPGDF, use_container_width=True, hide_index = True)


                ##### RESET PAST GUESSES BUTTON #####
                def resetGuesses():
                    st.session_state.pastDatesGenerated = []
                    st.session_state.pastCorrectGuesses = []
                    st.session_state.pastCorrectDays = []
                    st.session_state.pastDaysGuessed = []
                    st.session_state.pastGuessTimes = []
                    st.session_state.IBpastDatesGenerated = []
                    st.session_state.IBpastCorrectGuesses = []
                    st.session_state.IBpastCorrectDays = []
                    st.session_state.IBpastDaysGuessed = []
                    st.session_state.IBpastGuessTimes = []

                st.session_state.resetGuessesButton = st.button("Reset Past Guesses")
                if st.session_state.resetGuessesButton == True:
                    resetGuesses()



        




    ########## AUTOMATICALLY GENERATE NEW DATE ##########

    if st.session_state.prevAnsCorrect == True:
        if autoRegen == True:
            generateButtonPressed()
        st.rerun()

    ########## RESET STATS BUTTON ##########
    if st.session_state.resetStatsButton == True:
        st.rerun()

    ########## RESET GUESSES BUTTON ##########
    if st.session_state.resetGuessesButton == True:
        st.rerun()




with howToTab:
    st.write("figure it out yourself")




########## TO DO ##########
# Color the day they're guessing using <span style='color: red;'>{st.session_state.correctDay}</span>)
# Intro and other explanation pages
# Link to numberphile video?
# Other practice: just doomsdays, 12s or 16s practice
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
# timer
# Overall scorekeeping
# Think about making delta answer time not appear when 0?
# Better message to tell when correct (use same thing as date range header)
# Reset stats button?
# Option to show the answer