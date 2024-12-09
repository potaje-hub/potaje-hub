import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from telegram import Update, Message, Chat, User  # type: ignore
from telegram.ext import ContextTypes  # type: ignore
import sys
import os
from app.modules.telegram_bot.main import (
    start, login, is_valid_email, email, password, cancel, logout,
    handle_document, my_datasets, login_to_portal, test, logged_in_users, upload, media_route
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
    
    assert context.user_data['email'] == "user1@example.com", f"Esperado 'user1@example.com', pero obtuvimos {context.user_data['email']}"
    
    update.message.text = "1234"
    await password(update, context)
    context.bot.send_message.assert_any_call(chat_id=12345, text="Login exitoso para user1@example.com.")

    assert 12345 in logged_in_users
    
            
def test_is_valid_email():
    assert is_valid_email("test@example.com")
    assert not is_valid_email("invalid-email")
    assert is_valid_email("another.test@domain.org")


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
    password = "password123"

    assert not login_to_portal(session, base_url, email, password)


@pytest.mark.asyncio
async def test_logout(context, update):

    with patch("app.modules.telegram_bot.main.session.get") as mock_get:
        mock_get.return_value = MagicMock()
        await logout(update, context)

    context.bot.send_message.assert_any_call(
        chat_id=12345, text="Sesión cerrada correctamente."
    )

@pytest.mark.asyncio
async def test_handle_document_logged_in(update, context):
    logged_in_users[12345] = "mock_session_token"

    # Mocks necesarios
    @patch("app.modules.telegram_bot.main.media_route", "app/modules/telegram_bot/tests/")
    @patch("os.makedirs")
    @patch("os.path.exists", return_value=False)  # Simula que la carpeta no existe
    async def inner(mock_exists, mock_makedirs):

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

    await inner()
            
@pytest.mark.asyncio
async def test_handle_document_invalid_format(update, context):
    logged_in_users[12345] = "mock_session_token"
    update.message.document.file_name = "invalid_file.txt"
    await handle_document(update, context)
    context.bot.send_message.assert_any_call(chat_id=12345, text="Solo se permiten archivos con extensión .uvl. Por favor, adjunte un archivo válido.")


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
    file_content = b"mock file content"
    update.message.document.file_id = "mock_file_id"
    with patch("app.modules.telegram_bot.main.download_file") as mock_download_file, \
         patch("app.modules.telegram_bot.main.upload_to_portal") as mock_upload_to_portal:
        mock_download_file.return_value = file_content
        mock_upload_to_portal.return_value = True
        await upload(update, context)
        mock_download_file.assert_called_once_with("mock_file_id")
        mock_upload_to_portal.assert_called_once_with("mock_session_token", file_content)
        context.bot.send_message.assert_any_call(chat_id=12345, text="Archivo subido correctamente a Uvlhub.")