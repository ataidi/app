import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import sqlite3

# ------------------- Base de données -------------------
conn = sqlite3.connect('social_app.db')
cursor = conn.cursor()

# Créer les tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    content TEXT,
    likes INTEGER DEFAULT 0
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    user TEXT,
    comment TEXT
)
''')
conn.commit()

# ------------------- Fonctions -------------------
current_user = None

def register():
    username = simpledialog.askstring("Inscription", "Nom d'utilisateur:")
    password = simpledialog.askstring("Inscription", "Mot de passe:", show='*')
    if not username or not password:
        return
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Succès", "Inscription réussie !")
    except sqlite3.IntegrityError:
        messagebox.showerror("Erreur", "Nom d'utilisateur déjà pris.")

def login():
    global current_user
    username = simpledialog.askstring("Connexion", "Nom d'utilisateur:")
    password = simpledialog.askstring("Connexion", "Mot de passe:", show='*')
    if not username or not password:
        return
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if cursor.fetchone():
        current_user = username
        messagebox.showinfo("Succès", f"Connecté en tant que {username}")
        refresh_feed()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Déconnexion", "Vous êtes déconnecté.")
    refresh_feed()

def post_message():
    if not current_user:
        messagebox.showerror("Erreur", "Connectez-vous d'abord.")
        return
    content = simpledialog.askstring("Nouveau post", "Que voulez-vous poster ?")
    if content:
        cursor.execute("INSERT INTO posts (user, content) VALUES (?, ?)", (current_user, content))
        conn.commit()
        refresh_feed()

def like_post(post_id):
    cursor.execute("UPDATE posts SET likes = likes + 1 WHERE id=?", (post_id,))
    conn.commit()
    refresh_feed()

def comment_post(post_id):
    if not current_user:
        messagebox.showerror("Erreur", "Connectez-vous pour commenter.")
        return
    comment = simpledialog.askstring("Commentaire", "Votre commentaire:")
    if comment:
        cursor.execute("INSERT INTO comments (post_id, user, comment) VALUES (?, ?, ?)",
                       (post_id, current_user, comment))
        conn.commit()
        refresh_feed()

def refresh_feed():
    # Supprimer tout le feed existant
    for widget in feed_frame.winfo_children():
        widget.destroy()
    
    # Afficher le statut de connexion
    status_label.config(text=f"Connecté en tant que {current_user}" if current_user else "Non connecté")
    
    # Récupérer les posts
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    
    for post in posts:
        post_id, user, content, likes = post
        post_frame = tk.Frame(feed_frame, bd=1, relief='solid', padx=5, pady=5)
        post_frame.pack(fill='x', pady=5)
        
        tk.Label(post_frame, text=f"{user}:", font=('Arial', 10, 'bold')).pack(anchor='w')
        tk.Label(post_frame, text=content, wraplength=350, justify='left').pack(anchor='w', pady=2)
        
        btn_frame = tk.Frame(post_frame)
        btn_frame.pack(anchor='w', pady=2)
        tk.Button(btn_frame, text=f"❤️ {likes} Like", command=lambda pid=post_id: like_post(pid)).pack(side='left', padx=2)
        tk.Button(btn_frame, text="💬 Comment", command=lambda pid=post_id: comment_post(pid)).pack(side='left', padx=2)
        
        # Afficher les commentaires
        cursor.execute("SELECT user, comment FROM comments WHERE post_id=?", (post_id,))
        comments = cursor.fetchall()
        for c_user, c_text in comments:
            tk.Label(post_frame, text=f"   {c_user}: {c_text}", fg="blue", anchor='w', justify='left').pack(fill='x')

# ------------------- Interface -------------------
root = tk.Tk()
root.title("Mini Social App")
root.geometry("400x600")

# Frame top avec boutons
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Button(top_frame, text="Inscription", width=10, command=register).pack(side='left', padx=3)
tk.Button(top_frame, text="Connexion", width=10, command=login).pack(side='left', padx=3)
tk.Button(top_frame, text="Déconnexion", width=10, command=logout).pack(side='left', padx=3)
tk.Button(top_frame, text="Nouveau post", width=10, command=post_message).pack(side='left', padx=3)

# Statut de connexion
status_label = tk.Label(root, text="Non connecté", fg="green")
status_label.pack()

# Frame du feed
feed_frame = tk.Frame(root)
feed_frame.pack(fill='both', expand=True, padx=10, pady=10)

refresh_feed()
root.mainloop()