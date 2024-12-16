import pytest
import os

from app.modules.auth.models import User
from app.modules.dataset.services import DataSetService
from app.modules.zenodo.services import ZenodoService
from app.modules.featuremodel.models import FeatureModel, FMMetaData
from app.modules.dataset.models import DSMetaData, DSMetrics, DataSet, PublicationType
from app import db


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        user_test = User(email='pablo@example.com', password='1234')
        db.session.add(user_test)
        db.session.commit()

        ds_metrics_test = DSMetrics(
            number_of_models="1",
            number_of_features="1"
        )

        ds_meta_data_test = DSMetaData(
            title="test fakenodo",
            description="test fakenodo",
            publication_type=PublicationType.PATENT,
            publication_doi="10.8888/test.doi",
            dataset_doi="10.8888/dataset.doi",
            tags="fk1,fk2",
            ds_metrics=ds_metrics_test
        )

        dataset_test = DataSet(
            user_id=1,
            ds_meta_data_id=1
        )

        fm_meta_data_test = FMMetaData(
            uvl_filename="file.uvl",
            title="tst fakenodo",
            description="tst fakenodo",
            publication_type=PublicationType.PATENT,
            publication_doi="10.8888/fm.doi",
            tags="fk1,fk2",
            uvl_version="1.0"
        )

        # Add the feature model
        feature_model_test = FeatureModel(
            data_set_id=1,
            fm_meta_data=fm_meta_data_test
        )

        # Add child elements
        ds_meta_data_test_child = DSMetaData(
            title="test fakenodo",
            description="test fakenodo",
            publication_type=PublicationType.PATENT,
            publication_doi="10.8888/data.doi",
            dataset_doi="10.8888/dataset.doi",
            tags="fk1,fk2",
            ds_metrics=ds_metrics_test
        )

        dataset_test_child = DataSet(
            user_id=1,
            ds_meta_data_id=2
        )

        fm_meta_data_test_child = FMMetaData(
            uvl_filename="file.zip",
            title="tst fakenodo",
            description="tst fakenodo",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            publication_doi="10.8888/doi.fm.doi",
            tags="fk1,fk2",
            uvl_version="1.0"
        )

        feature_model_test_child = FeatureModel(
            data_set_id=2,
            fm_meta_data=fm_meta_data_test_child
        )

        # Add all elements to the database
        db.session.add_all([
            ds_metrics_test,
            ds_meta_data_test,
            dataset_test,
            fm_meta_data_test,
            feature_model_test,
            ds_meta_data_test_child,
            dataset_test_child,
            fm_meta_data_test_child,
            feature_model_test_child
        ])
        db.session.commit()

    yield test_client


def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"


def test_upload_file_success_uvl(test_client):

    zenodo_service = ZenodoService()
    dataset_service = DataSetService()

    dataset = dataset_service.get_by_id(1)
    assert dataset is not None, "Dataset not found in the database"

    feature_model = FeatureModel.query.filter_by(data_set_id=1).first()
    assert feature_model is not None, "Feature model not found for the given dataset ID"

    user = User.query.filter_by(email='pablo@example.com').first()
    assert user is not None, "Test user not found in the database"

    uvl_filename = "file.uvl"
    user_id = user.id
    file_path = f"./uploads/user_{user_id}/dataset_{dataset.id}/{uvl_filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, "wb") as f:
            f.write(b"Mock content for testing UVL file upload.")

        zenodo_service.upload_file(dataset, 43, feature_model, user=user)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def test_upload_file_success_zip(test_client):

    zenodo_service = ZenodoService()
    dataset_service = DataSetService()

    dataset = dataset_service.get_by_id(2)
    feature_model = FeatureModel.query.filter_by(data_set_id=2).first()

    user = User.query.filter_by(email='pablo@example.com').first()
    assert user is not None, "Test user not found in the database"

    zip_filename = "file.zip"
    user_id = user.id
    file_path = f"./uploads/user_{user_id}/dataset_{dataset.id}/{zip_filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(b"Mock content for testing zip file upload.")

    zenodo_service.upload_file(dataset, 43, feature_model, user=user)

    os.remove(file_path)
