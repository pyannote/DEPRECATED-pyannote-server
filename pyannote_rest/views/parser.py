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
#from flask.ext.cors import origin
from pyannote_rest.crossdomain import crossdomain

parser = Blueprint('parser', __name__, url_prefix='/parser')

from camomilizer import Camomilizer
camomilizer = Camomilizer()


# ==== Supported formats ====

import pyannote.parser.mdtm
import pyannote.parser.uem

SUPPORTED_FORMAT = {
    'mdtm': [pyannote.parser.mdtm, pyannote.parser.mdtm.MDTMParser],
    'uem': [pyannote.parser.uem, pyannote.parser.uem.UEMParser],
}


# GET /parser/ returns
@parser.route('/', methods=['GET'])
@crossdomain(origin='*', headers='Content-Type')
def get_supported():
    return json.dumps(sorted(SUPPORTED_FORMAT))


@parser.route('/<format>/', methods=['GET', 'POST'])
@crossdomain(origin='*', headers='Content-Type')
def parse_file(format):

    if request.method == 'POST':

        # initialize new parser for requested format
        parser = SUPPORTED_FORMAT[format][1]()

        # parse uploaded file
        uploaded = request.files['file']
        parser.read(uploaded)

        return json.dumps(camomilizer.parser_to_media(parser))

    if request.method == 'GET':

        return SUPPORTED_FORMAT[format][0].__doc__
