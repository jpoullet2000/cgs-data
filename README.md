# cgs-data
Databases in CGS (HBase, MySQL, Metastore) + additional storage files (AVRO).
This package is part of the [**CGS**](https://github.com/jpoullet2000/cgs) project. The goal of this package is to describe the data in CGS, how they are created, how they are stored. Scripts to import data into the different tables are available and are described below. 

Clinical data are stored in MySQL tables. 
Genomics/Exomics data are stored in HBase (accessible via Hive Metastore) and in AVRO files.

To generate the tables one needs the corresponding rights to do so. 

For the moment, only variant information is meant to be stored in HBase and AVRO files (see [here](http://avro.apache.org/docs/1.3.0/) for more details about the AVRO format).  

## AVRO schema
Under development.

## HBase table definition and generation
Under development.

## MySQL table definition and generation
Under development.

## Conversion of VCF files to AVRO
Under development.

## Bulk load of AVRO files into HBase
Under development.

## Metastore table definition on top of HBase (accessible via Hive, Pig, Impala, etc)
Under development.

## Implementing security in HBase
Under development.
