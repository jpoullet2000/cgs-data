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

```
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
```

where

- *dataStructureName* is the name of the data structure and thus the name of the folder
- *name* is the table name
- *type* is the table type (HBase, MySQL, metastore, AVRO)
- *description* is the description of the table
- *database* is the database where to add the table
- *source* is the data file where the table fields are defined

### <a name="referenceFile">File with reference fields</a>
The reference file is a tab-separated-value file with 2 columns:

- **id**: field id (integer, *mandatory*, *must be unique*)
- **name**: field name (string, *mandatory*)
- **description**: field description (string, *mandatory*)
- **type**: field type (['integer','string','boolean','date'], *optional*)

The goal of this file is to list all fields that are found in the different tables/schema of the data structure. In the source files, one can refer to the reference field **id** or **name**. 
If in the source file the type columns remains empty for one field, the parser will take the *type* value in the reference file for the corresponding field.

Let's illustrate this. Suppose one of your row in *reference.tsv* is
`10    gene_symbol    gene symbol    string`

and a corresponding row in *sourceFiles/variants.tsv* is

`10    variants.gene_symbol    `.

Since there is no definition of the type in *sourceFiles/variants.tsv*, the parser takes the *type* value in *reference.tsv*, i.e. *string* in this case. Depending on the type of the table (HBase, MySQL, etc) the parser may choose the closest type it could find for that specific table. For instance, if *sourceFiles/variants.tsv* is a MySQL table, the parser will choose *text* as type for that variable. The *text* type in MySQL is very general and may contain any string. However, it may slow down the queries and takes more disk space that actually needed. So, in this kind of case, it is recommended to redefine a type in *sourceFiles/variants.tsv* which will be taken as default.

The value *10* in both files indicates the reference field id. 

### <a name="referenceFile">Source files for table generation</a>
The source files are located in the folder *sourceFiles* of the corresponding data structure folder. 
The syntax to be used in these files depends on the type of the table/schema (HBase, MySQL, AVRO, etc).
We detail the syntax for:

- [HBase](#hbaseSource)
- [MySQL](#mysqlSource)
- [AVRO](#avroSource)

in the following subsections.

#### <a name="hbaseSource">HBase table definition and generation</a>
Under development.

#### <a name="mysqlSource">MySQL table definition and generation</a>
Under development.

#### <a name="avroSource">AVRO schema</a>
An AVRO schema is not per se a table in a database but a file with the extension *.avsc*.
Under development.


## Conversion of VCF files to AVRO
Under development.

## Bulk load of AVRO files into HBase
Under development.

## Metastore table definition on top of HBase (accessible via Hive, Pig, Impala, etc)
Under development.

## Implementing security in HBase
Under development.
