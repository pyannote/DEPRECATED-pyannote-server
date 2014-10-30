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

from flask import Blueprint
from flask import request
from flask import json

metric = Blueprint('metric', __name__, url_prefix='/metric')


from pyannote.metrics.diarization import \
    DiarizationErrorRate, DiarizationPurity, DiarizationCoverage
from pyannote.metrics.detection import \
    DetectionErrorRate
from pyannote.metrics.identification import \
    IdentificationErrorRate, IdentificationRecall, IdentificationPrecision
from pyannote.metrics.segmentation import \
    SegmentationPurity, SegmentationCoverage

SUPPORTED_METRIC = {
    'diarization': [
        DiarizationErrorRate, DiarizationCoverage, DiarizationPurity],
    'detection': [
        DetectionErrorRate],
    'identification': [
        IdentificationErrorRate,
        IdentificationRecall, IdentificationPrecision],
    'segmentation': [
        SegmentationCoverage, SegmentationPurity]
}


@metric.route('/', methods=['GET'])
def get_supported():

    if request.method == 'GET':
        return json.dumps(sorted(SUPPORTED_METRIC))


@metric.route('/<name>/', methods=['POST'])
def compute_metric(name):

    if request.method == 'POST':

        metrics = [m() for m in SUPPORTED_METRIC[name]]

        data = request.json
        R = data['reference']
        H = data['hypothesis']

        return json.dumps({
            m.metric_name(): m(R, H, detailed=True)
            for m in metrics
        })
