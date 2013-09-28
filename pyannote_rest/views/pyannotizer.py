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

from pyannote import Segment, Timeline, Annotation


class PyAnnotizer(object):
    """Convert Camomile JSON to PyAnnote objects"""

    def __init__(self):
        super(PyAnnotizer, self).__init__()

    def fragment_to_segment(self, fragment):
        return Segment(
            start=float(fragment['start']),
            end=float(fragment['end'])
        )

    def segment_to_fragment(self, segment):

        return {'start': segment.start, 'end': segment.end}

    def data_to_label(self, data):
        return str(data)

    def annotations_to_timeline(self, annotations):

        timeline = Timeline()

        for a in annotations:
            segment = self.fragment_to_segment(a['fragment'])
            timeline.add(segment)

        return timeline

    def layer_to_timeline(self, layer):
        raise NotImplementedError()

    # def timeline_to_layer(self, timeline):

    #     return {
    #         'layer_type': 'PyAnnote Timeline',
    #         'fragment_type': 'segment',
    #         'data_type': None,
    #         'annotations': self.timeline_to_annotations(timeline),
    #     }

    def annotations_to_annotation(self, annotations):

        annotation = Annotation()

        for a in annotations:
            segment = self.fragment_to_segment(a['fragment'])
            label = self.data_to_label(a['data'])
            annotation[segment, annotation.new_track(segment)] = label

        return annotation

    def layer_to_annotation(self, layer):
        raise NotImplementedError()

    # def annotation_to_layer(self, annotation):

    #     return {
    #         'layer_type': 'PyAnnote Annotation',
    #         'modality': annotation.modality,
    #         'fragment_type': 'segment',
    #         'data_type': 'label',
    #         'annotations': self.annotation_to_annotations(annotation),
    #     }
