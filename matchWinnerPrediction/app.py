# streamlit run streamlit_app.py

import joblib
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import pickle
import streamlit.components.v1 as components

le = LabelEncoder()
st.markdown("<h1 style='text-align: center;'>Match Winner Prediction</h1>", unsafe_allow_html=True)
home = st.text_input("Enter Home Team: ")
away = st.text_input("Enter Away Team: ")
toss = st.select_slider("Toss Winner: ", [home, away])
bat = st.selectbox("Toss Choice: ", ["Batting First", "Bowling First"])
isNeutral = st.checkbox("Is the match played on a neutral venue (World Cup)?")


model = joblib.load('matchWinnerPrediction/model.joblib')

winlast5, winlast4, winlast3, winlast2, winlast1 = pickle.load(
    open("matchWinnerPrediction/winlast.pkl", "rb"))
losslast5, losslast4, losslast3, losslast2, losslast1 = pickle.load(
    open("matchWinnerPrediction/losslast.pkl", "rb"))
drawlast5, drawlast4, drawlast3, drawlast2, drawlast1 = pickle.load(
    open("matchWinnerPrediction/drawlast.pkl", "rb"))

# Encoding home team
def homeEncoding(home):
    homeEncodedDict = {'Afghanistan': 0, 'Africa XI': 1, 'Asia XI': 2, 'Australia': 3, 
    'Bangladesh': 4, 'Bermuda': 5, 'Canada': 6, 'England': 7, 'Hong Kong': 8, 'ICC World XI': 9, 'India': 10, 'Ireland': 11, 'Kenya': 12, 'Namibia': 13, 'Nepal': 14, 'Netherlands': 15, 'New Zealand': 16, 'Oman': 17, 'P.N.G.': 18, 'Pakistan': 19, 'Scotland': 20, 'South Africa': 21, 'Sri Lanka': 22, 'U.A.E.': 23, 'U.S.A.': 24, 'West Indies': 25, 'Zimbabwe': 26}
    return homeEncodedDict[home]

# Encoding away team
def awayEncoding(away):
    awayEncodedDict = {'Afghanistan': 0, 'Africa XI': 1, 'Asia XI': 2, 'Australia': 3, 'Bangladesh': 4, 'Bermuda': 5, 'Canada': 6, 'East Africa': 7, 'England': 8, 'Hong Kong': 9, 'ICC World XI': 10, 'India': 11, 'Ireland': 12, 'Kenya': 13, 'Namibia': 14, 'Nepal': 15, 'Netherlands': 16, 'New Zealand': 17, 'Oman': 18, 'P.N.G.': 19, 'Pakistan': 20, 'Scotland': 21, 'South Africa': 22, 'Sri Lanka': 23, 'U.A.E.': 24, 'U.S.A.': 25, 'West Indies': 26, 'Zimbabwe': 27}
    return awayEncodedDict[away]

# predicting using model
def lang_predict(home, away, toss, bat, isNeutral):
    label = model.predict([[homeEncoding(home), 0.5, toss, bat, awayEncoding(away), isNeutral, winlast5[home], winlast4[home], winlast3[home], winlast2[home], winlast1[home], winlast5[away], winlast3[away], winlast3[away], winlast2[away], winlast1[away], losslast5[home], losslast4[home], losslast3[home],
                          losslast2[home], losslast1[home], losslast5[away], losslast4[away], losslast3[away], losslast2[away], losslast1[away], drawlast5[home], drawlast4[home], drawlast3[home], drawlast2[home], drawlast1[home], drawlast5[away], drawlast4[away], drawlast3[away], drawlast2[away], drawlast1[away]]])
    return label

# Encoding toss for home and away
if toss == home:
    toss = 2.0
else:
    toss = 1.0

# Encoding toss decision for home and away
if toss == 2.0 and bat == "Batting First":
    bat = 1.0
elif toss == 2.0 and bat == "Bowling First":
    bat = 2.0
elif toss == 1.0 and bat == "Batting First":
    bat = 2.0
elif toss == 1.0 and bat == "Bowling First":
    bat = 1.0

def component(alert, winner):
    components.html(
                """
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
                <style>
                body {
                    background-color: transparent;
                }
                </style>
                <div class="alert alert-""" + alert + """" role="alert">
                <h2 class="alert-heading text-center">""" + winner + """</h2>
                </div>
                """, height=100
            )

# final predict button
if st.button("Predict"):
    if home != '' and away != '' and toss != '' and bat != '':
        result = lang_predict(home, away, toss, bat, isNeutral)
        if result == 0:
            component("success", home + " Wins!")
        elif result == 1:
            component("warning", away + " Wins!")
        else:
            component("success", "Match ends in a draw")
    else:
        component("danger", "Error! Please fill all the fields")