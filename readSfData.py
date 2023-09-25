"""
Done: Create nested Archive directory
Done: Add current time to created backup
TODO: Check 'Last modified' timestamp before backup
"""

import logging
import os
from SFConnectionParser import SFConnection
import verifyLocalData as vld
import datetime
import snowflake.connector as sc
import configparser

# sfc = SFConnection()
# sfConnection = sfc.getSFConnection(sfc.getDirPath())
# curr = sfConnection.cursor()


def checkSFFiles(cur):
    listSF = []
    res = cur.execute(
        "SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME FROM INFM_DEV_DB.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE 'DIM_%_DDL' AND TABLE_NAME NOT LIKE 'D_TGT%';"
    ).fetchall()
    for i in res:
        listSF.append(f"{i[0]}.{i[1]}.{i[2]}")
    return listSF


"""
def verifySFUpload(tableListSFDiff):#, SfReplaceFlag, SfReplaceBackupFlag):
"""
# Verifies tables on SF, asks for user input, returns Y/N
"""
    if tableListSFDiff:
        logging.info('File(s) missing on SF:', tableListSFDiff)
        while True:
            try:
                SfUploadFlag = input('File(s) missing from Snowflake. Would you like to upload tables? [Y/N]: ').upper()
                if SfUploadFlag not in ('Y' , 'N'):
                    raise ValueError('Invalid Input. Try again.')
                break
            except ValueError as ve:
                logging.error(ve)
        
        return SfUploadFlag
    else:
        logging.info('All SF tables synchronised')
"""
# def verifySfReplace(SfReplaceFlag = 'N', SfReplaceBackupFlag = 'N'):
#    while True:
#        try:
#            SfReplaceFlag = input("Would you like to replace the existing tables? [Y/N]: ").upper()
#            if SfReplaceFlag not in ('Y', 'N'):
#                raise ValueError('Invalid Input. Try again.')
#            SfReplaceBackupFlag = input("Would you like to backup the files? [Y/N]: ").upper()
#            if SfReplaceBackupFlag not in ('Y', 'N'):
#                raise ValueError('Invalid Input. Try again.')
#            break
#        except ValueError as ve:
#            print(ve)
#    return SfReplaceFlag, SfReplaceBackupFlag


def uploadSqlToSf(filename, cur):
    # open file
    with open(filename, mode="r", encoding="utf8", newline="\n") as file:
        ### delimiter cleaning
        content = file.read()
        content = content.replace("\n", "")
        content = content.replace("\t", " ")
        content = content.replace(";", ";\n")
        content = content.split("\n")
        # print(content[:-1])
        ### execute on snowflake
        for sql_cmd in content:
            cur.execute(sql_cmd)
        response = cur.fetchone()
        if response:
            logging.info(response[0][0])


def replaceSfTable(tableList, cur):
    for table in tableList:
        table_replace_query = cur.execute(
            f"select get_ddl('TABLE','{table}',true);"
        ).fetchone()[0]
        cur.execute(table_replace_query)
        response = cur.fetchall()
        if response:
            logging.info(response[0][0])


def renameFilenameDate(bkpDirPath, res):
    for file in res:
        filename = file[0]
        old_name = os.path.join(bkpDirPath, filename)
        new_name = filename.split(".")[0]
        ext = ".".join(filename.split(".")[1:])
        # Append current time to the file name in the formet name + time + .ext
        new_name = f"{new_name}_{datetime.datetime.now().strftime('%H-%M-%S')}.{ext}"
        if os.path.isfile(old_name):
            os.rename(old_name, os.path.join(bkpDirPath, new_name))


# Get backup before modifying table + rename files
def backupSfTable(bkpDirPath, tableList, cur):
    for table in tableList:
        tb = table.split(".")[-1]
        logging.info("Getting data for table:", tb)
        sql_cmd = f"get @%{tb} file://{bkpDirPath};"
        try:
            cur.execute(sql_cmd)
            res = cur.fetchall()
            renameFilenameDate(bkpDirPath, res)
        except sc.errors.OperationalError:
            logging.debug("No data available for:", tb)


# readSFData.backupSfTable(vld.createArchiveSubdir(sfcp.getDirPath()),['INFM_DEV_DB.PUBLIC.D_EMP_DDL','INFM_DEV_DB.PUBLIC.D_DEPT_DDL'],sfcp.getSFConnection().cursor())
# readSFData.replaceSfTable(['INFM_DEV_DB.PUBLIC.D_DEPT_DDL', 'INFM_DEV_DB.PUBLIC.D_EMP_DDL', 'INFM_DEV_DB.PUBLIC.D_PAYROLL_DDL'], sfcp.getSFConnection().cursor())
