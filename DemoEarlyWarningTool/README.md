# Asynchronous Activity 1: Student Early Warning Tool Using KNIME

This repository contains the required output for Asynchronous Activity 1. The project uses KNIME to predict student risk status from academic performance data.

## Files

- `DemoEarlyWarningTool.knwf` - exported KNIME workflow
- `student_performance_knime.csv` - dataset used by the workflow
- `Bautista_AsherIan_KNIME_GitHub_Evidence.pdf` - screenshot evidence for the activity

## Algorithms

- Decision Tree
- Logistic Regression
- Random Forest

## How to Run

1. Import the `.knwf` file into KNIME Analytics Platform.
2. Configure the CSV Reader and select the included dataset.
3. Connect the CSV Reader to the learner you want to use and set `risk_status` as its target column.
4. Execute the configured nodes and review the resulting model output.

## Author

Asher Ian Bautista

## Course and Section

CS0065 - Intelligent Systems, AN43
