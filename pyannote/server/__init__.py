#!/usr/bin/env python
# encoding: utf-8

#
# The MIT License (MIT)
#
# Copyright (c) 2013-2014 CNRS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr/

from flask import Flask
from flask.json import JSONEncoder, JSONDecoder
import pyannote.core.json


class PyAnnoteJSONEncoder(JSONEncoder):

    def default(self, o):

        from pyannote.core.segment import Segment
        from pyannote.core.timeline import Timeline
        from pyannote.core.annotation import Annotation
        from pyannote.core.transcription import Transcription

        if isinstance(o, (Segment, Timeline, Annotation, Transcription)):
            return o.for_json()

        return super(PyAnnoteJSONEncoder, self).default(o)


class PyAnnoteJSONDecoder(JSONDecoder):
    def __init__(self, **kwargs):
        super(PyAnnoteJSONDecoder, self).__init__(
            object_hook=pyannote.core.json.object_hook, **kwargs)

app = Flask(__name__)
app.json_encoder = PyAnnoteJSONEncoder
app.json_decoder = PyAnnoteJSONDecoder


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
