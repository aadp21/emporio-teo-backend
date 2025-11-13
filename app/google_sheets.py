# app/google_sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from tkinter import messagebox

ARCHIVO_SHEETS = "Inventario_Emporio_Teo"  # Archivo principal en tu Google Drive

# ========================================
# Conexión a Google Sheets
# ========================================
def conectar_google_sheets():
    """
    Conecta a Google Sheets usando la cuenta de servicio y devuelve el cliente.
    """
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        print("✅ Conexión establecida con Google API")
        return client
    except Exception as e:
        print(f"❌ Error al conectar a Google Sheets: {e}")
        # si estás en entorno consola y no quieres ventanas, puedes comentar esta línea:
        # messagebox.showerror("Error", f"No se pudo conectar a Google Sheets:\n{e}")
        return None

# ========================================
# Abrir hoja específica dentro del archivo
# ========================================
def abrir_hoja(nombre_hoja):
    """
    Abre una hoja específica dentro del archivo principal.
    """
    client = conectar_google_sheets()
    if client is None:
        return None

    try:
        archivo = client.open(ARCHIVO_SHEETS)
        sheet = archivo.worksheet(nombre_hoja)
        print(f"📄 Hoja '{nombre_hoja}' abierta correctamente.")
        return sheet
    except gspread.WorksheetNotFound:
        print(f"❌ La hoja '{nombre_hoja}' no se encontró dentro del archivo '{ARCHIVO_SHEETS}'.")
        # messagebox.showerror("Error", f"La hoja '{nombre_hoja}' no se encontró...")
        return None
    except gspread.SpreadsheetNotFound:
        print(f"❌ El archivo '{ARCHIVO_SHEETS}' no se encontró en tu Google Drive.")
        # messagebox.showerror("Error", f"El archivo '{ARCHIVO_SHEETS}' no se encontró...")
        return None


