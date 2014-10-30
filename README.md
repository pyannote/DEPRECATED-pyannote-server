# PyAnnote REST API

## Installation

    $ pip install pyannote.server

## Running the server

    $ python -m pyannote.server.run

## Using the API

### Parsers

* `/parser/` returns list of supported file formats

        $ curl -X GET http://localhost:5000/parser/
        ["mdtm", "uem"]

* `/parser/<format>` parses `POST`ed file and returns its content in PyAnnote JSON format.


### Evaluation metrics

* `/metric/` returns list of available evaluation metrics

        $ curl -X GET http://localhost:5000/metric/
        ["detection", "diarization", "identification"]


* `/metric/<name>` compares `POST`ed reference and hypothesis annotations in JSON format and returns the corresponding evaluation metric.

    **Input format (JSON)**

        {
            "reference": [
                ...
            ],
            "hypothesis": [
                ...
            ]
        }

    **Output format (JSON)**

        {
            METRIC: {
                METRIC: value,
                COMPONENT_1: value_1, 
                COMPONENT_2: value_2, 
                ... # components are values from
                ... # which the final value is computed
            },
            ... # one call to /parser/<metric> may
            ... # return more than one sub-metrics
        }


### Error analysis

* `/error/diff` compares `POST`ed reference and hypothesis and returns their differences.

    **Input format (JSON)**

        # same format as for metric/<name>
        {
            "reference": [
                ...   
            ],   
            "hypothesis": [
                ... 
            ]
        }


* `/error/regression` compares `POST`ed reference with two hypotheses and returns regressions and/or improvements brought by the second one (`after`) over the first one (`before`).

    **Input format (JSON)**

        {
            "reference": [
                ...
            ],
            "before": [
                ...
            ],
            "after": [
                ...
            ]
        }
