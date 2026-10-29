# smICA bundled demo

This directory contains a small, self-contained dataset for demonstrating the
complete smICA workflow: PTU extraction, calibration loading, concentration
calculation, automatic ROI analysis for cells, and CSV export. Both channels of
each in-cellulo measurement are extracted with TCSPC statistical background
filtering; the in-vitro dextran measurements are extracted without that filter.
The `imaging_new_ptu` cell measurement is additionally re-extracted with the
standard PIE time gates so that the demo covers both filtering approaches.

The dataset is split by experimental context:

- `in_vitro/dextran_60nm`: one moderate-concentration dextran measurement and
  its calibration;
- `in_vitro/dextran_80nm`: one moderate-concentration dextran measurement and
  its calibration;
- `in_cellulo/cells_without_mrna/imaging_new_ptu`: one dual-channel cell
  measurement without mRNA and its session calibration;
- `in_cellulo/cells_without_mrna/imaging2_17_07_23`: a second dual-channel cell
  measurement without mRNA and its separate session calibration.

After installation, run:

```text
# Linux
./run_smICA --demo

# Windows
smICA.bat --demo
```

The launcher starts a dedicated local smICA automation server, sends the
commands listed explicitly in `run_demo.py`, exports `results.csv` in each data
directory, and then closes that dedicated smICA process. The selected
`imaging_new_ptu` measurement instead produces `results_tcspc.csv` and
`results_gating.csv`, allowing the two extraction variants to be inspected
separately. Intermediate `.pkl` files are generated next to the source PTU
files and reused by Phot2conc. For each cellular channel, the explicit command
sequence configures an automatic background range, calculates and accepts the
TCSPC filters, and selects the current-decay foreground filter before
extraction. The later gated pass disables statistical filtering and uses the
standard channel gates initialized when the dual-channel PIE file is loaded.

The GUI remains visible while the demonstration runs. Do not interact with it
until the script reports completion.
