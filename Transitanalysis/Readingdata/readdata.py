import kplr
import matplotlib.pyplot as plt
import numpy as np
import csv


client = kplr.API(data_root = "./data")

koi = client.koi(1169.01)

lcs = koi.get_light_curves(short_cadence=False, fetch=True)

f1 = open("PDCMAP.csv", "wb")
pdcmap = csv.writer(f1)
pdcmap.writerow(["Time", "Flux", "Quarter"])

for lc in lcs:
    with lc.open() as f:
        # The lightcurve data are in the first FITS HDU.
        hdu_data = f[1].data
        t= hdu_data["time"]
        flux = hdu_data["pdcsap_flux"]
        quality = hdu_data["sap_quality"]
        quarter = np.zeros(len(hdu_data["time"])) + f[0].header['QUARTER']
        flux = flux/np.median(flux)

        for j, time in enumerate(t):
        	if quality[j] == 0:
        		entries = [time-67.0, flux[j], quarter[j]]
        		pdcmap.writerow(entries)


f1.close()
