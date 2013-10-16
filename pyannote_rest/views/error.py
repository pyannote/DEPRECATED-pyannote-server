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

error = Blueprint('error', __name__, url_prefix='/error')

from pyannotizer import PyAnnotizer
from camomilizer import Camomilizer

pyannotizer = PyAnnotizer()
camomilizer = Camomilizer()

# ==== Supported formats ====

from pyannote.error.diff import Diff
diff = Diff()


@error.route('/diff', methods=['POST', 'OPTIONS'])
@origin(origin='*', methods=['POST', 'OPTIONS'])
def compute_diff():

    if request.method == 'POST':

        reference = request.json['reference']
        hypothesis = request.json['hypothesis']

        R = pyannotizer.annotations_to_annotation(reference)
        H = pyannotizer.annotations_to_annotation(hypothesis)

        D = diff.compare(R, H)

        return json.dumps(camomilizer.annotation_to_annotations(D))


@error.route('/regression', methods=['POST', 'OPTIONS'])
@origin(origin='*', methods=['POST', 'OPTIONS'])
def compute_regression():

    if request.method == 'POST':

        reference = request.json['reference']
        before = request.json['before']
        after = request.json['after']

        R = pyannotizer.annotations_to_annotation(reference)
        B = pyannotizer.annotations_to_annotation(before)
        A = pyannotizer.annotations_to_annotation(after)

        D = diff.regression(R, B, A)

        return json.dumps(camomilizer.annotation_to_annotations(D))
