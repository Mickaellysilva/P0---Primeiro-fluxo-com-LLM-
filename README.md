# P0 - Primeiro Fluxo com LLM

Aplicação em linha de comando (CLI) desenvolvida em Python para interpretar ideias informais de conteúdo e gerar roteiros estruturados para vídeos curtos (Reels/TikTok) utilizando um Modelo de Linguagem Grande (LLM).

---

## 1. Definição do Problema

Uma pessoa que realiza **gestão de redes sociais e criação de conteúdo para negócios locais** precisa transformar **ideias brutas e anotações informais de clientes (mensagens curtas ou tópicos soltos)** em **um roteiro estruturado para vídeos curtos contendo Gancho, Desenvolvimento e Chamada para Ação (CTA)**, porque atualmente enfrenta **dificuldade e perda de tempo para organizar solicitações vagas em uma estrutura persuasiva pronta para gravação**.

### Público-Alvo
Social media managers freelancers, criadores de conteúdo e pequenos empreendedores que produzem vídeos curtos para divulgação local.

### Especificação de Entrada e Saída
* **Entrada:** Texto livre em linguagem natural contendo o tema, produto, serviço ou promoção desejada.
* **Saída:** Texto estruturado em três blocos objetivos: Gancho (primeiros 3 segundos), Desenvolvimento e Chamada para Ação (CTA).

### Por que o uso de um LLM é justificável?
A entrada é fornecida em linguagem natural desestruturada, com ampla variação de contexto, vocabulário e objetivo comercial. Regras fixas, templates estáticos ou expressões regulares não conseguem interpretar a intenção comercial de frases informais nem adaptar a abordagem criativa ao nicho de cada cliente.

---

## 2. Arquitetura e Decisões Técnicas

O projeto foi estruturado para manter responsabilidades isoladas, facilitando a manutenção, os testes automatizados e a segurança de credenciais:

```text
P0-Primeiro-fluxo-LLM/
├── src/
│   ├── __init__.py
│   ├── config.py        # Carregamento e validação de variáveis de ambiente e parâmetros
│   ├── cli.py           # Captura e validação da entrada textual e exibição da saída
│   ├── prompt.py        # Preparação da instrução de sistema e montagem da solicitação
│   ├── llm_service.py   # Comunicação com a API do LLM, timeout e tratamento de falhas
│   ├── parser.py        # Validação e limpeza da resposta retornada pelo modelo
│   ├── exceptions.py    # Exceções customizadas para mensagens de erro compreensíveis
│   ├── logger.py        # Registro técnico de execução sem exposição de dados sensíveis
│   └── main.py          # Orquestração do fluxo principal da aplicação
├── tests/
│   ├── test_unit.py     # Testes simulados (mocks) de validação, configuração e falhas
│   └── test_integration.py # Teste real com o provedor configurado
├── .env.example         # Modelo de variáveis de ambiente sem credenciais reais
├── .gitignore           # Exclusão de ambiente virtual, logs e arquivo .env
├── requirements.txt     # Dependências com versões fixadas
└── README.md            # Documentação do projeto
