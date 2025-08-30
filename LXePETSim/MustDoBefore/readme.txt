In order for this to work, you must replace the philipsvereos.py file at opengate.contrib.pet.philipsvereos in the Opengate library with the philipsvereos.py in this folder.
This way, you can use either LYSO or LXe as your scintillation crystal just by putting writing it into the line crystal.material = "" as crystal.material = "LXe" or crystal.material = "LYSO".
