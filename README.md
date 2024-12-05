# Definição do problema
Dúvidas gerais sobre reciclagem e separação de resíduos domésticos. O objetivo da aplicação é servir como um chat explicativo sobre o tema. O público-alvo é qualquer habitante de centros urbanos que gostaria de diminuir sua pegada ambiental e dar um destino mais eficiente e ambientalmente correto ao seu próprio lixo.

# Casos de uso
Interaja com o agente via terminal, para obter informações e/ou dados complementares sobre reciclagem. Como resultado, o agente busca correspondências nas ferramentas personalizadas para fornecer a resposta mais adequada.

# Reflexão sobre o trabalho do agente
O uso do agente no projeto, por meio do framework ReAct, transformou uma tarefa que seria lenta e trabalhosa em uma experiência ágil e eficiente, capaz de lidar com um grande número de interações de forma flexível e dinâmica. Em comparação com uma abordagem manual, o agente possibilita um raciocínio mais rápido, respostas mais precisas e expansão simples, além de proporcionar automação, que são essenciais para oferecer uma experiência de usuário robusta e escalável.

# Instruções
1. Clone o repositório
2. Instale as dependências: pip install -r requirements.txt
3. Execute a aplicação: streamlit run app.py

Requisitos
Antes de executar o código, certifique-se de que você possui os seguintes requisitos:

Python 3.11.9: O código foi desenvolvido e testado com esta versão do Python. Certifique-se de ter uma versão compatível instalada no seu ambiente.
Pacotes necessários: O código utiliza diversas bibliotecas Python que precisam ser instaladas para o funcionamento adequado. A lista de pacotes necessários inclui:
    - langchain: Framework para construção de agentes e integração com LLMs (Modelos de Linguagem).
    - langchain-google-genai: Integração com o Google Generative AI (para processamento do modelo).
    - wikipedia: Biblioteca para consulta à Wikipedia.
    - dotenv: Para carregar variáveis de ambiente de um arquivo .env.