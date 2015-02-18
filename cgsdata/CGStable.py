import os

validDatabases = ("metastore","mysql","hbase","avro")
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class ReadingDataFileException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class CGStable(object):
    """ A CGS table (CGS=Centralized genomic system)

    Attributes:
        name (string): name of the database (chosen by the user)
        machine_ip (string): machine ip (master node) to connect to for generating the database
        source (string): source of information from which we build the schema of the table (typically a csv file) 
        database (string): database name (by default: "default")
        table_type (string): table type (ex: "metastore", "mysql", "hbase")
    """
    def __init__(self, name, machine_ip,database="default",table_type="undefined"):
        self.name = name
        self.machine_ip = machine_ip
        self.database = database
        self.table_type = table_type

    def getName(self):
        return self.name

    def getMachineIP(self):
        return self.machine_ip

    def getDatabaseName(self):
        return self.database

    def show(self):
        print("""
        Table name: %s
        Machine IP: %s
        Database: %s
        Table type: %s
        Schema source: %s""" % (self.name, self.machine_ip,self.database, self.table_type, self.source))

    def readingTableSourceFile(self):
        """ Reads a source file to rebuild the schema of the table corresponding to the selected type
        The file is a xlsx file with in rows the variable/field names and in columns the table type (ex:hbase, metastore)
        The xlsx file contains 2 sheets: one for NoSQL and another one for MySQL and there are named so (sheet1=NoSQL, sheet2=MySQL).
        The data/data.conf file makes the correspondences between the table_type and the column names in the sheet
        The xlsx file may contain more than one column, only the ones corresponding to *table_type* will be selected.   
        This function is very specific and may not be convenient for any use case
        """
        def tableTypes2columnNames(f):
            """ Make the correspondences between the column names and the table type
                It returns a dictionary: key = table_type, value = column name

                :param f: filename (data/data.conf file)
                :type f: string
                :returns type_colnames: dictionary with key = table_type, value = column name  
            """
            type_colnames = dict()
            h = open(f)
            while 1:
                line = h.readline()
                if not line:
                    break
                if not (line.startswith('#') or line.startswith('[')) : ## do not read comment or category table (NoSQL, MySQL)
                    ls = line.strip().split('=')
                    type_colnames[ls[0]]=ls[1]
            h.close()
            return(type_colnames)
            
        ## check that table_type is not undefined
        if self.table_type not in validDatabases:
            raise ReadingDataFileException("You must be defined a table type: " + ",".join(validDatabases))

        ## check that the data.conf file exists
        dataconf_file = os.path.join("{}","data","data.conf").format(BASE_DIR)
        if not os.path.isfile(dataconf_file):
            raise ReadingDataFileException("The data configuration file 'data.conf' does not exist. It should be added in your $CGSHOME/cgsdata/data/ directory")

        ## create a source file if none is given 
        if self.source == ""
            self.source = os.path.join("{}","data","dataTable.xlsx").format(BASE_DIR)

        ## check that the dataTable.xlsx file exists
        if not os.path.isfile(self.source):
            raise ReadingDataFileException("The data file containing the description of the tables does not exist. It should be added in your $CGSHOME/cgsdata/data/ directory or explicitly given when constructing the CGStable object")

        ## reading the correspondence file data/data.conf: table_type -- column_name
        type_colnames = tableTypes2columnNames(dataconf_file)
                        
        ## read the column names (header)
                
        ## check whether table_type is contained in the column names, otherwise return an error
    
        ## send the list of values for the selected column and return it  

        
    def __str__(self):
        return "Table name: %s\nMachine IP: %s\nDatabase: %s\nTable type: %s" % (self.name, self.machine_ip,self.database, self.table_type)

    
class MetastoreTable(CGStable):
    """ A metastore table in the Hadoop framework that can be further queried by Hive, Impala, Pig, etc

    Attributes:
       
    """
    def __init__(self, name, machine_ip, database="default"):
        CGStable.__init__(self, name, machine_ip, database, table_type="metastore")

    def createTable(self):
        """ Create a metastore table
            This table is built using the Hive programming language which should be available on the "machine_ip" (permissions should be given).
            SSH access should be allowed to built this table 
        
        """
        ## reading the source file

        
        ## building the hive script

        ## creating the metastore table by executing the Hive script on the remote machine (SSH)

class HBaseTable(CGStable):
    """ An HBase table in the Hadoop framework
       
    """
    def __init__(self, name, machine_ip, database="default"):
        CGStable.__init__(self, name, machine_ip, database, table_type="hbase")
        
    def createTable(self):
        """ Create an HBase table
            This table is created using an HBase script that can be run from a similar command as:
            $HBASE_HOME/bin/hbase shell createHBaseTable.sh <hbase_table_name>
            HBase must be installed on the 
        """
        def buildingHBaseSchema(field_list):
            """
            Building a HBase schema (table, column families) from a list of field values
            The field values should follow the syntax: <column_family>.<column_qualifier>
            """
            
            
        ## reading the source file
        field_list = self.readingTableSourceFile()
        ## building the HBase schema
        [table_name,column_families_list] = buidingHBaseSchema(field_list)
        ## create the HBase table by executing the HBase script on the remote machine (SSH)
        


class AvroSchema(CGStable):
    """ An AVRO schema
    
    """ 
    def __init__(self, name, machine_ip, database="default"):
        CGStable.__init__(self, name, machine_ip, database, table_type="avro")

    def createSchema(self):
        """ Create an AVRO schema

        """
        
