# Changelog

## v2.2.0 — 2026-10-21

### Added

#### PTU reading and frame-resolved data

- Added a `phconvert==0.10.1` backend for reconstructing PicoHarp 300 T3 images. Every acquired frame is integrated, while frame-resolved photon coordinates and intensity data are retained for further analysis.
- Added explicit reader provenance, TTTR record type, observed frame-marker count, integrated-frame count, PKL format version, and relevant library versions to newly generated PKL files.
- Added compact sparse storage of frame-resolved foreground and background photon weights. Phot2conc reconstructs individual frames without allocating a dense frame-by-pixel-by-microtime array.
- Preserved support for other PTU record types through the existing `readPTU_FLIM` reader. Errors from recognised PicoHarp 300 acquisitions are reported directly instead of silently switching readers.

#### Phot2conc calculations and display

- Added foreground-intensity, background-intensity, and foreground-lifetime display modes.
- Added channel-specific lifetime display ranges with responsive horizontal Viridis scales. PIE lifetimes use a common zero-based display axis without modifying stored lifetime values.
- Added background photons-per-pixel statistics, distributions, GUI results, and exports. Background values are not converted to molecule number or concentration.
- Added export-only frame-resolved foreground and background results. Text and Pickle tables retain the integrated results and append per-frame weighted counts, molecule number, concentration, uncertainty, median, background, and effective-pixel columns.
- Added overlap-corrected uncertainty estimates based on the effective number of independent pixels in the active ROI. The calculation uses the ROI geometry, PTU pixel size, and channel-specific Gaussian waist to account for overlapping confocal observation areas.
- Added `N_effective_pixels` to integrated and frame-resolved exports so the effective statistical sample size remains auditable.
- Added responsive sizing for image panels, legends, labels, lifetime-range controls, and other newly introduced widgets.

#### ROI workflows

- Added shared automatically detected ROI masks across foreground, background, and lifetime views.
- Added double-click export of automatically detected ROIs in single-cell mode while preserving the existing single-click workflow in `Many cells` mode.
- Preserved existing ROI naming and storage conventions for masks generated from foreground intensity.

#### TCP automation

- Added an optional versioned loopback TCP/JSON automation server. It can be enabled from the launcher or controlled from the About menu without changing the default interactive start-up.
- Added a Python command-line client with readable Bash and native Windows Batch launchers. No compiled automation-client executable is installed.
- Added public commands for application state, PTU extraction, decay gates, statistical filtering, Phot2conc calibration, display selection, ROI handling, calculations, results, and export.
- Added `phot2conc.load_calibration`, which loads a calibration JSON file through the same callback used by the Phot2conc file dialog.
- Added structured automation errors containing the failed public command and actionable details for recoverable precondition failures.
- Added per-PTU file sizes and measured extraction and Phot2conc wall times to batch-command responses for reproducibility and performance reporting.
- Added command logging before request transmission and the human-readable public command name to successful responses, allowing crash-test logs to identify the last attempted operation.
- Added callback-backed command execution using the same Dear PyGui callbacks as equivalent interactive actions, keeping visible GUI state and scripted results synchronised.
- Added batch extraction through the native `Apply to all` callback, including its progress window, list-box selection changes, and file-by-file GUI refresh. Gates and statistical-filter routines are configured once and then applied to the complete directory.
- Added batch Phot2conc processing through the native `Calculate all` callback, including GUI progress updates and calculations for every ROI associated with each measurement.
- Added the complete interactive statistical-filter sequence: opening filter setup, selecting or importing a decay, calculating and accepting filters, selecting the foreground filter, and applying it to all files.
- Added indefinite completion waiting for accepted long-running commands. Timeouts are used only for connection establishment and incomplete incoming requests, while the server and client wait for the GUI callback to finish.

#### Analytical add-ons

- Added a complete `templates/add_on_template` skeleton for directory-based analytical modes, including menu integration, layout, callbacks, resizing, configuration, and documentation.
- Added strict analytical-mode discovery that validates configuration and declared entry-point files before loading a mode.
- Added updater synchronisation for analytical modes distributed by the official repository. New and updated official modes are installed while locally maintained add-ons are preserved.

#### Tests

