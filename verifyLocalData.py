import logging
import os
import sys
import configparser
import SFConnectionParser as sfcp
from datetime import date, datetime

log_level = logging.INFO
log_fmt = "[%(levelname)s] - %(message)s"
logging.basicConfig(level=log_level, format=log_fmt)


def getDirPath():

    dirPath = os.path.dirname(os.path.realpath(__file__))
    dirPath = os.path.realpath(dirPath)

    return dirPath

    ################## Read config.ini ##################


def readConfigFile(dirPath):

    connectionFile = os.path.join(dirPath, "sfpy_config.ini")
    config = configparser.ConfigParser()
    config.read(connectionFile)

    return config


def checkSQLFiles(curDirPath):
    """
    Scans local directory for sql files.
    """
    config = readConfigFile(curDirPath)
    listSQL = []
    for rootdir, dirs, files in os.walk(curDirPath):
        for file in files:
            if file != ".DS_Store":
                listSQL.append(file[:-4])
    return listSQL


def loadSQLFiles(curDirPath):
    """
    Loads SQL files from local directory.
    """
    listSQL = []
    for rootdir, dirs, files in os.walk(curDirPath):
        for file in files:
            if file != ".DS_Store":
                listSQL.append(os.path.join(rootdir, file))
    return listSQL


def verifyDir(dirPath, newSubDir):
    """
    Checks if dir/subdir exists
    """
    if os.path.isdir(os.path.join(dirPath, newSubDir)):
        return os.path.join(dirPath, newSubDir)
    else:
        os.makedirs(os.path.join(dirPath, newSubDir))
        return os.path.join(dirPath, newSubDir)


def createArchiveSubdir(dirPath, newDirName="Archive"):
    """
    Creates date-wise Archive directories: root/year/month/date/
    """
    curDirPath = verifyDir(dirPath, newDirName)

    curYear, curMonth, curDate = (datetime.now().strftime("%Y-%m-%d")).split("-")
    if not os.path.exists(os.path.join(curDirPath, curYear, curMonth, curDate)):
        os.makedirs(os.path.join(curDirPath, curYear, curMonth, curDate))

    return os.path.join(curDirPath, curYear, curMonth, curDate)


# dirPath = sfcp.getDirPath()
### Dir of src sql files, !!! MODIFY relative sub-folder

# sfConnection = sfcp.getSFConnection()
# cur = sfConnection.cursor()

# Change file name as per need
# readExcelWorkbook(os.path.join(dirPath, 'ddl_automation_excel.xlsx'), dirPath + "/src_sql/")
# sfConnection.close()
