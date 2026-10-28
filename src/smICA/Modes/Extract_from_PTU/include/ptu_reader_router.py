# This file is part of the smICA repository that is distributed under the MIT license; see below.
#
#
# ############################################################################
#
# MIT License
#
# Copyright (c) 2026 Tomasz Kalwarczyk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


'''
This file is part of the smICA repository distributed under the MIT license.

Reader selection and frame metadata shared by PTU Extract and Phot2conc.
'''


import os

import numpy as np

from .phconvert_reader import PhconvertPTUreader, UnsupportedPtuRecordError


def resolve_integrated_frame_count(file_info):
    '''Return the image frame divisor for new and historical PKL files.'''

    if 'Integrated frames' in file_info:
        return max(int(file_info['Integrated frames']), 1)
    return max(int(file_info.get('Number of frames', 1)) - 1, 1)


def _load_legacy_reader():
    '''Load the historical reader only when another PTU record type requires it.'''

    try:
        from Required.Third_party.readPTU_FLIM import PTUreader
    except ImportError as error:
        raise ImportError(
            'This PTU record type is not supported by the phconvert backend '
            'and requires the optional readPTU_FLIM fallback. Run the smICA '
            'installer again and accept the legacy reader download, or place '
            'readPTU_FLIM.py in Required/Third_party manually.'
        ) from error
    return PTUreader


class RoutedPtuReader:
    '''Select phconvert for PicoHarp 300 T3 and preserve the legacy fallback.'''

    PHCONVERT_BACKEND = 'phconvert (PicoHarp 300 T3)'
    LEGACY_BACKEND = 'readPTU_FLIM (legacy fallback)'

    def __init__(self, file_path, print_header_data=False, legacy_factory=None):
        self.file_path = os.path.abspath(os.path.expanduser(os.fspath(file_path)))
        self._uses_phconvert = False

        try:
            self.ptu_image = PhconvertPTUreader(self.file_path)
        except UnsupportedPtuRecordError:
            if legacy_factory is None:
                legacy_factory = _load_legacy_reader()
            self.ptu_image = legacy_factory(
                str(self.file_path), print_header_data=print_header_data
            )
            self.backend_name = self.LEGACY_BACKEND
        else:
            self._uses_phconvert = True
            self.backend_name = self.PHCONVERT_BACKEND

        self.head = self.ptu_image.head

    @property
    def uses_phconvert(self):
        return self._uses_phconvert

    @property
    def per_frame_intensity(self):
        '''Return frame-resolved intensity when the phconvert reader is active.'''

        if not self._uses_phconvert:
            return None
        return self.ptu_image.frame_intensity

    def reconstruct(self, rows_to_skip=0):
        '''Return the six arrays used by PTU Extract.'''

        if rows_to_skip < 0:
            raise ValueError('rows_to_skip must be non-negative.')
        if self._uses_phconvert:
            return self.ptu_image.reconstruct_flim_data(
                rows_to_skip=rows_to_skip,
                include_final_frame=True
            )
        if rows_to_skip:
            return self.ptu_image.get_flim_data_stack_omit(rows_to_skip)
        return self.ptu_image.get_flim_data_stack()

    def accumulate_frame_images(self, detector, microtime_bins, weights=None):
        '''Return weighted frame images when frame coordinates are available.'''

        if not self._uses_phconvert:
            return None
        return self.ptu_image.accumulate_frame_images(
            detector,
            microtime_bins,
            weights=weights,
        )

    def frame_image_data(
            self,
            detector,
            microtime_bins,
            foreground_weights,
            background_weights):
        '''Return compact frame data when the phconvert backend is active.'''

        if not self._uses_phconvert:
            return None
        return self.ptu_image.frame_image_data(
            detector,
            microtime_bins,
            foreground_weights,
            background_weights,
        )

    def processing_metadata(self, marker_stream=None):
        '''Return reader provenance and image frame accounting.'''

        if self._uses_phconvert:
            marker_count = int(np.count_nonzero(
                self.ptu_image.marker_masks == self.ptu_image.frame_mask
            ))
            integrated_count = marker_count
            record_type = self.ptu_image.record_type
        else:
            if marker_stream is None:
                raise ValueError(
                    'Legacy frame metadata requires the reconstructed marker stream.'
                )
            marker_count = int(
                np.count_nonzero(np.asarray(marker_stream) == 4)
            )
            integrated_count = max(marker_count - 1, 1)
            record_type = 'legacy-supported PTU record'

        return {
            'Reader backend': self.backend_name,
            'TTTR record type': record_type,
            'Frame markers': marker_count,
            'Integrated frames': integrated_count
        }