- Added `dev_tests`, a cross-platform `pytest` suite covering PTU reader selection, frame-resolved calculations, automatic ROI handling, documentation building, installer contracts, analytical add-ons, and TCP/GUI automation.
- Added `calc_tests`, containing standalone numerical unit tests, reference PTU data, calibration and ROI files, expected results, and complete TCP-driven end-to-end workflows for Linux and Windows.
- Added numerical tests for calibration, ROI masking, foreground and background restoration, weighted lifetime maps, frame-resolved calculations, and invalid-pixel handling.
- Added detailed numerical test output showing each test purpose, expected and calculated values, units, tolerances, and pass/fail status.
- Added launcher option `--test` so an installed smICA instance can run the numerical validation suite without starting the GUI.
- Added resumable reference workflows with visible state files, explicit calibration loading, command logging, processed-file counts, elapsed time, machine information, and final reports.

### Changed

#### Scientific calculations and data handling

- Changed the default Phot2conc uncertainty to the quadrature combination of the effective spatial SEM and shared calibration uncertainty. Selecting `Errors as SEM` now reports only the effective spatial SEM.
- Preserved TCSPC-filtered foreground and background intensities as floating-point arrays throughout extraction, display, Phot2conc calculations, and export so fractional statistical-filter weights are not truncated.
- Phot2conc now uses the integrated-frame count stored in new PKL files. Older PKL files retain the historical `F-1` interpretation for backward compatibility.
- Frame-resolved results remain export-only and are intentionally not added to the GUI results table.
- Background images use the corresponding foreground normalisation so foreground and background intensities remain directly comparable.

#### Installation, updates, and packaging

- Moved the Linux and Windows installers to the repository root beside `setup.py`.
- Replaced setuptools-generated automation-client entry points with explicit, inspectable Bash and Windows Batch scripts backed by the Python client module.
- Updated the Windows installer to use native Batch control flow and reliable `errorlevel` handling without requiring PowerShell or Git for Windows.
- Updated runtime and installer paths to use cross-platform `os.path` operations.
- Updated the application updater to use the `main` branch and removed obsolete handling of a separate `REWRITE_ROI` installation directory.
- Updated release builders to locate the repository independently of the current working directory, use the root-level installers, include documentation sources, and exclude generated documentation, backup directories, and development caches.
- Added pinned installation dependencies required by the bundled documentation and analysis workflows, including `jupyter-book==2.1.2`, `seaborn==0.13.2`, and `scikit-learn==1.5.2`.
- Installation now builds the bundled HTML manual from the supplied Jupyter Book sources. The updater rebuilds the installed manual after updating the application.

#### Documentation

- Updated the user manual for the revised GUI, new image products, uncertainty calculation, exported columns, installed validation tests, and TCP automation.
- Added dedicated chapters covering automation commands, server operation, automation design and coverage, and analytical-mode development.
- Updated GUI screenshots and added the documentation update month and year to the manual landing page.
- Added repository-level instructions for running `dev_tests`, numerical unit tests, and the end-to-end reference workflow.
- Added a developer guide for extending raster reconstruction to other PicoQuant devices and TTTR formats from other vendors.

### Fixed

- Corrected PicoHarp 300 frame normalisation so every reconstructed frame contributes to newly generated integrated images while preserving compatibility with older PKL files.
- Corrected weighted-lifetime calculations after TCSPC filtering so fractional filter weights are retained.
- Corrected Dear PyGui result updates by converting NumPy and Pandas scalar values to native Python floats, preventing `Python value error. Must be float` failures during batch Phot2conc calculations.
- Reset statistical-filter controls when a new PTU directory is loaded and ignored hidden detector channels during automated `Apply to all` validation, matching interactive behaviour when switching between two-channel PIE and single-channel acquisitions.
- Reset file-specific foreground and background results when loading a new measurement so results cannot be carried over between files.
- Prevented failures caused by empty background curves, missing ROI collections, empty automatic detections, and unavailable display subprocessors.
- Prevented automation from selecting filters or decay components unavailable for the loaded channel. These conditions now return actionable precondition errors instead of opaque internal failures.
- Corrected matrix-valued unit-test output so expected and calculated arrays are separated and remain readable.
- Corrected lifetime-range widget sizing so values and labels remain visible after window resizing and font scaling.

### Repository maintenance

- Standardised the application version as `v2.2.0` across source files, documentation, metadata, and installers.
- Standardised licence and copyright headers in maintained source files while preserving third-party source files unchanged.
- Excluded Python bytecode, test-runner state, notebook checkpoints, documentation caches, and other generated development artefacts from version control and release packages.
