import json
import logging
import re

from archytas.react import Undefined
from archytas.tool_utils import AgentRef, LoopControllerRef, is_tool, tool, toolset

from beaker_kernel.lib.agent import BaseAgent
from beaker_kernel.lib.context import BaseContext


logger = logging.getLogger(__name__)


@toolset()
class ElwoodToolset:
    """Toolset for Elwood context"""

    @tool()
    async def generate_code(self, code_request: str, agent: AgentRef, loop: LoopControllerRef) -> None:
        """
        Use this if you are asked to generate code to manipulate a dataset.

        You should ALWAYS use functions from the 'elwood' module within elwood.

        You should ALWAYS look at the docstrings for the functions in the code you write to determine how to use them.

        If any functions require additional arguments, please ask the user to provide these and do not guess at their values.

        Args:
            code_request (str): A fully grammatically correct description of what the code should do.
        """
        prompt = f"""
    You are tasked with writing Python code using the Elwood library to process geo temporal data in datatsets.

    Please generate Python code to satisfy the user's request below.

        Request:
        ```
        {code_request}
        ```
    
    When using elwood, please use 'from elwood import elwood' to import the correct module.
    
    Below are the publicly accessible functions in the Elwood library.
    
    Your task is to use these functions to perform the following tasks:

        -Process a given dataset through the elwood standardizer using the process function, where you need to specify the filepath, JSON mapper filename (mp), admin level, output file, and optional GADM GeoDataFrame.

        -Normalize the features in a given dataframe using either the normalize_features or normalize_features_robust functions.

        -Clip geographical data in a dataframe based on polygon shapes using the clip_geo function.

        -Clip data in a dataframe based on time ranges using the clip_dataframe_time function.

        -Rescale the time periodicity of a dataframe using the rescale_dataframe_time function.

        -Regrid a dataframe with detectable geo-resolution using the regrid_dataframe_geo function.

        -Get the boundary box of a geographical dataset using the get_boundary_box function.

        -Get the temporal boundary of a dataframe using the get_temporal_boundary function.

        -Load GADM matches for a specified admin level using the get_gadm_matches function.

        -List all unique values for a specified admin level using the gadm_list_all function.

    After you select a function to use, you MUST look up the function docstring. This teaches you what arguments to use in the code.

    You use the get_available_functions tool or read the function docstrings to learn how to use them. (Use <function>.__doc__ to read the docstring).

    Ensure to handle any required dependencies, and provide a well-documented and efficient solution. Feel free to create helper functions or classes if needed.

    You also have access to the libraries pandas, numpy, scipy, matplotlib and the full elwood library.

    Please generate the code as if you were programming inside a Jupyter Notebook and the code is to be executed inside a cell.
    You MUST wrap the code with a line containing three backticks (```) before and after the generated code.
    No addtional text is needed in the response, just the code block."""

        llm_response = await agent.query(prompt)
        loop.set_state(loop.STOP_SUCCESS)
        preamble, code, coda = re.split("```\w*", llm_response)
        result = json.dumps(
            {
                "action": "code_cell",
                "language": "python3",
                "content": code.strip(),
            }
        )
        return result

    generate_code.__doc__

    @tool()
    async def get_available_functions(self, agent: AgentRef) -> None:
        """
        This function should be used to discover the available functions in the elwood library and get an object containing their docstrings so you can figure out how to use them.

        This uses 'from elwood import elwood' to access the public module of the elwood library.

        This function will return an object and store it into self.elwood_functions. The object will be a dictionary with the following structure:
        {
           function_name: <function docstring>,
           ...
        }

        Read the docstrings to learn how to use the functions and which arguments they take.
        """
        functions = {}
        code = agent.context.get_code("elwood_info")
        elwood_info_response = await agent.context.beaker_kernel.evaluate(
            code,
            parent_header={},
        )
        elwood_info = elwood_info_response.get("return")
        for var_name, info in elwood_info.items():
            if var_name in functions:
                functions[var_name] = info
            else:
                functions[var_name] = info

        self.elwood__functions = functions

        return functions

    get_available_functions.__doc__

    @tool()
    async def open_dataset_as_dataframe(filepath: str, agent: AgentRef) -> None:
        """
        This function should be used to open a dataset as a dataframe.

        You should use the filepath provided to open the dataset.

        Args:
            filepath (str): The filepath to the dataset to open.
        """
        code = agent.context.get_code(
            "elwood_open_dataset_as_dataframe",
            {
                "filepath": filepath,
            },
        )
        result = await agent.context.beaker_kernel.evaluate(
            code,
            parent_header={},
        )

        dataframe = result.get("return")

        return dataframe

    @tool()
    async def get_boundary_box(self, dataframe: str, geo_columns: object, agent: AgentRef) -> None:
        """
        This function should be used to get the boundary box of a geographical dataset.

        You are expected to have a dataframe with geographical data in it.

        You need to know the names of the geographical columns in the dataset.

        Args:
            dataframe (str): The name of the dataframe to get the boundary box of.
            geo_columns (object): The names of the geographical columns in the dataset.
                This is an object with the keys 'lat_column' and 'lon_column'.
                The 'lat_column' key should have the name of the latitude column and the 'lon_column' key should have the name of the longitude column.
        """

        code = agent.context.get_code(
            "elwood_get_boundary_box",
            {
                "dataframe": dataframe,
                "geo_columns": geo_columns,
            },
        )
        result = await agent.context.beaker_kernel.evaluate(
            code,
            parent_header={},
        )

        boundary_info = result.get("return")

        return boundary_info

    get_boundary_box.__doc__

    @tool()
    async def regrid_geo_temporal_dataset(
        self,
        dataframe: str,
        geo_columns: object,
        time_column: str,
        scale_multiplier: float,
        aggregation_functions: list,
        agent: AgentRef,
    ) -> str:
        """
        This function should be used to regrid a dataframe with detectable geo-resolution.

        You are expected to have a dataframe with geographical data in it.

        You need to know the names of the geographical columns in the dataset.

        You should put these columns into an object as follows:

        {
            "lat_column": <latitude column name>,
            "lon_column": <longitude column name>
        }

        You also need to know the name of the time column in the dataset.

        You also need to what scale multiplier they would like to use for the regridding operation.

        Finally, you need one (or a list) of aggregations functions to use for the data in the dataset.

        Args:
            dataframe (str): The name of the dataframe to regrid.
            geo_columns (object): The names of the geographical columns in the dataset.
                This is an object with the keys 'lat_column' and 'lon_column'.
                The 'lat_column' key should have the name of the latitude column and the 'lon_column' key should have the name of the longitude column.
            time_column (str): The name of the time column in the dataset.
            scale_multiplier (float): The scale multiplier to use for the regridding operation. This can be a number less than 1 for upscaling or greater than 1 for downscaling.
            aggregation_functions (list): The aggregation functions to use for the data in the dataset. This is a list containing strings of the aggregation functions to use.

        Returns:
            str: The name of the regridded dataframe.
        """

        code = agent.context.get_code(
            "elwood_regridding",
            {
                "dataframe": dataframe,
                "geo_columns": geo_columns,
                "time_column": time_column,
                "scale_multiplier": scale_multiplier,
                "aggregation_functions": aggregation_functions,
            },
        )
        result = await agent.context.beaker_kernel.evaluate(
            code,
            parent_header={},
        )

        regridded_dataframe = result.get("return")

        return regridded_dataframe

    regrid_geo_temporal_dataset.__doc__


class ElwoodAgent(BaseAgent):
    """
    You are assisting us in modifying geo-temporal datasets.

    The main things you are going to do are regridding spatial datasets, temporally rescaling datasets, and clipping the extent of geo-temporal datasets.

    If you don't have the details necessary to use a tool, you should use the ask_user tool to ask the user for them.

    """

    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        tools = [ElwoodToolset]
        super().__init__(context, tools, **kwargs)