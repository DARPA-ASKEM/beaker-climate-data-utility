from elwood import elwood


dataframe = {{dataframe}}
geo_columns = {{geo_columns}}
time_column = {{time_column}}
scale_multiplier = {{scale_multiplier}}
aggregation_functions = {{aggregation_functions}}

regridded_frame = elwood.regrid_dataframe_geo(
    dataframe, geo_columns, time_column, scale_multiplier, aggregation_functions
)

regridded_frame
