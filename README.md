# cgs-data
Databases in CGS (HBase, MySQL, Metastore) + additional storage files (AVRO).
This package is part of the [**CGS**](https://github.com/jpoullet2000/cgs) project and aims to generate database "contents" in the Hadoop framework (based on the Cloudera distribution): table creation, data file conversions, table fields mapping, etc. 

**cgs-data** is

- *flexible*: any data structure can be imported into the CGS system (see [below](#dataStructure) for more info).  
- *extendable*: table generators can be written for any types of databases (so far we are compatible with MySQL and HBase, allowing the tsv format).   

More specifically this document describes the data in CGS, how they are created, how they are stored. Scripts to import data into the different tables are available and are described below. 

Clinical data are stored in MySQL tables. 
Genomics/Exomics data are stored in HBase (accessible via Hive Metastore) and in AVRO files.

To generate the tables one needs the corresponding rights to do so. 

For the moment, only variant information is meant to be stored in HBase and AVRO files (see [here](http://avro.apache.org/docs/1.3.0/) for more details about the AVRO format).  

## <a name="dataStructure">Generation of data structure in CGS</a> 
The main goal of this package is to be usable for any type of data schemas. If you are not happy with the data structures proposed, you just need to make your own.
It is simple, you just need to edit some configuration files. How does it work? A parser reads a config file which tells what are the tables that have to be created, their types (HBase, MySQL, etc), the file where to find the information about the table fields (source file). Then it connects to your Hadoop cluster/machine (can be done locally) and installs the different tables as defined in your config file. The description of the config file can be found in the subsection [Config file](#configFile). Connections between tables are likely to happen and corresponding field names may be confusing. That is why we have added a file which contains all the reference fields. For instance, the "sample_ID" field in a metastore table may corresponds to the "ID" field in your MySQL "sample" table. A description of the reference file can be found in the subsection [File with reference fields](#referenceFile). All files for one data structure are located in one folder: config file, reference file, source files. Some more information about the organization within this folder can be found in the subsection [Data structure folder tree](#datastructureTree). 


### <a name="datastructureTree">Data structure folder tree</a>
As mentioned previously, all files specific to a data structure are located in the same folder which has the name of the data structure. Here is an example of files that you will find in the *variants* data structure:
```
.
+-- config.yml
+-- reference.tsv
+-- sourceFiles
	+-- variants-hbase.tsv
	+-- sample-mysql.tsv
	+-- ...
```

### <a name="configFile">Config file</a>
The config file is a YAML file with the following structure:

---

dataStructureName: variants
tables:
	- name: sample
      type: MySQL
      description: sample table
      database: default
      source: sample.tsv

	- name: variants
      type: HBase
      description: variants table
      database: default
      source = variants.tsv
  
---

where

- *dataStructureName* is the name of the data structure and thus the name of the folder
- *name* is the table name
- *type* is the table type (HBase, MySQL, metastore, AVRO)
- *description* is the description of the table
- *database* is the database where to add the table
- *source* is the data file where the table fields are defined

### <a name="referenceFile">File with reference fields</a>
Under development.

### AVRO schema
An AVRO schema is not per se a table in a database but a file with the extension *.avsc*.
Under development.

### HBase table definition and generation
Under development.

### MySQL table definition and generation
Under development.

## Conversion of VCF files to AVRO
Under development.

## Bulk load of AVRO files into HBase
Under development.

## Metastore table definition on top of HBase (accessible via Hive, Pig, Impala, etc)
Under development.

## Implementing security in HBase
Under development.
