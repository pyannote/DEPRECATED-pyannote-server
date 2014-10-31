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

error = Blueprint('error', __name__, url_prefix='/error')

from pyannote.metrics.errors.identification import IdentificationErrorAnalysis
from pyannote.metrics.errors.segmentation import SegmentationError

identificationErrorAnalysis = IdentificationErrorAnalysis()
segmentation_error = SegmentationError()


@error.route('/diff', methods=['POST'])
def compute_diff():

    if request.method == 'POST':

        data = request.json
        R = data['reference']
        H = data['hypothesis']

        D = identificationErrorAnalysis.difference(R, H)

        return json.dumps(D)


@error.route('/regression', methods=['POST'])
def compute_regression():

    if request.method == 'POST':

        data = request.json

        R = data['reference']
        B = data['before']
        A = data['after']

        D = identificationErrorAnalysis.regression(R, B, A)

        return json.dumps(D)


@error.route('/segmentation', methods=['POST'])
def compute_segmentation_error():

    if request.method == 'POST':

        data = request.json
        R = data['reference']
        H = data['hypothesis']

        E = segmentation_error(R, H)

        return json.dumps(E)
