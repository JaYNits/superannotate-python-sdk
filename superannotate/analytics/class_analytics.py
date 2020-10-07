from .common import aggregate_annotations_as_df

from pathlib import Path
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

import json
import logging

logger = logging.getLogger("superannotate-python-sdk")


def class_distribution(export_root, project_names, visualize=True):
    """Aggregate distribution of classes across multiple projects.
    :param export_root: root export path of the projects
    :type export_root: Pathlike (str or Path)
    :param project_names: list of project names to aggregate through
    :type project_names: list of str
    :param visulaize: enables class histogram plot
    :type visualize: bool
    :return: DataFrame on class distribution with ["class", "count"] columns 
    :rtype: pandas DataFrame
    """

    logger.info(
        "Aggregating class distribution accross projects: {}.".format(
            ' '.join(project_names)
        ),
    )

    project_df_list = []
    for project_name in project_names:
        project_root = Path(export_root).joinpath(project_name)
        project_df = aggregate_annotations_as_df(project_root)
        project_df = project_df[["image_name", "instance_id", "class"]]
        project_df["project_name"] = project_name
        project_df_list.append(project_df)

    df = pd.concat(project_df_list, ignore_index=True)

    df["id"] = df["project_name"] + "_" + df["image_name"] + "_" + df[
        "instance_id"].astype(str)
    df = df.groupby("class")['id'].nunique()
    df = df.reset_index().rename(columns={'id': 'count'})
    df = df.sort_values(["count"], ascending=False)

    if visualize:
        fig = px.bar(
            df,
            x='class',
            y='count',
        )
        fig.update_traces(hovertemplate="%{x}: %{y}")
        fig.update_yaxes(title_text="Instance Count")
        fig.update_xaxes(title_text="")
        fig.show()

    return df


def attribute_distribution(export_root, project_names, visualize=True):
    """Aggregate distribution of attributes across multiple projects.
    :param export_root: root export path of the projects
    :type export_root: Pathlike (str or Path)
    :param project_names: list of project names to aggregate through
    :type project_names: list of str
    :param visulaize: enables attribute histogram plot
    :type visualize: bool
    :return: DataFrame on attribute distribution with ["class", "attribute name", "count"] columns 
    :rtype: pandas DataFrame
    """

    logger.info(
        "Aggregating attribute distribution accross projects: {}.".format(
            ' '.join(project_names)
        ),
    )

    project_df_list = []
    for project_name in project_names:
        project_root = Path(export_root).joinpath(project_name)
        project_df = aggregate_annotations_as_df(project_root)
        project_df_list.append(project_df[["class", "attribute_name"]])

    df = pd.concat(project_df_list, ignore_index=True)
    df = df.value_counts().reset_index().rename(columns={0: 'count'})
    df = df.sort_values(["class", "count"], ascending=False, ignore_index=True)

    if visualize:
        df["attribute_id"] = df["class"] + ":" + df["attribute_name"]
        fig = px.bar(
            df,
            x="attribute_id",
            y="count",
            color="class",
            custom_data=['attribute_name']
        )
        fig.update_traces(hovertemplate="%{customdata[0]}: %{y}")
        fig.update_yaxes(title_text="Instance Count")
        fig.update_xaxes(title_text="Attribute", showticklabels=False)
        fig.show()

    return df