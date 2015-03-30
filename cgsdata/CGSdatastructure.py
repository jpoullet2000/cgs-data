import os, sys
import yaml
import MySQLdb 
import subprocess
from starbase import Connection # rest API client to connect to HBASE

VALID_DATABASES = ("metastore","mysql","hbase","avro")
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR,"data")

class createDataStructureException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class ReadingDataFileException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

    
class CGSdatastructure(object):
    """ A CGS data structure

    Attributes:
        name (string): name of the data structure
        data_substructures (dictionary): dictionary of data substructures
        
        
    """
    def __init__(self, datastructure_path):
        config_file = os.path.join(datastructure_path,"config.yml")
        with open(config_file) as f:
            dic = yaml.load(f) 
        self.structureName = dic['dataStructureName']
        self.substructures = dic['substructures']
        self.created_substructures = []
        
    def show(self):
        substructure_names = [] 
        for s in self.substructures:
            substructure_names.append(s['name'])
        print("""
        Data structure name: %s
        Substructures: %s""" % (self.structureName, ",".join(substructure_names)))

    def create(self):
        """ This function creates the data structure
        Each of the data substructure is created.
        It returns the data substructures that could be created and add it to its list of created substructures.  
        
        """
        statusList = []
        ## generating the different substructures
        for s in self.substructures:
            ## create the data substructure object
            if s.type.lower() == "mysql":
                datasubstructure = MySQLSubstructure(**s)
            if s.type.lower() == "hbase":
                datasubstructure = HBaseSubstructure(**s)
            if s.type.lower() == "metastore":
                datasubstructure = MetastoreSubstructure(**s)
            if s.type.lower() == "avro":
                datasubstructure = AvroSubstructure(**s)
                
            print("Creating data substructure")
            print("--------------------------")
            datasubstructure.show()
            ## generate the substructure 
            statusList.append(datasubstructure.create())

        return(statusList)

                
class CGSdatasubstructure(object):
    """ A CGS data substructure (CGS=Centralized genomic system)
    A data substructure can be any database schema provided that it is contained on the same database. For instance, you cannot have a data substructure that has a MySQL table and a HBase table, all tables must be contained in the same database (here it would be either in MySQL or HBase, but not both).  
    
    Attributes:
        name (string): name of the data substructure (chosen by the user)
        host (string): machine ip or url (master node) to connect to for generating the database
        source (string): source of information from which we build the schema of the table (typically a csv file) 
        database (string): database name (by default: "default")
        datasubstructure_type (string): table type (ex: "metastore", "mysql", "hbase")
    """
    def __init__(self, **kwargs):
        mandatory_variables = ('structureName','database','name','host','source','type','user','password')
        if not set(kwargs.keys()).issuperset(set(mandatory_variables)):
            msg = "Error. The following variables are mandatory: %s" % ",".join(mandatory_variables)
            raise createDataStructureException(msg)
            #sys.exit(1)

        self.structureName = kwargs.pop('structureName')
        self.substructureName = kwargs.pop('name')
        self.host = kwargs.pop('host')
        self.port = kwargs.pop('port',0)
        source = kwargs.pop('source')
        if any(s in source for s in ('/','\\')): # check if source is a full path or just a file name (in the latter case, the source file must be in <BASE_DIR>/data/<data_structure_name>/sourceFiles/)
            self.source = source
        else:
            self.source = os.path.join(DATA_DIR,self.structureName,"sourceFiles",source)
        self.substructure_type = kwargs.pop('type')
        self.database = kwargs.pop('database','default')
        self.user = kwargs.pop('user')
        self.password = kwargs.pop('password')
        
                        
    def getSubstructureName(self):
        return self.name

    def getHostingMachine(self):
        return self.host

    def getDatabaseName(self):
        return self.database

    def getSourceFile(self):
        return self.source

    def getSubstructureType(self):
        return self.substructure_type
    
    def show(self):
        print("""
        Data substructure name: %s
        Host: %s
        Port: %s
        Database: %s
        User: %s
        Data substructure type: %s
        Schema source: %s""" % (self.substructureName, self.host, self.port, self.database, self.user, self.substructure_type, self.source))
    
    def __str__(self):
        return "Data substructure name: %s\nHost: %s\nDatabase: %s\nData substructure type: %s" % (self.name, self.host,self.database, self.substructure_type)

    
