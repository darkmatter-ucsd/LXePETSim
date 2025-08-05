#!/bin/bash

##
##
##  This is the Unix script to run the PET list-mode benchmark of the CASToR project.
##
##

# Set the CASToR reconstruction program
recon="castor-recon"
# Test the existency of the CASToR reconstruction program in the PATH
type ${recon} > /dev/null
if [ $? != 0 ]
then
  echo "***** In order to run the benchmark script, please add the CASToR binary folder into your PATH !"
  exit 1
fi

###########################
# Command-line options
###########################

# To get help about the command-line options, run the program without argument or with '-h',
# '-help' or '--help' options. Then specific help about the different parts of the project
# can be prompted using specific help options.

# General verbose level (the verbose level relative to each specific part of the CASToR project
# can be customize separately if desired using options '-vb-XXXX'; to get specific help about
# these options, run the main program with the option '-help-misc')
verbose="-vb 2"

# The data file header (here, a pet list-mode data file). You can have a look at this ascii
# header to see the different fields used by the reconstruction program.
datafile="-df philips_vereos_sim_single_100s_fine.cdh"

# The output file base name. All files saved on the disk by the program will use this base name
# with an appended suffix and an extension. As an alternative, you can use the option '-dout'
# instead of '-fout'; this will create a folder of the provided name, and all files will be
# saved inside this folder. Note that the CASToR programs create a '.log' file which logs
# everything that is prompted on the screen.
output="-fout philips_vereos_sim_single_data_100s_fine"
# This is an option to specify that we want to save the image of the last iteration only. If not
# specified, by default, all iterations will be saved. You can alse use the '-oit' option to
# specifiy the series of iterations that you want to save. Run the reconstruction program with
# the '-help-out' option to get details about all options specific to the output settings.
last_it="-oit -1"

# Number of iterations (2) and subsets (28). Using this option, you can also define sequences
# of iterations with different number of subsets. For example '-it 2:28,1:14,10:1' will perform
# 2 iterations using 28 subsets, followed by 1 iteration using 14 subsets and followed by 10
# iterations using 1 subset.
iteration="-it 8:28"

# Number of voxels of the reconstructed image (X,Y,Z)
voxels_number="-dim 300,150,1"
# Size of the field-of-view in mm (X,Y,Z). Alternatively, you can use the '-vox' option to specify
# the size of the voxels.
fov_size="-fov 300.,150.,2."
# An offset can be applied to the reconstructed field-of-view. By default the field-of-view is
# centered at coordinate [0.;0.;0.] in the global referential. The coordinates of the scanner
# defines the position of the lines-of-response.
offset="-off 0.,0.,0."

# The reconstruction algorithm. Here, we use an iterative optimization algorithm. If you want to
# get specific help on how to use this option or other algorithms, run the program with the
# '-help-algo' option. If you want to get the full list of all implemented optimization algorithms,
# run the program with the '-help-opti' option. From that list, you will get the description of
# how to parameterize each optimization algorithm. Here, for the MLEM algorithm, by not specifying
# any parameter, the default configuration file is used to parameterize the algorithm.
optimizer="-opti MLEM"

# The projection algorithm. Here the incremental Siddon projector is used. To get help about how to use
# this option, run the program with the '-help-proj' option and to get a list of all implemented
# projectors, use the '-help-projm' option.
projector="-proj joseph"

# By construction, CASToR can perform resolution modeling either using an image-based PSF, or through
# the use of complicated projectors. It cannot perform so-called sinogram-based resolution modeling
# because each event is processed independently from one to another.
# Here, we set an image-based PSF using a stationay Gaussian of 4mm transaxial and axial FWHM with 3.5
# sigmas in the convolution kernel. The '-conv' option is generic so that any implemented convolution
# module can be used through this option. To get specific help, run the program with the '-help-imgp'
# option and to get the list of all implemented convolution methods, run with the '-help-conv' option.

#psf="-conv gaussian,4.,0.,3.5::psf"

# Still using the '-conv' option, we set up a post-filter (6mm FWHM transaxial and axial with 3.5 sigmas
# in the convolution kernel) by specifying when to apply this convolution module, as for the PSF module.
# One can set up as many convolution modules as one wants.
#post="-conv gaussian,6.,0.,3.5::post"

# Parallel computation using the OpenMP library. If CASToR was not compiled using OpenMP, a warning will
# be displayed if this option is used, specifying that only one thread will be used. Here we specify '0'
# in order to let the computer choose the number of threads with respect to the available ressources.
# One can also manually specify the number of threads to be used. To get details about the computation
# settings, run the program with the '-help-comp' option.
thread="-th 0"

# We want to mask the extrem slices when saving the image. To do that, we use the '-slice-out' option
# in which we give the number of slices that we want to mask at both sides of the FOV.

#out_mask_axial="-slice-out 3"

# We want to flip the image along the Y axis before saving. To do that, we use the '-flip-out' option
# in which we give the different axis along which the image will be flipped before being saved.
out_flip="-flip-out Y"

sens="-sens philips_vereos_sim_data_fine_sensitivity.hdr"

###########################
# Launch the reconstruction
###########################

# Launch the benchmark
echo "=============================================================================================="
echo "Reconstruction is going on. Should take from one to several minutes depending on the hardware."
echo "=============================================================================================="
${recon} ${verbose} ${datafile} ${output} ${last_it} ${iteration} ${voxels_number} ${fov_size} ${offset} ${optimizer} ${projector} ${psf} ${post} ${thread} ${out_mask_axial} ${out_flip} ${sens}

# Finished
echo ""
exit 0

