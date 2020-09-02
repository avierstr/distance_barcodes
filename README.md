# distance_barcodes
This script calculates the **Levenshtein distance** between barcodes and looks for pools of barcodes with a mutual distance larger than a certain value.  It does it with comparing only the forward distance, and also with comparing the forward and complement reverse sequence.  The script starts with the maximum distance, and lowers it per digit until it reaches the minimum distance to be evaluated.

**How it works:**
I have done the following: 
Take barcodes with forward distances > 17:
BC10 - BC36 : 18
BC10 - BC65 : 18
BC11 - BC44 : 19
BC19 - BC44 : 18
BC36 - BC44 : 18
BC43 - BC44 : 18
BC44 - BC81 : 18
BC44 - BC87 : 18
barcode pool: ['BC10', 'BC11', 'BC19', 'BC36', 'BC43', 'BC44', 'BC65', 'BC81', 'BC87']

Compare all possible combinations of this pool: the distance of BC10-BC11, BC10-BC44, BC10-BC81, BC10-BC87, ... BC44-BC65.  If one of those couples is lower than 17, check which of the 2 barcodes is resulting in less barcodes at the end of the comparisons.  

BC36 - BC87 : 14

-> if BC36 is removed, 6 Barcodes left in pool at the end

-> if BC87 is removed, 7 Barcodes left in pool at the end

=> remove BC36

Do this for all combination in the pool.

I have noticed that changing the order of the comparisons in the pool resulted in different pools at the end, sometimes with less barcodes in the pool.  Then I added the option to do this random for 5000 times, keeping all unique pools with the maximum number of barcodes in a pool.
### Requirements:
- Python 3
- python3-dev, python3-setuptools, python3-pip, python3-wheel
  (`sudo apt-get install python3-dev python3-setuptools python3-pip python3-wheel`)
- c-implementation of Levenshtein: https://pypi.org/project/python-Levenshtein/
  (`python3 -m pip install python-Levenshtein`)
### Options:
`'-i', '--input'`: Input file in tab delimited format

`BC01	AAGAAAGTTGTCGGTGTCTTTGTG`

`BC02	TCGATTCCGTTTGTAGTCGTCTGT`

`BC03	GAGTCTTGTGTCCCAGTTACCAGG`

`'-min', '--mindistance'`: Minimum distance to evaluate.  Default=7

`'-max', '--maxdistance'`: Maximum distance to evaluate.  Default=15
### Command examples:

`python3 distance_barcodes.py -i 96_barcodes.txt` : process file with default settings.

`python3 distance_barcodes.py -i 96_barcodes.txt -max 20` : start with a maximum distances >20
 
The results are saved in a file "distance_barcodes.txt"

> Written with [StackEdit](https://stackedit.io/).
