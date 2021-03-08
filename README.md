### Description
Set of files to re-create numerical results published in the following articles:

* P.-Y. C. R. Taunay, C. J. Wordingham, E. Y. Choueiri, 
"Physics of Thermionic, Orificed Hollow Cathodes. Part 1: Theory and Experimental Validation" 
* P.-Y. C. R. Taunay, C. J. Wordingham, E. Y. Choueiri, 
"Physics of Thermionic, Orificed Hollow Cathodes. Part 2: Scaling Laws"

#### Numerical results
The numerical results we obtained are available in the ./results folder. Each file is stored 
as an HDF5 file. The cathode-package repository (DOI: ) 
contains further information about the structure of the HDF5 file itself.

For each "insert" result, the corresponding HDF5 group contains a brief description of the input 
conditions under the attribute "description".
We also have added a "simulation inventory" file that contains the model inputs, the location of the results 
in the HDF5 file, and a description of the simulation. 

#### Experimental data
The experimental data we used are available in the cathode-database repository 
(DOI: 10.5281/zenodo.3956853). Some of the data appear inline in some of the example files. 

### How to use
1. Download and install the cathode Python package (DOI: ).
2. Download cross section data (elastic, ionization, excitation) for argon and xenon from the LXCAT (lxcat.net) website.
3. Store cross section data as "gasname_all.dat" in a "data" folder. For example: 
```bash
mkdir data/
cp my_downloaded_data data/ar_all.dat
```
4. Use the provided scripts to re-create numerical results or plots from the article.

#### Re-creating numerical results
To re-create the numerical results, run the scripts that are located in the ./article folder. 
Each script will save data in an HDF5 file. 
If running from an interactive Python interface the variable 'dflist' 
will contain Pandas dataframes with the computed results. 
The dataframes can be manipulated to re-create the published numerical results. 

#### Re-creating article plots
We have added a few examples to re-create parts of the article plots in the ./article folder.
If running from the command line, make sure you add the 'show' command to the scripts to show plots:
```python 
plt.show()
``` 

### License
All software files are licensed under MIT license.
The numerical results are licensed under CC-BY-4.0. 

Pierre-Yves Taunay, 2021
