# Changelog

## v2.2.0 — 2026-10-29

### PTU reading and frame-resolved analysis

- Added a `phconvert==0.10.1` backend for PicoHarp 300 T3 acquisitions, including marker validation, raster reconstruction, integration of every complete frame, and explicit fallback to the optional `readPTU_FLIM` reader for other record types.
- Extended PKL output with reader and acquisition metadata plus compact frame-resolved foreground and background photon weights. Phot2conc can reconstruct individual frames from these data without allocating dense frame-by-pixel-by-microtime arrays.

### Phot2conc calculations and display

- Added foreground-intensity, background-intensity, and foreground-lifetime image products, shared automatic ROI masks, and channel-specific lifetime scales. Background statistics are reported as weighted photons per pixel and remain directly comparable with the corresponding foreground signal.
- Added export-only frame-resolved foreground and background results, including weighted counts, molecule number, concentration, uncertainty, and effective pixel count. Integrated and frame-resolved uncertainties now account for spatial overlap between neighbouring confocal observation areas; `Errors as SEM` selects the effective spatial SEM alone, while clearing it combines this term with calibration uncertainty.

### TCP automation and analytical add-ons

- Added a versioned loopback TCP/JSON server and inspectable Python, Bash, and Windows Batch clients. Automation uses the same Dear PyGui callbacks as interactive operation, supports complete statistical-filter, extraction, ROI, calibration, calculation, and export workflows, keeps native progress feedback active, identifies failed commands, and waits for long-running GUI operations to finish.
- Added validated discovery, templates, and updater support for directory-based analytical add-ons. Official modes can be installed or updated without overwriting locally maintained extensions.

### Validation, installation, and documentation

- Added cross-platform developer tests, installed calculation unit tests, and resumable TCP-driven end-to-end reference workflows. Unit-test reports expose expected and calculated values, units, and tolerances, and the installed validation suite can be launched with `--test` without starting the GUI.
- Added a cross-platform `--demo` workflow with four bundled PTU measurements, matching calibrations, explicit automation commands, and automatic CSV export from raw extraction through concentration calculation.
- Updated the installers and runtime paths for Linux and Windows. Installation of the optional legacy `readPTU_FLIM` fallback is handled conditionally by the installers; declining it or an installation failure does not block the primary PicoHarp 300 T3 reader provided by `phconvert`. The installers also build the bundled Jupyter Book manual automatically during installation and updates. The documentation now covers the revised GUI, calculations and exports, uncertainty model, automation interface, analytical add-ons, supported equipment, and repository-level validation procedures.

### Corrections

- Corrected frame normalisation and integrated-frame handling while retaining backward compatibility with older PKL files. TCSPC-filtered foreground, background, and lifetime calculations now preserve fractional statistical-filter weights as floating-point data throughout extraction, analysis, display, and export.
- Improved batch-analysis stability by resetting file- and directory-specific state, converting NumPy and pandas scalars before updating Dear PyGui widgets, and handling empty background curves, missing ROI collections, and empty automatic detections.
