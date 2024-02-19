from epic_api import (
    get_api,
    get_read_api,
    get_search_api,
    url_get_api,
    save_file,
    VERSION,
    RESOURCE,
)
from threading import Thread
from traceback import print_exc
from concurrent.futures import Future


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


@threaded
def test1():
    ID = "eqwL51yc.8a6agwXsiHt-VA3"
    status_code = get_read_api(
        ID, CLINICAL_NOTES_DIRECTORY, VERSION.R4, RESOURCE.BINARY
    )
    print("test1:", status_code)


@threaded
def test2():
    query = {
        "patient": "enh2Q1c0oNRtWzXArnG4tKw3",
        "_count": 100,
    }
    status_code = get_search_api(
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
    result = get_api(VERSION.R4, RESOURCE.BINARY, None, ID)
    print("test3:", result.status_code)
    save_file(result, f"{CLINICAL_NOTES_DIRECTORY}/test3_{ID}")


@threaded
def test4():
    query = {
        "class": "clinical-note",
        "patient": "enh2Q1c0oNRtWzXArnG4tKw3",
    }
    result = get_api(VERSION.STU3, RESOURCE.DOCUMENT_REFERENCE, query)
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
    result = get_api(VERSION.R4, RESOURCE.PATIENT, query)
    print("test5:", result.status_code)
    save_file(
        result, f"{CLINICAL_NOTES_DIRECTORY}/test5_{query['given']}_{query['family']}"
    )


@threaded
def test6():
    result = url_get_api(
        "R4/Patient?address=123 Main St.&address-city=Madison&address-postalcode=53703&address-state=Wisconsin&family=Mychart&gender=Female&given=Allison&telecom=608-123-4567"
    )
    print("test6:", result.status_code)
    save_file(result, f"{CLINICAL_NOTES_DIRECTORY}/test6_Mychart")


def test7():
    result = url_get_api(
        "R4/DocumentReference?patient=e7XZi7JJ6AZSxlmZBc9-Rdw3&category=clinical-note&_count=3"
    )
    print("test7:", result.status_code)
    save_file(result, f"{CLINICAL_NOTES_DIRECTORY}/test7_note")


if __name__ == "__main__":
    test2()
