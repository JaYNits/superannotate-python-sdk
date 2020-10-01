import logging

from .api import API
from .common import (
    annotation_status_int_to_str, annotation_status_str_to_int,
    image_path_to_annotation_paths, project_type_int_to_str,
    project_type_str_to_int, user_role_str_to_int
)
from .db.annotation_classes import (
    create_annotation_class, create_annotation_classes_from_classes_json,
    delete_annotation_class, download_annotation_classes_json,
    search_annotation_classes
)
from .db.exports import download_export, get_exports, prepare_export
from .db.images import (
    download_image, download_image_annotations, download_image_preannotations,
    get_image_annotations, get_image_bytes, get_image_metadata,
    get_image_preannotations, search_images, set_image_annotation_status,
    upload_annotations_from_file_to_image
)
from .db.projects import (
    create_project, delete_project, get_project_image_count,
    get_project_metadata, search_projects, share_project, unshare_project,
    upload_annotations_from_folder_to_project,
    upload_images_from_folder_to_project,
    upload_images_from_s3_bucket_to_project, upload_images_to_project,
    upload_preannotations_from_folder_to_project
)
from .db.teams import (
    delete_team_contributor_invitation, invite_contributor_to_team
)
from .db.users import search_team_contributors
from .exceptions import SABaseException
from .version import Version

from .input_converters.conversion import convert_annotation_format_from, convert_annotation_format_to

from .compareutils.compare import compare
#formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
formatter = logging.Formatter(fmt='SA-PYTHON-SDK - %(levelname)s - %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("superannotate-python-sdk")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

_api = API.get_instance()


def init(path_to_config_json):
    """Initializes and authenticates to SuperAnnotate platform using the config file.

    :param path_to_config_json: Location to config JSON file
    :type path_to_config_json: str or Path
    """
    _api.set_auth(path_to_config_json)
