import requests
import json
from pathlib import Path


def get_credentials(credentials_path: str):
    data = None
    with open(credentials_path, "r") as f:
        data = json.load(f)
    return data


MIME2EXT = {
    "text/html": "html",
    "text/rtf": "rtf",
    "application/xml": "xml",
    "application/json": "json",
}


class VERSION(str):
    STU3 = "STU3"
    R4 = "R4"


class RESOURCE(str):
    DOCUMENT_REFERENCE = "DocumentReference"
    BINARY = "Binary"
    PATIENT = "Patient"


class epic_api:
    def __init__(self, credentials_path: str, api: str):
        self.credentials = get_credentials(credentials_path)
        self.api = api

    def get_api(
        self, version: str, type: str, query: dict = None, *append_paths
    ) -> requests.Response:

        url = "/".join((self.api, version, type, *append_paths))

        return requests.get(url=url, headers=self.credentials, params=query)

    def get_search_api(
        self,
        filename: str,
        directory: str,
        version: str,
        resource: str,
        query: dict = None,
    ) -> int:
        result = self.get_api(version, resource, query)
        save_file(result, f"{directory}/{filename}")
        return result.status_code

    def get_read_api(self, id: str, directory: str, version: str, resource: str) -> int:
        result = self.get_api(version, resource, None, id)
        save_file(result, f"{directory}/{id}")
        return result.status_code

    def url_get_api(self, url: str) -> requests.Response:
        return requests.get(f"{self.api}/{url}", headers=self.credentials)


def save_file(response: requests.Response, filename: str) -> None:
    if response.status_code == requests.codes.ok:
        content_type = response.headers["Content-Type"]

        content_type_tokens = content_type.split("; ")

        file_extention = MIME2EXT.get(content_type_tokens[0], "")

        charset = None

        if len(content_type_tokens) > 1:
            content_type_data = content_type_tokens[1].split("=")
            if content_type_data[0] == "charset":
                charset = content_type_data[1]

        output_file = Path(f"data/{filename}.{file_extention}")
        output_file.parent.mkdir(exist_ok=True, parents=True)
        output_file.write_text(response.text, encoding=charset)
