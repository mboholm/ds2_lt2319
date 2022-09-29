# Lab 2: Form-filling dialogue DDD using an API
## Procedure
Each step of the assignment has been followed as instructed on Canvas. However, there are some minor adjustments.
### Training `rasa` without `sort = string`
For reasons suggested by José, `rasa` was trained with data generated without `string` as `sort`. That is, in `ddds`,

```
$ tala generate rasa lab2_weather_app eng --lookup-entries city:world-cities.csv --lookup-entries country:countries.csv -x string > ../rasa-nlu/training-data-eng.yml 
```
## A note on interaction tests
12 interaction design where designed for Lab 2, representing *main menu*, *incremental*, *one-shot*, *over-answering*, *other-answering*, and *answer-revision*; versions for requesting *temperature* and *weather*; and *polite/uncertainty*, and *reordered*. The last two "conditions" where design to test `rasa` trained NLU. They do not strictly follow forms in the `grammar.xml`:

-	*polite/uncertainty*, insert words for politeness and uncertainty in forms of the grammar
-	*reordered*, change the order of components compared with forms in the grammar

### Interaction tests using `http://tdm/interact`
As expected, when run with `http://tdm/interact`, all tests are completed, except the last two ones designed for testing the `rasa` NLU (*polite/uncertainty*, and *reordered*). 
### Interaction tests using `http://pipeline/interact`
Run with `http://pipeline/interact` there are some problems. The desired output of the http-service is forwarded to the dialogue, but there are troubles with producing the expected uttearnce. 

#### Episode 1
In the first episode, the problem for all the tests is illustrated by the following example.

```
expected:
  S> The temperature is * degrees.

but got:
  S> 29.
```
Here, it the value from the http-service is sent to the dialogue, but is not correctly embedded in the utterance. In the Discord channel for the course, José suggested that this might be some bug that could be ignored, for now. However, he suggested a solution.

#### Proposed solution 
As proposed by José, I have:
1. Updated the `nlg.json` file:
```
[
    {
        "match": "answer(temperature_to_get(&individual))",
        "utterance": "The temperature is &individual degrees."
    },
    {
        "match": "answer(weather_to_get(&individual))",
        "utterance": "The weather is &individual."
    }
]
```
2. I have opened a port for the database: 
```$ kubectl port-forward svc/couchdb-talkamatic-svc-couchdb 5984 -n couchdb-talkamatic &```
3. I have updated the database:
```
$ python3 update_couch_db.py nlg gusbohom --couchdb couchdb-talkamatic
Docs to post in nlg database
  Docs to add: ['answer(temperature_to_get(&individual))', 'answer(weather_to_get(&individual))']
  Docs to delete: []
  Docs to update: []
```

#### Episode 2
The above solution solved some of the tests, namely the "temperature" tests. However, another problem has appeared. Not only `answer(temperature_to_get(&individual))` moves are uttered as `"The temperature is &individual degrees."`, also the `answer(weather_to_get(&individual))` moves are. All three "weather" tests fail:
```
======================================================================
Failure in test 'incremental, Weather'
----------------------------------------------------------------------
On line 46 of /okteto/lab2_weather_app/test/interaction_tests_eng.txt,

expected:
  S> The weather is * .

but got:
  S> The temperature is clear sky degrees.

======================================================================
Failure in test 'overanswering, Weather'
----------------------------------------------------------------------
On line 52 of /okteto/lab2_weather_app/test/interaction_tests_eng.txt,

expected:
  S> The weather is * .

but got:
  S> The temperature is clear sky degrees.

======================================================================
Failure in test 'one-shot, Weather'
----------------------------------------------------------------------
On line 56 of /okteto/lab2_weather_app/test/interaction_tests_eng.txt,

expected:
  S> The weather is * .

but got:
  S> The temperature is clear sky degrees.

----------------------------------------------------------------------
```
At the moment, I leave this problem unsolved. 