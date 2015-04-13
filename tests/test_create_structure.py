import sys,os
import unittest
from cgsdata.CGSdatastructure import *

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class TestCreateSubstructure(unittest.TestCase):
    """ Class to test the creation of the table in the different databases
    
    """

    # ## MySQL substructure actions
    # def test_create_mysql_substructure(self):
    #     """ Test the creation of the MySQL substructure

    #     """
    #     structure = CGSdatastructure(os.path.join(BASE_DIR,"../cgsdata/data/test"))
    #     structure.show()
    #     s = structure.substructures[0] # selecting the MySQL data substructure
    #     datasubstructure = MySQLSubstructure(structureName = structure.structureName,**s)
    #     datasubstructure.show()
    #     status = datasubstructure.create()
    #     self.assertTrue(status == 'succeeded')

    # ## HBase substructure actions
    # def test_drop_hbase_substructure(self): 
    #     """ Test drop of the HBase substructure
    #     """
    #     structure = CGSdatastructure(os.path.join(BASE_DIR,"../cgsdata/data/test"))
    #     structure.show()
    #     s = structure.substructures[1] # selecting the HBase data substructure
    #     datasubstructure = HBaseSubstructure(structureName = structure.structureName,**s)
    #     datasubstructure.show()
    #     status = datasubstructure.drop_datastructure_from_yaml_file()
    #     self.assertTrue(status == 'succeeded')
         
    # def test_create_hbase_subtructure(self):
    #     """ Test the creation of the HBase substructure

    #     """
    #     structure = CGSdatastructure(os.path.join(BASE_DIR,"../cgsdata/data/test"))
    #     structure.show()
    #     s = structure.substructures[1] # selecting the HBase data substructure
    #     datasubstructure = HBaseSubstructure(structureName = structure.structureName,**s)
    #     datasubstructure.show()
    #     status = datasubstructure.create()
    #     self.assertTrue(status == 'succeeded')

        
    # ## test the creation of AVRO substructure (schema)
    # def test_create_avro_subtructure(self):
    #     """ Test the creation of the AVRO schema (.avsc) from a JSON file 

    #     """
    #     structure = CGSdatastructure(os.path.join(BASE_DIR,"../cgsdata/data/test"))
    #     structure.show()
    #     s = structure.substructures[2] # selecting the Avro data substructure
    #     datasubstructure = AvroSubstructure(structureName = structure.structureName,**s)
    #     datasubstructure.show()
    #     status = datasubstructure.create()
    #     self.assertTrue(status == 'succeeded')

    ## test the creation of the metastore substructure
    
