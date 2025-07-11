from .formatter import Formatter
from loguru import logger
import requests
from app.base.base_plugin import BasePlugin
from app.base.remote_data_plugin import RemoteDataPlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin
from app.base.document_data_plugin import DocumentDataPlugin
from typing import  Tuple, Optional
from app.readers.base_reader import BaseReader
import os


class Document(BasePlugin, PluginMetadataMixin,DocumentDataPlugin,  Formatter):
    """
    Document class for interacting with document data.
    """

    def __init__(self, connector_name : str, document_files:str):
        super().__init__(__name__)

        self.connection = {}

        self.connector_name = connector_name.replace(' ','_')
        self.params = {
            'document_files': document_files,
        }

        self.supported_types = {".pdf": "pdf", ".docx": "docx", ".txt": "text", ".yaml": "yaml"}


    def connect(self):
        """
        Mocked connection method for pdf.

        :return: Tuple containing connection status (True/False) and an error message if any.
        """
        return True, None


    def healthcheck(self)-> Tuple[bool, Optional[str]]:
        """
        Perform a health check by checking if the document is accessible.

        :return: Tuple containing the health status (True/False) and error message (if any).
        """
        logger.info("health check for documentations")

        try:
            data = []
            for file_info in self.params.get("document_files", []):
                file_path = file_info.get("file_path")
                if not file_path:
                    logger.error("File path is missing in the document file information.")
                    continue

                # Check if it's a URL or a local file
                if file_path.startswith("http://") or file_path.startswith("https://"):
                    try:
                        response = requests.head(file_path, allow_redirects=True, timeout=5)
                        if response.status_code >= 400:
                            logger.error(f"URL not accessible: {file_path}")
                        else:
                            data.append(file_path)
                    except Exception as e:
                        logger.error(f"Error accessing URL {file_path}: {e}")
                else:
                    if os.path.exists(file_path):
                        data.append(file_path)
                    else:
                        logger.error(f"Local file does not exist: {file_path}")
            if not data:
                raise ValueError("No data fetched during health check")
            
            return True, None
        except Exception as e:
            logger.exception(f"Exception during fetching data: {str(e)}")
            return False, str(e)

    def fetch_data(self, params=None):
        data = []

        for file_info in self.params.get("document_files", []):
            url = file_info.get("file_path")
            if url is None:
                logger.error("URL is missing in the document file information.")
                continue

            file_type = None

            for ext, typ in self.supported_types.items():
                if url.endswith(ext):
                    file_type = typ
                    break

            if file_type is None:
                logger.error(f"Unsupported file format: {url}")
                continue
            base_reader = BaseReader({
                "type": file_type,
                "path": [url]
            })
            data.extend(base_reader.load_data())

        return data


