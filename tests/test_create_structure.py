import sys,os
import unittest
from cgsdata.CGSdatastructure import *

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class TestCreateSubstructure(unittest.TestCase):
    """ Class to test the creation of the table in the different databases
    
    """

    ## test the creation of HBase substructure

    ## test the creation of AVRO substructure (schema)

    ## test the creation of the metastore substructure

    def test_create_mysql_substructure(self):
        """ Test the creation of the MySQL substructure

        """
        structure = CGSdatastructure(os.path.join(BASE_DIR,"../cgsdata/data/test"))
        structure.show()
        s = structure.substructures[0] # selecting the MySQL data substructure
        datasubstructure = MySQLSubstructure(structureName = structure.structureName,**s)
        datasubstructure.show()
        status = datasubstructure.create()
        self.assertTrue(status == 'succeeded')
    
    
    
