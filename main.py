import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class FileMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Mover with Extension Filter")
        self.root.geometry("400x350")  # Slightly taller to ensure visibility
        
        # Source and Destination Selection
        self.create_folder_selection()
        
        # Category Checkboxes
        self.create_category_checkboxes()
        
        # Ignore "old" Folder Option
        self.ignore_old_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Ignore files in 'old' or 'OLD' folders", variable=self.ignore_old_var).pack(anchor="w", padx=20, pady=5)
        
        # Move Files Button
        self.move_button = tk.Button(root, text="Move Files", command=self.move_files, width=20)
        self.move_button.pack(pady=10)  # Reduced padding for compactness
    
    def create_folder_selection(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Source Folder:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.source_folder_entry = tk.Entry(frame, width=30)
        self.source_folder_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(frame, text="Destination Folder:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.destination_folder_entry = tk.Entry(frame, width=30)
        self.destination_folder_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame, text="Browse", command=self.browse_destination).grid(row=1, column=2, padx=5, pady=5)

    def create_category_checkboxes(self):
        self.category_vars = {
            "Documents": tk.BooleanVar(),
            "Code Files": tk.BooleanVar(),
            "Design Files": tk.BooleanVar(),
            "Zip Files": tk.BooleanVar()
        }
        
        categories_frame = tk.Frame(self.root)
        categories_frame.pack(pady=5)

        tk.Label(categories_frame, text="Select File Categories to Move:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)

        for category, var in self.category_vars.items():
            cb = tk.Checkbutton(categories_frame, text=category, variable=var)
            cb.pack(anchor="w", padx=20)

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_folder_entry.delete(0, tk.END)
            self.source_folder_entry.insert(0, folder)

    def browse_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.destination_folder_entry.delete(0, tk.END)
            self.destination_folder_entry.insert(0, folder)

    def move_files(self):
        source_folder = self.source_folder_entry.get()
        destination_folder = self.destination_folder_entry.get()

        # Define file extensions for each category
        selected_extensions = []
        if self.category_vars["Documents"].get():
            selected_extensions.extend([".docx", ".doc", ".pdf", ".xlsx", ".xls", ".xlsb", ".ppt", ".pptx", ".txt", ".csv", ".md", ".json", ".xml"])
        if self.category_vars["Code Files"].get():
            selected_extensions.extend([".py", ".java", ".c", ".cpp", ".v", ".vhdl", ".sv"])
        if self.category_vars["Design Files"].get():
            selected_extensions.extend([".sch", ".brd"])
        if self.category_vars["Zip Files"].get():
            selected_extensions.extend([".zip", ".rar", ".7z"])

        if not os.path.isdir(source_folder):
            messagebox.showerror("Error", "Invalid source folder.")
            return
        if not os.path.isdir(destination_folder):
            messagebox.showerror("Error", "Invalid destination folder.")
            return
        if not selected_extensions:
            messagebox.showerror("Error", "Please select at least one file category.")
            return

        ignore_old = self.ignore_old_var.get()
        moved_files = 0

        # Walk through the directory to include subdirectories if needed
        for root_dir, _, files in os.walk(source_folder):
            # Ignore directories named "old" or "OLD" if the option is checked
            if ignore_old and ("old" in os.path.basename(root_dir).lower()):
                continue
            
            for filename in files:
                file_extension = os.path.splitext(filename)[1].lower()
                if file_extension in selected_extensions:
                    src_path = os.path.join(root_dir, filename)
                    dst_path = os.path.join(destination_folder, filename)
                    shutil.move(src_path, dst_path)
                    moved_files += 1
        
        messagebox.showinfo("Files Moved", f"Moved {moved_files} files.")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = FileMoverApp(root)
    root.mainloop()
