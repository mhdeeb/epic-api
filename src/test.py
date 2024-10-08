from epic_api import (
    epic_api,
    save_file,
    VERSION,
    RESOURCE,
)
from threading import Thread
from traceback import print_exc
from concurrent.futures import Future
import xml.etree.ElementTree as ET


def threaded(fn) -> Future:
    """@threaded decorator from https://stackoverflow.com/a/19846691"""

    def call_with_future(fn, future, args, kwargs):
        try:
            result = fn(*args, **kwargs)
            future.set_result(result)
        except Exception as exc:
            print_exc()  # LOGGER
            future.set_exception(exc)

    def wrapper(*args, **kwargs):
        future = Future()
        Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
        return future

    return wrapper


PATIENT_DIRECTORY = "patients"
CLINICAL_NOTES_DIRECTORY = "clinical_notes"

api = epic_api(
    "credentials.json",
    "https://vendorservices.epic.com/interconnect-amcurprd-username/api/FHIR",
)


@threaded
def test1():
    ID = "eqwL51yc.8a6agwXsiHt-VA3"
    status_code = api.get_read_api(
        ID, CLINICAL_NOTES_DIRECTORY, VERSION.R4, RESOURCE.BINARY
    )
    print("test1:", status_code)


@threaded
def test2():
    query = {
        "patient": "enh2Q1c0oNRtWzXArnG4tKw3",
        "class": "clinical-note",
        "_count": 100,
    }
    status_code = api.get_search_api(
        f"test2_{query['patient']}",
        PATIENT_DIRECTORY,
        VERSION.STU3,
        RESOURCE.DOCUMENT_REFERENCE,
        query,
    )
    print("test2:", status_code)


@threaded
def test3():
    ID = "eqwL51yc.8a6agwXsiHt-VA3"
    result = api.get_api(VERSION.R4, RESOURCE.BINARY, None, ID)
    print("test3:", result.status_code)
    save_file(result, f"{CLINICAL_NOTES_DIRECTORY}/test3_{ID}")


@threaded
def test4():
    query = {
        "class": "clinical-note",
        "patient": "enh2Q1c0oNRtWzXArnG4tKw3",
    }
    result = api.get_api(VERSION.STU3, RESOURCE.DOCUMENT_REFERENCE, query)
    print("test4:", result.status_code)
    save_file(result, f"{CLINICAL_NOTES_DIRECTORY}/test4_{query['patient']}")


@threaded
def test5():
    query = {
        "address": "123 Main St.",
        "address-city": "Madison",
        "address-postalcode": "53703",
        "address-state": "Wisconsin",
        "family": "Mychart",
        "gender": "Female",
        "given": "Allison",
        "telecom": "608-123-4567",
    }
    result = api.get_api(VERSION.R4, RESOURCE.PATIENT, query)
    print("test5:", result.status_code)
    save_file(
        result, f"{CLINICAL_NOTES_DIRECTORY}/test5_{query['given']}_{query['family']}"
    )


@threaded
def test6():
    result = api.url_get_api(
        "R4/Patient?address=123 Main St.&address-city=Madison&address-postalcode=53703&address-state=Wisconsin&family=Mychart&gender=Female&given=Allison&telecom=608-123-4567"
    )
    print("test6:", result.status_code)
    save_file(result, f"{CLINICAL_NOTES_DIRECTORY}/test6_Mychart")


@threaded
def test7():
    result = api.url_get_api("STU3/Binary/eeBl-ySJMCBtDT38pPJZG3Q3")
    print("test7:", result.status_code)
    save_file(result, f"{CLINICAL_NOTES_DIRECTORY}/test7_note")


@threaded
def test8():
    tree = ET.parse(f"data/{PATIENT_DIRECTORY}/test2_enh2Q1c0oNRtWzXArnG4tKw3.xml")

    @threaded
    def req(url: str) -> None:
        result = api.url_get_api(url)
        print(result.status_code)
        save_file(result, f"{CLINICAL_NOTES_DIRECTORY}/test8_{url[-1]}")

    root = tree.getroot()
    for child in root.findall(
        ".//{http://hl7.org/fhir}attachment/{http://hl7.org/fhir}url"
    ):
        url = "/".join(child.attrib["value"].rsplit("/", 3)[1:])
        req(url)


def patient_to_notes(id: str):
    query = {
        "patient": id,
        "class": "clinical-note",
        "_count": 100,
    }
    result = api.get_api(VERSION.STU3, RESOURCE.DOCUMENT_REFERENCE, query)
    print("patient_get:", "OK" if result.status_code == 200 else "FAIL")
    root = ET.fromstring(result.text)

    @threaded
    def req(url: str, filename: str) -> None:
        result = api.url_get_api(url)
        print(f"{filename}: {'OK' if result.status_code==200 else 'FAIL'}")
        save_file(result, f"{CLINICAL_NOTES_DIRECTORY}/{filename}")

    for child in root.findall(
        ".//{http://hl7.org/fhir}attachment/{http://hl7.org/fhir}url"
    ):
        last_three = child.attrib["value"].rsplit("/", 3)[1:]
        url = "/".join(last_three)
        req(url, f"{id}_{last_three[-1]}")


if __name__ == "__main__":
    patient_to_notes("enh2Q1c0oNRtWzXArnG4tKw3")
