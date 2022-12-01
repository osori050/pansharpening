get_ipython().system('pip install opencv-python')

from osgeo_utils.gdal_pansharpen import gdal_pansharpen
import rasterio as rio
from rasterio.enums import Resampling
from osgeo import gdal
from Simple_Pansharpen import *
import os

get_ipython().run_line_magic('load_ext', 'lab_black')


# If user selects Simple Mean pansharpening, Thomas Wang's method is applied. Otherwise, gdal_pansharpen() is used
def wrapper_pansharpen(
    pan_name,
    dst_filename,
    spectral_names,
    simple_mean=False,
    band_nums=None,
    weights=None,
    resampling=None,
    spat_adjust=None,
    bitdepth=None,
    nodata_value=False,
):
    """
    This function combines the simple_mean pansharpening developed by Thomas Wang and the pansharpening tool from GDAL.

    Inputs:
    - pan_name: File path of the higher resolution image to be used for pansharpening
    - spectral_names: File path of the coarser image to undergo pansharpening
    - band_nums: bands in the coarser image to undergo pansharpening when not applied to the whole dataset
    - weights: Specify a weight for the computation of the pseudo panchromatic value. There must be as many -w switches as input spectral bands
    - dst_filename: File path of pansharpened dataset to be written to file
    - resampling: Select a resampling algorithm (nearest, bilinear, cubic [default], cubicspline, lanczos, average)
    - spat_adjust: Select behavior when bands have not the same extent (union [default], intersection, none, nonewithoutwarning)
    - bitdepth: Specify the bit depth of the panchromatic and spectral bands (e.g. 12). If not specified, the NBITS metadata item from the panchromatic band will be used if it exists.
    - nodata_value: Specify nodata value for bands. Used for the resampling and pan-sharpening computation itself. If not set, deduced from the input bands, provided they have a consistent setting.
    - simple_mean: if True, pansharpening is performed using the pansharpen_simple_mean() function. Otherwise, gdal_pansharpen() is selected

    """
    if simple_mean == True:
        pansharpen(spectral_names, pan_name, dst_filename, method="simple_mean")
    else:
        gdal_pansharpen(
            pan_name=pan_name,
            spectral_names=[spectral_names],
            band_nums=band_nums,
            weights=weights,
            dst_filename=dst_filename,
            resampling=resampling,
            spat_adjust=spat_adjust,
            bitdepth=bitdepth,
            nodata_value=nodata_value,
        )

    return dst_filename



def stack_bands(pan_name, psh_names, dst_filename):
    """
    This function stacks the panchromatic band and the pansharpened dataset into a new raster file.

    Inputs:
    - pan_name: File path of the panchromatic band
    - psh_names: File path of the pansharpened dataset
    - dst_filename: File path of the stacked raster

    """
    rasters = [pan_name, psh_names]

    # Add up the number of bands to be stacked from the two input rasters
    sum_bands = sum([rio.open(rast).meta["count"] for rast in rasters])

    # Read the metadata of the panchromatic band and add the total number of bands to be stacked
    src = rio.open(rasters[0])
    meta = src.meta
    meta["count"] = sum_bands

    with rio.open(dst_filename, "w", **meta) as _out:
        out_band_index = 0  # Counter
        for raster in rasters:
            with rio.open(raster) as _in:
                num_bands = _in.meta["count"]
                for src_band in range(1, num_bands + 1):
                    out_band_index += 1
                    # Stacking
                    _out.write(_in.read(src_band), out_band_index)


                    

def create_pyramids(ds, resampling):
    """
    This function generates raster overviews for easy visualization

    Inputs:
    - ds: File path of pansharpened dataset
    - resampling: resampling algorithm

    """
    factors = [2, 4, 8, 16]
    dst = rasterio.open(ds, "r+")
    dst.build_overviews(factors, resampling)
    dst.update_tags(ns="rio_overview", resampling=str(resampling)[11:])
    dst.close()

    


    
def calculate_stats(raster):
    """
    This function uses gdal.Translate to specifically create band statistics.

    Inputs:
    raster: File path of the raster dataset

    """
    name = "stats.tif"  # Temporary file
    gdal.Translate(destName=name, srcDS=raster, stats=True)
    os.remove(name)



    
    
def resize(output_name, ds, Res, resampling, of="GTiff", ot=None):
    """
    This function resamples raster datasets without the use of an external band based only on resolution values inputed by the user.
    It benefits from gdal.Translate()

    Inputs:
    - output_name: File path to the output raster resized
    - ds: File path of input dataset
    - Res: The new size of the cells
    - resampling: resampling algorithm (nearest [default], bilinear, cubic, cubicspline, lanczos, average, rms, mode)
    - of: output format (GTiff is deafault)
    - ot: output type (Byte, UInt16, Int16, UInt32, Int32, Float32, Float64, CInt16, CInt32, CFloat32 or CFloat64)

    """

    gdal.Translate(
        output_name, ds, xRes=Res, yRes=Res, resampleAlg=resampling, format=of
    )

