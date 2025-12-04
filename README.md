Portfolio Web 
--
Este é um projeto de portfólio pessoal feito com Flask, com um painel administrativo para gerenciar projetos, habilidades e experiências.
Os dados são armazenados em um banco SQLite, e toda a administração é feita por meio de uma API REST integrada ao painel.

Tecnologias
-
Python + Flask

Flask SQLAlchemy

HTML, CSS e JavaScript

SQLite

API REST (CRUD)
-
 Funcionalidades
Área pública

Exibe projetos, habilidades e experiências

Botão para baixar o currículo em PDF

Página totalmente dinâmica, alimentada pelo banco

Área administrativa (/admin)

CRUD de:
-
Projetos

Habilidades

Experiências

Salvamento via Fetch API (sem recarregar a página)

Interface dividida em abas

instalação e Execução
--
    Clone o repositório:

text
git clone https://github.com/APKOY/portifolio-profissional.git
cd portifolio-profissional

    Crie ambiente virtual e instale dependências:

text
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt

    Execute a aplicação:

text
flask run

API REST
--
/api/projects

/api/skills

/api/experiences

(GET, POST, PUT, DELETE)

licença
--
Este projeto está sob a licença MIT 

Contato
--
APKOY - alexsander.ribeiro.motta@gmail.com

Este portfólio foi desenvolvido como projeto acadêmico com base em um Project Model Canvas, focando em:

    Usabilidade para recrutadores e professores

    Design moderno e responsivo

    Funcionalidades práticas de gerenciamento

    Boas práticas de desenvolvimento web

    "Transformando ideias em projetos práticos, sempre focado em aprendizado contínuo e em criar soluções que façam sentido para pessoas de verdade."
