==================
java-doc-extractor
==================


Download java docs, extract Scala functions into a standardized JSON form, write to S3.


Description
===========

The java-doc-extractor gathers and standardizes Scala functions from the desired Java doc zip. The output is stored in AWS S3
as jsonl files. The extractor does not attempt to alter the data; it simply re-arranges data so it can be more easily indexed
down stream.
