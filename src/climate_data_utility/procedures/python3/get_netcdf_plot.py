import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

plot_variable_name = {{plot_variable_name}}
lat_col = "{{lat_col}}"
lon_col = "{{lon_col}}"
time_slice_index = {{time_slice_index}}

ds = {{dataset}}
if plot_variable_name is None:
    plot_variable_name = list(ds.data_vars)[0]

# plot first time slice of the `ts` variable


# Create a figure with an appropriate projection
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
ds[plot_variable_name].isel(time=time_slice_index).plot(
    ax=ax, transform=ccrs.PlateCarree(), x=lon_col, y=lat_col, add_colorbar=True
)

# Add coastlines for context
ax.coastlines()

plt.show()
