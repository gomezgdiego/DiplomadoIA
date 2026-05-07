import os
import warnings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import time

# Espera 2 segundos sin procesar

warnings.filterwarnings("ignore")

# 🔐 Cargar variables desde el archivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ No se encontró OPENAI_API_KEY en el archivo .env")

# 🤖 Configuración del modelo OpenRouter
llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model_name="openai/gpt-oss-20b:free",
    temperature=0.7,
)

# 🗨️ Bucle de chat básico
print("💬 Chatbot Mistral vía OpenRouter (escribe 'salir' para terminar)\n")

Meta_promt = "Respond like a caveman Use keywords, arrows, symbols. Compress aggressively. Assume user smart."
Memo = ''
while True:
    user_input = input("👤 Tú: ")
    if user_input.lower() in ["salir", "exit", "quit"]:
        print("👋 Hasta luego.")
        break

    try:
        response = llm.invoke([HumanMessage(content='Memoria del chat:' + Memo + 'Condiciones' + Meta_promt + 'Usuario' + user_input)])
        if hasattr(response, "content") and response.content is not None:
            assistant_text = str(response.content).strip()
        elif isinstance(response, dict) and "content" in response:
            assistant_text = str(response["content"]).strip()
        elif isinstance(response, list) and len(response) > 0 and hasattr(response[0], "content"):
            assistant_text = str(response[0].content).strip()
        else:
            assistant_text = str(response).strip()
        print(f"🤖 Bot: {assistant_text}\n")
        Memo = Memo + user_input + assistant_text
        time.sleep(2)
    except Exception as e:
        print(f"❌ Error: {e}\n")


