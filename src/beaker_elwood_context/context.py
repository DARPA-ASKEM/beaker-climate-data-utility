from typing import TYPE_CHECKING, Any, Dict

from beaker_kernel.lib.context import BaseContext
from beaker_kernel.lib.subkernels.python import PythonSubkernel

from .agent import ElwoodAgent

if TYPE_CHECKING:
    from beaker_kernel.kernel import LLMKernel
    from beaker_kernel.lib.agent import BaseAgent
    from beaker_kernel.lib.subkernels.base import BaseSubkernel


class ElwoodContext(BaseContext):
    slug = "elwood"
    agent_cls: "BaseAgent" = ElwoodAgent

    def __init__(
        self,
        beaker_kernel: "LLMKernel",
        subkernel: "BaseSubkernel",
        config: Dict[str, Any],
    ) -> None:
        if not isinstance(subkernel, PythonSubkernel):
            raise ValueError("This context is only valid for Python.")
        self.elwood__functions = {}
        self.config = config
        super().__init__(beaker_kernel, subkernel, self.agent_cls, config)

    async def auto_context(self):
        intro = f"""
    You are a software engineer working on a climate dataset operations tool in a Jupyter notebook.

    Your goal is to help users perform various operations on climate datasets, such as regridding NetCDF datasets and plotting/previewing NetCDF files. 
    Additionally, the tools provide functionality to retrieve datasets from a storage server.

    Please provide assistance to users with their queries related to climate dataset operations.

    Remember to provide accurate information and avoid guessing if you are unsure of an answer.
    """

        result = intro
        return result