class MySQLSubstructure(CGSdatasubstructure):
    """ A MySQL substructure

    The source file could be a sql dump or a yaml file  

    Attributes:
       
    """
    def __init__(self, **kwargs):
        ##CGSdatasubstructure.__init__(**kwargs)
        super(MySQLSubstructure,self).__init__(**kwargs)
        if self.port == 0:
            self.port = 3306
        
    def create_datastructure_from_sql_file(self):
        """ Create the data substructure based on a SQL dump file
        """

        ## check whether the connection is OK and create db if OK
        try:
            db = MySQLdb.connect(host=self.host, user=self.user,passwd=self.password,port=self.port)
            cursor = db.cursor()        
            cursor.execute("SELECT VERSION()")
            results = cursor.fetchone()
            if results:
                ## note that databases are often created within the sql file
                sql = "CREATE DATABASE IF NOT EXISTS %s" % self.database;
                cursor.execute(sql)
                cdb = cursor.fetchone()
                cursor.execute('use ' + self.database) 
                cursor.execute(file(self.source).read())
                results = cursor.fetchone()
                status = 'succeeded'
            else:
                msg = "ERROR IN CONNECTION"
                raise createDataStructureException(msg)
                status = 'failed'
        except MySQLdb.Error, e:
            msg = "ERROR %d IN CONNECTION: %s" % (e.args[0], e.args[1]) + "\nThe data structure " + self.structureName + " was not created. Make sure you have the permissions to the DB and that your data structure configuration files are correctly shaped. See cgs-data repository for more details."
            raise createDataStructureException(msg)
            status = 'failed'
     
        # try:
        #     ## create db
        #     cmdL = ["mysql", "--user=%s" % self.user, "--port=%s" % self.port, "--password=%s" % self.password, "--host=%s" % self.host, self.database, '1>&2']
        #     print(" ".join(cmdL))
        #     proc = subprocess.Popen(cmdL,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        #     out, err = proc.communicate(file(self.source).read())
        #     print(repr(out))
            
        #     status = 'succeeded'
        # except:
        #     msg = "Error: the data structure " + self.structureName + " was not created. Make sure you have the permissions to the DB and that your data structure configuration files are correctly shaped. See cgs-data repository for more details."
        #     status = 'failed'
        #     raise createDataStructureException(msg)
        
        return(status)
            
    def create(self):
        """ Create a MySQL substructure, that is a schema

        """
        ##
        datasubstructure_file = self.source
        if datasubstructure_file.endswith('.sql'):
            print('Generating the data substructure based on the SQL file')
            status = self.create_datastructure_from_sql_file()
            
        elif datasubstructure_file.endswith('.yml'):
            print('Generating the data substructure based on the YAML file')
            status = 'failed'
            raise ReadingDataFileException("Error: this file type is not yet supported")
        else:
            status = 'failed'
            raise ReadingDataFileException("Error: this file type is not yet supported")
        
        return(status)


