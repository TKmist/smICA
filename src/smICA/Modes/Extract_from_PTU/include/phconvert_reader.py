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

PicoHarp 300 T3 reader based on phconvert. Binary PTU decoding, overflow
correction and header parsing are delegated to phconvert. This module builds
the raster image expected by PTU Extract.
'''


import os

import numpy as np
from phconvert import pqreader


PICOHARP300_T3_RECORD = 'rtPicoHarp300T3'
DEFAULT_ROUTE_MAP = {1: 0, 2: 1, 4: 0}


class UnsupportedPtuRecordError(NotImplementedError):
    '''Signal that the selector should use the historical reader.'''


class PhconvertPTUreader:
    '''Read PicoHarp 300 T3 data and reconstruct the smICA FLIM image.'''

    def __init__(self, file_path, detector_route_map=None):
        self.file_path = os.path.abspath(os.path.expanduser(os.fspath(file_path)))
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(self.file_path)

        if detector_route_map is None:
            self.detector_route_map = dict(DEFAULT_ROUTE_MAP)
        else:
            self.detector_route_map = dict(detector_route_map)

        self.frame_intensity = None
        self.frame_coordinates = None
        self._decode_ptu()
        self._read_header_values()
        self._prepare_image_variables()
        self._validate_image_data()

    @staticmethod
    def _tag_value(tags, tag_name):
        if tag_name not in tags:
            raise ValueError('Required PTU header tag is missing: ' + tag_name)
        tag = tags[tag_name]
        if isinstance(tag, list):
            if len(tag) != 1:
                raise ValueError(
                    'Header tag ' + tag_name + ' must contain exactly one value.'
                )
            tag = tag[0]
        if 'data' in tag:
            return tag['data']
        return tag['value']

    def _decode_ptu(self):
        decoded = pqreader.load_ptu(
            str(self.file_path),
            return_marker=True,
            ovcfunc='base'
        )
        macro_ticks, route_ids, micro_bins, metadata, marker_routes = decoded

        self.record_type = str(metadata['record_type'])
        if self.record_type != PICOHARP300_T3_RECORD:
            raise UnsupportedPtuRecordError(
                self.record_type + ' is not supported by the phconvert image reader.'
            )

        marker_event = np.isin(route_ids, marker_routes)
        marker_masks = np.zeros(route_ids.shape, dtype=np.uint8)
        marker_masks[marker_event] = micro_bins[marker_event].astype(np.uint8)

        self.macro_ticks = macro_ticks.astype(np.uint64, copy=False)
        self.micro_bins = micro_bins.astype(np.uint16, copy=False)
        self.route_ids = route_ids
        self.marker_masks = marker_masks
        self.marker_routes = marker_routes
        self.metadata = metadata

    def _read_header_values(self):
        tags = self.metadata['tags']
        required_tags = (
            'MeasDesc_Resolution',
            'MeasDesc_GlobalResolution',
            'TTResult_SyncRate',
            'UsrPulseCfg',
            'ImgHdr_Ident',
            'ImgHdr_PixX',
            'ImgHdr_PixY',
            'ImgHdr_LineStart',
            'ImgHdr_LineStop',
            'ImgHdr_Frame',
            'ImgHdr_PixResol',
            'Measurement_SubMode',
            'TTResultFormat_TTTRRecType'
        )
        self.head = {
            tag_name: self._tag_value(tags, tag_name)
            for tag_name in required_tags
        }

    def _prepare_image_variables(self):
        self.image_width = int(self.head['ImgHdr_PixX'])
        self.image_height = int(self.head['ImgHdr_PixY'])
        self.line_start_mask = 2 ** (int(self.head['ImgHdr_LineStart']) - 1)
        self.line_stop_mask = 2 ** (int(self.head['ImgHdr_LineStop']) - 1)
        self.frame_mask = 2 ** (int(self.head['ImgHdr_Frame']) - 1)

    def _validate_image_data(self):
        if int(self.head['Measurement_SubMode']) == 0:
            raise ValueError('The PTU file is not a FLIM acquisition.')
        if int(self.head['ImgHdr_Ident']) not in (3, 9):
            raise NotImplementedError(
                'Scanner identifier ' + str(self.head['ImgHdr_Ident']) +
                ' is not supported.'
            )

        required_markers = {
            self.line_start_mask,
            self.line_stop_mask,
            self.frame_mask
        }
        observed_markers = set(np.unique(self.marker_masks).tolist())
        missing_markers = required_markers - observed_markers
        if missing_markers:
            raise ValueError(
                'Required raster marker masks are missing: ' +
                str(sorted(missing_markers))
            )

        if self.macro_ticks.size and np.any(self.macro_ticks[1:] < self.macro_ticks[:-1]):
            raise ValueError('Decoded macrotime ticks are not monotonic.')

    def describe(self):
        '''Return compact information useful for validation and notebooks.'''

        marker_counts = {
            int(marker): int(np.count_nonzero(self.marker_masks == marker))
            for marker in np.unique(self.marker_masks)
            if marker != 0
        }
        photon_event = self.marker_masks == 0
        detector_counts = {
            int(detector): int(
                np.count_nonzero(self.route_ids[photon_event] == detector)
            )
            for detector in np.unique(self.route_ids[photon_event])
        }
        return {
            'file': str(self.file_path),
            'record_type': self.record_type,
            'geometry': (self.image_height, self.image_width),
            'excitation_mode': str(self.head['UsrPulseCfg']),
            'event_count': int(self.macro_ticks.size),
            'photon_count': int(np.count_nonzero(photon_event)),
            'detector_counts': detector_counts,
            'marker_counts': marker_counts
        }

    def reconstruct_flim_data(self, rows_to_skip=0, include_final_frame=True):
        '''Build the integrated FLIM stack and retain frame-resolved intensity.'''

        if not isinstance(rows_to_skip, (int, np.integer)) or rows_to_skip < 0:
            raise ValueError('rows_to_skip must be a non-negative integer.')

        coordinates = self._assign_photon_coordinates(
            int(rows_to_skip), include_final_frame
        )
        lifetime_stack, intensity_map = self._accumulate_images(coordinates)
        mapped_channels = self._mapped_channels()

        return (
            lifetime_stack,
            intensity_map,
            self.marker_masks.copy(),
            self.macro_ticks.copy(),
            mapped_channels,
            self.micro_bins.copy()
        )

    def _mapped_channels(self):
        source_channels = self.route_ids.copy()
        marker_event = self.marker_masks != 0
        source_channels[marker_event] = self.marker_masks[marker_event]
        mapped_channels = self._map_detector_routes(source_channels)
        if mapped_channels.size and mapped_channels.max() > np.iinfo(np.uint8).max:
            raise ValueError('The detector axis exceeds uint8 compatibility.')
        return mapped_channels.astype(np.uint8)

    def _map_detector_routes(self, source_channels):
        mapped_channels = np.empty(source_channels.shape, dtype=np.int64)
        for raw_channel in np.unique(source_channels):
            raw_value = int(raw_channel)
            if raw_value not in self.detector_route_map:
                raise ValueError(
                    'No detector route mapping is configured for raw ID ' +
                    str(raw_value) + '.'
                )
            mapped_channels[source_channels == raw_channel] = (
                self.detector_route_map[raw_value]
            )
        if np.any(mapped_channels < 0):
            raise ValueError('Mapped detector indices must be non-negative.')
        return mapped_channels

    def _assign_photon_coordinates(self, rows_to_skip, include_final_frame):
        line_start_events = np.flatnonzero(self.marker_masks == self.line_start_mask)
        line_stop_events = np.flatnonzero(self.marker_masks == self.line_stop_mask)
        frame_events = np.flatnonzero(self.marker_masks == self.frame_mask)

        if line_start_events.size != line_stop_events.size:
            raise ValueError(
                'Line-start and line-stop marker counts are different.'
            )
        if line_start_events.size <= 10:
            raise ValueError('At least eleven scan rows are required.')
        if frame_events.size == 0:
            raise ValueError('No frame markers were decoded.')
        if np.any(line_start_events >= line_stop_events):
            raise ValueError('A line-stop marker must follow every line-start marker.')

        line_widths = (
            self.macro_ticks[line_stop_events[10:]].astype(np.int64) -
            self.macro_ticks[line_start_events[10:]].astype(np.int64)
        )
        sync_pulses_per_line = int(np.floor(np.mean(line_widths)))
        if sync_pulses_per_line <= 0:
            raise ValueError('The mean scan-line duration is invalid.')

        if include_final_frame:
            event_limit = self.macro_ticks.size - 1
        else:
            last_frame_sync = self.macro_ticks[frame_events[-1]]
            event_limit = int(np.flatnonzero(self.macro_ticks == last_frame_sync)[0])

        event_number = np.arange(self.macro_ticks.size)
        photon_events = np.flatnonzero(
            (self.marker_masks == 0) & (event_number <= event_limit)
        )

        line_number = (
            np.searchsorted(line_start_events, photon_events, side='right') - 1
        )
        has_line_start = line_number >= 0
        safe_line_number = np.maximum(line_number, 0)
        before_line_stop = photon_events < line_stop_events[safe_line_number]

        if frame_events.size == 1 and not include_final_frame:
            frame_number = np.zeros(photon_events.shape, dtype=np.int64)
            first_line_number = np.zeros(photon_events.shape, dtype=np.int64)
            valid_frame = np.ones(photon_events.shape, dtype=bool)
            number_of_frames = 1
        else:
            frame_number = (
                np.searchsorted(frame_events, photon_events, side='right') - 1
            ).astype(np.int64)
            valid_frame = frame_number >= 0
            safe_frame_number = np.maximum(frame_number, 0)
            first_line_number = np.searchsorted(
                line_start_events,
                frame_events[safe_frame_number],
                side='right'
            )
            if include_final_frame:
                number_of_frames = int(frame_events.size)
            else:
                number_of_frames = max(int(frame_events.size - 1), 1)

        line_in_frame = line_number - first_line_number
        if rows_to_skip:
            image_line = (
                line_in_frame - rows_to_skip + 3
            ) % self.image_height
            valid_line = (
                (line_in_frame >= rows_to_skip) &
                (line_in_frame < rows_to_skip + self.image_height)
            )
        else:
            image_line = line_in_frame
            valid_line = (
                (line_in_frame >= 0) &
                (line_in_frame < self.image_height)
            )

        line_start_sync = self.macro_ticks[line_start_events[safe_line_number]]
        sync_offset = (
            self.macro_ticks[photon_events].astype(np.int64) -
            line_start_sync.astype(np.int64)
        )
        image_pixel = np.floor(
            sync_offset.astype(np.float64) *
            self.image_width / sync_pulses_per_line
        ).astype(np.int64)
        valid_pixel = (image_pixel >= 0) & (image_pixel < self.image_width)

        image_channel = self._map_detector_routes(self.route_ids[photon_events])
        all_channels = self._mapped_channels()
        number_of_channels = int(np.unique(all_channels).size)
        number_of_tcspc_channels = int(np.unique(self.micro_bins).size)
        image_tcspc = self.micro_bins[photon_events].astype(np.int64)

        valid_tcspc = image_tcspc < number_of_tcspc_channels
        valid_channel = image_channel < number_of_channels
        accepted = (
            has_line_start & before_line_stop & valid_frame & valid_line &
            valid_pixel & valid_tcspc & valid_channel
        )

        coordinates = {
            'frame': frame_number[accepted],
            'line': image_line[accepted],
            'pixel': image_pixel[accepted],
            'detector': image_channel[accepted],
            'microtime': image_tcspc[accepted],
            'number_of_frames': number_of_frames,
            'number_of_channels': number_of_channels,
            'number_of_tcspc_channels': number_of_tcspc_channels
        }
        self.frame_coordinates = coordinates
        return coordinates

    def _accumulate_images(self, coordinates):
        flim_shape = (
            self.image_height,
            self.image_width,
            coordinates['number_of_channels'],
            coordinates['number_of_tcspc_channels']
        )
        lifetime_stack = np.zeros(flim_shape, dtype=np.uint16)
        np.add.at(
            lifetime_stack,
            (
                coordinates['line'],
                coordinates['pixel'],
                coordinates['detector'],
                coordinates['microtime']
            ),
            1
        )

        frame_shape = (
            coordinates['number_of_frames'],
            self.image_height,
            self.image_width,
            coordinates['number_of_channels']
        )
        self.frame_intensity = np.zeros(frame_shape, dtype=np.uint64)
        np.add.at(
            self.frame_intensity,
            (
                coordinates['frame'],
                coordinates['line'],
                coordinates['pixel'],
                coordinates['detector']
            ),
            1
        )

        intensity_map = lifetime_stack.sum(axis=(2, 3))
        return lifetime_stack, intensity_map

    def accumulate_frame_images(self, detector, microtime_bins, weights=None):
        '''Accumulate weighted detector images separately for every frame.'''

        if self.frame_coordinates is None:
            raise RuntimeError('Reconstruct FLIM data before requesting frame images.')

        coordinates = self.frame_coordinates
        microtime_bins = np.asarray(microtime_bins, dtype=np.int64)
        if microtime_bins.ndim != 1:
            raise ValueError('microtime_bins must be a one-dimensional sequence.')

        if weights is None:
            weights = np.ones(microtime_bins.size, dtype=np.float64)
        else:
            weights = np.asarray(weights, dtype=np.float64)
        if weights.shape != microtime_bins.shape:
            raise ValueError('weights must match microtime_bins.')

        number_of_tcspc_channels = coordinates['number_of_tcspc_channels']
        if np.any(microtime_bins < 0) or np.any(
                microtime_bins >= number_of_tcspc_channels):
            raise ValueError('A requested microtime bin is outside the decoded range.')

        bin_weights = np.zeros(number_of_tcspc_channels, dtype=np.float64)
        bin_weights[microtime_bins] = weights
        photon_weights = bin_weights[coordinates['microtime']]
        selected = (
            (coordinates['detector'] == int(detector)) &
            (photon_weights != 0)
        )

        frame_images = np.zeros(
            (
                coordinates['number_of_frames'],
                self.image_height,
                self.image_width,
            ),
            dtype=np.float64,
        )
        np.add.at(
            frame_images,
            (
                coordinates['frame'][selected],
                coordinates['line'][selected],
                coordinates['pixel'][selected],
            ),
            photon_weights[selected],
        )
        return frame_images

    def frame_image_data(
            self,
            detector,
            microtime_bins,
            foreground_weights,
            background_weights):
        '''Return a compact sparse representation of frame-resolved images.'''

        if self.frame_coordinates is None:
            raise RuntimeError('Reconstruct FLIM data before requesting frame data.')

        coordinates = self.frame_coordinates
        microtime_bins = np.asarray(microtime_bins, dtype=np.int64)
        foreground_weights = np.asarray(foreground_weights, dtype=np.float64)
        background_weights = np.asarray(background_weights, dtype=np.float64)
        if microtime_bins.ndim != 1:
            raise ValueError('microtime_bins must be a one-dimensional sequence.')
        if foreground_weights.shape != microtime_bins.shape:
            raise ValueError('foreground_weights must match microtime_bins.')
        if background_weights.shape != microtime_bins.shape:
            raise ValueError('background_weights must match microtime_bins.')

        number_of_tcspc_channels = coordinates['number_of_tcspc_channels']
        if np.any(microtime_bins < 0) or np.any(
                microtime_bins >= number_of_tcspc_channels):
            raise ValueError('A requested microtime bin is outside the decoded range.')

        foreground_lookup = np.zeros(number_of_tcspc_channels, dtype=np.float64)
        background_lookup = np.zeros(number_of_tcspc_channels, dtype=np.float64)
        foreground_lookup[microtime_bins] = foreground_weights
        background_lookup[microtime_bins] = background_weights
        event_foreground = foreground_lookup[coordinates['microtime']]
        event_background = background_lookup[coordinates['microtime']]
        selected = (
            (coordinates['detector'] == int(detector)) &
            ((event_foreground != 0) | (event_background != 0))
        )

        selected_frames = coordinates['frame'][selected]
        order = np.argsort(selected_frames, kind='stable')
        selected_frames = selected_frames[order]
        frame_counts = np.bincount(
            selected_frames,
            minlength=coordinates['number_of_frames'],
        )
        frame_offsets = np.concatenate(([0], np.cumsum(frame_counts)))

        return {
            'format': 'sparse_frame_images_v1',
            'shape': (
                int(coordinates['number_of_frames']),
                int(self.image_height),
                int(self.image_width),
            ),
            'frame_offsets': frame_offsets.astype(np.uint64),
            'line': coordinates['line'][selected][order].astype(np.uint32),
            'pixel': coordinates['pixel'][selected][order].astype(np.uint32),
            'foreground': event_foreground[selected][order].astype(np.float64),
            'background': event_background[selected][order].astype(np.float64),
        }
