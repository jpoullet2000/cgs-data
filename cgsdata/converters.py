import os,sys
import json, ast
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cgsdatatools'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
from cgsdatatools import flatten, id_generator
from .exception import *
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import shutil

class formatConverters(object):
    """ Format converters
    
    """
    def __init__(self,
                 input_file,
                 output_file,
                 input_type = "",
                 output_type = "",
                 converting_method = "default"):
        
        self.input_file = input_file
        self.output_file = output_file
        if input_type == "":
            sp = input_file.split('.')
            self.input_type = sp[len(sp)-1]
        else:
            self.input_type = input_type
            
        if output_type == "":
            sp = output_file.split('.')
            self.output_type = sp[len(sp)-1]
        else:
            self.output_type = output_type
    
        self.converting_method = converting_method

    def show(self):
        print("""
        Input file: %s
        Output file: %s
        Converting method""" % (self.input_type, self.output_type, self.converting_method))

    def convertJSON2FLATJSON(self):
        """ Convert a JSON file (for the format, see the documentation) to a flat JSON file or more accurately a series of JSON lines  
        """
        if self.input_type != 'json' or self.output_type != 'json':
            msg = "Error: json files must be given as input files."
            status = "failed"
            raise generalException(msg)
        
        f = open(self.input_file)
        h = open(self.output_file,'w')
        line = f.readline()
        jsl = json.loads(line)
        try:
            for i in jsl.keys():
                flatJSON = flatten(jsl[i])
                flatJSONLiteral = ast.literal_eval(json.dumps(flatJSON))
                h.write(str(flatJSONLiteral).replace("'",'"').replace(".","_") + '\n')
            status = "succeeded"
        except:
            msg = "Error: the json does not follow the right syntax."
            status = "failed"
            raise generalException(msg)
        return(status)
        f.close()
        h.close()
         
    def convertFLATJSON2AVRO(self,avscFile = ""):
        """ Convert a JSON file (for the format, see the documentation) to an AVRO file using AVSC for making the conversion
        """
        status = "failed"
        if avscFile == "":
            msg = "This feature is not yet implemented. Please provide an AVRO schema file (.avsc)."
            raise generalException(msg)
        else:
            schema = avro.schema.parse(open(avscFile).read())
            writer = DataFileWriter(open(self.output_file, "w"), DatumWriter(), schema)
            h = open(self.input_file)
            while 1: ## reading line per line in the flat json file and write them in the AVRO format
                line = h.readline()
                if not line:
                    break
                ls = line.strip()
                writer.append(ast.literal_eval(ls))

            h.close()
            writer.close()
            status = "succeeded"

        return(status)

        ## cmd = "java -jar ../avro-tools-1.7.7.jar fromjson --schema-file" + avscFile + " " + self.input_file > self.output_file 
        
        
def convertJSONdir2AVROfile(jsonDir, avroFile, avscFile):
    """ Convert all JSON files to one AVRO file
    """
    ## check if the input directory exists
    if not os.path.isdir(jsonDir):
        msg = "The directory %s does not exist" % jsonDir 
        raise generalException(msg)
    
    ## check if the avsc file exists
    if not os.path.isfile(avscFile): 
        msg = "The file %s does not exist" % avscFile 
        raise generalException(msg)
    
    ## convert JSON files to flat JSON files
    tmpJSONFLATDir = id_generator()
    os.makedirs(tmpJSONFLATDir)
    nbrJSONfiles = 0
    for f in os.listdir(jsonDir):
        if f.endswith(".json"):
            ft = f.replace(".json", "flat.json")
            converter = formatConverters(input_file = os.path.join(jsonDir,f) , output_file = os.path.join(tmpJSONFLATDir,ft))
            status = converter.convertJSON2FLATJSON()
            nbrJSONfiles += 1
            
    ## concat the flat JSON files into 1 flat JSON file 
    flatJSONFile = id_generator()
    o = open(flatJSONFile,"w")
    for f in os.listdir(tmpJSONFLATDir):
        h = open(os.path.join(tmpJSONFLATDir,f))
        while 1:
            line = h.readline()
            if not line:
                break
            o.write(line)
        h.close()
    o.close()
    
    ## reading the concatenated flat JSON file and write to AVRO file  
    converter = formatConverters(input_file = flatJSONFile, output_file = avroFile)
    status = converter.convertFLATJSON2AVRO(avscFile)
        
    ## cleaning up
    shutil.rmtree(tmpJSONFLATDir)
    os.remove(flatJSONFile)
    
    return(status)
    
















