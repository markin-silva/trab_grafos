# Projeto de Logística com Grafos

Este projeto tem como objetivo modelar um problema de logística usando grafos e implementar várias métricas e algoritmos de análise de grafos. O foco é otimizar rotas e transportar bens de forma eficiente, baseado nas informações fornecidas em arquivos de instâncias.

## Setup Inicial

### Pré-requisitos

Antes de rodar o projeto, você precisa ter o seguinte instalado na sua máquina:

- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

### Passos para Configuração

1. **Clone o repositório**:
   Clone este repositório para sua máquina local usando o comando:
   ```bash
   git clone https://github.com/markin-silva/trab_grafos.git
   cd trab_grafos
   ```

2. **Crie e ative um ambiente virtual**
   Isso é necessário para contornar restrições de instalação em ambientes gerenciados (PEP 668)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências**:
   Se o projeto tiver um arquivo `requirements.txt`, você pode instalar as dependências com:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o projeto**:
   Abra o arquivo `visualizacao.ipynb` em seu Jupyter ou VSCode e execute célula a célula.
   - Ele carregará os dados a partir do arquivo `../data/mggdb_0.25_4.dat` (ou outro `.dat`, caso você deseje).
   - Em seguida, imprimirá as estatísticas calculadas.

### Autores

- Marcus Vinícius Alves Silva
- Ayron Sanfra Silva Marinho
