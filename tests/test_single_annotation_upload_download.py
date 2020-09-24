from pathlib import Path
import filecmp
import json

import pytest

import superannotate as sa

sa.init(Path.home() / ".superannotate" / "config.json")

PROJECT_NAME = "testing_1419"


@pytest.mark.parametrize(
    "project_type,name,description,from_folder", [
        (
            "Vector",
            "Example Project test vector single annotation upload download",
            "test vector", Path("./tests/sample_project_vector")
        ),
        (
            "Pixel",
            "Example Project test pixel single annotation upload download",
            "test pixel", Path("./tests/sample_project_pixel")
        )
    ]
)
def test_annotation_download_upload(
    project_type, name, description, from_folder, tmpdir
):
    projects = sa.search_projects(name, return_metadata=True)
    for project in projects:
        sa.delete_project(project)
    project = sa.create_project(name, description, project_type)
    sa.upload_images_from_folder_to_project(
        project, from_folder, annotation_status="NotStarted"
    )
    sa.create_annotation_classes_from_classes_json(
        project, from_folder / "classes" / "classes.json"
    )
    sa.upload_annotations_from_folder_to_project(project, from_folder)
    image = sa.search_images(project)[2]
    sa.download_image_annotations(project, image, tmpdir)
    anns_json_in_folder = list(Path(tmpdir).glob("*.json"))
    anns_mask_in_folder = list(Path(tmpdir).glob("*.png"))
    assert len(anns_json_in_folder) == 1
    assert len(anns_mask_in_folder) == (1 if project_type == "Pixel" else 0)

    input_annotation_paths = sa.image_path_to_annotation_paths(
        from_folder / image, project_type
    )

    json1 = json.load(open(input_annotation_paths[0]))
    json2 = json.load(open(anns_json_in_folder[0]))
    for i in json1:
        del i["classId"]
    for i in json2:
        del i["classId"]
    assert json1 == json2
    if project_type == "Pixel":
        assert filecmp.cmp(
            input_annotation_paths[1], anns_mask_in_folder[0], shallow=False
        )
    # sa.download_image_preannotations(image, tmpdir)
