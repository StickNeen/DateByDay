import streamlit as st
import random
from datetime import datetime, timedelta
from collections import deque
import pandas as pd


st.title("Date by Day")


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
    ########## HEADER ##########
    st.header("How To Guess the Weekday?", divider="rainbow")

    st.write("### The Doomsday Method")

    st.write("""
    ⠀⠀⠀⠀The process I use to find the day of the week of any date is called the Doomsday Method. It uses the fact that for any given year, 
    certain easy-to-remember dates (doomsdays) are always on the same day of the week as each other. For example, if March 14th (pi day!) is 
    a Tuesday in a given year, March 21st and March 28th must also be Tuesdays that year, since they are exactly one and two weeks apart. 
    But also, October 10th and December 12th will be Tuesdays, since they are always the same day of the week as March 14th. March 14, 
    October 10, and December 12 are all examples of doomsdays which you can easily remember: pi day, 10/10, and 12/12. Further, if I know 
    that March 14th, 2000 was a Tuesday, I can quickly figure that March 15th was a Wednesday, or using our doomsdays, that October 13th was 
    a Friday (spooky!).


    ⠀⠀⠀⠀So that's the gist of how the Doomsday Method works. If you're interested, I highly recommend checking out one or both of 
    these youtube videos about it; they are how I found out about it in the first place, and they explain it very well.
    """)

    vidCol1, vidCol2 = st.columns(2)
    with vidCol1:
        st.video("https://youtu.be/z2x3SSBVGJU?si=apBiInuCWgmvVV6A")
    with vidCol2:
        st.video("https://youtu.be/714LTMNJy5M?si=Kq0JY4AT-RVhZYQz")

    st.write("""
    But if you're not much of one for intra-internet travel, I'll do my best to explain it here.
    ___   
    #### My Explanation
    ⠀⠀⠀⠀The Doomsday Method works in two steps, each with one main aspect of memorization. 
    First, you have to find what weekday the doomsdays of your year are, and then you have to 
    find the weekday of the specific date that you're looking for. I'll do my best to explain how each of those
    steps work, but if you don't care about the explanation and just want the specific steps, or if you
    think seeing the steps first would be helpful to you, there is a summary at the end. 
    <br>
    ##### Quick Tips
    ⠀⠀⠀⠀Before we get into the steps, here are two quick tips:
    <br>
    ⠀⠀⠀⠀First, because we'll be doing a bit of math with weekdays, it's helpful
    to think of them as numbers -- Sunday = 0 (think "None-day"), Monday = 1 ("One-day"), Tuesday = 2 ("Twos-day"), 
    Wednesday = 3, Thursday = 4 ("Fours-day"), Friday = 5 ("Five-day"), and Saturday = 6. If you can think of the
    weekdays as numbers, it's much easier to quickly compute what comes 16 days after a Tuesday, for example.
    <br>
    ⠀⠀⠀⠀Second, since weekdays repeat every 7 days, 16 days after a Tuesday is the same as 9 or 2 days after a Tuesday.
    When you're adding days, you can subtract out extra 7s, or take the remainder when divided by 7 (modulate, if you're
    using math words).


    ##### Step One: The Year
    ⠀⠀⠀⠀Say you want to figure out what day of the week March 19th, 2000 was. Well, we know from our example above that March 14th, 2000 was a
    Tuesday, so March 19, 2000 must have been a Sunday. Great! But what if we now want to know what day of the week March 14th, 2001 was? The 
    trick is that each year, the doomsday moves forward one day of the week. So March 14th, 2001 was a Wednesday; March 14th, 2002 was a Thursday; 
    and March 14th, 2003 was a Friday. The tricky part is at 2004, since that's a leap year. On leap years, the doomsday increases by two days of 
    the week, so March 14th, 2004 was a Sunday. 
    <br>
    ⠀⠀⠀⠀So, to find what day of the week the doomsday of 2013 was, start at 2000, which you know was a Tuesday (or a 2, using tip one above). 
    Then, add 13 (or add 6, using tip two above) to get to 2013. Then to account for the leap years, add 13 ÷ 4, ignoring the remainder (that's 
    how many leap years there were from 2000 to 2013). So, 2 + 6 + 3 = 11. Using tip one, 11-7 = 4, which means that March 14th, 2013 was a Thursday. 
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1,1.7])

    with col1:
        st.write(" ###### ⠀⠀⠀⠀")
        st.write("""
    ⠀⠀⠀⠀How about finding the doomsday weekday for 1950? Well, that is where some memorization is needed. To have somewhere to work off of, you have 
    to remember the doomsday for the start of each century. 2000 was Tuesday, 1900 was Wednesday, 1800 was Friday, and 1700 was Sunday. The cycle repeats
    from there and is the same going to the future, so 2100 will be Sunday, 2200 will be Friday, and so on.
    <br>
    """, unsafe_allow_html=True)

    with col2:
        st.write(" ###### Century Chart")
        st.dataframe({"Year": ["1700","1800","1900","2000","2100","2200","2300","2400"],
         "Doomsday Day of the Week": ["Sunday", "Friday", "Wednesday", "Tuesday", "Sunday", "Friday", "Wednesday", "Tuesday"]},
          use_container_width=True)


    st.write("""
    ⠀⠀⠀⠀So, back to 1950. If 1900's doomsday was on a wednesday, we start at 3 (tip one). Then you have to add 50, but using tip two again, we can 
    subtract 49, which is a multiple of 7, to just add 1. Lastly, account for the leap years. 50 ÷ 4 = 12, or 5 (tip two). So, 3 + 1 + 5 = 9, 
    subtract 7 to get 2, and March 14th, 1950 was on a Tuesday.
    <br>
    ⠀⠀⠀⠀Here's one more tip for step one to make it easier. Every 12 years, the doomsday moves forward one day. So 2000 is a Tuesday doomsday, 2012 
    is a Wednesday, 2024 a Thursday. That can be helpful when you have bigger numbers in the year, like 1979. For 1979, we'd start from 3 again, then 
    consider which multiple of 12 gets us close to 79. 12 x 6 is 72, so you can add 6 and then work from 72. Add 7 more to get to 79, plus 1 (7 ÷ 4) for 
    the leap year between 1972 and 1979. So all together, 3 (starting point) + 6 (12 x 6 = 72) + 7 (79-72) + 1 (7 ÷ 4) = 17, or 3 using tip two. 
    So, 1979's doomsday was on a Wednesday.
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1,1.1])

    with col1:
        st.write("""
    ##### Step Two: The Date
    ⠀⠀⠀⠀Once you're able to find what day of the week the doomsday was for your preferred year, you have to use the doomsdays to get to your specific date.
    For this step, you have to memorize a doomsday in each month. March's is pi day, which we have already used in examples. April, June, August, October, 
    and December are self-explanatory, and for May, July, September, and November, remember the mnemonic "Working 9 to 5 at the 7-Eleven." January and Febuary
    are a bit tricky, since they change if it's a leap year. January is the 3rd for three years and the 4th evey fourth year (leap years), and Febuary is always the last
    day of the month (28th normally, 29th on leap years).
    """)

    with col2:
        st.write(" ###### Doomsday Chart")
        st.dataframe({"Month": ["January","February","March","April","May","June","July","August","September","October","November","December"],
         "Doomsday (Month/Day)": ["1/3 (1/4)", "2/28 (2/29)", "3/14", "4/4", "5/9", "6/6", "7/11", "8/8", "9/5", "10/10", "11/7", "12/12"]},
          use_container_width=True)

    st.write("""
    ⠀⠀⠀⠀To know whether a year is a leap year for the January and February doomsdays, check if the last two numbers of the year are divisble by four.
    So 2034 is not a leap year, since 34 is not divisible by 4, but 2096 is, since 96 is divisible by 4. It's a bit more confusing for the centuries;
    the rule is that every 100 years the leap year is skipped, unless the year is divisible by 400, in which case it is a leap year. So, 1700, 1800, and 1900
    weren't leap years, but 2000 was. 2100, 2200, and 2300 won't be leap years, but 2400 will be. It's a bit confusing, but it hardly ever comes up.
    <br>
    ⠀⠀⠀⠀So, let's say you want to find out what day of the week June 30th, 1979 was. We know from step one that 1979's doomsday was Wednesday. From there,
    we use the June doomsday, 6/6. From the 6th to the 30th is 24 days (30-6), which is the same as adding 3 days (from tip two). So, Wednesday plus 3 is Saturday,
    and June 30th, 1979 was a Saturday.
    <br>
    ⠀⠀⠀⠀Let's try one more: February 13th, 1950. Again, we know from above that 1950's doomsday was a Tuesday. To use the February doomsday, check if 1950 was a leap
    year. 50 is not equally divisible by 4, so 1950 was not a leap year, and the doomsday is the 28th. Our date is before the doomsday, so we'll have to subtract. The
    13th is 15 days before the 28th (28-13), which is the same as 1 day before it (tip two). One day before Tuesday is Monday, so February 13th, 1950 was a Monday.


    ##### Summary
    ⠀⠀⠀⠀Ok, that was a lot. Here are the overall steps to find the day of the week for a random date. I'll use April 12, 1861 as my example.
    <br>
    1. Find which day of the week the doomsday for the start of your century is. 1800's doomsday was on Friday, so I'll remember 5.
    <br>
    2. Divide the last two digits of your year by 12, ignoring the remainder. 61 ÷ 12 = 5.
    <br>
    3. Find the remainder from the previous step. The remainder of 61 ÷ 12 is 1.
    <br>
    4. Divide the remainder you found in the previous step by 4, again ignoring the remainder. 1 ÷ 4 = 0.
    <br>
    5. Find the number of days between your day and the doomsday in your month. April 12 - April 4 = 8 days.
    <br>
    6. Add the numbers from the previous steps up and subtract 7 until the number you have is less than 7. 5 + 5 + 1 + 0 + 8 = 19. 19 - 7 = 12, 12 - 7 = 5.
    <br>
    7. Convert your number into a day of the week. 5 corresponds with Friday, so April 12, 1861 was a Friday.

    <br>
    ⠀⠀⠀⠀I hope that helped! Again, I highly recommend watching those videos if you're still confused, they explain everything better than I did. 
    If you already have, I recommend practice! Keeping all of the numbers straight is difficult at first, but with enough reps, you can figure it out
    pretty quickly. And then you have a wonderful new party trick! Happy calculating!

        
        
    """, unsafe_allow_html=True)

        


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