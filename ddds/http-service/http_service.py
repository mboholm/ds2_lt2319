# -*- coding: utf-8 -*-

import json

import requests # MB

from flask import Flask, request
from jinja2 import Environment

app = Flask(__name__)
environment = Environment()


def jsonfilter(value):
    return json.dumps(value)


environment.filters["json"] = jsonfilter


def error_response(message):
    response_template = environment.from_string("""
    {
      "status": "error",
      "message": {{message|json}},
      "data": {
        "version": "1.0"
      }
    }
    """)
    payload = response_template.render(message=message)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def query_response(value, grammar_entry):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": {{value|json}},
            "confidence": 1.0,
            "grammar_entry": {{grammar_entry|json}}
          }
        ]
      }
    }
    """)
    payload = response_template.render(value=value, grammar_entry=grammar_entry)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def multiple_query_response(results):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "result": [
        {% for result in results %}
          {
            "value": {{result.value|json}},
            "confidence": 1.0,
            "grammar_entry": {{result.grammar_entry|json}}
          }{{"," if not loop.last}}
        {% endfor %}
        ]
      }
    }
     """)
    payload = response_template.render(results=results)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def validator_response(is_valid):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "is_valid": {{is_valid|json}}
      }
    }
    """)
    payload = response_template.render(is_valid=is_valid)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/dummy_query_response", methods=['POST'])
def dummy_query_response():
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": "dummy",
            "confidence": 1.0,
            "grammar_entry": null
          }
        ]
      }
    }
     """)
    payload = response_template.render()
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/action_success_response", methods=['POST'])
def action_success_response():
    response_template = environment.from_string("""
   {
     "status": "success",
     "data": {
       "version": "1.1"
     }
   }
   """)
    payload = response_template.render()
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response

def switch(facts, X_for_search): # by MB
    if "from_rasa" in facts[X_for_search]["value"]:
        return facts[X_for_search]["grammar_entry"]
    else:
        return facts[X_for_search]["value"]

@app.route("/get_temp", methods=['POST'])
def get_temp(): # by MB
    payload = request.get_json() # MB. Note: Externally defined variable!
    facts   = payload["context"]["facts"]
    city    = switch(facts, "city_for_search")
    country = switch(facts, "country_for_search")

    if "unit_for_search" in facts:
        unit = switch(facts, "unit_for_search")       
    else:
        unit = "metric" # MB. ...or "standard"

    api_key = "8b9880be7d1dcfe6e8886ad128f67c15" # MB
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units={unit}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    temp = data["main"]["temp"]
    temp = str(int(temp))
    return query_response(value=temp, grammar_entry=None)

@app.route("/get_weather", methods=['POST'])
def get_weather(): # by MB
    payload = request.get_json() # Externally defined variable!
    facts   = payload["context"]["facts"]
    city    = switch(facts, "city_for_search")
    country = switch(facts, "country_for_search")    

    api_key = "8b9880be7d1dcfe6e8886ad128f67c15"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}" #MB. No need of units for the weather (default respone i Kalvin)
    response = requests.get(url)
    data = response.json()
    weather = data["weather"][0]["description"]
    return query_response(value=weather, grammar_entry=None)