class HBaseSubstructure(CGSdatasubstructure):
    """ An HBase data substructure in the Hadoop framework (default database)
       
    """
    def __init__(self, **kwargs):
        super(HBaseSubstructure,self).__init__(**kwargs)
        if self.port == 0:
            self.port = 8000 # this value can be found in hbase-site.xml (typically in /etc/hbase/conf.dist/)
    def drop_datastructure_from_yaml_file(self):
        """ Drop the data substructure based on a YAML file
        """
        ## loading the YAML file
        try:
            with open(self.source) as f:
                hbaseSchemaDic = yaml.load(f) 
        except:
            msg = "File %s could not be loaded. Please check the syntax of the '.yml' file." % self.source 
            raise createDataStructureException(msg)
            status = "failed"        
                
        try:
            c = Connection(host = self.host, port = int(self.port))
            for t in hbaseSchemaDic.keys():
                tC = c.table(t)
                tC.drop()
                status = "succeeded"
        except:
            msg = "Error: the HBase substructure could not be dropped. Please check your connection parameters or the syntax in your '.yml' file."
            raise createDataStructureException(msg)
            status = "failed"
        return(status)
             
    def create_datastructure_from_yaml_file(self):
        """ Create the data substructure based on a YAML file
        """
        ## loading the YAML file
        try:
            with open(self.source) as f:
                hbaseSchemaDic = yaml.load(f) 
        except:
            msg = "Error: the HBase substructure could not be created. File %s could not be loaded. Please check the syntax of the '.yml' file." % self.source 
            raise createDataStructureException(msg)
            status = "failed"        

        try:
            c = Connection(host = self.host, port = int(self.port))
            tbls = c.tables()
            tbls = [str(t) for t in tbls]
            ## check that none of the tables already exists 
            for t in hbaseSchemaDic.keys():
                if t in tbls:
                    msg  = "Error: the table %s already exists. If you use starbase in python you can drop the table by using \n>>> from starbase import Connection\n>>> c = Connection()\n>>> t = c.table(%s)\n>>> t.drop()" % (t,t) 
                    print(msg)
                    status = "failed"
                    raise createDataStructureException(msg)

            ## if none of the table(s) do(es) not exist, let's create them(it) 
            for t in hbaseSchemaDic.keys():
                columnFamilies = hbaseSchemaDic[t]['columnFamilies'].keys()
                tC = c.table(t)
                tC.create(*columnFamilies)
            status = "succeeded"
                                                    
        except:
            msg = "Error: the HBase substructure could not be created. Please check your connection parameters or the syntax in your '.yml' file."
            raise createDataStructureException(msg)
            status = "failed"

        return(status)
            
    def create(self):
        """ Create an HBase table
            This table is created using an HBase script that can be run from a similar command as:
            $HBASE_HOME/bin/hbase shell createHBaseTable.sh <hbase_table_name>
            HBase must be installed on the 
        """
        datasubstructure_file = self.source
        if datasubstructure_file.endswith('.yml'):
            print('Generating the data substructure based on the YML file')
            status = self.create_datastructure_from_yaml_file()
        else:
            status = 'failed'
            raise ReadingDataFileException("Error: this file type is not yet supported")
        
        return(status)

class MetastoreSubstructure(CGSdatasubstructure):
    """ A metastore table in the Hadoop framework that can be further queried by Hive, Impala, Pig, etc

    Attributes:
       
    """
    def __init__(self, name, host, database="default"):
        CGSdatasubstructure.__init__(self, name, host, database, substructure_type="metastore")

    def createTable(self):
        """ Create a metastore table
            This table is built using the Hive programming language which should be available on the "host" (permissions should be given).
            SSH access should be allowed to built this table 
        
        """
        ## reading the source file

        
        ## building the hive script

        ## creating the metastore table by executing the Hive script on the remote machine (SSH)
        
                             
class AvroSubstructure(CGSdatasubstructure):
    """ An AVRO schema
    
    """ 
    def __init__(self, name, host, database="default"):
        CGSdatasubstructure.__init__(self, name, host, database, substructure_type="avro")

    def createSchema(self):
        """ Create an AVRO schema

        """

        
def main(argv):
    """ The goal of this function is to build a new data structure.
    Credentials for each data substructure is created on the fly in the ~/.cgs/cgs_config_file
    This file should be protected: chmod 600 ~/.cgs/cgs_config_file 

    Usage: python CGSdatastructure.py <datastructure_path>

    Ex:  python CGSdatastructure.py /my/datastructure/path/
    """
    try:
        opts, args = getopt.getopt(argv[1:-1],"hd:",["datastructure_path="])
    except getopt.GetoptError:
        print(argv[0] + " -d <datastructure_path>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(argv[0] +" -d <datastructue_path>")
            sys.exit()
        elif opt in ("-d", "--datastructure-path"):
            datastructure_path = arg
    ## creating the datastructure object
    datastructure = CGSdatastructure(datastructure_path)
    status = datastructure.create()
    return(status)
    
if __name__ == "__main__":
    datastructure_path = sys.argv[1]
    ## check that the folder path exists
    if os.path.isdir(datastructure_path):
        try:
            status = main(datastructure_path)
        except:
            raise createDataStructureException("A problem occurs when trying to create the datastructure.")
    else:
        raise createDataStructureException(datastructure_path + " does not exist or is not a folder")
