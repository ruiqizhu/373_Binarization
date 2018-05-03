# 373_Binarization
This is an app called Oocyte Binarization for CMU 67373 consulting project. It is designed for researchers in Kodiak Laboratory to perform crab oocyte area analysis more easily and efficiently.

## Usage

Process_images.py is run from the command line and takes in a folder name as an argument. This folder should be the directory where images for crabs are stored. For example, this command might be run from the directory:
`python process_images.py images`
	
The images directory specified in the command must be configured a specific way. It expects a directory structure within the specified folder with crab sample numbers as the folder name with individual images inside of it. An example directory is displayed below:

	images
		0
			untitled000.tif
			untitled001.tif
		1
			untitled000.tif
		2
			untitled000.tif
		3
			untitled000.tif
		4
		
## Result

Running this command will take any .tif file and create 2 new files, a resized version of the original and a labeled version that has been filtered. These can then be used to load into the Crab n' Click application. Do NOT change the file names after the processing has been done.