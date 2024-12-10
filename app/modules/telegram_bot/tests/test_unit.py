import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from telegram import (
    Update, Message, Chat, User, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import ContextTypes
from decouple import config
from app.modules.telegram_bot.main import (
    start, login, is_valid_email, email, password, cancel, logout, BASE_URL,
    handle_document, login_to_portal, test, logged_in_users, my_datasets,
    upload, title, description, publication_type, doi, tags, confirmation
)


class MockFile:
    def __init__(self):
        self.file_name = "test_file.uvl"
        self.filename = self.file_name

    async def download_to_drive(self, path):
        pass


@pytest.fixture
def context():
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    mock_context.bot.send_message = AsyncMock()  # Mock de send_message
    mock_context.user_data = {}
    return mock_context


@pytest.fixture
def update():
    mock_update = MagicMock(spec=Update)
    mock_update.effective_chat = MagicMock(spec=Chat)
    mock_update.effective_chat.id = 12345  # ID del chat
    mock_update.message = MagicMock(spec=Message)
    mock_update.message.document = MagicMock()  # Mock de documento
    mock_update.message.document.file_name = 'test_file.uvl'  # Nombre de archivo simulado
    mock_update.message.document.get_file = AsyncMock(return_value=MockFile())  # Simula el comportamiento awaitable
    mock_update.message.chat = mock_update.effective_chat
    mock_update.message.from_user = MagicMock(spec=User)  # Mock del usuario
    return mock_update


@pytest.mark.asyncio
async def test_start(update, context):
    await start(update, context)

    context.bot.send_message.assert_any_call(
        chat_id=12345, text="Bienvenido al bot de Uvlhub"
    )
    context.bot.send_message.assert_any_call(
        chat_id=12345, text="Usa /help para ver la lista de comandos o /login para iniciar sesión"
    )


@pytest.mark.asyncio
async def test_login_flow(update, context):
    logged_in_users.clear()

    await login(update, context)
    context.bot.send_message.assert_any_call(chat_id=12345, text="Introduzca el correo electrónico.")

    update.message.text = "user1@example.com"
    await email(update, context)
    context.bot.send_message.assert_any_call(chat_id=12345, text="Introduzca la contraseña.")

    assert context.user_data['email'] == "user1@example.com", \
        f"Esperado 'user1@example.com', pero obtuvimos {context.user_data['email']}"

    update.message.text = "1234"
    await password(update, context)
    context.bot.send_message.assert_any_call(chat_id=12345, text="Login exitoso para user1@example.com.")

    assert 12345 in logged_in_users


def test_is_valid_email():
    assert is_valid_email("test@example.com") is True
    assert is_valid_email("invalid-email") is False
    assert is_valid_email("another.test@domain.org") is True


@patch('requests.Session')
def test_login_to_portal(mock_session):
    mock_response_login = MagicMock()
    mock_response_login.text = '<input name="csrf_token" value="mock_token">'
    mock_session.return_value.get.return_value = mock_response_login

    mock_response_post = MagicMock()
    mock_response_post.text = '<a>Login</a>'
    mock_session.return_value.post.return_value = mock_response_post

    session = mock_session.return_value
    base_url = "http://example.com"
    email = "test@example.com"
    password = config('MARIADB_PASSWORD')

    assert login_to_portal(session, base_url, email, password) is False


@pytest.mark.asyncio
async def test_logout(context, update):

    with patch("app.modules.telegram_bot.main.session.get") as mock_get:
        mock_get.return_value = MagicMock()
        await logout(update, context)

    context.bot.send_message.assert_any_call(
        chat_id=12345, text="Sesión cerrada correctamente."
    )


@pytest.mark.asyncio
@patch("app.modules.telegram_bot.main.session.get")
async def test_my_datasets(mock_get, update, context):

    mock_get.return_value.text = """
        <h1>My datasets</h1>
        <div>
            <a href="http://example.com/dataset/1">Dataset 1</a>
            <a href="http://example.com/dataset/2">Dataset 2</a>
        </div>
        <h5>Unsynchronized datasets</h5>
        <table>
            <tr><th>Unsynchronized Datasets</th></tr>
            <tr><td><a href="/dataset/3">Dataset 3</a></td></tr>
        </table>
    """

    logged_in_users[12345] = "mock_session_token"

    await my_datasets(update, context)

    context.bot.send_message.assert_any_call(
        chat_id=12345,
        text="Datasets sincronizados:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Dataset 1", url="http://example.com/dataset/1")],
            [InlineKeyboardButton("Dataset 2", url="http://example.com/dataset/2")]
        ])
    )
    context.bot.send_message.assert_any_call(
        chat_id=12345,
        text="Datasets no sincronizados:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Dataset 3", url=f"{BASE_URL}/dataset/3")]
        ])
    )


