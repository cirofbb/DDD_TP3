import os
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import wikipedia

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*LangChain.*")

load_dotenv()

# Inicializando o modelo
try:
    llm = GoogleGenerativeAI(model="gemini-pro")
except Exception as e:
    print("Erro ao configurar o modelo LLM:", e)
    exit()

# Ferramenta para responder perguntas sobre reciclagem
#def responder_reciclagem(pergunta: str) -> str:
    #return "Essa é uma consulta especializada sobre reciclagem. Você pode reciclar materiais como plástico, vidro, papel e metal. Verifique as diretrizes locais para mais detalhes."
    

# Base de conhecimento sobre reciclagem
reciclagem_info = {
    "mercado da reciclagem": (
        "Os plásticos representam 17% de todos os resíduos que são processados pela cadeia da reciclagem e "
        "38% do valor comercializado pelos catadores de materiais recicláveis (FUNDAÇÃO HEINRICH BÖLL BRASIL, 2020).\n\n"
        "O Brasil ocupa a quarta posição entre os maiores produtores de resíduos plásticos do mundo, antecedido pelos "
        "Estados Unidos (70,8 milhões de toneladas), China (54,7 milhões de toneladas) e Índia (19,3 milhões de toneladas). "
        "Cada brasileiro gera cerca de um quilo de lixo plástico por semana, o que coloca o Brasil em segundo lugar em produção "
        "per capita de resíduos, atrás apenas dos Estados Unidos."
    ),
    "atuação dos municípios": (
        "Apenas 27,5% das cidades brasileiras oferecem serviço de coleta seletiva porta-a-porta, modelo operacional mais indicado "
        "para aumentar as taxas de reciclagem de RSU (resíduos sólidos urbanos).\n\n"
        "Somente 6,5% dos municípios têm relações formalizadas com as associações e cooperativas, considerando tanto contratos quanto convênios e termos de cooperação."
    ),
    "atuação dos catadores": (
        "9 em cada 10 kgs de embalagens recicladas chegam à indústria de reciclagem por meio do trabalho dos catadores.\n\n"
        "64% das unidades de triagem municipais são geridas por associações ou cooperativas de catadores.\n\n"
        "74% dos catadores associados em cooperativas têm escolaridade de até o ensino fundamental completo, e 2% concluíram o ensino superior."
    ),
    "parque industrial da reciclagem popular": (
        "A produtividade média por catador em 2022 foi de 0,95 ton/trabalhador/mês.\n\n"
        "A produtividade média por catador associado/cooperado é de 2,2 toneladas em organizações que possuem os equipamentos básicos "
        "e cerca de 1,0 tonelada/trabalhador/mês em organizações que atuam sem os equipamentos básicos, mesmo valor de 2022.\n\n"
        "No ano de 2022, a remuneração média dos catadores associados/cooperados foi de R$1.478,82, 22% acima do salário-mínimo vigente no Brasil à época."
    ),
    "taxas de recuperação": (
        "Foram gerados 81,8 milhões de toneladas de resíduos sólidos urbanos em 2021 no Brasil, pouco mais de 1% a menos do que em 2020, "
        "tendo sido coletado 76,1 milhões de toneladas, dos quais mais de 80% foram materiais reaproveitáveis e recicláveis.\n\n"
        "Entre 2021 foram relatados os seguintes índices de reciclagem de plástico pós-consumo no Brasil:\n"
        "- PET: 56,4%\n- PEAD: 29%\n- PP: 20,3%\n- PEBD: 10,6%\n- PS: 9,4%\n- PVC: 3%\n- Plásticos pós-consumo (média): 23,4%"
    ),
}

# Função para consultar o menu de informações
def consultar_infos_reciclagem(topico: str) -> str:
    topico = topico.lower()
    if topico in reciclagem_info:
        return reciclagem_info[topico]
    else:
        return (
            "Desculpe, não tenho informações sobre esse tópico. "
            "Tente: 'mercado da reciclagem', 'atuação dos municípios', 'atuação dos catadores', "
            "'parque industrial da reciclagem popular' ou 'taxas de recuperação'."
        )

def processar_pergunta(question: str) -> str:
    """
    Processa a pergunta, utilizando as ferramentas configuradas no agente.
    """
    try:
        # Tenta usar a ferramenta RecyclingInfo
        resposta_reciclagem = consultar_infos_reciclagem(question)
        if resposta_reciclagem:
            return resposta_reciclagem
        
        # Caso nenhuma resposta seja encontrada, tenta a WikipediaSearch
        resposta_wikipedia = buscar_definicao_wikipedia(question)
        if resposta_wikipedia:
            return resposta_wikipedia
        
        # Resposta padrão caso nenhuma ferramenta forneça informações
        return "Desculpe, não consegui encontrar informações sobre esse tópico. Tente reformular sua pergunta."
    
    except Exception as e:
        return f"Erro ao processar a pergunta: {str(e)}"

def buscar_definicao_wikipedia(termo: str) -> str:
    try:
        # Busca o resumo na Wikipédia
        resultado = wikipedia.summary(termo, sentences=2)
        return resultado
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Há muitas possibilidades para '{termo}'. Seja mais específico: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return f"Não foi possível encontrar informações sobre '{termo}' na Wikipédia."
    except Exception as e:
        return f"Ocorreu um erro ao buscar informações: {str(e)}"

# Inicializa o agente com a ferramenta personalizada
tools = [
    Tool(
        name="RecyclingInfo",
        func=consultar_infos_reciclagem,
        description=(
            "Oferece informações sobre reciclagem com base em um menu de tópicos pré-definidos. "
            "Exemplo de uso: 'Fale sobre o mercado da reciclagem' ou 'Quais são as taxas de recuperação?'"
        )
    ),
    Tool(
        name="WikipediaSearch",
        func=buscar_definicao_wikipedia,
        description=(
            "Busca definições e informações gerais sobre reciclagem e temas ambientais relacionados diretamente na Wikipédia. "
            "Exemplo de uso: 'O que é reciclagem?' ou 'Explique sobre sustentabilidade'."
    )
    )
]

# Memória da conversa
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Inicializando o agente
try:
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
        memory=memory
    )
except Exception as e:
    print("Erro ao inicializar o agente:", e)
    exit()

# Função principal para interagir com o modelo
def main():
    print("\nBem-vindo ao assistente! Pergunte qualquer coisa sobre reciclagem ou digite 'sair' para encerrar.")
    while True:
        question = input("\nVocê: ")
        if question.lower() in ["sair", "exit"]:
            print("Até logo!")
            break
        try:
            # Verifica se o LLM deve ser usado diretamente
            if any(topic in question.lower() for topic in ["mercado", "municípios", "catadores", "taxas"]):
                response = agent.run(question)
            else:
                response = llm(question)
            print(f"Assistente: {response}")
        except Exception as e:
            print(f"Erro: {str(e)}")

if __name__ == "__main__":
    main()
