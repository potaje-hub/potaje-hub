import logging
import os
import shutil
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Document
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
import requests
from bs4 import BeautifulSoup
import re
from app.modules.dataset.services import DataSetService


dataset_service = DataSetService()


csrf_token = None

def login_to_portal(session, base_url, email, password):
    global csrf_token
    login_page = session.get(f"{base_url}/login")
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    login_data = {
        "csrf_token": csrf_token,
        "email": email,
        "password": password,
        "submit": "Login"
    }
    login_response = session.post(f"{base_url}/login", data=login_data, verify=False)
    soup = BeautifulSoup(login_response.text, 'html.parser')
    if soup.find('a', string="Login"):
        return False
    return True

TOKEN = '7318289178:AAGlwhBrbP-6RVSpx67k-B1izPLZYMIrRO0'
BASE_URL = "http://127.0.0.1:5000"
# BASE_URL = "https://www.uvlhub.io"
# BASE_URL = "https://fa09-193-147-173-132.ngrok-free.app"


EMAIL, PASSWORD = range(2)
TITLE, DESCRIPTION, PUBLICATION_TYPE, DOI, TAGS, CONFIRMATION = range(6)

VALID_PUBLICATION_TYPES = [
    "None", "Annotation Collection", "Book", "Book Section", "Conference Paper", 
    "Data Management Plan", "Journal Article", "Patent", "Preprint", 
    "Project Deliverable", "Project Milestone", "Proposal", "Report", 
    "Software Documentation", "Taxonomic Treatment", "Technical Note", 
    "Thesis", "Working Paper", "Other"
]

session = requests.Session()
logged_in_users = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def is_valid_email(email: str) -> bool:
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bienvenido al bot de Uvlhub. Usa /login para iniciar sesión")

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id in logged_in_users:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Ya ha iniciado sesión.")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Use /help para conocer los comandos disponibles.")

        return
    if os.path.exists("telegram_bot/media/" + str(update.effective_chat.id)):
        shutil.rmtree("telegram_bot/media/" + str(update.effective_chat.id), ignore_errors=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Introduzca el correo electrónico.")
    return EMAIL

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    if not is_valid_email(email):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Introduzca una dirección de correo válida.")
        return EMAIL
    context.user_data['email'] = email
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Introduzca la contraseña.")
    return PASSWORD

async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    email = context.user_data['email']
    auth = login_to_portal(session, BASE_URL, email, password)
    if auth:
        logged_in_users[update.effective_chat.id] = email
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Login exitoso para {email}.")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Use /help para conocer los comandos disponibles.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Login fallido, verifique sus credenciales.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Acción cancelada.")
    return ConversationHandler.END

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session.get(f"{BASE_URL}/logout")
    logged_in_users.pop(update.effective_chat.id, None)
    shutil.rmtree("telegram_bot/media/" + str(update.effective_chat.id), ignore_errors=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sesión cerrada correctamente.")

async def my_datasets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in logged_in_users:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Debe iniciar sesión para usar este comando.")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Usa /login para iniciar sesión")
        return
    login_page = session.get(f"{BASE_URL}/dataset/list")
    soup = BeautifulSoup(login_page.text, 'html.parser')
    
    #Sync
    data_sync = soup.find('h1', string="My datasets").find_next_sibling('div')
    dataset_links_sync = data_sync.find_all('a', href=True)
    keyboard_sync = [
        [InlineKeyboardButton(link.get_text().strip(), url=str(link['href']).replace("http://localhost:5000", BASE_URL))]
        for link in dataset_links_sync if not link.get_text().strip().startswith("http://localhost:5000")
    ]
    reply_markup_sync = InlineKeyboardMarkup(keyboard_sync)    
    
    # Async
    data_async = soup.find('h5', string="Unsynchronized datasets").find_next('table').find_all('tr')
    keyboard_async=[]
    for row in data_async[1:]:
        link = row.find('a')
        if link:
            text = link.get_text(strip=True)
            href = link['href']
            keyboard_async.append([InlineKeyboardButton(text, f"{BASE_URL}{href}")])
            
    reply_markup_async = InlineKeyboardMarkup(keyboard_async)    
        
    if((len(keyboard_sync)+len(keyboard_async))==0):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No existen datasets")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Datasets sincronizados:", reply_markup=reply_markup_sync)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Datasets no sincronizados:", reply_markup=reply_markup_async)
    
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in logged_in_users:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Debe iniciar sesión para subir archivos a Uvlhub.")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Usa /login para iniciar sesión")
        return
    document: Document = update.message.document
    if not document.file_name.endswith('.uvl'):
        await update.message.reply_text("Solo se permiten archivos con extensión .uvl. Por favor, adjunte un archivo válido.")
        return ConversationHandler.END
    if not os.path.exists("telegram_bot/media/" + str(update.effective_chat.id)):
        os.makedirs("telegram_bot/media/" + str(update.effective_chat.id))
    file_path = os.path.join("telegram_bot/media/" + str(update.effective_chat.id), document.file_name)
    
    file = await document.get_file()
    await file.download_to_drive(file_path)
    context.user_data['file_path'] = file_path

    total_files = len(os.listdir("telegram_bot/media/" + str(update.effective_chat.id)))
    await update.message.reply_text(f"Se han subido un total de {total_files} archivos.")

    try:
        with open(file_path, "rb") as f:
            files = {
                "file": (document.file_name, f, "application/octet-stream")
            }
            response = session.post(
                f"{BASE_URL}/dataset/file/upload",
                data={"csrf_token": csrf_token},
                files=files
            )
        
        if response.status_code == 200:
            await update.message.reply_text(f"Archivo '{document.file_name}' subido exitosamente a Uvlhub.")
        else:
            await update.message.reply_text(f"Error al subir el archivo a Uvlhub: {response.status_code}\n{response.text}")
    except Exception as e:
        await update.message.reply_text(f"Error durante la subida del archivo: {str(e)}")
            
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists("telegram_bot/media/" + str(update.effective_chat.id)) or len(os.listdir("telegram_bot/media/" + str(update.effective_chat.id)))<1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Debes adjuntar primero uno o varios archivos")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Si no tienes archivos .uvl, puedes descargarte uno usando /test")
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Escriba el título del dataset")
    return TITLE

