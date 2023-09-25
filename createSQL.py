"""
Checklist to run createSQL.py:
1. Place `createSQL.py` in the master directory
2. Check credentials in `config.ini` file
3. Place Excel sheet containing table metadata in the master directory
"""

import logging
import os
from readExcelData import ReadExcelData
import verifyLocalData as vld

red = ReadExcelData()

### Get directory
dirPath = vld.getDirPath()
print("\nMaster Directory:", dirPath)
sqlDirPath = vld.verifyDir(dirPath, "src_sql")  #!Change source folder for SQLs
config = vld.readConfigFile(dirPath)

tableListLocal = vld.checkSQLFiles(sqlDirPath)
# print(tableListLocal)

if __name__ == "__main__":

    log_level = logging.INFO
    log_fmt = "[%(levelname)s] - %(message)s"
    # logging.basicConfig(level=log_level,format=log_fmt)

    try:
        ### Ask user to perform replace + backup operation(s) on SF
        missingSqlFlag = config["local_files"]["create_missing_sql"]

        ### LOCAL DIRECTORY OPERATIONS
        ### Checks local files and asks users for input
        if missingSqlFlag:
            red.readExcelWorkbook(
                os.path.join(dirPath, "SAMPLE_TBL-STRUCTURE.xlsx"), sqlDirPath
            )
            # logging.info('\nMissing local files updated!\n')

    finally:
        logging.info("\nFinished SQL operations.\nReady to upload.")


"""
DONE:
1. Check local dirs and SF for tables (can add views, SPs)
2. Compares local dirs and SF 
3. Additional parameters will be read from configuration file.
4. Verify data in excel sheets

TODO: 
1. Check last modified entry for files before backup
2. Create list of sheets/tables for quicker access
"""
