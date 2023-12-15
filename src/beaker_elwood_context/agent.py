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
    async def generate_code(self, query: str, agent: AgentRef, loop: LoopControllerRef) -> None:
        """
        Use this if you are asked to generate code to manipulate a dataset.

        You should ALWAYS use functions from the 'elwood' module within elwood.

        You should ALWAYS look at the docstrings for the functions in the code you write to determine how to use them.

        If any functions require additional arguments, please ask the user to provide these and do not guess at their values.

        Args:
            query (str): A fully grammatically correct description of what the code should do.
        """
        prompt = """
    You are tasked with writing Python code using the Elwood library to process and normalize geo temporal data in datatsets. 
    
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

    You use the available functions tool or read the function docstrings to learn how to use them. (Use <function>.__doc__ to read the docstring).

    Ensure to handle any required dependencies, and provide a well-documented and efficient solution. Feel free to create helper functions or classes if needed.

    You also have access to the libraries pandas, numpy, scipy, matplotlib and the full elwood library.

    Please generate the code as if you were programming inside a Jupyter Notebook and the code is to be executed inside a cell.
    You MUST wrap the code with a line containing three backticks (```) before and after the generated code.
    No addtional text is needed in the response, just the code block."""

        llm_response = await agent.oneshot(prompt=prompt, query=query)
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
    async def get_available_functions(self) -> None:
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
        code = self.context.get_code("elwood_info")
        elwood_info_response = await self.beaker_kernel.evaluate(
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


class ElwoodAgent(BaseAgent):
    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        tools = [ElwoodToolset]
        super().__init__(context, tools, **kwargs)
