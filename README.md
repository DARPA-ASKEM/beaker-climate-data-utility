# Beaker Climate Data Utility

## About

Beaker Climate Data Utility is a Beaker module designed to handle geographical/climate data. It provides a set of tools for detecting the resolution of a dataset, which can be particularly useful when regridding a dataset or when the resolution is unknown.

#### Before and After regridding operations:

![before_regridding_image](https://github.com/DARPA-ASKEM/beaker-climate-data-utility/blob/main/static/SLP_before_regrid.png?raw=true)
![after_regridding_image](https://github.com/DARPA-ASKEM/beaker-climate-data-utility/blob/main/static/SLP_after_regrid.png?raw=true)

## Startup

To use Beaker Climate Data Utility, follow these steps:

1. Navigate to the project directory: `cd beaker-climate-data-utility`
2. Create a `.env` file and fill it out with the necessary environment variables. Refer to the `envfile.sample` file for the required variables.
3. Launch the container using Docker Compose: `docker-compose up -d`
4. Access the Beaker Climate Data Utility application at `http://localhost:8888/dev_ui?`

You can view the logs with `docker logs -f beaker-climate-data-utility-jupyter-1`

## Usage

Once in the user interface, you can use the notebook like a regular Jupyter notebook. There is also an LLM assistant you can use to access special features in the notebook.

The kernel can interface with dataset storage on the HMI server through custom messages.


To retrieve a dataset from the HMI server, send a custom message named `download_dataset_request` with the payload:
```
{
    "uuid":"<your id here>",
    "filename":"<your filename here>"
}
```
This dataset will be loaded into the jupyter notebook environment as an xarray dataset called `dataset`.


To save a dataset to the HMI server, you need to send a custom message named `save_dataset_request` and provide the name of the xarray dataset variable you want to save with a payload:
```
{
    "dataset":<your dataset variable name here>,
    "filename":"<your chosen filename for the persisted data here>"
}
```
This will return a dataset uuid from the HMI server with your new dataset.


You can request the LLM to provide you plotting code in order to preview netcdf files.
The LLM will ask for a variable name in the notebook, and if you have any particular geographical column names, a data variable name, and a time slice index.
There are defaults for latter 3 values.

You can request the LLM to provide regridding code in order to regrid a netcdf dataset.

