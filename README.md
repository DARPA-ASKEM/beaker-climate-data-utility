# Beaker Climate Data Utility

Beaker Climate Data Utility is a Beaker module designed to handle geographical/climate data. It provides a set of tools for detecting the resolution of a dataset, which can be particularly useful when regridding a dataset or when the resolution is unknown.

## Startup

To use Beaker Climate Data Utility, follow these steps:

1. Navigate to the project directory: `cd beaker-climate-data-utility`
2. Create a `.env` file and fill it out with the necessary environment variables. Refer to the `envfile.sample` file for the required variables.
3. Launch the container using Docker Compose: `docker-compose up -d`
4. Access the Beaker Climate Data Utility application at `http://localhost:8888/dev_ui?`

You can view the logs with `docker logs -f beaker-climate-data-utility-jupyter-1`

## Usage

Once in the user interface, you can use the notebook like a regular Jupyter notebook. There is also an LLM assistant you can use to access special features in the notebook.

You can request the LLM to retrieve a dataset from the HMI server. You will need to provide a uuid and a filename.

You can request the LLM to provide you plotting code in order to preview netcdf files.
The LLM will ask for a variable name in the notebook, and if you have any particular geographical column names, a data variable name, and a time slice index.
There are defaults for latter 3 values.

You can request the LLM to provide regridding code in order to regrid a netcdf dataset.

You can also request the LLM save a dataset to the HMI server. This will take a dataset variable from the notebook and persist it to the HMI.

