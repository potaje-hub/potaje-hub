
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from telegram import Update, Message, Chat, User  # type: ignore
from telegram.ext import ContextTypes  # type: ignore
import sys
import os
from telegram_bot.main import (
    start, login, is_valid_email, logout,
    handle_document, login_to_portal, test
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


@pytest.fixture
def context():
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    mock_context.bot.send_message = AsyncMock()  # Mock de send_message
    return mock_context


@pytest.mark.asyncio
async def test_start():
    mock_update = AsyncMock(spec=Update)
    mock_update.effective_chat.id = 12345

    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    mock_context.bot.send_message = AsyncMock()

    await start(mock_update, mock_context)

    mock_context.bot.send_message.assert_any_call(
        chat_id=12345, text="Bienvenido al bot de Uvlhub"
    )
    mock_context.bot.send_message.assert_any_call(
        chat_id=12345, text="Usa /help para ver la lista de comandos o /login para iniciar sesión"
    )


@pytest.mark.asyncio
async def test_login():
    mock_update = AsyncMock(spec=Update)
    mock_update.effective_chat.id = 12345

    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    mock_context.bot.send_message = AsyncMock()

    result = await login(mock_update, mock_context)

    mock_context.bot.send_message.assert_any_call(
        chat_id=12345, text="Introduzca el correo electrónico."
    )
    assert result == 0  # EMAIL constant


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
async def test_logout():
    mock_update = AsyncMock(spec=Update)
    mock_update.effective_chat.id = 12345

    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    mock_context.bot.send_message = AsyncMock()

    with patch("main.session.get") as mock_get:
        mock_get.return_value = MagicMock()
        await logout(mock_update, mock_context)

    mock_context.bot.send_message.assert_any_call(
        chat_id=12345, text="Sesión cerrada correctamente."
    )


@pytest.fixture
def update():
    mock_update = MagicMock(spec=Update)
    mock_update.effective_chat = MagicMock(spec=Chat)
    mock_update.effective_chat.id = 12345  # ID del chat
    mock_update.message = MagicMock(spec=Message)
    mock_update.message.document = MagicMock()  # Mock de documento
    mock_update.message.document.file_name = 'test_file.uvl'  # Nombre de archivo simulado
    mock_update.message.chat = mock_update.effective_chat
    mock_update.message.from_user = MagicMock(spec=User)  # Mock del usuario
    return mock_update


@pytest.mark.asyncio
async def test_handle_document():
    mock_update = AsyncMock(spec=Update)
    mock_update.effective_chat.id = 12345
    mock_update.message.document.file_name = "test.uvl"

    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    mock_context.bot.send_message = AsyncMock()

    await handle_document(mock_update, mock_context)

    mock_context.bot.send_message.assert_any_call(
        chat_id=12345, text="Debe iniciar sesión para subir archivos a Uvlhub."
    )


@pytest.mark.asyncio
async def test_test_command():
    mock_update = AsyncMock(spec=Update)
    mock_update.effective_chat.id = 12345

    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    mock_context.bot.send_document = AsyncMock()

    await test(mock_update, mock_context)

    mock_context.bot.send_document.assert_called_once()
