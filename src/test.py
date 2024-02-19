from request import (
    get_read_api,
    get_search_api,
    VERSIONS,
    RESOURCES,
)

PATIENT_DIRECTORY = "patients"
CLINICAL_NOTES_DIRECTORY = "clinical_notes"

ID = "eqwL51yc.8a6agwXsiHt-VA3"
get_read_api(ID, CLINICAL_NOTES_DIRECTORY, VERSIONS.R4, RESOURCES.BINARY)

query = {"family": "lufhir", "given": "kazuya", "birthdate": "1986-02-23"}
get_search_api("test", PATIENT_DIRECTORY, VERSIONS.R4, RESOURCES.PATIENT, query)
