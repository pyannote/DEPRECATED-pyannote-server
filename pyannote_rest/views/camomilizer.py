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


from pyannote import Segment, Timeline, Annotation, Unknown
from pyannote.parser.base import BaseTimelineParser, BaseAnnotationParser, BaseTextualAnnotationParser


class Camomilizer(object):
    """Convert PyAnnote objects to Camomile format"""

    def __init__(self):
        super(Camomilizer, self).__init__()

    def segment_to_fragment(self, segment):

        return {'start': segment.start, 'end': segment.end}

    def label_to_data(self, label):
        if isinstance(label, Unknown):
            return str(label)
        else:
            return label

    def timeline_to_annotations(self, timeline):

        return [
            {
                'fragment': self.segment_to_fragment(s),
                'data': None,
            } for s in timeline
        ]

    def timeline_to_layer(self, timeline):

        return {
            'layer_type': 'PyAnnote Timeline',
            'fragment_type': 'segment',
            'data_type': None,
            'annotations': self.timeline_to_annotations(timeline),
        }

    def annotation_to_annotations(self, annotation):

        return [
            {
                'fragment': self.segment_to_fragment(s),
                'data': self.label_to_data(l),
            } for s, _, l in annotation.itertracks(label=True)
        ]

    def annotation_to_layer(self, annotation):

        return {
            'layer_type': 'PyAnnote Annotation',
            'modality': annotation.modality,
            'fragment_type': 'segment',
            'data_type': 'label',
            'annotations': self.annotation_to_annotations(annotation),
        }

    def parser_to_media(self, parser):

        media = []

        for uri in parser.uris:

            if isinstance(parser, BaseTimelineParser):
                layers = [
                    self.timeline_to_layer(parser(uri=uri))
                ]

            if isinstance(parser, (BaseAnnotationParser, BaseTextualAnnotationParser)):
                layers = [
                    self.annotation_to_layer(
                        parser(uri=uri, modality=modality))
                    for modality in parser.modalities
                ]

            media.append({'name': uri, 'layers': layers})

        return media
