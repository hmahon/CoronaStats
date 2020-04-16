import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
pd.set_option('mode.chained_assignment', None)

# Loading the files
raw_county_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")
raw_state_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")

# Uppercasing the values so dont have to deal with that
raw_county_data['county'] = raw_county_data['county'].str.upper() 
raw_county_data['state'] = raw_county_data['state'].str.upper() 
raw_state_data['state'] = raw_state_data['state'].str.upper()



# --------------- Helper Functions for my code ----------------------
def convert_day_to_speech(day):
    if day == 1:
        day = '1st'
    elif day == 2:
        day = '2nd'
    elif day == 3:
        day = '3rd'
    elif day == 4:
        day = '4th'
    elif day == 5:
        day = '5th'
    elif day == 6:
        day = '6th'
    elif day == 7:
        day = '7th'
    elif day == 8:
        day = '8th'
    elif day == 9:
        day = '9th'
    elif day == 10:
        day = '10th'
    elif day == 11:
        day = '11th'
    elif day == 12:
        day = '12th'
    elif day == 13:
        day = '13th'
    elif day == 14:
        day = '14th'
    elif day == 15:
        day = '15th'
    elif day == 16:
        day = '16th'
    elif day == 17:
        day = '17th'
    elif day == 18:
        day = '18th'
    elif day == 19:
        day = '19th'
    elif day == 20:
        day = '20th'
    elif day == 21:
        day = '21st'
    elif day == 22:
        day = '22nd'
    elif day == 23:
        day = '23rd'
    elif day == 24:
        day = '24th'
    elif day == 25:
        day = '25th'
    elif day == 26:
        day = '26th'
    elif day == 27:
        day = '27th'
    elif day == 28:
        day = '28th'
    elif day == 29:
        day = '29th'
    elif day == 30:
        day = '30th'
    elif day == 31:
        day = '31st'      
    return day
	
	
def convert_month_to_speech(month):
    if month == 1:
        month = 'January'
    elif month == 2:
        month = 'February'
    elif month == 3:
        month = 'March'
    elif month == 4:
        month = 'April'
    elif month == 5:
        month = 'May'
    elif month == 6:
        month = 'June'
    elif month == 7:
        month = 'July'
    elif month == 8:
        month = 'August'
    elif month == 9:
        month = 'September'
    elif month == 10:
        month = 'October'
    elif month == 11:
        month = 'November'
    elif month == 12:
        month = 'December'
    return month

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    
    # this is the only title that matters as of 1/10/20
    card_title = 'Corona Virus Tracking'
    
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': card_title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
    
