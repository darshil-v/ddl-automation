Steps:

0. Ensure your system has Python 3.* installed. Additionally, Python package manager `pip`
    (https://pip.pypa.io/en/stable/installation/) should be installed to download necessary
    libraries and dependencies. Once `pip` is installed, run the following command:
    > pip install -r requirements.txt
    
    Some of the modules may vary based on the operating systems. Kindly check module
    documentation for your system if error persists.

1. Run `excelDataCheck.py` to check syntax and table formatting. 
    Column format: col #, col name, datatype, precision/length, scale, null condition, constraits
    Currently the code follows above formating strictly.
    Refer to `sf_datatypes.txt` for list of permissible datatypes.
    Ensure there are no errors before proceeding to next step.

2. Run `createSQL.py`. This creates DDL scripts to be run on Snowflake.
    A folder `src_sql` will be created containing the sql files.
    `Archive` folder will be created to backup existing data on Snowflake (Partially working).

3. Run `uploadToSnowflake.py` to create/replace tables.
    The code first checks for existing files on SF and local system. For the current version
    Replace and Upload flags need to be updated manually in the config file.
    