async def title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['title'] = update.message.text
    await update.message.reply_text("Proporcione una descripción para el datset.")
    return DESCRIPTION

async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['description'] = update.message.text
    await update.message.reply_text("¿Qué tipo de publicación es? Selecciona una opción de la lista.")
    
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in VALID_PUBLICATION_TYPES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Selecciona el tipo de publicación:", reply_markup=reply_markup)
    return PUBLICATION_TYPE

async def publication_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    publication_type = query.data
    
    context.user_data['publication_type'] = publication_type
    
    await query.answer()
    await query.edit_message_text(f"Tipo de publicación seleccionado: {publication_type}")
    
    await query.message.reply_text("Proporcione el DOI de la publicación.")
    return DOI

async def doi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['doi'] = update.message.text
    await update.message.reply_text("Indique las etiquetas separadas por comas.")
    return TAGS

async def tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['tags'] = update.message.text.split(',')
    archives = "\n".join(f"- {archivo}" for archivo in os.listdir("telegram_bot/media/" + str(update.effective_chat.id)))
    
    await update.message.reply_text(f"Datos recopilados:\n"
                                  f"Título: {context.user_data['title']}\n"
                                  f"Descripción: {context.user_data['description']}\n"
                                  f"Tipo de publicación: {context.user_data['publication_type']}\n"
                                  f"DOI: {context.user_data['doi']}\n"
                                  f"Etiquetas: {', '.join(context.user_data['tags'])}\n"
                                f"Archivos adjuntos:\n{archives}")    
    
    keyboard = [
        [InlineKeyboardButton("Confirmar", callback_data="confirm_upload")],
        [InlineKeyboardButton("Cancelar", callback_data="cancel_upload")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("¿Estás seguro de querer subir el dataset con estos datos?", reply_markup=reply_markup)
    
    return CONFIRMATION

async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global csrf_token
    query = update.callback_query
    await query.answer()
    
    if query.data == "confirm_upload":
        data = {
            "csrf_token": csrf_token,
            "title": context.user_data['title'],
            "desc": context.user_data['description'],
            "publication_type": str(context.user_data['publication_type']).replace("_", "").replace(" ","").lower(),
            "publication_doi": "",
            "tags": ','.join(context.user_data['tags']),
        }
        
        user_dir = os.path.join("media", str(update.effective_chat.id))
        file_list = os.listdir(user_dir)
        
        for i, file_name in enumerate(file_list):
            data[f"feature_models-{i}-uvl_filename"] = file_name
            data[f"feature_models-{i}-title"] = ''
            data[f"feature_models-{i}-desc"] = ''
            data[f"feature_models-{i}-publication_type"] = str(context.user_data['publication_type']).replace("_", "").replace(" ","").lower()
            data[f"feature_models-{i}-publication_doi"] = ''
            data[f"feature_models-{i}-tags"] = ','.join(context.user_data['tags'])
            data[f"feature_models-{i}-uvl_version"] = ''
        
        response = session.post(f"{BASE_URL}/dataset/upload", data=data)

        if response.status_code == 200:
            await query.edit_message_text("Dataset subido exitosamente a Uvlhub.")
        else:
            print(response.json())
            await query.edit_message_text(f"Error en la subida: {response.json().get('message', 'Error desconocido')}")
        
    elif query.data == "cancel_upload":
        await query.edit_message_text("Subida del dataset cancelada.")

    return ConversationHandler.END


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "media/prueba.uvl"
    
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_path, 'rb'))

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "/start - Inicia el bot.\n"
        "/login - Inicia sesión con tu correo y contraseña.\n"
        "/logout - Cierra sesión.\n"
        "/myDatasets - Muestra tus datasets.\n"
        "Para empezar con el proceso de subida, adjunta los archivos en formato .uvl y luego envía el comando /upload.\n"
        "/upload - Sube los archivos adjuntados a Uvlhub\n"
        "/test - Descarga un archivo .uvl de prueba.\n"
        "/cancel - Cancela el proceso de subida.\n"
        "/help - Muestra esta lista de comandos.\n"
        
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

