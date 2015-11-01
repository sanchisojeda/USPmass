# USPmass
In this repository I share a series of tools designed to measure the
mass and radius of an exoplanet using time series photometric data from the Kepler
telescope and radial velocities measured with Keck . The tools are written in Python as a
series of Ipython Notebooks, with annoted comments and structured in
different folders. 

## Input:

* Kepler data: The Kepler data is downloaded from the public MAST
archive. The script to do so can be found in
"Transitanalysis/Readingdata/readdata.py". This script generates a csv
file, "PDCMAP.csv", which contains the time and stellar flux for each
of the images obtained with the Kepler telescope in the 4 years of its
main mission.

* Keck data: The radial velocities obtained with the keck telescope are provided as a text file with 7 columns, that can be easily read into python using the read_table command. 

## Packages used:

