from datetime import datetime
import pytest
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType
from app.modules.auth.models import User
from app import create_app, db
from app.modules.hubfile.models import Hubfile
from app.modules.featuremodel.models import FeatureModel


@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


@pytest.fixture(scope='module')
def init_database(test_client):
    with test_client.application.app_context():
        user = User(email='testuser@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        # Crear metadatos de prueba
        ds_meta_data = DSMetaData(
            title='Test Dataset',
            description='This is a test dataset',
            publication_type=PublicationType.BOOK,
            publication_doi='10.1234/testpubdoi',
            dataset_doi='10.1234/testdatasetdoi',
            tags='test, dataset',
            authors=[]
        )
        db.session.add(ds_meta_data)
        db.session.commit()

        new_dataset = DataSet(
            user_id=user.id,
            ds_meta_data_id=ds_meta_data.id,
            created_at=datetime.now()
        )
        db.session.add(new_dataset)
        db.session.commit()

        feature_model = FeatureModel(
            data_set_id=new_dataset.id
        )
        db.session.add(feature_model)
        db.session.commit()

        hubfile = Hubfile(
            name='file1.uvl',
            checksum='abc123',
            size=12345,
            feature_model_id=feature_model.id
        )
        db.session.add(hubfile)
        db.session.commit()

        yield db, user, ds_meta_data, hubfile

        db.session.remove()
        db.drop_all()


def test_download_all_dataset_not_logged_in(test_client):
    response = test_client.get("/dataset/download_all", follow_redirects=False)
    assert response.status_code == 302, "Expected 302 Redirect when not logged in"
    assert "/login" in response.headers["Location"], "Expected redirect to login page"


def test_download_all_dataset_logged_in(test_client, init_database):
    db, user, ds_meta_data, hubfile = init_database

    login_response = test_client.post("/login", data=dict(
        email="testuser@example.com",
        password="testpassword"
    ), follow_redirects=True)
    assert login_response.status_code == 200, "Login failed"

    response = test_client.get("/dataset/download_all", follow_redirects=True)
    assert response.status_code == 200, "Download all datasets was successful"

    test_client.get("/logout", follow_redirects=True)


def test_download_Splot(test_client, init_database):
    db, user, ds_meta_data, hubfile = init_database

    login_response = test_client.post("/login", data=dict(
        email="testuser@example.com",
        password="testpassword"
    ), follow_redirects=True)
    assert login_response.status_code == 200, "Login failed"

    new_dataset = DataSet(
        user_id=user.id,
        ds_meta_data_id=ds_meta_data.id,
        files=hubfile,
        created_at=datetime.now()
    )

    db.session.add(new_dataset)
    db.session.commit()

    response = test_client.get(f"/dataset/download_Splot/{new_dataset.id}", follow_redirects=True)
    assert response.status_code == 200, "Download all datasets was successful"

    test_client.get("/logout", follow_redirects=True)
