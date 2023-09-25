import configparser
import logging  # install
import os
import sys
import snowflake.connector as sc


class SFConnection:
    def __init__(self):
        pass

    ################## Get Local Directory ##################
    def getDirPath(self):

        dirPath = os.path.dirname(os.path.realpath(__file__))
        dirPath = os.path.realpath(dirPath)

        return dirPath

    ################## Read config.ini ##################
    def readConfigFile(self, dirPath):
        connectionFile = os.path.join(dirPath, "sfpy_config.ini")
        config = configparser.ConfigParser()
        config.read(connectionFile)

        return config

    ############ Read Config file and return connection to snowflake ############
    def getSFConnection(self, dirPath):

        # find the path
        # dirPath = self.getDirPath()
        # reads configuration data from connection file
        config = self.readConfigFile(dirPath)
        logging.info("\nConfiguration parameters read!")

        # aws_access_key = config['aws']['AWS_ACCESS_KEY_ID']
        # aws_secret_key = config['aws']['AWS_SECRET_ACCESS_KEY']
        accountName = config["snowflake"]["account"]
        # snowflakeAccountName = accountName + "." + region

        snowflakeUser = config["snowflake"]["user"]
        snowflakePassword = config["snowflake"]["password"]
        snowflakeRoleName = config["snowflake"]["role"]
        snowflakeDatabaseName = config["snowflake"]["database"]
        snowflakeSchemaName = config["snowflake"]["schema"]
        snowflakeWarehouseName = config["snowflake"]["warehouse"]
        sfConnection = sc.connect(
            user=snowflakeUser,
            password=snowflakePassword,
            account=accountName,
            role=snowflakeRoleName,
            database=snowflakeDatabaseName,
            schema=snowflakeSchemaName,
            warehouse=snowflakeWarehouseName,
        )
        logging.info("\nConnected to SnowFlake!\n")
        return sfConnection

    def readExtraParameters(self, dirPath):
        config = self.readConfigFile(dirPath)

        upload_missing_flag = config["snowflake_backup"]["upload_missing_tables"]
        backup_flag = config["snowflake_backup"]["backup_tables"]
        replace_flag = config["snowflake_backup"]["replace_tables"]

        return upload_missing_flag, backup_flag, replace_flag


# sfConnection = getSFConnection()
# getCopyIntoInfo(sfConnection)
