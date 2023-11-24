# DataFeedTask

## Overview

This python package reads data from desired source (i.e. xml) to desired destination (i.e. sqllite).

## Requirements


Make sure you have the following prerequisites installed before proceeding.

- **Python 3:** Visit [Python's official website](https://www.python.org/) to download and install Python 3.
  
- **pip3:** If it's not included with your Python installation, you can install it by following the instructions [here](https://pip.pypa.io/en/stable/installation/).

- **PyBuilder:** Install PyBuilder using pip3 by running the following command:

### Setting up PYTHONPATH

Set the `PYTHONPATH` environment variable to include the path to your modules. It is most likely you will encounter an error while running the build if you don't set PYTHONPATH. So it's better to set it before running the build. Open a terminal and run the following command to add the 'src/main/python' directory to your `PYTHONPATH`:
 ```bash
 export PYTHONPATH=$PYTHONPATH:/home/yourusername/DataFeedTask/src/main/python
 ```
Replace `/home/yourusername/DataFeedTask/src/main/python` with the actual path to your 'src/main/python' directory.

  ```bash
  pip3 install pybuilder
  pyb install
  ```


## Running the Script

To run the DataFeedTask script, follow these steps:

1. **Navigate to the Script Directory:**
   Open a terminal and change to the directory where your main script is located.

   ```bash
   cd /home/yourusername/DataFeedTask/src/main/python
   ```
   Run the script using the following command:
   ```bash
    python3 main.py --source-type "xml" --destination-type "sqlite" /path/to/source_file.xml /path/to/destination_file.db
    ```
  Replace /path/to/source_file.xml and /path/to/destination_file.db with the actual name of your script and the paths to your source XML file and destination SQLite file.

  Example:
  ```bash
      python3 main.py --source-type "xml" --destination-type "sqlite" feed.xml sqlite.db
  ```




