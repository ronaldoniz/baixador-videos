import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import urllib.request
import json
from yt_dlp import YoutubeDL

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Baixador de Vídeos")
        self.root.geometry("500x280")
        self.root.resizable(False, False)
        
        self.create_widgets()

    def create_widgets(self):
        lbl_instrucao = tk.Label(self.root, text="Cole o link do vídeo abaixo:", font=("Arial", 11))
        lbl_instrucao.pack(pady=15)

        self.txt_url = tk.Entry(self.root, width=50, font=("Arial", 10))
        self.txt_url.pack(pady=5)
        self.txt_url.focus()

        self.btn_download = tk.Button(self.root, text="Baixar Vídeo (MP4)", command=self.start_download_thread, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=5, pady=5)
        self.btn_download.pack(pady=15)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        
        self.lbl_status = tk.Label(self.root, text="", font=("Arial", 9, "italic"))
        self.lbl_status.pack(pady=5)

        self.lbl_info = tk.Label(self.root, text="", font=("Arial", 10, "bold"), fg="#1a5f7a")
        self.lbl_info.pack(pady=2)

    def start_download_thread(self):
        url = self.txt_url.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Por favor, insira um link válido.")
            return

        self.btn_download.config(state="disabled")
        self.progress.pack(pady=5)
        self.progress['value'] = 0
        self.lbl_status.config(text="Processando informações do vídeo...")
        self.lbl_info.config(text="")

        thread = threading.Thread(target=self.process_download, args=(url,))
        thread.start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            
            if total > 0:
                percent = (downloaded / total) * 100
                self.root.after(0, self.update_progress_ui, percent)

            eta = d.get('eta')
            if eta is not None:
                minutes, seconds = divmod(eta, 60)
                eta_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
                self.root.after(0, self.update_eta_ui, eta_str)
            else:
                self.root.after(0, self.update_eta_ui, "Calculando...")

        elif d['status'] == 'finished':
            self.root.after(0, self.update_status_ui, "Download concluído! Salvando arquivo...")

    def update_progress_ui(self, percent):
        self.progress['value'] = percent

    def update_eta_ui(self, eta_str):
        percent_val = self.progress['value']
        self.lbl_info.config(text=f"Progresso: {percent_val:.1f}% | Tempo restante: {eta_str}")

    def update_status_ui(self, text):
        self.lbl_status.config(text=text)

    def download_tiktok_alternative(self, url, download_dir):
        api_url = f"https://www.tikwm.com/api/?url={url}"
        
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        if data.get('code') == 0:
            video_url = data['data']['play']
            title = data['data'].get('title', 'tiktok_video')
            clean_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            clean_title = clean_title[:50] if clean_title else "tiktok_video"
            
            output_path = os.path.join(download_dir, f"{clean_title}.mp4")
            
            self.root.after(0, self.update_status_ui, "Baixando vídeo do TikTok...")
            
            urllib.request.urlretrieve(video_url, output_path)
            self.root.after(0, self.download_success)
        else:
            raise Exception(data.get('msg', 'Erro desconhecido na API do TikTok'))

    def process_download(self, url):
        user_profile = os.environ.get("USERPROFILE") or os.environ.get("HOME")
        download_dir = os.path.join(user_profile, "Downloads")

        if "tiktok.com" in url:
            try:
                self.download_tiktok_alternative(url, download_dir)
            except Exception as e:
                self.root.after(0, self.download_error, f"Falha na API alternativa do TikTok: {str(e)}")
            return

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [self.progress_hook],
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.root.after(0, self.download_success)
        except Exception as e:
            self.root.after(0, self.download_error, str(e))

    def download_success(self):
        self.progress.pack_forget()
        self.btn_download.config(state="normal")
        self.lbl_status.config(text="")
        self.lbl_info.config(text="")
        self.txt_url.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Vídeo baixado com sucesso e salvo na sua pasta de Downloads!")

    def download_error(self, error_msg):
        self.progress.pack_forget()
        self.btn_download.config(state="normal")
        self.lbl_status.config(text="")
        self.lbl_info.config(text="")
        messagebox.showerror("Erro", f"Não foi possível baixar o vídeo.\nErro: {error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()