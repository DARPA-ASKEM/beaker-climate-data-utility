from elwood import elwood
import pandas
import xarray


def netcdf2df_processor(netcdf: str) -> pandas.DataFrame:
    """
    Produce a dataframe from a NetCDF4 file.

    Parameters
    ----------
    netcdf: str
        Path to the netcdf file

    Returns
    -------
    DataFrame
        The resultant dataframe
    """
    try:
        data_source = xarray.open_dataset(netcdf)
    except:
        raise AssertionError(
            f"Improperly formatted netCDF file ({netcdf}), xarray could not convert it to a dataframe."
        )

    dataframe = data_source.to_dataframe()
    final_dataframe = dataframe.reset_index()

    return final_dataframe


def open_dataset(filepath):
    filetype = filepath.split(".")[-1]

    dataframe = None

    if filetype == "nc" or filetype == "nc4" or filetype == "netcdf":
        dataframe = netcdf2df_processor(filepath)
    elif filetype == "csv":
        dataframe = pandas.read_csv(filepath)
    elif filetype == "xlsx" or filetype == "xls":
        dataframe = pandas.read_excel(filepath)

    if dataframe is None:
        raise AssertionError("The dataframe could not be created.")

    return dataframe


dataframe = open_dataset(f"{{filepath}}")
geo_columns = {{geo_columns}}
polygons_list = {{polygons_list}}

if dataframe is None:
    raise AssertionError("The dataframe could not be created.")

clipped_frame = elwood.clip_geo(
    dataframe=dataframe,
    geo_columns=geo_columns,
    polygons_list=polygons_list,
)

clipped_frame
