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


class VERSIONS(str):
    STU3 = "STU3"
    R4 = "R4"


class RESOURCES(str):
    DOCUMENT_REFERENCE = "DocumentReference"
    BINARY = "Binary"
    PATIENT = "Patient"


def get_api(file: str, version: str, type: str, query: dict = None, *append_paths):

    query_string = ""

    if query != None and len(query) > 0:
        query_string = "?" + "&".join(["=".join(item) for item in query.items()])

    url = "/".join((API, version, type, *append_paths)) + query_string

    r = requests.get(url=url, headers=credentials)

    if r.status_code == requests.codes.ok:
        content_type = r.headers["Content-Type"]

        content_type_tokens = content_type.split("; ")

        file_extention = MIME2EXT.get(content_type_tokens[0], "")

        charset = None

        if len(content_type_tokens) > 1:
            content_type_data = content_type_tokens[1].split("=")
            if content_type_data[0] == "charset":
                charset = content_type_data[1]

        output_file = Path(f"data/{file}.{file_extention}")
        output_file.parent.mkdir(exist_ok=True, parents=True)
        output_file.write_text(r.text, encoding=charset)


def get_search_api(
    filename: str, directory: str, version: str, resource: str, query: dict = None
):
    get_api(f"{directory}/{filename}", version, resource, query)


def get_read_api(id: str, directory: str, version: str, resource: str):
    get_api(f"{directory}/{id}", version, resource, None, id)
