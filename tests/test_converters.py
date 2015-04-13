import sys,os
import unittest
from cgsdata import converters

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class TestFormatConverters(unittest.TestCase):
    """ Class to test the format converters
    JSON => flat JSON
    JSON => AVRO (using AVRO schema)
    
    """

    # def test_json_to_flatjson(self):
    #     """ Test the conversion of json to flat json
    #     """
    #     input_file = os.path.join(BASE_DIR,"../cgsdata/data/test/sourceFiles/vcfdata_avro.json")
    #     output_file = "outjson.json"
    #     converter = converters.formatConverters(input_file = input_file , output_file = output_file)
    #     status = converter.convertJSON2FLATJSON()
    #     self.assertTrue(status == 'succeeded')


            
    # def test_flatjson_to_avro(self):
    #     """ Test the conversion of json to flat json
    #     """
    #     # avscFile = os.path.join(BASE_DIR,"../tests/data/vcfdata_avro.avsc")
    #     # jsonFile = os.path.join(BASE_DIR,"../tests/data/vcfdata_flatten.json")
    #     # output_file = "vcfdata_data.avro"

    #     # avscFile = os.path.join(BASE_DIR,"../tests/data/vcfdata_avro_GT.avsc")
    #     # jsonFile = os.path.join(BASE_DIR,"../tests/data/vcfdata_1000patients_10variants_flat.json")
    #     # output_file = "vcfdata_data_GT_10variants.avro"

    #     avscFile = os.path.join(BASE_DIR,"../tests/data/vcfdata_avro_GT.avsc")
    #     jsonFile = "/home/jbp/Downloads/1000genomes/ALL.chr17.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypesRED.json"
    #     output_file = "/home/jbp/Downloads/1000genomes/vcf_GT_1000gen_748variants.avro"
            
    #     converter = converters.formatConverters(input_file = jsonFile , output_file = output_file)
    #     status = converter.convertFLATJSON2AVRO(avscFile)
    #     self.assertTrue(status == 'succeeded')

    #     # jsonFile = os.path.join(BASE_DIR,"../test/data/vcfdata_flatten.json")
    #     # output_file = "vcfdata_data.avro"

    #     # status = converter.convertflatJSON2AVRO()
    #     # self.assertTrue(status == 'succeeded')


                
    # def test_jsondir_to_avro(self):
    #     """ Test the conversion of a directory of json files to a single AVRO file 
    #     """
    #     avscFile = os.path.join(BASE_DIR,"../tests/data/vcfdata_avro.avsc")
    #     jsonDir = os.path.join(BASE_DIR,"../tests/data/chr17")
    #     #jsonDir = "/home/jbp/Downloads/1000genomes/jsonfilesRED/chr17_1000patients"
    #     avroFile = "vcfdata_1000patients.avro"

    #     status = converters.convertJSONdir2AVROfile(jsonDir, avroFile = avroFile, avscFile = avscFile)
    #     self.assertTrue(status == 'succeeded')

    
    # def test_vcf_to_flatjson(self):
    #     """ Test the conversion of a vcf file in a flat json file 
    #     """
        
    #     # vcfFile = os.path.join(BASE_DIR,"../tests/data/ALL.chr17.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes_10Variants.vcf")
    #     # flatjsonFile = "vcfdata_1000patients_10variants_flat.json"

    #     vcfFile = "/home/jbp/Downloads/1000genomes/ALL.chr17.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypesRED.vcf"
    #     flatjsonFile = "/home/jbp/Downloads/1000genomes/ALL.chr17.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypesRED.json"
        
    #     converter = converters.formatConverters(input_file = vcfFile, output_file = flatjsonFile)
    #     status = converter.convertVCF2FLATJSON()
    #     self.assertTrue(status == 'succeeded')

