"""
DuplicateFinder - Tool for finding and removing duplicate files between folders
Developed for FiveM/RedM - Extensions: .ycd, .ydr, .ytyp, .ybn

Author: Victor Z
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from collections import defaultdict
import threading

# Install send2trash if not exists
try:
    from send2trash import send2trash
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "send2trash", "-q"])
    from send2trash import send2trash


# ===== INTERNATIONALIZATION =====
TRANSLATIONS = {
    'en': {
        'title': '🔍 DuplicateFinder - Duplicate File Checker',
        'main_title': '🔍 DuplicateFinder',
        'subtitle': 'Find and remove duplicate files between two folders',
        'folder_selection': '📁 Folder Selection',
        'folder_1': 'Folder 1:',
        'folder_2': 'Folder 2:',
        'select': '📂 Select',
        'settings': '⚙️ Settings',
        'extensions': 'Extensions:',
        'ext_ycd': '.ycd (Animations)',
        'ext_ydr': '.ydr (Models)',
        'ext_ytyp': '.ytyp (Types)',
        'ext_ybn': '.ybn (Collisions)',
        'delete_from': 'Delete duplicates from:',
        'scan_btn': '🔍 Scan for Duplicates',
        'delete_btn': '🗑️ Move to Recycle Bin',
        'clear_btn': '🔄 Clear',
        'status_ready': 'Ready to scan...',
        'status_scanning': '⏳ Scanning...',
        'status_complete': 'Scan complete!',
        'status_deleting': '🗑️ Moving to recycle bin...',
        'results': '📋 Results',
        'col_filename': 'Filename',
        'col_path1': 'Folder 1 Path',
        'col_path2': 'Folder 2 Path',
        'col_size': 'Size',
        'summary_found': '📊 Found {count} duplicate file(s) | Total: {size}',
        'summary_none': '✅ No duplicate files found!',
        'warn_select_folders': 'Please select both folders before scanning!',
        'err_folder1_not_found': 'Folder 1 not found:\n{path}',
        'err_folder2_not_found': 'Folder 2 not found:\n{path}',
        'warn_select_extension': 'Please select at least one extension!',
        'info_no_duplicates': 'No duplicates to remove!',
        'confirm_delete_title': 'Confirm Deletion',
        'confirm_delete_msg': 'Move {count} file(s) from {folder} to Recycle Bin?\n\nFiles can be recovered from Windows Recycle Bin.',
        'complete_title': 'Complete',
        'complete_msg': '✅ Files moved to recycle bin: {success}\n❌ Errors: {errors}\n\nFiles can be restored from Windows Recycle Bin.',
        'status_removed': 'Complete: {count} files removed',
        'err_scan': 'Error during scan:\n{error}',
        'lang_btn': '🌐 PT-BR',
        'select_folder_title': 'Select Folder {num}'
    },
    'pt': {
        'title': '🔍 DuplicateFinder - Verificador de Arquivos Duplicados',
        'main_title': '🔍 DuplicateFinder',
        'subtitle': 'Encontre e remova arquivos duplicados entre duas pastas',
        'folder_selection': '📁 Seleção de Pastas',
        'folder_1': 'Pasta 1:',
        'folder_2': 'Pasta 2:',
        'select': '📂 Selecionar',
        'settings': '⚙️ Configurações',
        'extensions': 'Extensões:',
        'ext_ycd': '.ycd (Animações)',
        'ext_ydr': '.ydr (Modelos)',
        'ext_ytyp': '.ytyp (Tipos)',
        'ext_ybn': '.ybn (Colisões)',
        'delete_from': 'Deletar duplicados de:',
        'scan_btn': '🔍 Verificar Duplicados',
        'delete_btn': '🗑️ Mover para Lixeira',
        'clear_btn': '🔄 Limpar',
        'status_ready': 'Pronto para verificar...',
        'status_scanning': '⏳ Verificando...',
        'status_complete': 'Verificação concluída!',
        'status_deleting': '🗑️ Movendo para lixeira...',
        'results': '📋 Resultados',
        'col_filename': 'Arquivo',
        'col_path1': 'Caminho Pasta 1',
        'col_path2': 'Caminho Pasta 2',
        'col_size': 'Tamanho',
        'summary_found': '📊 Encontrados {count} arquivo(s) duplicado(s) | Total: {size}',
        'summary_none': '✅ Nenhum arquivo duplicado encontrado!',
        'warn_select_folders': 'Selecione as duas pastas antes de verificar!',
        'err_folder1_not_found': 'Pasta 1 não encontrada:\n{path}',
        'err_folder2_not_found': 'Pasta 2 não encontrada:\n{path}',
        'warn_select_extension': 'Selecione pelo menos uma extensão!',
        'info_no_duplicates': 'Nenhum duplicado para remover!',
        'confirm_delete_title': 'Confirmar Exclusão',
        'confirm_delete_msg': 'Mover {count} arquivo(s) da {folder} para a Lixeira?\n\nOs arquivos podem ser recuperados da Lixeira do Windows.',
        'complete_title': 'Concluído',
        'complete_msg': '✅ Arquivos movidos para lixeira: {success}\n❌ Erros: {errors}\n\nOs arquivos podem ser restaurados da Lixeira do Windows.',
        'status_removed': 'Concluído: {count} arquivos removidos',
        'err_scan': 'Erro ao verificar:\n{error}',
        'lang_btn': '🌐 EN',
        'select_folder_title': 'Selecione a Pasta {num}'
    }
}


class DuplicateFinderApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'en'
        self.root.title(self.t('title'))
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.path1 = tk.StringVar()
        self.path2 = tk.StringVar()
        self.ext_ycd = tk.BooleanVar(value=True)
        self.ext_ydr = tk.BooleanVar(value=True)
        self.ext_ytyp = tk.BooleanVar(value=True)
        self.ext_ybn = tk.BooleanVar(value=True)
        self.delete_from = tk.StringVar(value="path1")
        
        self.duplicates = []
        self.files_path1 = {}
        self.files_path2 = {}
        
        self.create_widgets()
    
    def t(self, key, **kwargs):
        """Get translated string."""
        text = TRANSLATIONS[self.current_lang].get(key, key)
        if kwargs:
            text = text.format(**kwargs)
        return text
    
    def toggle_language(self):
        """Toggle between English and Portuguese."""
        self.current_lang = 'pt' if self.current_lang == 'en' else 'en'
        self.refresh_ui()
    
    def refresh_ui(self):
        """Refresh all UI text with current language."""
        self.root.title(self.t('title'))
        
        # Update all text elements
        self.title_label.config(text=self.t('main_title'))
        self.subtitle_label.config(text=self.t('subtitle'))
        self.paths_frame.config(text=self.t('folder_selection'))
        self.path1_label.config(text=self.t('folder_1'))
        self.path2_label.config(text=self.t('folder_2'))
        self.path1_btn.config(text=self.t('select'))
        self.path2_btn.config(text=self.t('select'))
        self.config_frame.config(text=self.t('settings'))
        self.ext_label.config(text=self.t('extensions'))
        self.chk_ycd.config(text=self.t('ext_ycd'))
        self.chk_ydr.config(text=self.t('ext_ydr'))
        self.chk_ytyp.config(text=self.t('ext_ytyp'))
        self.chk_ybn.config(text=self.t('ext_ybn'))
        self.delete_label.config(text=self.t('delete_from'))
        self.radio_path1.config(text=self.t('folder_1').replace(':', ''))
        self.radio_path2.config(text=self.t('folder_2').replace(':', ''))
        self.scan_btn.config(text=self.t('scan_btn'))
        self.delete_btn.config(text=self.t('delete_btn'))
        self.clear_btn.config(text=self.t('clear_btn'))
        self.results_frame.config(text=self.t('results'))
        self.lang_btn.config(text=self.t('lang_btn'))
        
        # Update treeview headers
        self.tree.heading("filename", text=self.t('col_filename'))
        self.tree.heading("path1", text=self.t('col_path1'))
        self.tree.heading("path2", text=self.t('col_path2'))
        self.tree.heading("size", text=self.t('col_size'))
        
        # Update status if it's the default
        current_status = self.status_var.get()
        if current_status in [TRANSLATIONS['en']['status_ready'], TRANSLATIONS['pt']['status_ready']]:
            self.status_var.set(self.t('status_ready'))
        
    def create_widgets(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== HEADER =====
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Language button (top right)
        self.lang_btn = ttk.Button(header_frame, text=self.t('lang_btn'), command=self.toggle_language, width=10)
        self.lang_btn.pack(side=tk.RIGHT)
        
        # ===== TITLE =====
        self.title_label = ttk.Label(
            main_frame, 
            text=self.t('main_title'), 
            font=('Segoe UI', 18, 'bold')
        )
        self.title_label.pack(pady=(0, 5))
        
        self.subtitle_label = ttk.Label(
            main_frame, 
            text=self.t('subtitle'),
            font=('Segoe UI', 10)
        )
        self.subtitle_label.pack(pady=(0, 15))
        
        # ===== FOLDER SELECTION =====
        self.paths_frame = ttk.LabelFrame(main_frame, text=self.t('folder_selection'), padding="10")
        self.paths_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Folder 1
        path1_frame = ttk.Frame(self.paths_frame)
        path1_frame.pack(fill=tk.X, pady=5)
        
        self.path1_label = ttk.Label(path1_frame, text=self.t('folder_1'), width=10)
        self.path1_label.pack(side=tk.LEFT)
        ttk.Entry(path1_frame, textvariable=self.path1, width=70).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.path1_btn = ttk.Button(path1_frame, text=self.t('select'), command=lambda: self.select_folder(1))
        self.path1_btn.pack(side=tk.LEFT)
        
        # Folder 2
        path2_frame = ttk.Frame(self.paths_frame)
        path2_frame.pack(fill=tk.X, pady=5)
        
        self.path2_label = ttk.Label(path2_frame, text=self.t('folder_2'), width=10)
        self.path2_label.pack(side=tk.LEFT)
        ttk.Entry(path2_frame, textvariable=self.path2, width=70).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.path2_btn = ttk.Button(path2_frame, text=self.t('select'), command=lambda: self.select_folder(2))
        self.path2_btn.pack(side=tk.LEFT)
        
        # ===== SETTINGS =====
        self.config_frame = ttk.LabelFrame(main_frame, text=self.t('settings'), padding="10")
        self.config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Extensions
        ext_frame = ttk.Frame(self.config_frame)
        ext_frame.pack(fill=tk.X, pady=5)
        
        self.ext_label = ttk.Label(ext_frame, text=self.t('extensions'))
        self.ext_label.pack(side=tk.LEFT, padx=(0, 10))
        self.chk_ycd = ttk.Checkbutton(ext_frame, text=self.t('ext_ycd'), variable=self.ext_ycd)
        self.chk_ycd.pack(side=tk.LEFT, padx=10)
        self.chk_ydr = ttk.Checkbutton(ext_frame, text=self.t('ext_ydr'), variable=self.ext_ydr)
        self.chk_ydr.pack(side=tk.LEFT, padx=10)
        self.chk_ytyp = ttk.Checkbutton(ext_frame, text=self.t('ext_ytyp'), variable=self.ext_ytyp)
        self.chk_ytyp.pack(side=tk.LEFT, padx=10)
        self.chk_ybn = ttk.Checkbutton(ext_frame, text=self.t('ext_ybn'), variable=self.ext_ybn)
        self.chk_ybn.pack(side=tk.LEFT, padx=10)
        
        # Delete option
        delete_frame = ttk.Frame(self.config_frame)
        delete_frame.pack(fill=tk.X, pady=5)
        
        self.delete_label = ttk.Label(delete_frame, text=self.t('delete_from'))
        self.delete_label.pack(side=tk.LEFT, padx=(0, 10))
        self.radio_path1 = ttk.Radiobutton(delete_frame, text=self.t('folder_1').replace(':', ''), variable=self.delete_from, value="path1")
        self.radio_path1.pack(side=tk.LEFT, padx=10)
        self.radio_path2 = ttk.Radiobutton(delete_frame, text=self.t('folder_2').replace(':', ''), variable=self.delete_from, value="path2")
        self.radio_path2.pack(side=tk.LEFT, padx=10)
        
        # ===== ACTION BUTTONS =====
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        self.scan_btn = ttk.Button(
            action_frame, 
            text=self.t('scan_btn'), 
            command=self.start_scan,
            style='Accent.TButton'
        )
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(
            action_frame, 
            text=self.t('delete_btn'), 
            command=self.delete_duplicates,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            action_frame, 
            text=self.t('clear_btn'), 
            command=self.clear_results
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar(value=self.t('status_ready'))
        status_label = ttk.Label(action_frame, textvariable=self.status_var, foreground="gray")
        status_label.pack(side=tk.RIGHT, padx=10)
        
        # ===== RESULTS =====
        self.results_frame = ttk.LabelFrame(main_frame, text=self.t('results'), padding="10")
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(self.results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(
            tree_frame, 
            columns=("filename", "path1", "path2", "size"),
            show="headings",
            selectmode="extended"
        )
        
        self.tree.heading("filename", text=self.t('col_filename'))
        self.tree.heading("path1", text=self.t('col_path1'))
        self.tree.heading("path2", text=self.t('col_path2'))
        self.tree.heading("size", text=self.t('col_size'))
        
        self.tree.column("filename", width=200)
        self.tree.column("path1", width=250)
        self.tree.column("path2", width=250)
        self.tree.column("size", width=80)
        
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # ===== SUMMARY =====
        self.summary_var = tk.StringVar(value="")
        summary_label = ttk.Label(main_frame, textvariable=self.summary_var, font=('Segoe UI', 10, 'bold'))
        summary_label.pack(pady=5)
        
    def select_folder(self, folder_num):
        """Open dialog to select folder."""
        folder = filedialog.askdirectory(title=self.t('select_folder_title', num=folder_num))
        if folder:
            folder = os.path.normpath(folder)
            if folder_num == 1:
                self.path1.set(folder)
            else:
                self.path2.set(folder)
    
    def get_extensions(self):
        """Return set of selected extensions."""
        extensions = set()
        if self.ext_ycd.get():
            extensions.add('.ycd')
        if self.ext_ydr.get():
            extensions.add('.ydr')
        if self.ext_ytyp.get():
            extensions.add('.ytyp')
        if self.ext_ybn.get():
            extensions.add('.ybn')
        return extensions
    
    def get_files_from_path(self, base_path, extensions):
        """Collect files from a directory."""
        files = defaultdict(list)
        
        if not os.path.exists(base_path):
            return files
        
        for root, dirs, filenames in os.walk(base_path):
            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext in extensions:
                    full_path = os.path.join(root, filename)
                    files[filename.lower()].append(full_path)
        
        return files
    
    def format_size(self, size_bytes):
        """Format size in readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    def start_scan(self):
        """Start scan in separate thread."""
        path1 = self.path1.get()
        path2 = self.path2.get()
        
        if not path1 or not path2:
            messagebox.showwarning("Warning", self.t('warn_select_folders'))
            return
        
        if not os.path.exists(path1):
            messagebox.showerror("Error", self.t('err_folder1_not_found', path=path1))
            return
        
        if not os.path.exists(path2):
            messagebox.showerror("Error", self.t('err_folder2_not_found', path=path2))
            return
        
        extensions = self.get_extensions()
        if not extensions:
            messagebox.showwarning("Warning", self.t('warn_select_extension'))
            return
        
        # Disable buttons during scan
        self.scan_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.status_var.set(self.t('status_scanning'))
        
        # Run in separate thread
        thread = threading.Thread(target=self.scan_folders, args=(path1, path2, extensions))
        thread.start()
    
    def scan_folders(self, path1, path2, extensions):
        """Scan folders and find duplicates."""
        try:
            # Collect files
            self.files_path1 = self.get_files_from_path(path1, extensions)
            self.files_path2 = self.get_files_from_path(path2, extensions)
            
            # Find duplicates
            common_files = set(self.files_path1.keys()) & set(self.files_path2.keys())
            
            self.duplicates = []
            total_size = 0
            
            for filename in common_files:
                paths1 = self.files_path1[filename]
                paths2 = self.files_path2[filename]
                
                for p1 in paths1:
                    size = os.path.getsize(p1)
                    total_size += size
                    self.duplicates.append({
                        'filename': filename,
                        'path1': p1,
                        'path2': paths2[0] if paths2 else "",
                        'size': size
                    })
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_results(total_size))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", self.t('err_scan', error=str(e))))
            self.root.after(0, lambda: self.scan_btn.config(state=tk.NORMAL))
    
    def update_results(self, total_size):
        """Update UI with results."""
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fill with duplicates
        for dup in self.duplicates:
            self.tree.insert("", tk.END, values=(
                dup['filename'],
                os.path.dirname(dup['path1']),
                os.path.dirname(dup['path2']),
                self.format_size(dup['size'])
            ))
        
        # Update summary
        count = len(self.duplicates)
        if count > 0:
            self.summary_var.set(self.t('summary_found', count=count, size=self.format_size(total_size)))
            self.delete_btn.config(state=tk.NORMAL)
        else:
            self.summary_var.set(self.t('summary_none'))
            self.delete_btn.config(state=tk.DISABLED)
        
        self.scan_btn.config(state=tk.NORMAL)
        self.status_var.set(self.t('status_complete'))
    
    def delete_duplicates(self):
        """Move duplicates to recycle bin."""
        if not self.duplicates:
            messagebox.showinfo("Info", self.t('info_no_duplicates'))
            return
        
        delete_from = self.delete_from.get()
        folder_name = self.t('folder_1').replace(':', '') if delete_from == "path1" else self.t('folder_2').replace(':', '')
        
        confirm = messagebox.askyesno(
            self.t('confirm_delete_title'),
            self.t('confirm_delete_msg', count=len(self.duplicates), folder=folder_name)
        )
        
        if not confirm:
            return
        
        self.delete_btn.config(state=tk.DISABLED)
        self.status_var.set(self.t('status_deleting'))
        
        success = 0
        errors = 0
        
        for dup in self.duplicates:
            try:
                path_to_delete = dup['path1'] if delete_from == "path1" else dup['path2']
                if os.path.exists(path_to_delete):
                    send2trash(path_to_delete)
                    success += 1
            except Exception as e:
                errors += 1
                print(f"Error deleting {dup['filename']}: {e}")
        
        # Clear results
        self.clear_results()
        
        # Show result
        messagebox.showinfo(
            self.t('complete_title'),
            self.t('complete_msg', success=success, errors=errors)
        )
        
        self.status_var.set(self.t('status_removed', count=success))
    
    def clear_results(self):
        """Clear results."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.duplicates = []
        self.summary_var.set("")
        self.delete_btn.config(state=tk.DISABLED)
        self.status_var.set(self.t('status_ready'))


def main():
    root = tk.Tk()
    
    # Configure icon if available
    try:
        root.iconbitmap(default='')
    except:
        pass
    
    app = DuplicateFinderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
