# 📦 Gerenciador de Estoque

Projeto desenvolvido com **FastAPI** para o gerenciamento de produtos em estoque. Com ele, é possível cadastrar, consultar e controlar entradas e saídas de produtos, garantindo um fluxo de inventário eficiente e organizado.

## 🚀 Como executar

Siga os passos abaixo para rodar o projeto localmente:

### 1. Clone o repositório

```bash
git clone https://github.com/luanfred/gerenciador-estoque.git
cd gerenciador-estoque
```

### 2. Criar o arquivo `.env`
Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis de ambiente:

```bash
DB_USER=seu_usuario_postgres
DB_PASSWORD=sua_senha_segura
DB_HOST=seu_host_ou_endpoint
DB_PORT=5432
DB_NAME=seu_banco_de_dados

JWT_SECRET=sua_chave_secreta
```
### 3. Executar o projeto

```bash
docker-compose up --build -d
```
### 4. Acessar a API
A API estará disponível em `http://localhost:8000`. Você pode acessar a documentação interativa da API através do Swagger em `http://localhost:8000/docs` ou do ReDoc em `http://localhost:8000/redoc`.
