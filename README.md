# USPmass
In this repository I share a series of tools designed to measure the
mass and radius of an exoplanet using time series photometric data from the Kepler
telescope and radial velocities measured with Keck . The tools are written in Python as a
series of Ipython Notebooks, with annoted comments and structured in
different folders. Before describing each one, it is important to note that you will need the following packages are used and are required to run the scripts:

* Scipy: Including pandas, numpy, matplotlib, interpolate and optimize.
* From Dan Foreman-Mackey (https://github.com/dfm): Transit, emcee, george, corner, kplr
* Other tools: Csv

## Transitanalysis folder:

### Input

Kepler data: The Kepler data is downloaded from the public MAST
archive. The script to do so can be found in
"Transitanalysis/Readingdata/readdata.py". This script generates a csv
file, "PDCMAP.csv", which contains the time and stellar flux for each
of the images obtained with the Kepler telescope in the 4 years of its
main mission.

### Output:

* "finalparameters.txt": Transit parameters describing the orbit and properties of the planet
* "finaltransitephemeris.csv": Updated orbital period and time of transit for the planet
* "Planetproperties.csv": Marginalized distribution for the planet mass and radius, based on RVanalysis too
* "Transtittimes.csv": Individual transit times with associated uncertainties
* "triangle.png": Contour plots for the results of the MCMC applied to the folded transit light curve

### Main scripts:

* "Prelimtransitfit.ipynb": Uses initial guess for the transit parameters to generate a folded light curve and obtain an improved guess for certain transit parameters like the transit depth and impact parameter. These new parameters are used to generate folded light curves for each quarter (individual transits are barely detectable), which are then fitted to obtain transit times. The script outputs the final orbital period and time of transit and the final folded light curve to be analized in the next script.
* "Transitfit.ipynb": Computes the final transit parameters with a large MCMC run, using all the information from "Prelimtransitfit.ipynb".


* Keck data: The radial velocities obtained with the keck telescope are provided as a text file with 7 columns, that can be easily read into python using the read_table command. 
