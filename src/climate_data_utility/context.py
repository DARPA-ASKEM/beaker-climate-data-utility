from typing import TYPE_CHECKING, Any, Dict, Optional
import json
import codecs

from beaker_kernel.lib.context import BaseContext
from beaker_kernel.lib.subkernels.python import PythonSubkernel

from beaker_kernel.lib.utils import intercept

from archytas.tool_utils import LoopControllerRef


from .agent import ClimateDataUtilityAgent

import logging

if TYPE_CHECKING:
    from beaker_kernel.kernel import LLMKernel
    from beaker_kernel.lib.agent import BaseAgent
    from beaker_kernel.lib.subkernels.base import BaseSubkernel

logger = logging.getLogger(__name__)


class ClimateDataUtilityContext(BaseContext):
    slug = "climate_data_utility"
    agent_cls: "BaseAgent" = ClimateDataUtilityAgent

    def __init__(
        self,
        beaker_kernel: "LLMKernel",
        subkernel: "BaseSubkernel",
        config: Dict[str, Any],
    ) -> None:
        if not isinstance(subkernel, PythonSubkernel):
            raise ValueError("This context is only valid for Python.")
        self.climate_data_utility__functions = {}
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

        return intro

    @intercept()
    async def download_dataset_request(self, message):
        """
        This is used to download a dataset from the HMI server.
        """

        content = message.content
        uuid = content.get("uuid")
        filename = content.get("filename")
        if filename is None:
            filename = f"{uuid}.nc"

        code = self.get_code(
            "hmi_dataset_download",
            {
                "id": uuid,
                "filename": filename,
            },
        )

        code_download = await self.beaker_kernel.evaluate(
            code,
            parent_header={},
        )

        download_bytes = code_download.get("return")

    @intercept()
    async def save_dataset_request(self, message):
        """
        This tool is used to save a dataset to the HMI server.
        The 'dataset' argument is the variable name of the dataset to save in the notebook environment.
        """

        content = message.content
        dataset = content.get("dataset")
        new_dataset_filename = content.get("filename")

        create_code = self.get_code(
            "hmi_create_dataset",
            {
                "identifier": new_dataset_filename,
            },
        )
        create_response = await self.beaker_kernel.evaluate(
            create_code,
            parent_header={},
        )

        create_response_object = create_response.get("return")

        if isinstance(create_response_object, str):
            return create_response_object

        id = create_response_object.get("id")

        persist_code = self.get_code(
            "hmi_dataset_put",
            {
                "data": dataset,
                "id": id,
                "filename": f"{new_dataset_filename}",
            },
        )

        result = await self.beaker_kernel.evaluate(
            persist_code,
            parent_header={},
        )

        persist_status = result.get("return")

        self.beaker_kernel.send_response(
            "iopub",
            "save_dataset_response",
            {"dataset_create_status": create_response_object, "file_upload_status": persist_status},
        )
