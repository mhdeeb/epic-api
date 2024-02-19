import requests
import json
from pathlib import Path

API = "https://vendorservices.epic.com/interconnect-amcurprd-username/api/FHIR"


def get_credentials(credentials_path: str):
    data = None
    with open(credentials_path, "r") as f:
        data = json.load(f)
    return data


credentials = get_credentials("credentials.json")

MIME2EXT = {
    "text/html": "html",
    "text/rtf": "rtf",
    "application/xml": "xml",
}


class VERSION(str):
    STU3 = "STU3"
    R4 = "R4"


class RESOURCE(str):
    DOCUMENT_REFERENCE = "DocumentReference"
    BINARY = "Binary"
    PATIENT = "Patient"


def get_api(
    version: str, type: str, query: dict = None, *append_paths
) -> requests.Response:

    query_string = ""

    if query and len(query) > 0:
        query_string = "?" + "&".join(["=".join(item) for item in query.items()])

    url = "/".join((API, version, type, *append_paths)) + query_string

    return requests.get(url=url, headers=credentials)


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


def get_search_api(
    filename: str, directory: str, version: str, resource: str, query: dict = None
) -> None:
    result = get_api(version, resource, query)
    save_file(result, f"{directory}/{filename}")


def get_read_api(id: str, directory: str, version: str, resource: str) -> None:
    result = get_api(version, resource, None, id)
    save_file(result, f"{directory}/{id}")
