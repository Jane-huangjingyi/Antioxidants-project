# 04.3 Qualify the identified Flex reader

The researcher identified the Opentrons Flex Absorbance Plate Reader Module GEN1. Accessory inventory remains pending. Official capabilities and local unknowns are kept separately in the [platform decision file](../config/platform_decisions.json). No assay setting or laboratory execution is approved.

The [product page](https://opentrons.com/products/opentrons-flex-absorbance-plate-reader-module-gen1) documents flat-bottom 96-well endpoint/kinetic measurement but no reader temperature control or shaking. The [hardware specifications](https://docs.opentrons.com/absorbance-plate-reader/product-specs/) list four channels: 450, 562, 600 and 650 nm. These are discrete channels, not a spectral scanner. [Compatibility documentation](https://docs.opentrons.com/protocol-designer/create-protocol/modules-fixtures/) distinguishes Flex from OT-2 support.

## Method consequence

The [source-linked comparison](Method_Platform_Compatibility.csv) identifies crocin at 450 nm as the first optical development candidate. Its source is the separately audited 2002 method, not a recovered 2015 capacity equation. The audited PGR and ABTS wavelengths are absent from the standard channels. Choosing a nearby channel would constitute a modified method requiring new validation. No commercial filter change or hardware modification is assumed.

The scientific objective remains molar chemical capacity. Optical compatibility alone does not establish capacity, broad chemical coverage or a final candidate ranking. Continue the [staged pilot](../02_pilot_design/README.md) after configuration review.

## Thermal and timing qualification

Do not prescribe a continuously heated 37 C reader assay. A separate heater can condition a plate, but transfer and reading produce a temperature history that must be measured. Compare a documented controlled ambient-temperature development route with a separately qualified heat/transfer/read route once accessories are known. Neither is selected now. Record actual well temperature, reagent equilibration, mixing, plate-transfer time, first-read dead time and cycle duration. AAPH-driven chemistry must be qualified under the chosen temperature history. The literature ORAC-FL pH 7.4/37 C analysis scope remains unchanged and does not set this new assay's conditions.

## Software and data qualification

The [Python API guide](https://docs.opentrons.com/python-api/modules/absorbance-plate-reader/) identifies `absorbanceReaderV1`, API support from 2.21 and a required Flex Gripper. Installed versions and gripper availability remain unknown. Its export has measurement grids plus metadata; it is not our raw-trace schema. Read-start/end timestamps do not establish exact per-well initiation times. Preserve native files and actual addition logs, and validate the timestamp-conversion rule before calculating kinetic AUC. No importer is asserted compatible before an actual export is inspected.

Prefer unreferenced raw-channel readings during method development. API reference subtraction is different from a matched no-probe control and can remove genuine signal. A separate diagnostic channel needs validation, including its time cost and candidate absorption. No reference channel or interval is selected here. Plate layout, pipette capacity, mixing and dispensing order will be resolved after the local inventory is known; no runnable robot protocol has been generated.

## Reproduce

Run `python 04_absorbance_assay/03_platform_compatibility/check_platform_compatibility.py`, followed by `python 04_absorbance_assay/02_pilot_design/validate_pilot_readiness.py`. The checks regenerate the compatibility table and hashed [platform readiness](platform_readiness.json), while preserving all unapproved assay settings. These are documentation/computational checks, not hardware tests.
