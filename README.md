# 📊 Análise de Dados - Chatbot Consultor Virtual

Projeto para análise de dados históricos de perguntas e respostas do chatbot consultor virtual de moedores de carne, usando Python e Pandas.

## 📋 Descrição

Este projeto tem como objetivo analisar as interações dos usuários com o chatbot consultor virtual, focando nas respostas fornecidas e nos produtos recomendados. A análise permite entender padrões de comportamento, preferências dos usuários e eficácia das recomendações do chatbot.

## 🚀 Tecnologias

- **Python 3.x**
- **Pandas** - Manipulação e análise de dados
- **NumPy** - Operações numéricas

## 📁 Estrutura do Projeto

```
ia-chatbot/
├── base-dados.csv          # Dados históricos de perguntas/respostas dos usuários
├── importar_dados.py       # Script principal de análise de dados
├── requirements.txt        # Dependências Python do projeto
├── README.md              # Documentação do projeto
├── .gitignore             # Arquivos ignorados pelo Git
└── venv/                  # Ambiente virtual Python (não versionado)
```

## 🔧 Instalação

### Clonar o Repositório

```bash
git clone https://github.com/Matheuschiqueto/ia-chatbot.git
cd ia-chatbot
```

### Configurar o Ambiente

1. Certifique-se de ter Python 3.x instalado

2. Crie um ambiente virtual (recomendado):
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 📊 Como Usar

### Importar e Visualizar os Dados

Execute o script principal:

```bash
python importar_dados.py
```

### O que o Script Faz

O script `importar_dados.py` realiza uma análise completa dos dados históricos:

1. ✅ **Importação dos Dados**: Carrega o arquivo `base-dados.csv` com encoding UTF-8
2. 📊 **Informações Básicas**: Exibe total de registros, colunas e estrutura do DataFrame
3. 🔍 **Primeiros Registros**: Mostra uma prévia dos dados (primeiros 5 registros)
4. 📦 **Análise de Produtos**: Calcula distribuição de produtos recomendados com percentuais
5. 📝 **Análise de Perguntas**: Detalha a distribuição de respostas para cada pergunta
6. 🔗 **Correlações**: Analisa relações entre respostas específicas e produtos escolhidos
7. 📊 **Resumo Geral**: Fornece estatísticas consolidadas dos dados

## 📝 Formato dos Dados

O arquivo `base-dados.csv` contém dados reais do chatbot de consultoria de moedores de carne:
- **Ordem**: Número de ordem do registro
- **Nome + Nº**: Identificação do usuário
- **11 Perguntas**: Sobre finalidade, quantidade, voltagem, tipo de carne, preferências, locksup, espaço, orçamento, etc.
- **Produto escolhido**: A recomendação final baseada nas respostas

### Estrutura:

| Ordem | Nome | Pergunta 1 | Pergunta 2 | ... | Produto escolhido |
|-------|------|-----------|-----------|-----|------------------|
| 1 | Paulo1 | Uso doméstico | De 2 até 10 kg | ... | Moedor de carne caf 114 total inox |

## 🎯 Funcionalidades

### ✅ Implementado
- ✅ Importação de dados CSV usando pandas
- ✅ Visualização de informações básicas do dataset
- ✅ Análise estatística descritiva
- ✅ Distribuição de produtos escolhidos com percentuais
- ✅ Análise detalhada de todas as perguntas e respostas
- ✅ Análise de correlações entre respostas e produtos
- ✅ Resumo geral dos dados
- ✅ Suporte para colunas com nomes personalizados

### 🔜 Melhorias Futuras
- 📈 Visualizações gráficas com matplotlib e seaborn
- 📊 Dashboard interativo para análise dos dados
- 📁 Suporte para múltiplos formatos de arquivo (Excel, JSON)
- 🔍 Análise de tendências temporais
- 📧 Exportação de relatórios em PDF/HTML
- 🔄 Integração com API do chatbot para análise em tempo real

## 📊 Análises Disponíveis

O script `importar_dados.py` fornece:

1. **Informações Básicas**
   - Total de registros
   - Total de colunas
   - Estrutura do DataFrame

2. **Primeiros Registros**
   - Visualização dos primeiros 5 registros

3. **Estatísticas Descritivas**
   - Contagens, frequências, valores únicos

4. **Análise de Máquinas**
   - Total de máquinas únicas
   - Distribuição de recomendações

5. **Análise de Perguntas**
   - Distribuição de respostas por pergunta
   - Padrões nas escolhas dos usuários
   - Percentuais de cada resposta

6. **Análise de Correlação**
   - Relação entre respostas específicas e produtos escolhidos
   - Padrões de recomendação baseados em combinações de respostas

7. **Resumo Geral**
   - Total de respostas analisadas
   - Número de perguntas e produtos
   - Produto mais recomendado

## 🐛 Solução de Problemas

### Erro: "Arquivo não encontrado"
**Solução**: Certifique-se de estar na pasta do projeto e que o arquivo `base-dados.csv` existe:
```bash
cd ia-chatbot
ls base-dados.csv
```

### Erro: "pandas não encontrado"
**Solução**: Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro de encoding
O arquivo CSV usa encoding UTF-8. Se houver problemas, verifique a codificação do arquivo.

## 📊 Exemplo de Saída

O script gera uma análise completa mostrando:
- Distribuição de todos os produtos escolhidos
- Análise detalhada de cada pergunta com percentuais
- Correlações entre as 3 primeiras perguntas e os produtos recomendados
- Resumo estatístico geral

## 📞 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👤 Autor

**Matheus Chiqueto**

- GitHub: [@Matheuschiqueto](https://github.com/Matheuschiqueto)

## 🔗 Projeto Relacionado

Este projeto faz parte do ecossistema do [Chatbot Consultor Virtual](https://github.com/Matheuschiqueto/consultor-virtual), fornecendo ferramentas de análise para os dados históricos do chatbot.

---
**Versão**: 1.1.0  
**Status**: 🟢 Funcional  
**Última atualização**: README atualizado para publicação no GitHub

