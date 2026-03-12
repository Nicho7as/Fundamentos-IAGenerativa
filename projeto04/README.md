DESAFIO AULA 04 - Assistente com Memória (TechBuddy)
Este projeto consiste em um chatbot inteligente integrado à API da Groq, focado em persistência de dados, gerenciamento de contexto e execução de funções externas (Function Calling).

Como Executar
Instale as dependências necessárias:

pip install groq python-dotenv

Configure suas chaves:
No arquivo .env na raiz da pasta projeto04, adicione sua chave:

GROQ_API_KEY=sua_chave_gsk_aqui

Inicie o assistente:

python main.py


Funcionalidades Implementadas
Parte 1 - Controle de Memória: Implementação do comando /limpar que remove o histórico da sessão e apaga o arquivo físico de persistência.

Parte 2 - Persona do Assistente: Definição do assistente "TechBuddy", com tom educado, uso de emojis e foco técnico.

Parte 3 - Limite de Memória: Sistema que mantém apenas as últimas 10 mensagens (janela deslizante) para otimizar o uso de tokens e manter o foco.

Parte 4 - Integração de Funções (Tools):

gerar_senha: Cria senhas aleatórias seguras via Python.

converter_temperatura: Realiza conversões entre Celsius e Fahrenheit.

Parte 5 - Persistência de Dados: Uso de arquivo historico.json para que o bot carregue conversas anteriores automaticamente ao ser iniciado.

Reflexões e Dificuldades
Dificuldades Encontradas
Compatibilidade de APIs: A transição da biblioteca OpenAI para a Groq exigiu ajustes no cliente e na nomenclatura dos modelos, especialmente após a desativação de versões antigas do Llama.

Sincronização de Variáveis: Configurar o python-dotenv para garantir que a chave da API fosse lida corretamente sem expô-la no código fonte.

Reflexão Técnica
Se o histórico crescer muito, quais problemas podem ocorrer?
O custo de tokens aumenta drasticamente a cada interação. Além disso, o modelo pode sofrer com a "perda de foco" (context window limit), começando a alucinar ou ignorar as instruções iniciais da persona.

Por que algumas tarefas são melhores resolvidas por funções Python?
LLMs são modelos probabilísticos e frequentemente erram cálculos exatos ou geração de caracteres específicos (como senhas). O Python é determinístico e garante 100% de precisão em tarefas lógicas e matemáticas.

Quais riscos existem ao deixar o LLM tomar decisões sobre quando usar uma função?
O risco de execução indevida. Se o usuário usar uma linguagem ambígua, o LLM pode disparar uma função desnecessária ou com parâmetros errados, o que pode causar inconsistência nos dados do sistema.