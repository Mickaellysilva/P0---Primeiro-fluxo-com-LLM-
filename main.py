import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("LLM_API_KEY")

client = genai.Client(api_key=api_key)

ideia = input("Digite a ideia do post ou video curto: ")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=(
        "Transforme a ideia abaixo em um roteiro curto para Reels/TikTok "
        "contendo: Gancho (3s iniciais), Desenvolvimento e Chamada para Acao (CTA).\n\n"
        f"Ideia: {ideia}"
    ),
)

print("\n--- ROTEIRO GERADO ---\n")
print(response.text)