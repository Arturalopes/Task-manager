from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date, datetime
import calendar

app = Flask(__name__)

DB_NAME = "tasks.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        task_date TEXT,
        task_time TEXT,
        color TEXT DEFAULT '#3b82f6',
        category TEXT,
        completed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ==========================
# CALENDÁRIO (PÁGINA INICIAL)
# ==========================

@app.route("/")
def calendar_view():

    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)

    now = datetime.now()

    if not month:
        month = now.month

    if not year:
        year = now.year

    conn = get_connection()
    cursor = conn.cursor()

    cal = calendar.monthcalendar(year, month)

    cursor.execute("""
        SELECT *
        FROM tasks
    """)

    tasks = cursor.fetchall()

    tasks_by_day = {}

    for task in tasks:

        if task["task_date"]:

            try:

                task_year, task_month, task_day = map(
                    int,
                    task["task_date"].split("-")
                )

                if (
                    task_year == year and
                    task_month == month
                ):

                    if task_day not in tasks_by_day:
                        tasks_by_day[task_day] = []

                    tasks_by_day[task_day].append(task)

            except:
                pass

    conn.close()

    prev_month = month - 1
    prev_year = year

    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    next_month = month + 1
    next_year = year

    if next_month == 13:
        next_month = 1
        next_year += 1

    return render_template(
        "calendar.html",
        calendar=cal,
        tasks_by_day=tasks_by_day,
        month_name=calendar.month_name[month],
        year=year,
        prev_month=prev_month,
        prev_year=prev_year,
        next_month=next_month,
        next_year=next_year
    )


# ==========================
# GERENCIADOR DE TAREFAS
# ==========================

@app.route("/tasks")
def index():

    filter_type = request.args.get("filter", "all")

    conn = get_connection()
    cursor = conn.cursor()

    today = date.today().isoformat()

    if filter_type == "pending":

        cursor.execute("""
            SELECT *
            FROM tasks
            WHERE completed = 0
            ORDER BY task_date
        """)

    elif filter_type == "completed":

        cursor.execute("""
            SELECT *
            FROM tasks
            WHERE completed = 1
            ORDER BY task_date DESC
        """)

    elif filter_type == "overdue":

        cursor.execute("""
            SELECT *
            FROM tasks
            WHERE task_date < ?
            AND completed = 0
            ORDER BY task_date
        """, (today,))

    elif filter_type == "today":

        cursor.execute("""
            SELECT *
            FROM tasks
            WHERE task_date = ?
            ORDER BY task_time
        """, (today,))

    else:

        cursor.execute("""
            SELECT *
            FROM tasks
            ORDER BY
            CASE
                WHEN task_date IS NULL THEN 1
                ELSE 0
            END,
            task_date,
            task_time
        """)

    tasks = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
    """)
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE completed = 0
    """)
    pending = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE completed = 1
    """)
    completed = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        pending=pending,
        completed=completed,
        filter_type=filter_type
    )


# ==========================
# ADICIONAR TAREFA
# ==========================

@app.route("/add", methods=["POST"])
def add_task():

    title = request.form.get("title")
    description = request.form.get("description")
    task_date = request.form.get("date")
    task_time = request.form.get("time")
    color = request.form.get("color")
    category = request.form.get("category")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (
            title,
            description,
            task_date,
            task_time,
            color,
            category
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        task_date,
        task_time,
        color,
        category
    ))

    conn.commit()
    conn.close()

    return redirect("/tasks")


# ==========================
# CONCLUIR
# ==========================

@app.route("/complete/<int:task_id>")
def complete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = 1
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

    return redirect("/tasks")


# ==========================
# REABRIR
# ==========================

@app.route("/undo/<int:task_id>")
def undo_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = 0
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

    return redirect("/tasks")


# ==========================
# EXCLUIR
# ==========================

@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE
        FROM tasks
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

    return redirect("/tasks")


if __name__ == "__main__":
    app.run(debug=True)