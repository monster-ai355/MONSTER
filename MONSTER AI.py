import os
import customtkinter as ctk
import time
import json
from PIL import Image, ImageTk
from tkinter import messagebox
import ollama

LOCALES = {
    "Türkçe": {
        "title_s1": "MONSTER - KURULUM",
        "title_s2": "MONSTER - GÜVENLİ GİRİŞ",
        "title_s3": "MONSTER - ANA SİSTEM",
        "identity": "GİRİŞ",
        "enter_name": "İsminizi Giriniz :",
        "next": "İleri",
        "error_s1": "Devam etmek için lütfen isminizi girin.",
        "login": "GİRİŞ",
        "email": "Kullanıcı Adı / E-posta :",
        "password": "Şifre :",
        "robot": "Robot değilim",
        "error_s2": "E-posta ve Şifre boş bırakılamaz.",
        "error_robot": "Lütfen robot olmadığınızı doğrulayın.",
        "signin": "Giriş Yap",
        "register": "Kayıt Ol",
        "register_title": "KAYIT PANELİ",
        "remember_me": "Beni Hatırla",
        "guest_btn": "Kayıt Olmadan Gir",
        "guest_warning": "Misafir Modu: En fazla 15 mesaj gönderebilirsin!",
        "guest_limit_exceeded": "Mesaj sınırına ulaştın! Devam etmek için giriş yapmalısın.",
        "invalid_email": "Geçersiz E-posta adresi (@outlook.com veya @gmail.com olmalı).",
        "invalid_login": "Geçersiz Kullanıcı Adı veya Şifre.",
        "not_registered": "Kayıt olunmadı."
    },
    "English": {
        "title_s1": "MONSTER - INITIALIZATION",
        "title_s2": "MONSTER - SECURE LOGIN",
        "title_s3": "MONSTER - CORE SYSTEM",
        "identity": "LOGIN",
        "enter_name": "Enter Your Name :",
        "next": "Next",
        "error_s1": "Please enter your name to proceed.",
        "login": "LOGIN",
        "email": "User Name / E-mail :",
        "password": "Password :",
        "robot": "I'm not a robot",
        "error_s2": "E-mail and Password cannot be empty.",
        "error_robot": "Please verify that you are not a robot.",
        "signin": "Sign in",
        "register": "Register",
        "register_title": "REGISTRATION",
        "remember_me": "Remember Me",
        "guest_btn": "Continue Without Registering",
        "guest_warning": "Guest Mode: You can send up to 15 messages!",
        "guest_limit_exceeded": "Message limit reached! You must log in to continue.",
        "invalid_email": "Invalid Email (@outlook.com or @gmail.com only).",
        "invalid_login": "Invalid Username or Password.",
        "not_registered": "Not registered."
    },
    "Deutsch": {
        "title_s1": "MONSTER - INITIALISIERUNG",
        "title_s2": "MONSTER - SICHERER LOGIN",
        "title_s3": "MONSTER - KERSYSTEM",
        "identity": "ANMELDUNG",
        "enter_name": "Geben Sie Ihren Namen ein :",
        "next": "Weiter",
        "error_s1": "Bitte geben Sie Ihren Namen ein, um fortzufahren.",
        "login": "ANMELDUNG",
        "email": "Benutzername / E-Mail :",
        "password": "Passwort :",
        "robot": "Ich bin kein Roboter",
        "error_s2": "E-Mail und Passwort dürfen nicht leer sein.",
        "error_robot": "Bitte bestätigen Sie, dass Sie kein Roboter sind.",
        "signin": "Einloggen",
        "register": "Registrieren",
        "register_title": "REGISTRIERUNG",
        "remember_me": "Merken",
        "guest_btn": "Ohne Registrierung fortfahren",
        "guest_warning": "Gastmodus: Sie können bis zu 15 Nachrichten senden!",
        "guest_limit_exceeded": "Nachrichtenlimit erreicht! Sie müssen sich anmelden.",
        "invalid_email": "Ungültige E-Mail (@outlook.com oder @gmail.com).",
        "invalid_login": "Ungültige E-Mail oder Passwort.",
        "not_registered": "Nicht registriert."
    },
    "Français": {
        "title_s1": "MONSTER - INITIALISATION",
        "title_s2": "MONSTER - CONNEXION SÉCURISÉE",
        "title_s3": "MONSTER - SYSTÈME CENTRAL",
        "identity": "CONNEXION",
        "enter_name": "Entrez Votre Nom :",
        "next": "Suivant",
        "error_s1": "Veuillez entrer votre nom pour continuer.",
        "login": "CONNEXION",
        "email": "Nom d'utilisateur / E-mail :",
        "password": "Mot de passe :",
        "robot": "Je ne suis pas un robot",
        "error_s2": "L'e-mail et le mot de passe ne peuvent pas être vides.",
        "error_robot": "Veuillez vérifier que vous n'êtes pas un robot.",
        "signin": "Se connecter",
        "register": "S'inscrire",
        "register_title": "INSCRIPTION",
        "remember_me": "Se souvenir de moi",
        "guest_btn": "Continuer sans s'inscrire",
        "guest_warning": "Mode invité : Vous pouvez envoyer jusqu'à 15 messages !",
        "guest_limit_exceeded": "Limite de messages atteinte ! Vous devez vous connecter.",
        "invalid_email": "E-mail invalide (@outlook.com ou @gmail.com uniquement).",
        "invalid_login": "E-mail ou mot de passe invalide.",
        "not_registered": "Pas inscrit."
    },
    "Español": {
        "title_s1": "MONSTER - INICIALIZACIÓN",
        "title_s2": "MONSTER - INICIO DE SESIÓN SEGURO",
        "title_s3": "MONSTER - SISTEMA CENTRAL",
        "identity": "ACCESO",
        "enter_name": "Ingrese Su Nombre :",
        "next": "Siguiente",
        "error_s1": "Por favor, ingrese su nombre para continuar.",
        "login": "ACCESO",
        "email": "Usuario / Correo electrónico :",
        "password": "Contraseña :",
        "robot": "No soy un robot",
        "error_s2": "El correo y la contraseña no kunnen estar vacíos.",
        "error_robot": "Por favor, verifique que no es un robot.",
        "signin": "Iniciar sesión",
        "register": "Registrarse",
        "register_title": "REGISTRO",
        "remember_me": "Recordarme",
        "guest_btn": "Continuar sin registrarse",
        "guest_warning": "Modo invitado: ¡Puedes enviar hasta 15 mensajes!",
        "guest_limit_exceeded": "¡Límite de mensajes alcanzado! Debes iniciar sesión.",
        "invalid_email": "Correo no válido (solo @outlook.com o @gmail.com).",
        "invalid_login": "Correo o contraseña no válidos.",
        "not_registered": "No registrado."
    },
    "Русский": {
        "title_s1": "MONSTER - ИНИЦИАЛИЗАЦИЯ",
        "title_s2": "MONSTER - БЕЗОПАСНЫЙ ВХОД",
        "title_s3": "MONSTER - ОСНОВНАЯ СИСТЕМА",
        "identity": "ВХОД",
        "enter_name": "Введите Ваше Имя :",
        "next": "Далее",
        "error_s1": "Пожалуйста, введите ваше имя, чтобы продолжить.",
        "login": "ВХОД",
        "email": "Имя пользователя / E-mail :",
        "password": "Пароль :",
        "robot": "Я не робот",
        "error_s2": "E-mail и пароль ne могут быть пустыми.",
        "error_robot": "Пожалуйста, подтвердите, что вы ne робот.",
        "signin": "Войти",
        "register": "Регистрация",
        "register_title": "REGISTRATION",
        "remember_me": "Запомнить меня",
        "invalid_email": "Неверный фомат (@outlook.com или @gmail.com).",
        "invalid_login": "Неверный e-mail или пароль.",
        "not_registered": "Не зарегистрирован."
    }
}

class MonsterAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.conversation_history = [
            {
                'role': 'system', 
                'content': (
                    "Doğru cevaplar ver. Samimi ol ve emojiler kullan. Ama çok sık emoji kullanma 1/20 kullan gibi. "
                    "Bana soru sorma sadece benim sorularıma cevap ver. "
                    "Saçmalamadan ve en fazla kısa kısa 2 öneride bulunabilirsin. "
                    "Çok uzun cevaplar vermeden arkadaş gibi konuş ve duygularını da yine 1/8 kelimede gibi ifade edebilirsin (konuya bağlı değişiklik gösterebilir)"
                    "Sana denmediği sürece asla 5 satırdan fazla yazı yazıp gönderme kısa kısa yaz sadece senden isteneni."
                )
            }
        ]

        self.geometry("1000x950")
        self.configure(fg_color="#0a0a0a")
        
        self.selected_lang = "Türkçe"
        self.saved_first_name = ""
        self.user_display_tag = ""
        self.current_screen = 1
        
        self.is_guest = False
        self.message_count = 0
        self.max_guest_messages = 15

        self.db_file = "registered_users.json"
        self.remember_file = "remembered_users.txt"
        self.registered_users = self.load_users_from_db()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.load_background_image()
        self.bind("<Configure>", self.resize_background)
        
        self.lang_menu = ctk.CTkOptionMenu(
            self, 
            values=list(LOCALES.keys()),
            command=self.change_language,
            fg_color="#181818",
            button_color="#2c3e50",
            button_hover_color="#3498db",
            font=("Consolas", 12)
        )
        self.lang_menu.place(relx=0.95, rely=0.03, anchor="ne")
        self.lang_menu.set("Türkçe")
        
        self.show_screen_1()

    def fix_i_character(self, event):
        widget = event.widget
        if hasattr(widget, "get"):
            current_text = widget.get()
            fixed_text = current_text
            replacements = {
                "þ": "ş", "Þ": "Ş",
                "ý": "ı", "Ý": "I",
                "ð": "ğ", "Ð": "Ğ",
                "ç": "ç", "Ç": "Ç",
                "ö": "ö", "Ö": "Ö",
                "ü": "ü", "Ü": "Ü"
            }
            for bad, good in replacements.items():
                fixed_text = fixed_text.replace(bad, good)
            if current_text != fixed_text:
                cursor_pos = widget.index("insert")
                widget.delete(0, "end")
                widget.insert(0, fixed_text)
                widget.icursor(cursor_pos)

    def load_background_image(self):
        self.bg_path = "matrix.png"
        if os.path.exists(self.bg_path):
            self.original_bg_img = Image.open(self.bg_path)
        else:
            self.original_bg_img = None

    def resize_background(self, event=None):
        if self.original_bg_img:
            w = self.winfo_width()
            h = self.winfo_height()
            resized_img = self.original_bg_img.resize((w, h), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_img)
            self.bg_label.configure(image=self.bg_image)

    def load_users_from_db(self):
        defaults = {
            "mustafaomerefe_24@outlook.com": "192837465Omer",
            "Admin123": "20150119"
        }
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    defaults.update(data)
            except:
                pass
        return defaults

    def save_users_to_db(self):
        savable = {k: v for k, v in self.registered_users.items() if k not in ["mustafaomerefe_24@outlook.com", "Admin123"]}
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(savable, f, ensure_ascii=False, indent=4)

    def change_language(self, choice):
        self.selected_lang = choice
        self.update_ui_text()

    def update_ui_text(self):
        ln = LOCALES[self.selected_lang]
        if self.current_screen == 1:
            self.title(ln["title_s1"])
            self.identity_lbl.configure(text=ln["identity"])
            self.enter_name_lbl.configure(text=ln["enter_name"])
            self.next_btn.configure(text=ln["next"])
            if hasattr(self, "screen1_error") and self.screen1_error.cget("text") != "":
                self.screen1_error.configure(text=ln["error_s1"])
        elif self.current_screen == 2:
            self.title(ln["title_s2"])
            self.login_lbl.configure(text=ln["login"])
            self.email_lbl.configure(text=ln["email"])
            self.pwd_lbl.configure(text=ln["password"])
            self.robot_check.configure(text=ln["robot"])
            self.signin_btn.configure(text=ln["signin"])
            self.reg_btn.configure(text=ln["register"])
            self.remember_check.configure(text=ln["remember_me"])
            if hasattr(self, "guest_btn"):
                self.guest_btn.configure(text=ln["guest_btn"])
        elif self.current_screen == 2.5:
            self.title(ln["register"])
            self.reg_panel_lbl.configure(text=ln["register_title"])
            self.reg_email_lbl.configure(text=ln["email"])
            self.reg_pwd_lbl.configure(text=ln["password"])
            self.reg_submit_btn.configure(text=ln["register"])
            self.reg_back_btn.configure(text=ln["next"])
        elif self.current_screen == 3:
            self.title(ln["title_s3"])

    def show_screen_1(self):
        self.current_screen = 1
        self.screen1_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.screen1_frame.place(relx=0.5, rely=0.5, anchor="center")

        content_box = ctk.CTkFrame(self.screen1_frame, fg_color="#080808", border_width=1, border_color="#1f2937", corner_radius=15)
        content_box.pack(padx=20, pady=20, fill="both", expand=True)

        self.identity_lbl = ctk.CTkLabel(content_box, text="", font=("Consolas", 64, "bold"), text_color="white")
        self.identity_lbl.pack(pady=(20, 40), padx=30)

        self.enter_name_lbl = ctk.CTkLabel(content_box, text="", font=("Segoe UI", 14), text_color="#aaaaaa", anchor="w")
        self.enter_name_lbl.pack(fill="x", padx=40)
        
        self.first_name_entry = ctk.CTkEntry(content_box, width=380, height=50, corner_radius=25, fg_color="#e0e0e0", text_color="black", font=("Segoe UI", 14))
        self.first_name_entry.pack(pady=(5, 20), padx=40)
        self.first_name_entry.bind("<KeyRelease>", self.fix_i_character)
        self.first_name_entry.bind("<Return>", lambda e: self.transition_to_screen_2())
        
        self.screen1_error = ctk.CTkLabel(content_box, text="", font=("Segoe UI", 12), text_color="#e74c3c")
        self.screen1_error.pack(pady=5)

        self.next_btn = ctk.CTkButton(content_box, text="", width=180, height=45, corner_radius=22, fg_color="#3498db", hover_color="#2980b9", font=("Segoe UI", 16, "bold"), command=self.transition_to_screen_2)
        self.next_btn.pack(pady=(10, 20))
        self.update_ui_text()

    def transition_to_screen_2(self):
        name = self.first_name_entry.get().strip()
        if not name:
            self.screen1_error.configure(text=LOCALES[self.selected_lang]["error_s1"])
            return
        self.saved_first_name = name
        self.screen1_frame.destroy()
        self.show_screen_2()

    def show_screen_2(self):
        self.current_screen = 2
        self.reg_btn = ctk.CTkButton(self, text="", width=100, height=30, fg_color="#1e3a8a", hover_color="#172554", font=("Segoe UI", 12, "bold"), command=self.show_register_screen)
        self.reg_btn.place(relx=0.05, rely=0.03, anchor="nw")
        
        self.screen2_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.screen2_frame.place(relx=0.5, rely=0.5, anchor="center")

        content_box = ctk.CTkFrame(self.screen2_frame, fg_color="#080808", border_width=1, border_color="#2c3e50", corner_radius=15)
        content_box.pack(padx=20, pady=20)

        self.login_lbl = ctk.CTkLabel(content_box, text="", font=("Consolas", 72, "bold"), text_color="white")
        self.login_lbl.pack(pady=(20, 20), padx=40)

        self.email_lbl = ctk.CTkLabel(content_box, text="", font=("Segoe UI", 14), text_color="#aaaaaa", anchor="w")
        self.email_lbl.pack(fill="x", padx=50)
        
        self.email_entry = ctk.CTkEntry(content_box, width=380, height=50, corner_radius=25, fg_color="#e0e0e0", text_color="black", font=("Segoe UI", 14))
        self.email_entry.pack(pady=(5, 0), padx=50)
        self.email_entry.bind("<KeyRelease>", lambda e: [self.fix_i_character(e), self.handle_autocomplete(e)])
        self.email_entry.bind("<Return>", lambda e: self.attempt_final_login())

        self.autocomplete_list = ctk.CTkScrollableFrame(content_box, width=360, height=0, fg_color="#181818", border_width=1, border_color="#2c3e50")
        self.autocomplete_list.pack(pady=(2, 10), padx=50)
        self.autocomplete_list.pack_forget()

        self.pwd_lbl = ctk.CTkLabel(content_box, text="", font=("Segoe UI", 14), text_color="#aaaaaa", anchor="w")
        self.pwd_lbl.pack(fill="x", padx=50, pady=(10, 0))
        
        pwd_group = ctk.CTkFrame(content_box, fg_color="transparent")
        pwd_group.pack(fill="x", padx=50, pady=(5, 10))
        
        self.pwd_entry = ctk.CTkEntry(pwd_group, height=50, corner_radius=25, fg_color="#e0e0e0", text_color="black", show="*", font=("Segoe UI", 14))
        self.pwd_entry.pack(side="left", fill="x", expand=True)
        self.pwd_entry.bind("<Return>", lambda e: self.attempt_final_login())
        self.pwd_entry.bind("<KeyRelease>", self.fix_i_character)
        
        self.pwd_toggle_btn = ctk.CTkButton(pwd_group, text="👁️", width=30, height=30, fg_color="#1c1c1c", hover_color="#2c3e50", corner_radius=15, font=("Segoe UI", 12), command=lambda: self.toggle_password_visibility(self.pwd_entry, self.pwd_toggle_btn))
        self.pwd_toggle_btn.pack(side="right", padx=(5, 0))

        self.remember_check = ctk.CTkCheckBox(content_box, text="", font=("Segoe UI", 12), text_color="white", fg_color="#3b82f6", hover_color="#2563eb")
        self.remember_check.pack(pady=5, anchor="w", padx=50)

        self.robot_check = ctk.CTkCheckBox(content_box, text="", font=("Segoe UI", 12), text_color="white", fg_color="#27ae60", hover_color="#2ecc71")
        self.robot_check.pack(pady=5, anchor="w", padx=50)

        self.screen2_error = ctk.CTkLabel(content_box, text="", font=("Segoe UI", 12), text_color="#e74c3c")
        self.screen2_error.pack(pady=5)

        self.signin_btn = ctk.CTkButton(content_box, text="", width=180, height=45, corner_radius=22, fg_color="#ff0000", hover_color="#cc0000", font=("Segoe UI", 16, "bold"), command=self.attempt_final_login)
        self.signin_btn.pack(pady=(10, 10))

        self.guest_btn = ctk.CTkButton(content_box, text="", width=200, height=40, corner_radius=20, fg_color="#27ae60", hover_color="#2ecc71", font=("Segoe UI", 13, "bold"), command=self.enter_as_guest)
        self.guest_btn.pack(pady=(5, 20))

        self.update_ui_text()

    def enter_as_guest(self):
        if not self.saved_first_name:
            self.saved_first_name = "Misafir"
        self.is_guest = True
        self.user_display_tag = f"GUEST: {self.saved_first_name.upper()}"
        self.screen2_frame.destroy()
        if hasattr(self, 'reg_btn') and self.reg_btn.winfo_exists():
            self.reg_btn.destroy()
        self.initialize_core_ui()

    def show_register_screen(self):
        self.current_screen = 2.5
        self.screen2_frame.destroy()
        self.reg_btn.destroy()
        
        self.reg_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.reg_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        content_box = ctk.CTkFrame(self.reg_frame, fg_color="#080808", border_width=1, border_color="#10b981", corner_radius=15)
        content_box.pack(padx=20, pady=20)
        
        self.reg_panel_lbl = ctk.CTkLabel(content_box, text="", font=("Consolas", 64, "bold"), text_color="white")
        self.reg_panel_lbl.pack(pady=(20, 40), padx=40)
        
        self.reg_email_lbl = ctk.CTkLabel(content_box, text="", font=("Segoe UI", 14), text_color="#e0e0e0", anchor="w")
        self.reg_email_lbl.pack(fill="x", padx=50)
        self.reg_email_entry = ctk.CTkEntry(content_box, width=380, height=50, corner_radius=25, fg_color="#e0e0e0", text_color="black", font=("Segoe UI", 14))
        self.reg_email_entry.pack(pady=(5, 20), padx=50)
        self.reg_email_entry.bind("<KeyRelease>", self.fix_i_character)
        self.reg_email_entry.bind("<Return>", lambda e: self.handle_registration())
        
        self.reg_pwd_lbl = ctk.CTkLabel(content_box, text="", font=("Segoe UI", 14), text_color="#e0e0e0", anchor="w")
        self.reg_pwd_lbl.pack(fill="x", padx=50)
        
        reg_pwd_group = ctk.CTkFrame(content_box, fg_color="transparent")
        reg_pwd_group.pack(fill="x", padx=50, pady=(5, 20))
        
        self.reg_pwd_entry = ctk.CTkEntry(reg_pwd_group, height=50, corner_radius=25, fg_color="#e0e0e0", text_color="black", show="*", font=("Segoe UI", 14))
        self.reg_pwd_entry.pack(side="left", fill="x", expand=True)
        self.reg_pwd_entry.bind("<KeyRelease>", self.fix_i_character)
        self.reg_pwd_entry.bind("<Return>", lambda e: self.handle_registration())
        
        self.reg_pwd_toggle_btn = ctk.CTkButton(reg_pwd_group, text="👁️", width=30, height=30, fg_color="#1c1c1c", hover_color="#2c3e50", corner_radius=15, font=("Segoe UI", 12), command=lambda: self.toggle_password_visibility(self.reg_pwd_entry, self.reg_pwd_toggle_btn))
        self.reg_pwd_toggle_btn.pack(side="right", padx=(5, 0))
        
        self.reg_error = ctk.CTkLabel(content_box, text="", font=("Segoe UI", 12), text_color="#f87171")
        self.reg_error.pack(pady=5)
        
        self.reg_submit_btn = ctk.CTkButton(content_box, text="", width=180, height=45, corner_radius=22, fg_color="#10b981", hover_color="#059669", font=("Segoe UI", 16, "bold"), command=self.handle_registration)
        self.reg_submit_btn.pack(pady=5)

        self.reg_back_btn = ctk.CTkButton(content_box, text="", width=100, height=35, corner_radius=15, fg_color="#4b5563", hover_color="#374151", font=("Segoe UI", 12), command=self.back_to_login)
        self.reg_back_btn.pack(pady=(5, 20))
        self.update_ui_text()

    def toggle_password_visibility(self, entry_widget, btn_widget):
        if entry_widget.cget("show") == "*":
            entry_widget.configure(show="")
            btn_widget.configure(text="🔒")
        else:
            entry_widget.configure(show="*")
            btn_widget.configure(text="👁️")

    def handle_registration(self):
        email = self.reg_email_entry.get().strip()
        pwd = self.reg_pwd_entry.get().strip()
        ln = LOCALES[self.selected_lang]
        if not email or not pwd:
            self.reg_error.configure(text=ln["error_s2"])
            return
        if not (email.endswith("@outlook.com") or email.endswith("@gmail.com")):
            self.reg_error.configure(text=ln["invalid_email"])
            return
        self.registered_users[email] = pwd
        self.save_users_to_db()
        self.back_to_login()

    def back_to_login(self):
        self.reg_frame.destroy()
        self.show_screen_2()

    def handle_autocomplete(self, event):
        val = self.email_entry.get().strip()
        for child in self.autocomplete_list.winfo_children():
            child.destroy()
        if not val:
            self.autocomplete_list.pack_forget()
            return
        saved_emails = []
        if os.path.exists(self.remember_file):
            with open(self.remember_file, "r") as f:
                saved_emails = [line.strip() for line in f.readlines() if line.strip()]
        matches = [m for m in saved_emails if m.lower().startswith(val.lower())]
        if matches:
            self.autocomplete_list.pack(pady=(2, 5), fill="x", padx=10)
            self.autocomplete_list.configure(height=min(len(matches) * 32, 95))
            for match in matches:
                btn = ctk.CTkButton(
                    self.autocomplete_list, 
                    text=match, 
                    fg_color="transparent", 
                    text_color="white", 
                    hover_color="#2c3e50", 
                    anchor="w",
                    height=28,
                    font=("Segoe UI", 12),
                    command=lambda m=match: self.select_autocomplete(m)
                )
                btn.pack(fill="x")
        else:
            self.autocomplete_list.pack_forget()

    def select_autocomplete(self, email):
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, email)
        self.autocomplete_list.pack_forget()

    def save_remembered_user(self, email):
        existing = []
        if os.path.exists(self.remember_file):
            with open(self.remember_file, "r") as f:
                existing = [line.strip() for line in f.readlines() if line.strip()]
        if email not in existing:
            existing.append(email)
            with open(self.remember_file, "w") as f:
                for e in existing:
                    f.write(e + "\n")

    def attempt_final_login(self):
        email = self.email_entry.get().strip()
        password = self.pwd_entry.get().strip()
        ln = LOCALES[self.selected_lang]

        if not email or not password:
            self.screen2_error.configure(text=ln["error_s2"])
            return
        if not self.robot_check.get():
            self.screen2_error.configure(text=ln["error_robot"])
            return

        isAdmin = (email == "mustafaomerefe_24@outlook.com" and password == "192837465Omer")
        isCustomAdmin = (email == "Admin123" and password == "20150119")

        if not isCustomAdmin and not isAdmin:
            if not (email.endswith("@outlook.com") or email.endswith("@gmail.com")):
                self.screen2_error.configure(text=ln["invalid_email"])
                return

        if not isAdmin and not isCustomAdmin and email not in self.registered_users:
            self.screen2_error.configure(text=ln["not_registered"])
            return

        if isAdmin or isCustomAdmin or (email in self.registered_users and self.registered_users[email] == password):
            if self.remember_check.get():
                self.save_remembered_user(email)
            if isAdmin or isCustomAdmin:
                self.user_display_tag = f"👑 {email.upper()}"
            else:
                self.user_display_tag = email
        else:
            self.screen2_error.configure(text=ln["invalid_login"])
            return

        self.is_guest = False
        self.screen2_frame.destroy()
        if hasattr(self, 'reg_btn') and self.reg_btn.winfo_exists():
            self.reg_btn.destroy()
        self.initialize_core_ui()

    def initialize_core_ui(self):
        self.current_screen = 3
        self.lang_menu.lift() 

        self.user_tag = ctk.CTkLabel(self, text=self.user_display_tag.upper(), font=("Consolas", 14, "bold"), text_color="#e74c3c" if "ADMIN" in self.user_display_tag else "#3498db")
        self.user_tag.place(relx=0.78, rely=0.03, anchor="ne")

        self.top_title = ctk.CTkLabel(self, text="MONSTER", font=("Consolas", 36, "bold"), text_color="#2ecc71")
        self.top_title.place(relx=0.5, rely=0.03, anchor="n")

        self.admin_users_menu = ctk.CTkOptionMenu(
            self,
            values=["Kullanıcılar v"],
            command=self.handle_admin_menu_click,
            fg_color="#181818",
            button_color="#c0392b",
            button_hover_color="#e74c3c",
            font=("Consolas", 12)
        )
        self.admin_users_menu.place(relx=0.05, rely=0.03, anchor="nw")
        
        if "ADMIN" in self.user_display_tag:
            self.refresh_admin_menu_list()
        else:
            self.admin_users_menu.configure(state="disabled")
            self.admin_users_menu.place_forget()

        self.chat_scroll = ctk.CTkScrollableFrame(self, fg_color="#080808", border_width=1, border_color="#2c3e50")
        self.chat_scroll.pack(fill="both", expand=True, padx=40, pady=(85, 10))

        if self.is_guest:
            ln = LOCALES[self.selected_lang]
            self.add_message_bubble(ln["guest_warning"], sender="monster")

        self.ctrl_frame = ctk.CTkFrame(self, fg_color="#181818", border_width=1, border_color="#2c3e50")
        self.ctrl_frame.pack(fill="x", padx=40, pady=20)
        
        self.entry = ctk.CTkEntry(self.ctrl_frame, height=50, text_color="white", fg_color="#0a0a0a")
        self.entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.entry.bind("<KeyRelease>", self.fix_i_character)
        self.entry.bind("<Return>", lambda e: self.send_logic())

        self.update_ui_text()

    def refresh_admin_menu_list(self):
        user_list = ["Kullanıcılar v"]
        for u_email in self.registered_users.keys():
            if u_email not in ["mustafaomerefe_24@outlook.com", "Admin123"]:
                user_list.append(u_email)
        self.admin_users_menu.configure(values=user_list)
        self.admin_users_menu.set("Kullanıcılar")

    def handle_admin_menu_click(self, choice):
        if choice == "Kullanıcılar":
            return
        confirm = messagebox.askyesno("Kullanıcıyı Sil", f"'{choice}' kullanıcısını kalıcı olarak silmek istiyor musunuz?")
        if confirm:
            if choice in self.registered_users:
                del self.registered_users[choice]
                self.save_users_to_db()
                self.refresh_admin_menu_list()
                messagebox.showinfo("Başarılı", f"{choice} başarıyla silindi.")
        else:
            self.admin_users_menu.set("Kullanıcılar")

    def process_ai(self, prompt, file_path=None):
        try:
            model_name = 'llava' if file_path else 'gemma3:4b'
            
            if file_path:
                self.conversation_history.append({'role': 'user', 'content': prompt if prompt else "Analyze, Sir.", 'images': [file_path]})
            else:
                self.conversation_history.append({'role': 'user', 'content': prompt})
            
            res = ollama.chat(model=model_name, messages=self.conversation_history)
            reply = res['message']['content']
            
            self.conversation_history.append({'role': 'assistant', 'content': reply})
            return reply
        except Exception as e: 
            return f"Sistem hatası: {str(e)}"

    def add_message_bubble(self, text, sender="user"):
        row_frame = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        row_frame.pack(fill="x", pady=8, padx=5)

        bubble = ctk.CTkFrame(row_frame, fg_color="#1a365d" if sender == "user" else "#4c1d95", corner_radius=15)
        bubble.pack(side="right" if sender == "user" else "left", anchor="e" if sender == "user" else "w")
            
        lbl = ctk.CTkLabel(bubble, text=text, font=("Segoe UI", 13), text_color="white", fg_color="transparent", wraplength=400, justify="left")
        lbl.pack(padx=15, pady=10)
        self.chat_scroll._parent_canvas.yview_moveto(1.0)

    def send_logic(self):
        msg = self.entry.get().strip()
        if not msg: return
        
        if self.is_guest:
            if self.message_count >= self.max_guest_messages:
                ln = LOCALES[self.selected_lang]
                messagebox.showwarning("Sınır Aşıldı", ln["guest_limit_exceeded"])
                return
            self.message_count += 1

        self.add_message_bubble(msg, sender="user")
        self.entry.delete(0, "end")
        
        # Yapay zekayı arka planda çalıştırıyoruz
        import threading
        threading.Thread(target=self.run_ai, args=(msg,), daemon=True).start()

    def run_ai(self, msg):
        response = self.process_ai(msg)
        self.after(0, lambda: self.add_message_bubble(response, sender="monster"))

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    app = MonsterAI()
    app.mainloop()