def total_country(metric):
    
    print('function = total_country')
    print('metric = ', metric)
    data = raw_state_data

    if metric == 'cases':    
        current_date = data['date'].max()
        data = data[data['date']==current_date]
        cases_total = data['cases'].sum()
        cases_total = round(cases_total, -3)
        year, month, day = (int(x) for x in current_date.split('-'))
        day = convert_day_to_speech(day)        
        month = convert_month_to_speech(month)
        speech_output = 'There have been {0} cases in the United States as of {1} {2}'.format(cases_total, month, day)


    elif metric == 'deaths':
        current_date = data['date'].max()
        data = data[data['date']==current_date]
        deaths_total = data['deaths'].sum()
        deaths_total = round(deaths_total, -1)
        year, month, day = (int(x) for x in current_date.split('-'))
        day = convert_day_to_speech(day)
        month = convert_month_to_speech(month)
        speech_output = 'There have been {0} deaths in the United States as of {1} {2}'.format(deaths_total, month, day)

    reprompt_text = "Ask something else. We have numbers for any state or county"

    session_attributes = {}
    card_title = "Country Totals"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def total_timeframe_country(metric, timeframe_unit, timeframe_metric):

    print('function = total_timeframe_country')
    print('metric = ', metric)
    print('timeframe_unit =', timeframe_unit)
    print('timeframe_metric =', timeframe_metric)
   
    data = raw_state_data

    if timeframe_metric == 'days':
        if timeframe_unit == 1:
            timeframe_metric = '24 hours' 
        data['Datetime'] = pd.to_datetime(data['date'], format= '%Y-%m-%d')
        max_date = data['Datetime'].max()
        min_date = max_date - timedelta(timeframe_unit)
        data = data[data['Datetime'] >= min_date]
        data = data.groupby("Datetime").sum()
        if timeframe_unit == 1:
            timeframe_unit = ''
        if metric == 'cases':
            min_cases = data['cases'].min()
            max_cases = data['cases'].max()
            new_cases = round(max_cases - min_cases,-3) 
            speech_output = 'There were {0} new cases in the last {1} {2}'.format(new_cases, timeframe_unit, timeframe_metric)  
        elif metric == 'deaths':
            min_deaths = data['deaths'].min()
            max_deaths = data['deaths'].max()
            new_deaths = round(max_deaths - min_deaths,-1)  
            speech_output = 'There were {0} new deaths in the last {1} {2}'.format(new_deaths, timeframe_unit, timeframe_metric)

        
    elif timeframe_metric == 'weeks':
        if timeframe_unit == 1:
            timeframe_metric = 'week'        
        data['Datetime'] = pd.to_datetime(data['date'], format= '%Y-%m-%d')
        max_date = data['Datetime'].max()
        min_date = max_date - (timedelta(timeframe_unit) * 7) 
        data = data[data['Datetime'] >= min_date]
        data = data.groupby("Datetime").sum()
        if timeframe_unit == 1:
            timeframe_unit = ''
        if metric == 'cases':
            min_cases = data['cases'].min()
            max_cases = data['cases'].max()
            new_cases = round(max_cases - min_cases, -3)
            speech_output = 'There have been {0} new cases in the last {1} {2}'.format(new_cases, timeframe_unit, timeframe_metric)
        elif metric == 'deaths':
            min_deaths = data['deaths'].min()
            max_deaths = data['deaths'].max()
            new_deaths = round(max_deaths - min_deaths, -1)  
            speech_output = 'There have been {0} new deaths in the last {1} {2}'.format(new_deaths, timeframe_unit, timeframe_metric)

        
    elif timeframe_metric == 'months':
        if timeframe_unit == 1:
            timeframe_metric = 'month'        
        data['Datetime'] = pd.to_datetime(data['date'], format= '%Y-%m-%d')
        max_date = data['Datetime'].max()
        min_date = max_date - (timedelta(timeframe_unit) * 30) 
        data = data[data['Datetime'] >= min_date]
        data = data.groupby("Datetime").sum()
        if timeframe_unit == 1:
            timeframe_unit = ''
        if metric == 'cases':
            min_cases = data['cases'].min()
            max_cases = data['cases'].max()
            new_cases = round(max_cases - min_cases, -3) 
            speech_output = 'There have been {0} new cases in the last {1} {2}'.format(new_cases, timeframe_unit, timeframe_metric)
        elif metric == 'deaths':
            min_deaths = data['deaths'].min()
            max_deaths = data['deaths'].max()
            new_deaths = round(max_deaths - min_deaths, -1)  
            speech_output = 'There have been {0} new deaths in the last {1} {2}'.format(new_deaths, timeframe_unit, timeframe_metric)


    reprompt_text = "Ask something else. We have numbers for any state or county"

    session_attributes = {}
    card_title = "Country Totals - Specific Timeframe"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def total_state(metric, state):
    print('function = total_state')
    print('metric = ', metric)
    print('state =', state)
    
    data = raw_state_data
    data = data[data['state'] == state]

    if metric == 'cases':
        current_date = data['date'].max()
        data = data[data['date']==current_date]
        cases_total = data['cases'].sum()
        cases_total = round(cases_total, -2)
        year, month, day = (int(x) for x in current_date.split('-'))
        day = convert_day_to_speech(day)
        month = convert_month_to_speech(month)
        speech_output = 'There have been {0} cases in {3} as of {1}, {2}'.format(cases_total, month, day, state)   

    elif metric == 'deaths': 
        current_date = data['date'].max()
        data = data[data['date']==current_date]
        deaths_total = data['deaths'].sum()
        deaths_total = round(deaths_total, -2)
        year, month, day = (int(x) for x in current_date.split('-'))        
        day = convert_day_to_speech(day)
        month = convert_month_to_speech(month)
        speech_output = 'There have been {0} deaths in {3} as of {1}, {2}'.format(deaths_total, month, day, state)
    

    reprompt_text = "Ask something else. We have numbers for any state or county"

    session_attributes = {}
    card_title = "State Totals - All Time"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def total_timeframe_state(metric, timeframe_unit, timeframe_metric, state):
    print('function = total_timeframe_state')
    print('metric = ', metric)
    print('timeframe_unit =', timeframe_unit)
    print('timeframe_metric =', timeframe_metric)
    print('state =', state)
   
    data = raw_state_data 
    data = data[data['state'] == state]

    if timeframe_metric == 'days':
        if timeframe_unit == 1:
            timeframe_metric = '24 hours' 
        data['Datetime'] = pd.to_datetime(data['date'], format= '%Y-%m-%d')
        max_date = data['Datetime'].max()
        min_date = max_date - timedelta(timeframe_unit)
        data = data[data['Datetime'] >= min_date]
        data = data.groupby("Datetime").sum()
        if timeframe_unit == 1:
            timeframe_unit = ''
        if metric == 'cases':
            min_cases = data['cases'].min()
            max_cases = data['cases'].max()
            new_cases = round(max_cases - min_cases,-1) 
            speech_output = 'There were {0} new cases in {3} in the last {1} {2}'.format(new_cases, timeframe_unit, timeframe_metric, state)
        elif metric == 'deaths':
            min_deaths = data['deaths'].min()
            max_deaths = data['deaths'].max()
            new_deaths = round(max_deaths - min_deaths, -1)  
            speech_output = 'There were {0} new deaths in {3} in the last {1} {2}'.format(new_deaths, timeframe_unit, timeframe_metric, state)        
        
    elif timeframe_metric == 'weeks':
        if timeframe_unit == 1:
            timeframe_metric = 'week'        
        data['Datetime'] = pd.to_datetime(data['date'], format= '%Y-%m-%d')
        max_date = data['Datetime'].max()
        min_date = max_date - (timedelta(timeframe_unit) * 7) 
        data = data[data['Datetime'] >= min_date]
        data = data.groupby("Datetime").sum()
        if timeframe_unit == 1:
            timeframe_unit = ''
        if metric == 'cases':
            min_cases = data['cases'].min()
            max_cases = data['cases'].max()
            new_cases = round(max_cases - min_cases, -2) 
            speech_output = 'There have been {0} new cases in {3} in the last {1} {2}'.format(new_cases, timeframe_unit, timeframe_metric, state)
        elif metric == 'deaths':
            min_deaths = data['deaths'].min()
            max_deaths = data['deaths'].max()
            new_deaths = round(max_deaths - min_deaths, -2)
            speech_output = 'There have been {0} new deaths in {3} in the last {1} {2}'.format(new_deaths, timeframe_unit, timeframe_metric, state)
        
    elif timeframe_metric == 'months':
        if timeframe_unit == 1:
            timeframe_metric = 'month'        
        data['Datetime'] = pd.to_datetime(data['date'], format= '%Y-%m-%d')
        max_date = data['Datetime'].max()
        min_date = max_date - (timedelta(timeframe_unit) * 30) 
        data = data[data['Datetime'] >= min_date]
        data = data.groupby("Datetime").sum()
        if timeframe_unit == 1:
            timeframe_unit = ''
        if metric == 'cases':
            min_cases = data['cases'].min()
            max_cases = data['cases'].max()
            new_cases = round(max_cases - min_cases, -2) 
            speech_output = 'There have been {0} new cases in {3} in the last {1} {2}'.format(new_cases, timeframe_unit, timeframe_metric, state)
        elif metric == 'deaths':
            min_deaths = data['deaths'].min()
            max_deaths = data['deaths'].max()
            new_deaths = round(max_deaths - min_deaths, -2) 
            speech_output = 'There have been {0} new deaths in {3} in the last {1} {2}'.format(new_deaths, timeframe_unit, timeframe_metric, state)        

    reprompt_text = "Ask something else. We have numbers for any state or county"

    session_attributes = {}
    card_title = "State Totals - Specific Timeframe"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def total_county(metric, state, county):
    print('function = total_county')
    print('metric = ', metric)
    print('state =', state)
    print('county = ', county)

    data = raw_county_data 
    data = data[data['state'] == state]
    data = data[data['county'] == county]
  
    if metric == 'cases':
        current_date = data['date'].max()
        data = data[data['date']==current_date]
        cases_total = data['cases'].sum()
        cases_total = round(cases_total, -2)
        year, month, day = (int(x) for x in current_date.split('-'))
        day = convert_day_to_speech(day)
        month = convert_month_to_speech(month)    
        speech_output = 'There have been {0} cases in {3} as of {1}, {2}'.format(cases_total, month, day, county) 

    elif metric == 'deaths':
        current_date = data['date'].max()
        data = data[data['date']==current_date]
        deaths_total = data['deaths'].sum()
        deaths_total = round(deaths_total, -1)
        year, month, day = (int(x) for x in current_date.split('-'))
        day = convert_day_to_speech(day)
        month = convert_month_to_speech(month)  
        speech_output = 'There have been {0} deaths in {3} County as of {1}, {2}'.format(deaths_total, month, day, county)
        
    reprompt_text = "Ask something else. We have numbers for any state or county"
    
    session_attributes = {}
    card_title = "County Totals - All Time"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def total_timeframe_county(metric, timeframe_unit, timeframe_metric, state, county):
    print('function = total_timeframe_county')
    print('metric = ', metric)
    print('timeframe_unit =', timeframe_unit)
    print('timeframe_metric =', timeframe_metric)
    print('state =', state)
    print('county =', county)

    data = raw_county_data 
    data = data[data['state'] == state]
    data = data[data['county'] == county]

    if timeframe_metric == 'days':
        if timeframe_unit == 1:
            timeframe_metric = '24 hours' 
        data['Datetime'] = pd.to_datetime(data['date'], format= '%Y-%m-%d')
        max_date = data['Datetime'].max()
        min_date = max_date - timedelta(timeframe_unit)
        data = data[data['Datetime'] >= min_date]
        data = data.groupby("Datetime").sum()
        if timeframe_unit == 1:
            timeframe_unit = ''
        if metric == 'cases':
            min_cases = data['cases'].min()
            max_cases = data['cases'].max()
            new_cases = max_cases - min_cases 
            speech_output = 'There were {0} new cases in {3} County in the last {1} {2}'.format(new_cases, timeframe_unit, timeframe_metric, county)

        elif metric == 'deaths':
            min_deaths = data['deaths'].min()
            max_deaths = data['deaths'].max()
            new_deaths = max_deaths - min_deaths  
            speech_output = 'There were {0} new deaths in {3} County in the last {1} {2}'.format(new_deaths, timeframe_unit, timeframe_metric, county)
        
    elif timeframe_metric == 'weeks':
        if timeframe_unit == 1:
            timeframe_metric = 'week'        
        data['Datetime'] = pd.to_datetime(data['date'], format= '%Y-%m-%d')
        max_date = data['Datetime'].max()
        min_date = max_date - (timedelta(timeframe_unit) * 7) 
        data = data[data['Datetime'] >= min_date]
        data = data.groupby("Datetime").sum()
        if timeframe_unit == 1:
            timeframe_unit = ''
        if metric == 'cases':
            min_cases = data['cases'].min()
            max_cases = data['cases'].max()
            new_cases = max_cases - min_cases 
            speech_output = 'There have been {0} new cases in {3} County in the last {1} {2}'.format(new_cases, timeframe_unit, timeframe_metric, county)

        elif metric == 'deaths':
            min_deaths = data['deaths'].min()
            max_deaths = data['deaths'].max()
            new_deaths = max_deaths - min_deaths  
            speech_output = 'There have been {0} new deaths in {3} County in the last {1} {2}'.format(new_deaths, timeframe_unit, timeframe_metric, county)
        
    elif timeframe_metric == 'months':
        if timeframe_unit == 1:
            timeframe_metric = 'month'        
        data['Datetime'] = pd.to_datetime(data['date'], format= '%Y-%m-%d')
        max_date = data['Datetime'].max()
        min_date = max_date - (timedelta(timeframe_unit) * 30) 
        data = data[data['Datetime'] >= min_date]
        data = data.groupby("Datetime").sum()
        if timeframe_unit == 1:
            timeframe_unit = ''
        if metric == 'cases':
            min_cases = data['cases'].min()
            max_cases = data['cases'].max()
            new_cases = max_cases - min_cases 
            speech_output = 'There have been {0} new cases in {3} County in the last {1} {2}'.format(new_cases, timeframe_unit, timeframe_metric, county)
        elif metric == 'deaths':
            min_deaths = data['deaths'].min()
            max_deaths = data['deaths'].max()
            new_deaths = max_deaths - min_deaths  
            speech_output = 'There have been {0} new deaths in {3} County in the last {1} {2}'.format(new_deaths, timeframe_unit, timeframe_metric, county)
    
    reprompt_text = "Ask something else. We have numbers for any state or county"

    session_attributes = {}
    card_title = "County Totals - Specific Timeframe"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    print('Checkpoint 5 - response is built')
        
