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

parser = Blueprint('parser', __name__, url_prefix='/parser')

from camomilizer import Camomilizer
camomilizer = Camomilizer()


# ==== Supported formats ====

from pyannote.parser.mdtm import MDTMParser
from pyannote.parser.uem import UEMParser

SUPPORTED_FORMAT = {
    'mdtm': MDTMParser,
    'uem': UEMParser,
}


# GET /parser/ returns
@parser.route('/', methods=['GET'])
def get_supported():
    return json.dumps(sorted(SUPPORTED_FORMAT))


@parser.route('/<format>/', methods=['GET', 'POST'])
def parse_file(format):

    if request.method == 'POST':

        # initialize new parser for requested format
        parser = SUPPORTED_FORMAT[format]()

        # parse uploaded file
        uploaded = request.files['file']
        parser.read(uploaded)

        return json.dumps(camomilizer.parser_to_media(parser))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
