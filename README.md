# ERP Oficina

Sistema web para gestão de oficinas mecânicas de motos.
O projeto permite controlar clientes, veículos, ordens de serviço e peças utilizadas em cada atendimento.

## Features

- Cadastro de clientes e veículos
- Cadastro de produtos e serviços
- Ordens de serviço com cálculo automático de valor
- Controle de estoque
- Geração de PDF da OS
- Dashboard

## Tech Stack

- Python / Django
- PostgreSQL
- Docker / Docker Compose
- Bootstrap 5

## Run Locally

```bash
git clone https://github.com/Anailton10/erp_oficina.git
cd erp_oficina
python -m venv venv
```

Ative o ambiente virtual:

```bash
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
cp .env_example .env
# edite o .env com suas credenciais
```

```bash
python manage.py migrate
python manage.py seed
python manage.py runserver
```

## Run with Docker

```bash
cp .env_example .env
# edite o .env e defina DB_HOST=erp_db
```

```bash
docker compose up -d
```

O container já executa `migrate`, `seed` e sobe o servidor automaticamente.

Acesse em `http://127.0.0.1:8000`

Para encerrar:

```bash
docker compose down
```

## Roadmap

- [x] Cadastro de clientes
- [x] Cadastro de veículos
- [x] Cadastro de produtos e serviços
- [x] Ordens de serviço completas
- [x] Controle de estoque
- [x] Geração de PDF da OS
- [x] Dashboard
