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

API REST
--
/api/projects

/api/skills

/api/experiences

(GET, POST, PUT, DELETE)
