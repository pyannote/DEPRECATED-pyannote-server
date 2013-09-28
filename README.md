# PyAnnote REST API

## Requirements

    $ pip install pyannote
    $ pip install flask

## Running the server

    $ python -m pyannote_rest.run

## Using the API

### Parsers

* `/parser/` returns list of supported file formats

        $ curl -X GET http://localhost:5000/parser/
        ["mdtm", "uem"]

* `/parser/<format>` parses `POST`ed file and returns its content in Camomile JSON format.

    **Example with `mdtm` file format**

        $ curl -X POST -F file=@demo/reference.mdtm http://localhost:5000/parser/mdtm/
        [
            {
                name: "media_name",
                layers: {
                    data_type: "label",
                    fragment_type: "segment",
                    annotations: [
                        {
                            fragment: {

                            }
                        },
                    ]
                }
            }
        ]

    **Example with `uem` file format** 

        $ curl -X POST -F file=@demo/transcribed.uem http://localhost:5000/parser/uem/


### Evaluation metrics

* `/metric/` returns list of available evaluation metrics

        $ curl -X GET http://localhost:5000/metric/
        ["detection", "diarization", "identification"]


* `/metric/<name>` compares `POST`ed reference and hypothesis and returns the corresponding evaluation metric.

    **Input format (JSON)**

        {
            "reference": [...],
            "hypothesis": [...]
        }

    **Output format (JSON)**

        {

        }

    **Examples**

        $ curl -X POST -H "Content-Type: application/json" -d @demo/metric.json  http://localhost:5000/metric/diarization/
        $ curl -X POST -H "Content-Type: application/json" -d @demo/metric.json  http://localhost:5000/metric/identification/


### Error analysis

* `/error/diff` compares `POST`ed reference and hypothesis and returns their differences.

    **Input format (JSON)**

        {
            "reference": [...],
            "hypothesis": [...]
        }

    **Output format (JSON)**

        {

        }

    **Examples**

        $ curl -X POST -H "Content-Type: application/json" -d @demo/diff.json http://localhost:5000/error/diff

* `/error/regression` compares `POST`ed reference and two hypotheses and returns regressions and/or improvements brought by the second one.

    **Input format (JSON)**

        {
            "reference": [...],
            "before": [...],
            "after": [...]
        }

    **Output format (JSON)**

        {

        }

    **Examples**

        $ curl -X POST -H "Content-Type: application/json" -d @demo/regression.json http://localhost:5000/error/regression
