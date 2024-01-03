from elwood import elwood
import pandas
import xarray


def open_dataset(filepath):
    filetype = filepath.split(".")[-1]

    dataframe = None

    if filetype == "nc" or filetype == "nc4" or filetype == "netcdf":
        dataframe = elwood.netcdf2df(filepath)
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
