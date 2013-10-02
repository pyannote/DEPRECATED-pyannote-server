# PyAnnote REST API

## Installation

    $ git clone https://github.com/hbredin/pyannote.git
    $ cd pyannote
    $ git checkout develop
    $ python setup.py develop

    $ pip install pyannote-rest

## Running the server

    $ python -m pyannote_rest.run

## Using the API

### Parsers

* `/parser/` returns list of supported file formats

        $ curl -X GET http://localhost:5000/parser/
        ["mdtm", "uem"]

* `/parser/<format>` parses `POST`ed file and returns its content in Camomile JSON format.

    **Output format (JSON)**

        [
            {
                "name": MEDIA_NAME,
                "layers": [
                    {
                        "data_type": DATA_TYPE,
                        "fragment_type": FRAGMENT_TYPE,
                        "layer_type": LAYER_TYPE,
                        "annotations": [
                            {
                                "data": DATA,
                                "fragment": FRAGMENT,
                            },
                            ... # one layer usually contains
                            ... # more than one annotation
                        ]
                    },
                    ... # one file main contain more 
                    ... # more than one layer per medium 
                ]
            },
            ... # one file usually contains layers
            ... # for more than one medium 
        ]


    **Example with `mdtm` file format**

        $ curl -X POST -F file=@demo/reference.mdtm http://localhost:5000/parser/mdtm/
        [
            {
                "layers": [
                    {
                        "annotations": [
                            {
                                "data": "Olivier_TRUCHOT",
                                "fragment": {
                                    "end": 2530.698,
                                    "start": 2530.0
                                }
                            },
                            ...,
                            {
                                "data": "Arno_KLARSFELD",
                                "fragment": {
                                    "end": 2540.0,
                                    "start": 2539.66
                                }
                            }
                        ],
                        "data_type": "label",
                        "fragment_type": "segment",
                        "layer_type": "PyAnnote Annotation",
                        "modality": "speaker"
                    }
                ],
                "name": "BFMTV_BFMStory_2012-01-10_175800"
            },
            {
                "layers": [
                    {
                        "annotations": [
                            {
                                "data": "Cecile_ESMENGIAUD",
                                "fragment": {
                                    "end": 609.147,
                                    "start": 600.0
                                }
                            },
                            ...,
                            {
                                "data": "Frederic_DE_LANOUVELLE",
                                "fragment": {
                                    "end": 620.0,
                                    "start": 615.862
                                }
                            }
                        ],
                        "data_type": "label",
                        "fragment_type": "segment",
                        "layer_type": "PyAnnote Annotation",
                        "modality": "speaker"
                    }
                ],
                "name": "BFMTV_BFMStory_2012-01-23_175800"
            }
        ]


### Evaluation metrics

* `/metric/` returns list of available evaluation metrics

        $ curl -X GET http://localhost:5000/metric/
        ["detection", "diarization", "identification"]


