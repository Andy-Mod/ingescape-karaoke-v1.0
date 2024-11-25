import tkinter as tk
from tkinter import ttk
import csv

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("CSV Table Display")
        self.geometry("800x400")
        self.minsize(600, 300)  
        
        self.rowconfigure(0, weight=1)  
        self.columnconfigure(0, weight=1)  
        
        menu_bar = tk.Menu(self)
        
        scene_menu = tk.Menu(menu_bar, tearoff=0)
        scene_menu.add_command(label="Load CSV Table", command=lambda: self.show_csv_table("Score"))
        scene_menu.add_command(label="Exit", command=self.quit)
        
        menu_bar.add_cascade(label="Scenes", menu=scene_menu)
        
        self.config(menu=menu_bar)
        
        self.frame = None
        self.show_csv_table("Score")

    def show_csv_table(self, sort_by):
        if self.frame:
            self.frame.destroy()
        
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")  
        
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(self.frame, show="headings")
        
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.load_csv_data("data/sample_data.csv", sort_by)
        
        self.tree.grid(row=0, column=0, sticky="nsew")  
        vsb.grid(row=0, column=1, sticky="ns")  
        hsb.grid(row=1, column=0, sticky="ew")  
        
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def load_csv_data(self, filepath, sort_by):
        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  
                
                self.tree["columns"] = ["Rank"] + headers
                self.tree.heading("Rank", text="Rank")
                self.tree.column("Rank", width=50, anchor="center")
                
                for header in headers:
                    self.tree.heading(header, text=header)
                    self.tree.column(header, width=100, anchor="center")
                
                rows = list(reader)

                if sort_by in headers:
                    sort_index = headers.index(sort_by)
                    rows.sort(key=lambda x: float(x[sort_index]) if x[sort_index].replace('.', '', 1).isdigit() else x[sort_index], reverse=True)
                
                for index, row in enumerate(rows):
                    rank = index + 1
                    self.tree.insert("", "end", values=(rank, *row))

        except Exception as e:
            print(f"Error loading CSV file: {e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
