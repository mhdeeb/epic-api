from epic_api import (
    get_api,
    get_read_api,
    get_search_api,
    save_file,
    VERSION,
    RESOURCE,
)

PATIENT_DIRECTORY = "patients"
CLINICAL_NOTES_DIRECTORY = "clinical_notes"

# ID = "eibaYRQF6yVTF.5R2n92hhMhIzS.lJx9doPV5HgjIawc3"


def test1():
    ID = "eqwL51yc.8a6agwXsiHt-VA3"
    get_read_api(ID, CLINICAL_NOTES_DIRECTORY, VERSION.R4, RESOURCE.BINARY)


def test2():
    query = {"family": "lufhir", "given": "kazuya", "birthdate": "1986-02-23"}
    get_search_api("test", PATIENT_DIRECTORY, VERSION.R4, RESOURCE.PATIENT, query)


def test3():
    ID = "eqwL51yc.8a6agwXsiHt-VA3"
    result = get_api(VERSION.R4, RESOURCE.BINARY, None, ID)
    save_file(result, f"{CLINICAL_NOTES_DIRECTORY}/{ID}")


def test4():
    query = {"family": "lufhir", "given": "kazuya", "birthdate": "1986-02-23"}
    result = get_api(VERSION.R4, RESOURCE.PATIENT, query)
    save_file(result, f"{PATIENT_DIRECTORY}/test")


if __name__ == "__main__":
    test2()
