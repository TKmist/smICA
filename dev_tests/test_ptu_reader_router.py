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


from __future__ import annotations

import numpy as np
import pytest

from Modes.Extract_from_PTU.include import ptu_reader_router as router_module


class FakePhconvertReader:
    head = {"UsrPulseCfg": "PIE"}
    frame_mask = 4
    marker_masks = np.array([0, 4, 0, 4, 0, 4], dtype=np.uint8)
    record_type = "rtPicoHarp300T3"

    def __init__(self, source_path: str) -> None:
        self.frame_intensity = None

    def reconstruct_flim_data(self, **kwargs: object) -> tuple[np.ndarray, ...]:
        self.frame_intensity = np.ones((3, 2, 2, 1), dtype=np.uint64)
        return tuple(np.array([index]) for index in range(6))


class FakeLegacyReader:
    head = {"UsrPulseCfg": "Standard"}

    def __init__(self, source_path: str, print_header_data: bool = False) -> None:
        self.source_path = source_path

    def get_flim_data_stack(self) -> tuple[np.ndarray, ...]:
        return tuple(np.array([index]) for index in range(6))

    def get_flim_data_stack_omit(self, rows: int) -> tuple[np.ndarray, ...]:
        return tuple(np.array([rows + index]) for index in range(6))


def test_phconvert_route_keeps_all_marked_frames(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(router_module, "PhconvertPTUreader", FakePhconvertReader)
    selected = router_module.RoutedPtuReader("measurement.ptu")

    contract = selected.reconstruct()
    metadata = selected.processing_metadata(contract[2])

    assert selected.uses_phconvert
    assert metadata["Frame markers"] == 3
    assert metadata["Integrated frames"] == 3
    assert selected.per_frame_intensity.shape == (3, 2, 2, 1)


def test_unsupported_record_uses_legacy_route(monkeypatch: pytest.MonkeyPatch) -> None:
    def unsupported(source_path: str) -> None:
        raise router_module.UnsupportedPtuRecordError("other hardware")

    monkeypatch.setattr(router_module, "PhconvertPTUreader", unsupported)
    selected = router_module.RoutedPtuReader(
        "measurement.ptu", legacy_factory=FakeLegacyReader
    )

    contract = selected.reconstruct(rows_to_skip=2)
    metadata = selected.processing_metadata(
        np.array([0, 4, 0, 4, 0, 4], dtype=np.uint8)
    )

    assert not selected.uses_phconvert
    assert contract[0][0] == 2
    assert metadata["Frame markers"] == 3
    assert metadata["Integrated frames"] == 2


def test_picoharp_validation_error_is_not_hidden(monkeypatch: pytest.MonkeyPatch) -> None:
    def invalid_picoharp(source_path: str) -> None:
        raise ValueError("missing raster markers")

    monkeypatch.setattr(router_module, "PhconvertPTUreader", invalid_picoharp)
    with pytest.raises(ValueError, match="missing raster markers"):
        router_module.RoutedPtuReader(
            "measurement.ptu", legacy_factory=FakeLegacyReader
        )


@pytest.mark.parametrize(
    ("file_info", "expected"),
    [
        ({"Number of frames": 10, "Integrated frames": 10}, 10),
        ({"Number of frames": 10}, 9),
        ({"Number of frames": 1}, 1),
    ],
)
def test_frame_divisor_supports_new_and_historical_pickles(
    file_info: dict[str, int], expected: int
) -> None:
    assert router_module.resolve_integrated_frame_count(file_info) == expected


def test_weighted_frame_images_preserve_frame_and_filter_weights() -> None:
    reader = object.__new__(router_module.PhconvertPTUreader)
    reader.image_height = 2
    reader.image_width = 2
    reader.frame_coordinates = {
        "frame": np.array([0, 0, 1, 1, 1]),
        "line": np.array([0, 1, 0, 0, 1]),
        "pixel": np.array([0, 1, 0, 0, 1]),
        "detector": np.array([0, 0, 0, 0, 1]),
        "microtime": np.array([0, 2, 2, 1, 2]),
        "number_of_frames": 2,
        "number_of_tcspc_channels": 3,
    }

    images = reader.accumulate_frame_images(
        detector=0,
        microtime_bins=np.array([0, 2]),
        weights=np.array([1.0, 0.5]),
    )

    expected = np.array([
        [[1.0, 0.0], [0.0, 0.5]],
        [[0.5, 0.0], [0.0, 0.0]],
    ])
    np.testing.assert_array_equal(images, expected)


def test_weighted_frame_images_validate_weight_shape() -> None:
    reader = object.__new__(router_module.PhconvertPTUreader)
    reader.image_height = 1
    reader.image_width = 1
    reader.frame_coordinates = {
        "frame": np.array([0]),
        "line": np.array([0]),
        "pixel": np.array([0]),
        "detector": np.array([0]),
        "microtime": np.array([0]),
        "number_of_frames": 1,
        "number_of_tcspc_channels": 1,
    }

    with pytest.raises(ValueError, match="weights must match"):
        reader.accumulate_frame_images(0, [0], weights=[1.0, 2.0])


def test_sparse_frame_data_reconstructs_foreground_and_background() -> None:
    reader = object.__new__(router_module.PhconvertPTUreader)
    reader.image_height = 2
    reader.image_width = 2
    reader.frame_coordinates = {
        "frame": np.array([0, 0, 1, 1, 1]),
        "line": np.array([0, 1, 0, 0, 1]),
        "pixel": np.array([0, 1, 0, 0, 1]),
        "detector": np.array([0, 0, 0, 0, 1]),
        "microtime": np.array([0, 2, 2, 1, 2]),
        "number_of_frames": 2,
        "number_of_tcspc_channels": 3,
    }

    frame_data = reader.frame_image_data(
        detector=0,
        microtime_bins=[0, 2],
        foreground_weights=[1.0, 0.5],
        background_weights=[0.0, 0.25],
    )

    assert frame_data["format"] == "sparse_frame_images_v1"
    assert frame_data["shape"] == (2, 2, 2)
    np.testing.assert_array_equal(frame_data["frame_offsets"], [0, 2, 3])
    np.testing.assert_array_equal(frame_data["foreground"], [1.0, 0.5, 0.5])
    np.testing.assert_array_equal(frame_data["background"], [0.0, 0.25, 0.25])
