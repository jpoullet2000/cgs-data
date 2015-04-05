import sys,os
import unittest
from cgsdata import converters

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class TestFormatConverters(unittest.TestCase):
    """ Class to test the format converters
    JSON => flat JSON
    JSON => AVRO (using AVRO schema)
    
    """

    def test_json_to_flatjson(self):
        """ Test the conversion of json to flat json
        """
        input_file = os.path.join(BASE_DIR,"../cgsdata/data/test/sourceFiles/vcfdata_avro.json")
        output_file = "outjson.json"
        converter = converters.formatConverters(input_file = input_file , output_file = output_file)
        status = converter.convertJSON2FLATJSON()
        self.assertTrue(status == 'succeeded')
        
    def test_flatjson_to_avro(self):
        """ Test the conversion of json to flat json
        """
        avscFile = os.path.join(BASE_DIR,"../tests/data/vcfdata_avro.avsc")
        jsonFile = os.path.join(BASE_DIR,"../tests/data/vcfdata_flatten.json")
        output_file = "vcfdata_data.avro"

        converter = converters.formatConverters(input_file = jsonFile , output_file = output_file)
        status = converter.convertFLATJSON2AVRO(avscFile)
        self.assertTrue(status == 'succeeded')

        # jsonFile = os.path.join(BASE_DIR,"../test/data/vcfdata_flatten.json")
        # output_file = "vcfdata_data.avro"

        # status = converter.convertflatJSON2AVRO()
        # self.assertTrue(status == 'succeeded')
        
    def test_jsondir_to_avro(self):
        """ Test the conversion of a directory of json files to a single AVRO file 
        """
        avscFile = os.path.join(BASE_DIR,"../tests/data/vcfdata_avro.avsc")
        jsonDir = os.path.join(BASE_DIR,"../tests/data/chr17")
        #jsonDir = "/home/jbp/Downloads/1000genomes/jsonfilesRED/Chr17"
        avroFile = "vcfdata_data.avro"

        status = converters.convertJSONdir2AVROfile(jsonDir, avroFile = avroFile, avscFile = avscFile)
        self.assertTrue(status == 'succeeded')
