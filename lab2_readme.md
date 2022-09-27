# Lab 2: Form-filling dialogue DDD using an API
## Procedure
Each step of the assignment has been followed as instructed on Canvas. However, there are some minor adjustments.
### Training `rasa` without `sort = string`
For reasons suggested by José, `rasa` was trained with data generated without `string` as `sort`. That is, in `ddds`,

```
$ tala generate rasa lab2_weather_app eng --lookup-entries city:world-cities.csv --lookup-entries country:countries.csv -x string > ../rasa-nlu/training-data-eng.yml 
```
## A note on interaction tests
13 interaction design where designed for Lab 2, representing *main menu*, *incremental*, *one-shot*, *over-answering*, *other-answering*, and *answer-revision*; versions for requesting *temperature* and *weather*; and *polite/uncertainty*, *reordered* and *miss-spelled*. The last three "conditions" where design to test `rasa` trained NLU. They do not strictly follow forms in the `grammar.xml`:

-	*polite/uncertainty*, insert words for politeness and uncertainty in forms of the grammar
-	*reordered*, change the order of components compared with forms in the grammar
-	*miss-spelled* words (not considered in the grammar)

### Interaction tests using `http://tdm/interact`
As expected, when run with `http://tdm/interact`, all tests are completed, except the three last ones designed for testing the `rasa` NLU (*polite/uncertainty*, *reordered* and *miss-spelled*). 
### Interaction tests using `http://pipeline/interact`
Run with `http://tdm/interact` the utterances are not completed as expected. However, the error is systematic. Consider, for example: 
```
expected:
  S> The temperature is * degrees.

but got:
  S> 29.
```
The system does not pass the value from the http-service to the template for system answer ("The temperature is $TEMPERATURE degrees"), but only returns the value. All tests fail in this manner. This error is ignored, as suggested by José, on the Discord channel for the course. 
