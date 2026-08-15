**Nota:** Este projeto foi desenvolvido seguindo o curso FastAPI Beyond CRUD (https://youtube.com/playlist?list=PLEt8Tae2spYnHy378vMlPH--87cfeh33P) de Ssali Jonathan (jod35 - https://github.com/jod35/fastapi-beyond-CRUD), como prática de construção de APIs REST robustas com FastAPI.

**🔗 Documentação interativa (Swagger):** [fastapi-beyond-crud-crrs.onrender.com/api/v1/docs](https://fastapi-beyond-crud-crrs.onrender.com/api/v1/docs)

Conta de teste para explorar endpoints autenticados sem passar pelo fluxo de verificação por e-mail (que usa uma caixa de testes/sandbox): `email: demo@example.com` / `senha: demo1234`

*Nota: por estar em um plano gratuito, a primeira requisição pode levar alguns segundos enquanto o serviço "acorda".*

_Sobre o projeto_

Bookly é uma API REST para um serviço de avaliações de livros, construída com FastAPI e SQLModel. O projeto inclui autenticação de usuários via JWT, tratamento de erros customizado, versionamento de API, testes automatizados, e documentação interativa automática via Swagger.

_Adaptação de infraestrutura_

O tutorial original usa Celery + Redis para tarefas em background. O serviço de deploy gratuito utilizado (Render) não oferecia suporte a worker deployment no plano gratuito, então precisei remover essa camada para viabilizar o deploy do projeto — adaptando o fluxo da aplicação para funcionar corretamente sem tarefas assíncronas em background.

_Funcionalidades_
- Cadastro, login e autenticação de usuários via JWT
- CRUD completo para livros e avaliações (reviews)
- Tratamento de exceções customizado (usuário não encontrado, credenciais inválidas, token inválido, etc.)
- Versionamento de API (/api/v1/...)
- Testes automatizados (pytest)
- Documentação interativa (Swagger/OpenAPI)
- Migrações de banco de dados com Alembic

_Tecnologias_
- Python, FastAPI, SQLModel
- PostgreSQL
- Alembic (migrações)
- Pytest (testes)
- Docker

_Como rodar localmente_
```bash
git clone [seu repositório]
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
fastapi dev src/
```

_Como rodar os testes_
```bash
pytest
```

---

**Note:** This project was built following Ssali Jonathan's (jod35 — https://github.com/jod35/fastapi-beyond-CRUD) FastAPI Beyond CRUD course (https://youtube.com/playlist?list=PLEt8Tae2spYnHy378vMlPH--87cfeh33P), as practice for building robust REST APIs with FastAPI.

**🔗 Interactive API docs (Swagger):** [fastapi-beyond-crud-crrs.onrender.com/api/v1/docs](https://fastapi-beyond-crud-crrs.onrender.com/api/v1/docs)

Demo account for exploring authenticated endpoints without going through the email verification flow (which uses a sandbox inbox): `email: demo@example.com` / `password: demo1234`

*Note: since this runs on a free tier, the first request may take a few seconds while the service "wakes up."*

_About the project_

Bookly is a REST API for a book review service, built with FastAPI and SQLModel. The project includes JWT-based user authentication, custom error handling, API versioning, automated tests, and automatic interactive documentation via Swagger.

_Infrastructure adaptation_

The original tutorial uses Celery + Redis for background tasks. The free deployment service used (Render) didn't support worker deployment on its free tier, so I removed that layer to make the project deployable — adapting the application flow to work correctly without background async tasks.

_Features_
- User signup, login, and JWT authentication
- Full CRUD for books and reviews
- Custom exception handling (user not found, invalid credentials, invalid token, etc.)
- API versioning (/api/v1/...)
- Automated tests (pytest)
- Interactive documentation (Swagger/OpenAPI)
- Database migrations with Alembic

_Technologies_
- Python, FastAPI, SQLModel
- PostgreSQL
- Alembic (migrations)
- Pytest (tests)
- Docker

_Running locally_
```bash
git clone [your repository]
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
fastapi dev src/
```

_Running tests_
```bash
pytest
```
