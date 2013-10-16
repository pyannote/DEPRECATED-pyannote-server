#!/usr/bin/env python
# encoding: utf-8

#
# The MIT License (MIT)
#
# Copyright (c) 2013 Hervé BREDIN (http://herve.niderb.fr/)
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

from flask import Blueprint
from flask import request
from flask import json
from flask.ext.cors import origin


metric = Blueprint('metric', __name__, url_prefix='/metric')

from pyannotizer import PyAnnotizer
pyannotizer = PyAnnotizer()

# ==== Supported formats ====

from pyannote.metric.diarization import \
    DiarizationErrorRate, DiarizationPurity, DiarizationCoverage
from pyannote.metric.detection import \
    DetectionErrorRate
from pyannote.metric.identification import \
    IdentificationErrorRate, IdentificationRecall, IdentificationPrecision


SUPPORTED_METRIC = {
    'diarization': [
        DiarizationErrorRate, DiarizationCoverage, DiarizationPurity],
    'detection': [
        DetectionErrorRate],
    'identification': [
        IdentificationErrorRate, IdentificationRecall, IdentificationPrecision]
}


@metric.route('/', methods=['GET', 'OPTIONS'])
@origin(origin='*', methods=['GET', 'OPTIONS'])
def get_supported():
    return json.dumps(sorted(SUPPORTED_METRIC))


@metric.route('/<name>/', methods=['POST', 'OPTIONS'])
@origin(origin='*', methods=['POST', 'OPTIONS'])
def compute_metric(name):

    if request.method == 'POST':

        metrics = [m() for m in SUPPORTED_METRIC[name]]

        reference = request.json['reference']
        hypothesis = request.json['hypothesis']

        R = pyannotizer.annotations_to_annotation(reference)
        H = pyannotizer.annotations_to_annotation(hypothesis)

        return json.dumps({
            m.metric_name(): m(R, H, detailed=True)
            for m in metrics
            }
        )
