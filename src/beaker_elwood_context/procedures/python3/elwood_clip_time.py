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
time_column = f"{{time_column}}"
time_ranges = {{time_ranges}}

if dataframe is None:
    raise AssertionError("The dataframe could not be created.")

clipped_frame = elwood.clip_dataframe_time(
    dataframe=dataframe,
    time_column=time_column,
    time_ranges=time_ranges,
)

clipped_frame
