This code is a Python script for processing and analyzing electronic density of states (DOS) data from VASP calculations.
Required input files
 - DOSCAR
 - POSCAR/CONTCAR
For each element, it calculates additional columns for total s, p, and d contributions, as well as t2g and eg orbital contributions, and shifts the energy scale so that the Fermi energy is at zero. 
It also inverts the sign of the down-spin channels for plotting consistency.

The user is prompted to enter the number of formula units, which is used to normalize the total DOS. The script then processes the total DOS data, normalizes it, and combines up and down spin channels.

Finally, the script writes the processed DOS data for each element and the total DOS to CSV files in a new or existing "DOS_data" directory, making the data ready for further analysis or plotting.
