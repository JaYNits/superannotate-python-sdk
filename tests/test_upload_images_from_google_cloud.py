import os
from pathlib import Path

import pytest

import superannotate as sa

test_root = Path().resolve() / 'tests'

PROJECT_NAME = 'test_google_cloud_upload'
GOOGLE_PROJECT = 'siam'
BUCKET_NAME = 'superannotate-python-sdk-tests'


@pytest.mark.skipif(
    "SA_CLOUD_TESTS" not in os.environ or os.environ["SA_CLOUD_TESTS"] != "1",
    reason="Requires env variable to be set"
)
def test_upload_images_from_google_cloud_to_project():
    folder_path_with_test_imgs = 'cat_pics_sdk_test'
    folder_path_empty = 'empty_folder'
    folder_path_non_existent = 'nonex'
    test_folders = [
        (folder_path_with_test_imgs, [6, 0, 6, 0]),
        (folder_path_empty, [0, 0, 0, 0]),
        (folder_path_non_existent, [0, 0, 0, 0])
    ]
    if sa.search_projects(PROJECT_NAME) != []:
        sa.delete_project(PROJECT_NAME)
    proj_data = sa.create_project(PROJECT_NAME, "test", "Vector")
    for folder_path, true_res in test_folders:
        uploaded_urls, uploaded_filenames, duplicate_filenames, not_uploaded_urls = sa.upload_images_from_google_cloud_to_project(
            proj_data,
            GOOGLE_PROJECT,
            BUCKET_NAME,
            folder_path,
            annotation_status='InProgress',
            image_quality_in_editor="original"
        )
        assert len(uploaded_urls) == true_res[0]
        assert len(duplicate_filenames) == true_res[1]
        assert len(uploaded_filenames) == true_res[2]
        assert len(not_uploaded_urls) == true_res[3]