async def handle_new_file_during_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="No entendí ese comando.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    login_handler = ConversationHandler(
        entry_points=[CommandHandler('login', login)],
        states={
            EMAIL: [MessageHandler(filters.TEXT, email)],
            PASSWORD: [MessageHandler(filters.TEXT, password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    document_handler=MessageHandler(filters.Document.ALL, handle_document)
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('upload', upload)],
    states={
        TITLE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, title),
            MessageHandler(filters.Document.ALL, handle_new_file_during_upload) 
        ],
        DESCRIPTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, description),
            MessageHandler(filters.Document.ALL, handle_new_file_during_upload)
        ],
        PUBLICATION_TYPE: [
            CallbackQueryHandler(publication_type),
            MessageHandler(filters.Document.ALL, handle_new_file_during_upload)
        ],
        DOI: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, doi),
            MessageHandler(filters.Document.ALL, handle_new_file_during_upload)
        ],
        TAGS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, tags),
            MessageHandler(filters.Document.ALL, handle_new_file_during_upload)
        ],
        CONFIRMATION: [
            CallbackQueryHandler(confirmation),
            MessageHandler(filters.Document.ALL, handle_new_file_during_upload)
            ],
        },
    fallbacks=[CommandHandler('cancel', cancel)],
    )
    logout_handler = CommandHandler('logout', logout)
    list_my_datasets_handler = CommandHandler('myDatasets', my_datasets)
    test_handler = CommandHandler('test', test)
    help_handler = CommandHandler('help', help)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(start_handler)
    application.add_handler(login_handler)
    application.add_handler(logout_handler)
    application.add_handler(document_handler)
    application.add_handler(list_my_datasets_handler)
    application.add_handler(conversation_handler)
    application.add_handler(test_handler)
    application.add_handler(help_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