# --------------- TEST FUNCTION # -----------------
def get_test_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    print('Understanding test function')
    session_attributes = {}
    card_title = "Test"
    speech_output = "This is a test message"
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
		
		


		
############# pre configured 
		
		

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome to your #1 source for corona stats"
    speech_output = "Welcome to Corona Stats. Ask me how many cases or deaths are in the U.S., your state, or your county"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, let's help you track this virus!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_help_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Help for Corona Stats"
    speech_output = "To use this skill, say things like How many deaths in Orange County California in the past two weeks"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, let's help you track this virus!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_fallback_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Fallback for Corona Stats"
    speech_output = "Sorry, I'm not the brightest and don't understand. To use this skill, say things like, 'How many cases were there in California yesterday?'"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, let's help you track this virus!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Hope you got what you needed! " \
                    "Remember to wash your hands and have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']


 ## NOTETODO: MAKE SURE YOU REMOVE 'RETURN' WHEN MAKING THESE FUNCTONS ABOVE!!!     

    # Dispatch to your skill's intent handlers
    if intent_name == "total_country":
        print('understanding the total_country function is being called')
        metric = intent['slots']['metric']['value']
        print('understanding the total_country function is being called')
        return total_country(metric)

    elif intent_name == "total_state":
        print('understanding the total_state function is being called')
        metric = intent['slots']['metric']['value']
        state = intent['slots']['state']['value'].upper()  # uppercasing 
        print('understanding the total_state function is being called')
        return total_state(metric, state)

    elif intent_name == "total_county":
        print('understanding the total_county function is being called')
        metric = intent['slots']['metric']['value']
        state = intent['slots']['state']['value'].upper()  # uppercasing 
        county = intent['slots']['county']['value'].upper()  # uppercasing 
        print('understanding the total_county function is being called')
        return total_county(metric, state, county)

    elif intent_name == 'total_timeframe_country':
        print('understanding the total_timeframe_country function is being called')
        if 'value' in intent['slots']['timeframe_unit']:
            timeframe_unit = int(intent['slots']['timeframe_unit']['value'])
        else:
            timeframe_unit = 1
    # need to adjust for plural. synonym isn't doing the job. could consider a fuzzy match
        if intent['slots']['timeframe_metric']['value'] == 'today':
            timeframe_metric = 'days'  
        elif intent['slots']['timeframe_metric']['value'] == 'yesterday':
            timeframe_metric = 'days'    
        elif intent['slots']['timeframe_metric']['value'] == 'day':
            timeframe_metric = 'days'
        elif intent['slots']['timeframe_metric']['value'] == 'week':
            timeframe_metric = 'weeks'
        elif intent['slots']['timeframe_metric']['value'] == 'month':
            timeframe_metric = 'months'
        else:
            timeframe_metric = intent['slots']['timeframe_metric']['value']
        metric = intent['slots']['metric']['value']
        return total_timeframe_country(metric, timeframe_unit, timeframe_metric)

    elif intent_name == 'total_timeframe_state':
        print('understanding the total_timeframe_state function is being called')
    
        if 'value' in intent['slots']['timeframe_unit']:
            timeframe_unit = int(intent['slots']['timeframe_unit']['value'])
        else:
            timeframe_unit = 1
    # need this to adjust for plural. synonym isn't doing the job. could consider a fuzzy match
        if intent['slots']['timeframe_metric']['value'] == 'today':
            timeframe_metric = 'days'  
        elif intent['slots']['timeframe_metric']['value'] == 'yesterday':
            timeframe_metric = 'days'    
        elif intent['slots']['timeframe_metric']['value'] == 'day':
            timeframe_metric = 'days'
        elif intent['slots']['timeframe_metric']['value'] == 'week':
            timeframe_metric = 'weeks'
        elif intent['slots']['timeframe_metric']['value'] == 'month':
            timeframe_metric = 'months'
        else:
            timeframe_metric = intent['slots']['timeframe_metric']['value']
        metric = intent['slots']['metric']['value']
        state = intent['slots']['state']['value'].upper()  # uppercasing 
        return total_timeframe_state(metric, timeframe_unit, timeframe_metric, state)


    elif intent_name == 'total_timeframe_county':
        print('understanding the total_timeframe_county function is being called')
    
        if 'value' in intent['slots']['timeframe_unit']:
            timeframe_unit = int(intent['slots']['timeframe_unit']['value'])
        else:
            timeframe_unit = 1
    # need this to adjust for plural. synonym isn't doing the job. could consider a fuzzy match
        if intent['slots']['timeframe_metric']['value'] == 'today':
            timeframe_metric = 'days'  
        elif intent['slots']['timeframe_metric']['value'] == 'yesterday':
            timeframe_metric = 'days'    
        elif intent['slots']['timeframe_metric']['value'] == 'day':
            timeframe_metric = 'days'
        elif intent['slots']['timeframe_metric']['value'] == 'week':
            timeframe_metric = 'weeks'
        elif intent['slots']['timeframe_metric']['value'] == 'month':
            timeframe_metric = 'months'
        else:
            timeframe_metric = intent['slots']['timeframe_metric']['value']
        metric = intent['slots']['metric']['value']
        state = intent['slots']['state']['value'].upper()  # uppercasing 
        county = intent['slots']['county']['value'].upper()  # uppercasing 
        return total_timeframe_county(metric, timeframe_unit, timeframe_metric, state, county)
        print('finished running function on lambda end')


    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()   
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
  #  if (event['session']['application']['applicationId'] !=
  #      "amzn1.echo-sdk-ams.app.amzn1.ask.skill.ec75bb33-b4b5-4d29-95c7-85cd9abe1674"):
  #      raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
            event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])

		
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
	
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])