@pytest.mark.asyncio
@patch("app.modules.telegram_bot.main.media_route", "app/modules/telegram_bot/tests/")
@patch("os.makedirs")
@patch("os.path.exists", return_value=False)  # Simula que la carpeta no existe
async def test_handle_document_logged_in(_, mock_makedirs, update, context):
    logged_in_users[12345] = "mock_session_token"

    mock_makedirs.return_value = None

    mock_file = MockFile()
    update.message.document.get_file = AsyncMock(return_value=mock_file)

    await handle_document(update, context)

    # Verifica que no se haya llamado a send_message
    context.bot.send_message.assert_not_called()

    # Verifica que no se haya llamado con el mensaje de error
    called_args = context.bot.send_message.call_args_list
    for call in called_args:
        assert f"Error durante la subida del archivo: {mock_file.filename}" not in call[1]["text"]


@pytest.mark.asyncio
async def test_handle_document_invalid_format(update, context):
    logged_in_users[12345] = "mock_session_token"
    update.message.document.file_name = "invalid_file.txt"
    await handle_document(update, context)
    context.bot.send_message.assert_any_call(chat_id=12345,
                                             text="Solo se permiten archivos con extensión .uvl. "
                                             + "Por favor, adjunte un archivo válido.")


@pytest.mark.asyncio
async def test_logout_not_logged_in(update, context):
    await logout(update, context)
    context.bot.send_message.assert_any_call(chat_id=12345, text="Sesión cerrada correctamente.")


@pytest.mark.asyncio
async def test_cancel_command(update, context):
    logged_in_users[12345] = "mock_session_token"
    await cancel(update, context)
    context.bot.send_message.assert_any_call(chat_id=12345, text="Acción cancelada.")


@pytest.mark.asyncio
async def test_test_command(update, context):
    update = AsyncMock(spec=Update)
    update.effective_chat.id = 12345

    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot.send_document = AsyncMock()

    await test(update, context)

    context.bot.send_document.assert_called_once()


@pytest.mark.asyncio
async def test_upload(update, context):
    logged_in_users[12345] = "mock_session_token"
    update.message.document.file_id = "mock_file_id"

    with patch('os.path.exists', return_value=True), \
         patch('os.listdir', return_value=['file1.uvl']), \
         patch('app.modules.telegram_bot.main.session.post') as mock_post:

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'message': 'Success'}

        await upload(update, context)

        context.bot.send_message.assert_any_call(chat_id=12345, text="Escriba el título del dataset")
        update.message.text = "Título"
        await title(update, context)

        update.message.text = "Descripción"
        await description(update, context)

        context.bot.send_message.assert_any_call(chat_id=12345,
                                                 text="¿Qué tipo de publicación es? Selecciona una opción de la lista.")

        valid_option = "other"

        callback_query = MagicMock()
        callback_query.data = valid_option
        update.callback_query = callback_query

        callback_query.answer = AsyncMock()
        callback_query.edit_message_text = AsyncMock()

        await publication_type(update, context)

        context.bot.send_message.assert_any_call(chat_id=12345, text="Proporcione el DOI de la publicación.")

        update.message.text = ""
        await doi(update, context)

        context.bot.send_message.assert_any_call(chat_id=12345, text="Indique las etiquetas separadas por comas.")
        update.message.text = "tag,test"
        await tags(update, context)

        callback_query.data = "confirm_upload"
        await confirmation(update, context)

        mock_post.assert_called_once_with(
            f"{BASE_URL}/dataset/upload",
            data={
                "csrf_token": "mock_token",
                "title": "Título",
                "desc": "Descripción",
                "publication_type": "other",
                "publication_doi": "",
                "tags": "tag,test",
                "feature_models-0-uvl_filename": "file1.uvl",
                "feature_models-0-title": "",
                "feature_models-0-desc": "",
                "feature_models-0-publication_type": "other",
                "feature_models-0-publication_doi": "",
                "feature_models-0-tags": "tag,test",
                "feature_models-0-uvl_version": ""
            }
        )

        context.bot.send_message.assert_any_call(chat_id=12345, text="Para ver el dataset, use /myDatasets")
