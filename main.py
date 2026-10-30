import datetime
import os
import tkinter as tk
from tkinter import messagebox

NOTES_DIR = "./my_notes"
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)


def check_password():
    entered_password = entry_pass.get().strip()
    if entered_password == "201610":
        frame_login.pack_forget()
        frame_notebook.pack(fill=tk.BOTH, expand=True)
        refresh_list()
    else:
        messagebox.showerror("Ошибка", "Неверный код доступа!")
        entry_pass.delete(0, tk.END)


def save_note():
    title = entry_title.get().strip()
    new_text = text_content.get("1.0", tk.END).strip()

    if not title:
        messagebox.showwarning("Ошибка", "Введите название заметки!")
        return

    if not new_text:
        messagebox.showwarning("Ошибка", "Текст заметки пуст!")
        return

    filename = os.path.join(NOTES_DIR, f"{title}.txt")
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    old_content = ""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            old_content = f.read()

    if old_content:
        full_content = (
            f"{old_content}\n\n=== Изменение: {now} ===\n{new_text}"
        )
    else:
        full_content = f"=== Создано: {now} ===\n{new_text}"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_content)
        messagebox.showinfo("Успех", f"Заметка '{title}' обновлена!")
        refresh_list()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")


def load_note(event=None):
    try:
        selected_index = listbox_notes.curselection()
        if not selected_index:
            return
        selected_title = listbox_notes.get(selected_index)

        filename = os.path.join(NOTES_DIR, f"{selected_title}.txt")
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        entry_title.delete(0, tk.END)
        entry_title.insert(0, selected_title)

        text_content.delete("1.0", tk.END)
        if "=== Изменение:" in content:
            parts = content.split("=== Изменение:")
            last_part = parts[-1]
            actual_text = last_part.split("===\n", 1)[1].strip()
            text_content.insert("1.0", actual_text)
        elif "=== Создано:" in content:
            actual_text = content.split("===\n", 1)[1].strip()
            text_content.insert("1.0", actual_text)
        else:
            text_content.insert("1.0", content)
    except Exception as e:
        pass


def show_history():
    title = entry_title.get().strip()
    if not title:
        messagebox.showwarning("Ошибка", "Сначала выберите заметку!")
        return

    filename = os.path.join(NOTES_DIR, f"{title}.txt")
    if not os.path.exists(filename):
        messagebox.showwarning("Ошибка", "Файл заметки не найден!")
        return

    with open(filename, "r", encoding="utf-8") as f:
        full_history = f.read()

    history_win = tk.Toplevel(root)
    history_win.title(f"История: {title}")
    history_win.geometry("400x500")
    history_win.configure(bg="#1e1e1e")

    txt_hist = tk.Text(history_win, font=FONT_MAIN, bg="#2d2d2d", fg="white")
    txt_hist.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    txt_hist.insert("1.0", full_history)
    txt_hist.config(state=tk.DISABLED)


def delete_note():
    try:
        selected_index = listbox_notes.curselection()
        if not selected_index:
            messagebox.showwarning("Ошибка", "Выберите заметку для удаления!")
            return
        selected_title = listbox_notes.get(selected_index)

        if messagebox.askyesno("Удаление", f"Удалить '{selected_title}'?"):
            filename = os.path.join(NOTES_DIR, f"{selected_title}.txt")
            if os.path.exists(filename):
                os.remove(filename)

            entry_title.delete(0, tk.END)
            text_content.delete("1.0", tk.END)
            refresh_list()
    except Exception as e:
        pass


def refresh_list():
    listbox_notes.delete(0, tk.END)
    files = []
    for file in os.listdir(NOTES_DIR):
        if file.endswith(".txt"):
            path = os.path.join(NOTES_DIR, file)
            files.append((file, os.path.getmtime(path)))

    files.sort(key=lambda x: x[1], reverse=True)

    for file, mtime in files:
        listbox_notes.insert(tk.END, file[:-4])


def clear_fields():
    entry_title.delete(0, tk.END)
    text_content.delete("1.0", tk.END)
    listbox_notes.selection_clear(0, tk.END)