* `/metric/<name>` compares `POST`ed reference and hypothesis and returns the corresponding evaluation metric.

    **Input format (JSON)**

        {
            "reference": [
                {
                    "data": DATA,
                    "fragment": FRAGMENT,
                },
                ... # reference layer usually contains 
                ... # more than one annotation
            ],
            "hypothesis": [
                {
                    "data": DATA,
                    "fragment": FRAGMENT,
                },
                ... # hypothesis layer usually contains
                ... # more than one annotation
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

    **Examples**

    * Speaker diarization

            $ curl -X POST -H "Content-Type: application/json" -d @demo/metric.json  http://localhost:5000/metric/diarization/
            {
                "coverage": {
                    "coverage": 0.971,
                    "correct": 11.394,
                    "total": 11.739
                },
                "diarization error rate": {
                    "diarization error rate": 0.150,
                    "confusion": 0.000,
                    "correct": 9.992,
                    "false alarm": 0.008,
                    "miss": 1.754,
                    "total": 11.746
                },
                "purity": {
                    "purity": 1.0,
                    "correct": 9.992,
                    "total": 9.992
                }
            }
 
    * Speaker identification

            $ curl -X POST -H "Content-Type: application/json" -d @demo/metric.json  http://localhost:5000/metric/identification/
            {
                "identification error rate": {
                    "identification error rate": 0.179,
                    "confusion": 0.340,
                    "correct": 9.652,
                    "false alarm": 0.008,
                    "miss": 1.754,
                    "total": 11.746
                },
                "precision": {
                    "# relevant retrieved": 9.652,
                    "# retrieved": 10.0,
                    "precision": 0.965
                },
                "recall": {
                    "# relevant": 11.746,
                    "# relevant retrieved": 9.652,
                    "recall": 0.822
                }
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

    **Output format (JSON)**

        [
            {
                "fragment": FRAGMENT,
                "data": [
                    "correct" | "miss" | "false alarm" | "confusion",
                    DATA_IN_REFERENCE,
                    DATA_IN_HYPOTHESIS,
                ]
            },
            ... # difference usually contains 
            ... # more than one annotation
        ]

    **Examples**

        $ curl -X POST -H "Content-Type: application/json" -d @demo/diff.json http://localhost:5000/error/diff
        [
            {
                "data": [
                    "miss",
                    "Arno_KLARSFELD",
                    null
                ],
                "fragment": {
                    "end": 2530.698,
                    "start": 2530.0
                }
            },
            {
                "data": [
                    "correct",
                    "Olivier_TRUCHOT",
                    "Olivier_TRUCHOT"
                ],
                "fragment": {
                    "end": 2530.698,
                    "start": 2530.0
                }
            },
            {
                "data": [
                    "false alarm",
                    null,
                    "Olivier_TRUCHOT"
                ],
                "fragment": {
                    "end": 2530.7,
                    "start": 2530.698
                }
            },
            ...,
            {
                "data": [
                    "confusion",
                    "Arno_KLARSFELD",
                    "Laurent_NEUMANN"
                ],
                "fragment": {
                    "end": 2540.0,
                    "start": 2539.665
                }
            }
        ]


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

    **Output format (JSON)**

        {
            {
                "fragment": FRAGMENT,
                "data": [
                    "both_correct" | "both_incorrect" | "improvement" | "regression",
                    [
                        "correct" | "miss" | "false alarm" | "confusion",
                        DATA_IN_REFERENCE,
                        DATA_IN_BEFORE
                    ],
                    [
                        "correct" | "miss" | "false alarm" | "confusion",
                        DATA_IN_REFERENCE,
                        DATA_IN_AFTER
                    ]
                ]
            },
            ... # regression usually contains 
            ... # more than one annotation

        }

    **Examples**

        $ curl -X POST -H "Content-Type: application/json" -d @demo/regression.json http://localhost:5000/error/regression
        [
            {
                "data": [
                    "both_correct",
                    [
                        "correct",
                        "Olivier_TRUCHOT",
                        "Olivier_TRUCHOT"
                    ],
                    [
                        "correct",
                        "Olivier_TRUCHOT",
                        "Olivier_TRUCHOT"
                    ]
                ],
                "fragment": {
                    "end": 2530.698,
                    "start": 2530.0
                }
            },
            {
                "data": [
                    "both_incorrect",
                    [
                        "miss",
                        "Arno_KLARSFELD",
                        null
                    ],
                    [
                        "miss",
                        "Arno_KLARSFELD",
                        null
                    ]
                ],
                "fragment": {
                    "end": 2530.698,
                    "start": 2530.0
                }
            },
            {
                "data": [
                    "improvement",
                    [
                        "confusion",
                        "Arno_KLARSFELD",
                        "Laurent_NEUMANN"
                    ],
                    [
                        "correct",
                        "Olivier_TRUCHOT",
                        "Olivier_TRUCHOT"
                    ]
                ],
                "fragment": {
                    "end": 2539.665,
                    "start": 2539.66
                }
            },
            ...
        ]
