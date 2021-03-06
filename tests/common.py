from pathlib import Path
import superannotate as sa


def upload_project(
    project_path,
    project_name,
    description,
    ptype,
    from_s3_bucket=None,
    annotation_status='NotStarted',
    image_quality_in_editor=None
):
    if isinstance(project_path, str):
        project_path = Path(project_path)

    projects = sa.search_projects(project_name, return_metadata=True)
    for project in projects:
        sa.delete_project(project)

    project = sa.create_project(project_name, description, ptype)

    sa.create_annotation_classes_from_classes_json(
        project,
        project_path / "classes" / "classes.json",
        from_s3_bucket=from_s3_bucket
    )
    sa.upload_images_from_folder_to_project(
        project,
        project_path,
        annotation_status=annotation_status,
        from_s3_bucket=from_s3_bucket,
        image_quality_in_editor=image_quality_in_editor
    )
    sa.upload_annotations_from_folder_to_project(
        project, project_path, from_s3_bucket=from_s3_bucket
    )

    return project