root = tk.Tk()
root.title("Секретный Блокнот")
root.geometry("450x800")
root.configure(bg="#1e1e1e")

FONT_MAIN = ("Arial", 14)
FONT_BOLD = ("Arial", 14, "bold")

frame_login = tk.Frame(root, bg="#1e1e1e")
frame_login.pack(fill=tk.BOTH, expand=True)

lbl_login = tk.Label(
    frame_login,
    text="ВВЕДИТЕ КОД ДОСТУПА",
    bg="#1e1e1e",
    fg="white",
    font=FONT_BOLD,
)
lbl_login.pack(pady=(200, 15))

entry_pass = tk.Entry(
    frame_login,
    font=("Arial", 18),
    bg="#2d2d2d",
    fg="white",
    justify="center",
    show="*",
)
entry_pass.pack(padx=40, pady=10, fill=tk.X)

btn_login = tk.Button(
    frame_login,
    text="ВОЙТИ",
    font=FONT_BOLD,
    bg="#007acc",
    fg="white",
    command=check_password,
    height=2,
)
btn_login.pack(padx=40, pady=20, fill=tk.X)

frame_notebook = tk.Frame(root, bg="#1e1e1e")

lbl_title = tk.Label(
    frame_notebook,
    text="Название заметки:",
    bg="#1e1e1e",
    fg="white",
    font=FONT_BOLD,
)
lbl_title.pack(pady=(10, 2))

entry_title = tk.Entry(
    frame_notebook, font=FONT_MAIN, bg="#2d2d2d", fg="white", insertbackground="white"
)
entry_title.pack(fill=tk.X, padx=15, pady=5)

lbl_content = tk.Label(
    frame_notebook, text="Текст:", bg="#1e1e1e", fg="white", font=FONT_BOLD
)
lbl_content.pack(pady=(5, 2))

text_content = tk.Text(
    frame_notebook,
    font=FONT_MAIN,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white",
    height=8,
)
text_content.pack(fill=tk.X, padx=15, pady=5)

frame_btns1 = tk.Frame(frame_notebook, bg="#1e1e1e")
frame_btns1.pack(fill=tk.X, padx=15, pady=4)

btn_save = tk.Button(
    frame_btns1,
    text="Новая",
    font=FONT_BOLD,
    bg="#007acc",
    fg="white",
    command=clear_fields,
    height=2,
)
btn_save.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

btn_update = tk.Button(
    frame_btns1,
    text="Сохранить / Изменить",
    font=FONT_BOLD,
    bg="#2ea44f",
    fg="white",
    command=save_note,
    height=2,
)
btn_update.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

frame_btns2 = tk.Frame(frame_notebook, bg="#1e1e1e")
frame_btns2.pack(fill=tk.X, padx=15, pady=4)

btn_history = tk.Button(
    frame_btns2,
    text="Показать историю",
    font=FONT_BOLD,
    bg="#ff9800",
    fg="white",
    command=show_history,
    height=2,
)
btn_history.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

btn_delete = tk.Button(
    frame_btns2,
    text="Удалить заметку",
    font=FONT_BOLD,
    bg="#cb2431",
    fg="white",
    command=delete_note,
    height=2,
)
btn_delete.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

lbl_list = tk.Label(
    frame_notebook,
    text="Ваши заметки (нажмите для открытия):",
    bg="#1e1e1e",
    fg="white",
    font=FONT_BOLD,
)
lbl_list.pack(pady=(10, 2))

frame_list = tk.Frame(frame_notebook, bg="#1e1e1e")
frame_list.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_notes = tk.Listbox(
    frame_list,
    font=FONT_MAIN,
    bg="#2d2d2d",
    fg="white",
    height=5,
    yscrollcommand=scrollbar.set,
    selectbackground="#007acc",
)
listbox_notes.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
scrollbar.config(command=listbox_notes.yview)

listbox_notes.bind("<<ListboxSelect>>", load_note)

root.mainloop()
