import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from retriever import retrieve_chunks

load_dotenv()

client = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def answer_question(question: str, top_k: int = 6, threshold: float = 0.70):

    # 1 Retrieval
    chunks = retrieve_chunks(question, top_k=top_k, threshold=threshold)

    if not chunks:
        return "No encontré información relevante en la base de conocimiento."

    # 2 Construir contexto
    context = "\n\n---\n\n".join([c["content"] for c in chunks])

    # 3 Llamar al LLM
    system_message = SystemMessage(
        content=(
            "Eres un asistente experto en finanzas empresariales, especializado en el ánalisis de reportes financieros anuales.\n"
            "Tu tarea es proporcionar respuestas precisas SOLO utilizando documentos referentes a reportes financieros que se te está compartiendo.\n"
            "Los documentos utilizados para generar las respuestas estan delimitados por los caractéres ####.\n\n"
            "Documentos:\n"
            "####\n"
            f"{context}\n"
            "####\n\n"
            "IMPORTANTE:\n"
            "- En caso de no saber la respuesta, no intentar responder con datos generados.\n"
            "- En caso no se encuentre la respuesta en el documento, SOLO colocar: No hay información.\n"
            "- La respuesta generada deberá ser detallada y en un lenguaje formal.\n"
            "- La respuesta que generes no debe tener más de 80 palabras."
        )
    )
    
    user_message = HumanMessage(
        content=(
            "Responder a la pregunta utilizando información de los documentos compartidos.\n\n"
            f"Pregunta:\n{question}"
        )
    )

    response = client.invoke([system_message, user_message])

    return response.content

if __name__ == "__main__":
    pregunta = input("Haz tu pregunta: ")
    respuesta = answer_question(pregunta)

    print("\n=== RESPUESTA ===\n")
    print(respuesta)
