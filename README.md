**Nota:** Este projeto foi desenvolvido seguindo o curso FastAPI Beyond CRUD (https://youtube.com/playlist?list=PLEt8Tae2spYnHy378vMlPH--87cfeh33P) de Ssali Jonathan (jod35 - https://github.com/jod35/fastapi-beyond-CRUD), como prática de construção de APIs REST robustas com FastAPI.
_Sobre o projeto_
Bookly é uma API REST para um serviço de avaliações de livros, construída com FastAPI e SQLModel. O projeto inclui autenticação de usuários via JWT, tratamento de erros customizado, versionamento de API, testes automatizados, e documentação interativa automática via Swagger.

_Adaptação de infraestrutura_
O tutorial original usa Celery + Redis para tarefas em background. O serviço de deploy gratuito utilizado (Render) não oferecia suporte a worker deployment no plano gratuito, então precisei remover essa camada para viabilizar o deploy do projeto — adaptando o fluxo da aplicação para funcionar corretamente sem tarefas assíncronas em background

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
