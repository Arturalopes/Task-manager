# Agenda de Tarefas

Uma aplicação web para organizar tarefas em um calendário mensal.

O projeto foi desenvolvido com Python, Flask e SQLite. A ideia foi criar uma alternativa simples para acompanhar compromissos e atividades do dia a dia, permitindo visualizar tudo em um calendário e também gerenciar as tarefas em uma página separada.

## Funcionalidades

* Criar tarefas com título, descrição, data e horário
* Definir cores para cada tarefa
* Organizar tarefas por categoria
* Visualizar tarefas em um calendário mensal
* Navegar entre os meses
* Pesquisar tarefas
* Filtrar tarefas pendentes, concluídas, atrasadas e do dia atual
* Marcar tarefas como concluídas
* Excluir tarefas

## Tecnologias

* Python
* Flask
* SQLite
* HTML
* CSS

## Como executar

Instale o Flask:

```bash
pip install flask
```

Execute a aplicação:

```bash
python app.py
```

Depois abra o navegador em:

```txt
http://127.0.0.1:5000
```

## Estrutura

```txt
├── app.py
├── tasks.db
├── templates
│   ├── calendar.html
│   └── index.html
└── static
    └── style.css
```

## Melhorias futuras

* Edição de tarefas
* Visualização semanal
* Login de usuários
* Notificações
* Responsividade para dispositivos móveis

## Autor

Desenvolvido como projeto de estudo e portfólio.
