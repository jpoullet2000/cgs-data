import yaml
import sys
import os

help = """
Converts two .csv files into YAML configuration files. This program requires three arguments:
    -The path to the .csv table of VCF fields
    -The path to the .csv table of the MySQL clinical database fields
    -The destination path where YAML files will be generated

The first .csv file contains information pertaining to the VCF fields. It should be structured with the following columns:
    -Field name
    -Description
    -Source
    -Category
    -Size
    -Alignment
    -Type
    -Example
    -Google Genomics resource
    -Impala metastore location
    -HBase metastore location
    -MySQL location
    -Name in VCF if applicable
A header row is expected.

The second .csv file contains information pertaining to the MySQL clinical database fields. It should be structured with the following columns:
    -Table name
    -Field
    -Type
    -Description
    -Example
A header row is expected.

A third argument is required for the path where output files will be saved
"""

arg_error = """
Please enter the following arguments: 
-The path to the .csv table of VCF fields
-The path to the .csv table of the MySQL clinical database fields
-The destination path where YAML files will be generated

Run with help for more information about the required inputs
"""

substructures_name = {"HBase":"variants_hbase", "MySQL":"clinical_mysql", "Metastore":"variants_metastore", "API":"variants_api"}

CSV_COMMA = "\t"

def parse_CSV_fields(filename):
    input = open(filename,'r').read().split('\n')[1:] #First line is assumed to be a header
    output = []
    for i in input:
        line = i.split(CSV_COMMA)
        output.append({"Highlander field":line[0],"description":line[1],"source":line[2],"category":line[3],"size":line[4],
                       "alignment":line[5],"Type":line[6],"Example":line[7],"IRIDIA resources based on Google Genomics resources":line[8],
                       "Impala":line[9],"HBase":line[10],"MySQL":line[11],"Original name in VCF if applicable":line[12]})
    return output


def make_HBase(field,HBase):
    location = field["HBase"].split(".")
    family_name = location[0]
    try:
        column_name = location[1]
    except Exception:
        print location
    variants = HBase.get("variants",{})
    family = variants.get(family_name,{})
    family[column_name] = {"type":field["Type"],"description":field["description"]}
    variants[family_name] = family
    HBase["variants"] = variants

def make_Metastore(field,Metastore):
    location = field["Impala"].split(".")
    table_name = ".".join(location[:-1])
    column_name = location[-1]
    table = Metastore.get(table_name,{"columns":{}})
    table["columns"][column_name] = {"type":field["Type"]}
    Metastore[table_name] = table

def make_AVRO(field,AVRO):
    pass

def make_API(field,API):
    pass

def make_substructures(field,HBase,Metastore):
    substructures = {}
    if field["HBase"] != "" and field["HBase"]!="/":
        substructures[substructures_name["HBase"]] = field["HBase"]
        make_HBase(field,HBase)
    if field["MySQL"] != "" and field["MySQL"]!="/":
        substructures[substructures_name["MySQL"]] = field["MySQL"]
    if field["Impala"] != "" and field["Impala"]!="/":
        substructures[substructures_name["Metastore"]] = field["Impala"]
        substructures[substructures_name["API"]] = field["Impala"]
        make_Metastore(field,Metastore)
    
    return substructures

def cgs_make_mapping(vcf_in_db,dest_path):
    fields=parse_CSV_fields(vcf_in_db)
    mapping = {}
    HBase = {}
    Metastore = {}
    for field in fields:
        variable = field["Highlander field"]
        mapping[variable] = {"description":field["description"]}
        substructures = make_substructures(field,HBase,Metastore)
    AVRO = Metastore
    API = Metastore
    config_output = open(dest_path+"/config.yml","w")
    config_output.write(yaml.dump(mapping,default_flow_style=False))
    config_output.close()
    hbase_output = open(dest_path+"/"+substructures_name["HBase"]+".yml","w")
    hbase_output.write(yaml.dump(HBase,default_flow_style=False))
    hbase_output.close()
    metastore_output = open(dest_path+"/"+substructures_name["Metastore"]+".yml","w")
    metastore_output.write(yaml.dump(Metastore,default_flow_style=False))
    metastore_output.close()
    avro_output = open(dest_path+"/"+substructures_name["API"]+".yml","w")
    avro_output.write(yaml.dump(AVRO,default_flow_style=False))
    avro_output.close()
    api_output = open(dest_path+"/"+substructures_name["Metastore"]+".yml","w")
    api_output.write(yaml.dump(API,default_flow_style=False))
    api_output.close()



def parse_CSV_MySQL(filename):
    input = open(filename,'r').read().split('\n')[1:] #First line is assumed to be a header
    output = []
    for i in input:
        line = i.split(CSV_COMMA)
        if any([j!="" for j in line]):
            output.append({"Table name":line[0],"Field":line[1],"Type":line[2],"Description":line[3],"Example":line[4]})
    return output

def cgs_make_MySQL(mysql_file,dest_path):
    mySQL_file = parse_CSV_MySQL(mysql_file)
    MySQL = {}
    for line in mySQL_file:
        if line["Table name"] != "":
            table_name = line["Table name"]
        table = MySQL.get(table_name,{"columns":{}})
        table["columns"][line["Field"]] = {"type":line["Type"]}
        MySQL[table_name] = table
    
    mysql_output = open(dest_path+"/"+substructures_name["MySQL"]+".yml","w")
    mysql_output.write(yaml.dump(MySQL,default_flow_style=False))
    mysql_output.close()


if __name__ == "__main__":
    if sys.argv[1] == "help":
        print help
    if len(sys.argv) != 4:
        print arg_error
    else:
        vcf_in_db = sys.argv[1]
        if os.path.isfile(vcf_in_db):
            mysql_file = sys.argv[2]
            if os.path.isfile(mysql_file):
                dest_path = sys.argv[3]
                if os.path.isdir(dest_path):
                    cgs_make_mapping(vcf_in_db,dest_path)
                    cgs_make_MySQL(mysql_file,dest_path)
                else:
                    print "The destination path is incorrect."
                    print arg_error
            else:
                print "The path to the table of the MySQL clinical database fields is incorrect."
                print arg_error
        else:
            print "The path to the table of VCF fields is incorrect."
            print arg_error
