# ERP Oficina

Sistema web para gestão de oficinas mecânicas de motos.

O projeto permite controlar clientes, veículos, ordens de serviço e peças utilizadas em cada atendimento.

O objetivo é ajudar pequenas oficinas a organizarem seus serviços e manterem o histórico de manutenção dos veículos.

## Features (Funcionalidades)

- Cadastro de clientes
- Cadastro de veículos
- Cadastro de produtos
- Criação de ordens de serviço
- Cálculo automático do valor da ordem de serviço com base nos produtos adicionados

## Tech Stack (Tecnologias Utilizadas)

- Python
- Django
- SQLite
- Bootstrap 5
- Bootstrap Icons

## Run Locally

Clone the project

```bash
git clone https://github.com/Anailton10/erp_oficina.git
```

Go to the project directory

```bash
cd erp_oficina
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run database migrations

```bash
python manage.py migrate
```
### Database Seed (Dados iniciais)

O projeto possui comandos de seed para popular o banco com dados básicos (clientes, veículos e catálogo de produtos/serviços).

Run command for seed Database
``` bash
python manage.py seed
```

Start the server

```bash
python manage.py runserver
```
## Roadmap

- [x] Cadastro de clientes
- [x] Cadastro de veículos
- [x] Cadastro de produtos e serviços
- [x] Ordens de serviço completas
- [x] Controle de estoque
- [x] Geração de PDF da OS
- [x] Dashboard