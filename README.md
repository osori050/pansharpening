# Resolution changing
GIS5578 Programming Project


This project has created a resampling tool able to up and downscale the resolution of a raster dataset. For the upscaling, we count on two methods: simple upscaling and pansharpening. The former consists of increasing the resolution of the dataset without using any additional inputs but the raster itself. In contrast, the latter requires an external band, which is often the panchromatic band, whose i) cell size is the target resolution, and ii) DN (digital number) values are combined with those of the coarser-resolution dataset. On the other hand, downscaling consists of decreasing the raster resolution and, like simple upscaling, does not need an external band. Furthermore, this tool includes a GUI that allows for the manipulation of multiple settings depending on the intended use of the imagery and operates independently of any dedicated image processing software. A second GUI has been created as a resizing tool in ArcGIS Pro.

The tool has incorporated successfully a simple-mean pansharpening function developed by Thomas Wang (Simple_Pansharpen.py), and a more complex function developed by GDAL into one big pansharpening tool wrapper. Additionally, the script creates raster pyramids (or overviews) by making use of 8 resampling techniques (such as nearest neighbor, bilinear interpolation, cubic convolution, etc.). Regarding the downscaling and simple upscaling, the function gdal.Translate() is used to change the cell size of the raster by utilizing 8 resampling techniques and creating band statistics. This function has been wrapped up together with pyramids into a bigger function called resize() in case the user wants to generate pyramids to the output as well. There is also a stack_bands() function that composites the panchromatic band and the pansharpened dataset into one single raster. Finally, a simple GUI has been developed and includes boxes to search for the input files, a button to select the resampling technique, and checkboxes to decide whether pyramids or statistics are desired.




