import tkinter as tk
from tkinter import ttk
import config

class MetaHeaderPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master,bg=config.paper)
        self.lblDay = tk.Label(self, text="Day: Monday", bg=config.paper, fg=config.ink, font=config.fontHeader)
        self.lblTimer = tk.Label(self, text="Timer: 120s", bg=config.paper, fg=config.terracotta, font=config.fontTimer)
        self.lblCapital = tk.Label(self, text="Capital: $10,000 | Rating: 3.0 Stars", bg=config.paper,fg=config.ink, font=config.fontHeader)

        self.lblDay.pack(side=tk.LEFT,padx = 15,pady= 10)
        self.lblTimer.pack(side=tk.LEFT, expand = True, pady=10)
        self.lblCapital.pack(side=tk.RIGHT, padx = 15, pady = 10 )

class DossierPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master,bg=config.paper)
        tk.Label(self, text="Client Dossier", font=config.fontHeader, bg=config.paper, fg=config.ink).pack(pady=(10,5))


        self.lblClientname = tk.Label(self, text="Client: Pending...", font=config.fontNarrative, bg=config.paper, fg=config.ink)
        self.lblClientname.pack(anchor="w", padx=10)
        self.lblParams = tk.Label(self, text="Party: 0 | Duration: 0 Days", font=config.fontList, bg=config.paper, fg=config.mutedSlate)
        self.lblParams.pack(anchor="w",padx=10,pady=(0,10))

        self.txt_email = tk.Text(self, height=8, font=config.fontNarrative, bg=config.parchment, fg=config.ink, wrap=tk.WORD, bd=0,padx=5,pady=5)
        self.txt_email.pack(fill=tk.X, padx=10, pady=5)
        self.txt_email.insert(tk.END, "Awaiting client email...")
        self.txt_email.config(state=tk.DISABLED)

        tk.Label(self, text="Agent Scratchpad", font=config.fontList, bg=config.paper, fg=config.mutedSlate).pack(anchor="w", padx=10, pady=(10,0))
        self.txt_scratchpad = tk.Text(self, font=config.fontList, bg=config.parchment, fg=config.ink, wrap=tk.WORD,bd=0,padx=5,pady =5)
        self.txt_scratchpad.pack(fill=tk.BOTH, expand=True, padx=10, pady= (0, 10))


class LogisticsMatrixPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=config.paper)
        style=ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook',  background=config.paper, borderwidth=0)
        style.configure('TNotebook.Tab', background=config.parchment, foreground=config.ink, font=config.fontList, padding=[10,2])
        style.map('TNotebook.Tab', background=[('selected', config.highlight)])
        self.notebook=ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tabFlights = tk.Frame(self.notebook, bg=config.paper)
        self.tabLodgings=tk.Frame(self.notebook, bg=config.paper)
        self.tabExcursions = tk.Frame(self.notebook, bg=config.paper)

        self.notebook.add(self.tabFlights, text="Flights")
        self.notebook.add(self.tabLodgings, text="Lodgings")
        self.notebook.add(self.tabExcursions, text="Excursions")

        self.listFlights = tk.Listbox(self.tabFlights, bg=config.paper, fg=config.ink, font=config.fontList, bd=0,highlightthickness=0,selectbackground=config.highlight,selectforeground = config.ink)
        self.listLodgings = tk.Listbox(self.tabLodgings, bg=config.paper, fg=config.ink, font=config.fontList, bd=0,highlightthickness=0, selectbackground=config.highlight, selectforeground=config.ink)
        self.listExcursions = tk.Listbox(self.tabExcursions, bg=config.paper, fg=config.ink, font=config.fontList, bd= 0, highlightthickness=0, selectbackground=config.highlight, selectforeground=config.ink)
        self.listExcursions.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

class ItineraryLedgerPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=config.paper)
        tk.Label(self, text="Itinerary Ledger", font=config.fontHeader, bg=config.paper, fg=config.ink).pack(pady=(10,5))
