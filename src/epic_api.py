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

    url = "/".join((API, version, type, *append_paths))

    return requests.get(url=url, headers=credentials, params=query)


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
) -> int:
    result = get_api(version, resource, query)
    save_file(result, f"{directory}/{filename}")
    return result.status_code


def get_read_api(id: str, directory: str, version: str, resource: str) -> int:
    result = get_api(version, resource, None, id)
    save_file(result, f"{directory}/{id}")
    return result.status_code


def url_get_api(url: str) -> requests.Response:
    return requests.get(f"{API}/{url}", headers=credentials)
