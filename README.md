# Nantes Traffic Data Archiver

## Description

This project contains a Python script (`fetch_traffic_snapshot.py`) designed to periodically fetch real-time traffic fluidity data for Nantes Métropole from their open data API. It retrieves all available records, saves them as timestamped CSV files in an `archive` directory, and logs its activity.

This script serves as the data source provider for the separate [Nantes Traffic Analysis Project](https://github.com/thelordofpigeons/nantes-traffic-analysis). *(<- Ensure this link is correct!)*

## Features

*   Fetches data from the `fluidite-axes-routiers-nantes-metropole` dataset API.
*   Handles API pagination to retrieve all records.
*   Saves snapshots as `nantes_traffic_snapshot_YYYYMMDD_HHMMSS.csv` in the `archive` folder (relative to execution path).
*   Logs execution status and errors to `log_output.txt` (relative to execution path).
*   Designed to be executed periodically via a scheduler (e.g., Windows Task Scheduler, cron).

## Data Source API

*   **Dataset:** Fluidité des axes routiers Nantes Métropole temps réel
*   **API Endpoint Used:** `https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/244400404_fluidite-axes-routiers-nantes-metropole/records`

## Project Structure (in Repository)
```text
nantes_traffic_archiver/
│
├── .gitignore # Specifies files ignored by Git (data, logs, build artifacts)
├── fetch_traffic_snapshot.py # The main Python script
├── README.md # This file
└── requirements.txt # Python dependencies
```
**Note:** The generated output folders/files (`archive/`, `dist/`, `build/`, `log_output.txt`, `*.exe`) are intentionally excluded from this Git repository via `.gitignore`.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/nantes-traffic-archiver.git
    cd nantes-traffic-archiver
    ```
2.  **Set up Environment (Recommended: Conda):**
    *   Ensure Anaconda or Miniconda is installed.
    *   Create or activate a suitable Conda environment. If you created one within the project (e.g., `.conda`), activate it:
        ```bash
        # Adjust path as needed
        conda activate "<path-to-your-project>\nantes_traffic_archiver\.conda"
        # Or activate by name
        # conda activate your_fetcher_env_name
        ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Requires `requests`, `pandas`)*

## Usage

There are two main ways to run this script:

**1. Direct Execution:**

*   Make sure your Conda environment is activated.
*   Run the script directly from the terminal:
    ```bash
    python fetch_traffic_snapshot.py
    ```
*   This will create the `archive/` directory (if it doesn't exist) and `log_output.txt` in the *current working directory* where you ran the command.

**2. Scheduled Execution (via `.exe` and Task Scheduler):**

*   **Build the Executable (Optional):** If you want a standalone `.exe` (as you mentioned you created), you'll need PyInstaller:
    ```bash
    pip install pyinstaller
    # Then build using the .spec file (if you have one) or directly:
    pyinstaller --onefile fetch_traffic_snapshot.py
    ```
    This will create the `.exe` inside a `dist` folder.
*   **Configure Windows Task Scheduler:**
    *   Open Task Scheduler.
    *   Create a new task.
    *   Set a trigger (e.g., Daily, recurring every 30 minutes).
    *   Set the action to "Start a program".
    *   Point the "Program/script" to the *full path* of `fetch_traffic_snapshot.exe` (e.g., `C:\Users\ASUS\Documents\Stage LS2N\nantes_traffic_archiver\dist\fetch_traffic_snapshot.exe`).
    *   **Crucially:** Set the "Start in (optional)" field to the directory where you want the `archive` folder and `log_output.txt` to be created (e.g., `C:\Users\ASUS\Documents\Stage LS2N\nantes_traffic_archiver\dist\` or even the root `nantes_traffic_archiver` folder). This ensures the script saves files in the expected location relative to the executable's "working directory" when run by the scheduler.
    *   Configure other settings like "Run whether user is logged on or not" if needed.

## Output Files

*   **`archive/nantes_traffic_snapshot_YYYYMMDD_HHMMSS.csv`:** CSV files containing the raw data fetched at the time indicated in the filename (UTC).
*   **`log_output.txt`:** A log file recording the start, end, and any errors during the script's execution.
