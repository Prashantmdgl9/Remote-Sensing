import rasterio
from rasterio import plot
%matplotlib inline
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
import earthpy.plot as ep
import earthpy.spatial as es

path = "Nuuk/Granule/Nuuk/IMG_DATA/R60m/"
# Visualise all the bands
bands = glob(path+"/*B?*.jp2")
bands.sort()
bands

len(bands)
array_stack, meta_data = es.stack(bands, nodata=-9999)

#array_stack = np.stack(lst)
titles = ['Aerosol', 'Blue', 'Green', 'Red', 'Vegetation Red Edge_0.70', 'Vegetation Red Edge_0.74',
          'Vegetation Red Edge_0.78', 'Water Vapour', 'SWIR_1.6', 'SWIR_2.1', 'NIR']

ep.plot_bands(array_stack, cmap = "terrain", title = titles)


ep.plot_rgb(array_stack, rgb=(3, 2, 1), stretch=True, str_clip=0.2, figsize=(10, 16))


band2, band3, band4 = array_stack[1:4]

def plot_mult_axis():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
    plot.show(band2, ax=ax1, cmap='Blues')
    plot.show(band3, ax=ax2, cmap='Greens')
    plot.show(band4, ax=ax3, cmap='Reds')
    fig.tight_layout()

plot_mult_axis()


#NDVI - Normalized Difference Vegetation Index (NDVI)

band4 = rasterio.open(path+"T22WDS_20200831T150809_B04_60m.jp2")
band8 = rasterio.open(path+"T22WDS_20200831T150809_B8A_60m.jp2")

red = band4.read(1).astype('float64')
nir = band8.read(1).astype('float64')
ndvi=np.where(
    (nir+red)==0.,
    0,
    (nir-red)/(nir+red))
ndvi[:5,:5]


ndviImage = rasterio.open('ndvi.tiff','w',driver='Gtiff',
                          width=band4.width,
                          height = band4.height,
                          count=1, crs=band4.crs,
                          transform=band4.transform,
                          dtype='float64')
ndviImage.write(ndvi,1)
ndviImage.close()


ndvi = rasterio.open('ndvi.tiff')
fig = plt.figure(figsize=(15,10))
plot.show(ndvi, cmap="RdYlGn")


band3 = rasterio.open(path+"T22WDS_20200831T150809_B03_60m.jp2")
band11 = rasterio.open(path+"T22WDS_20200831T150809_B11_60m.jp2")


green = band3.read(1).astype('float64')
swir = band11.read(1).astype('float64')
mndwi=np.where(
    (green+swir)==0.,
    0,
    (swir-green)/(swir+green))
mndwi[:5,:5]



mndwi_Image = rasterio.open('mndwi.tiff','w',driver='Gtiff',
                          width=band3.width,
                          height = band3.height,
                          count=1, crs=band3.crs,
                          transform=band3.transform,
                          dtype='float64')
mndwi_Image.write(mndwi,1)
mndwi_Image.close()

mndwi = rasterio.open('mndwi.tiff')
fig = plt.figure(figsize=(15,10))
plot.show(mndwi)
