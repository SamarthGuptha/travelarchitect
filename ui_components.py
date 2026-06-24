import tkinter as tk
from tkinter import ttk
import config

class MetaHeaderPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master,bg=config.paper)
        self.lblDay = tk.Label(self, text="Day: Monday", bg=config.paper, fg=config.ink, font=config.fontHeader)
        self.lblTimer = tk.Label(self, text="Timer: 120s", bg=config.paper, fg=config.terracotta, font=config.fontTimer)
        self.lblCapital = tk.Label(self, text="Capital: $10,000 | Rating: 3.0 Stars", bg=config.paper,fg=config.ink, font=config.fontHeader)
        self.canvasCoffee= tk.Canvas(self, width=40, height=40, bg=config.paper, highlightthickness=0)
        self.btnShop = tk.Button(self, text="[ Buy Tools ]", bg=config.highlight, fg=config.ink, font=config.fontList,relief=tk.FLAT,activebackground=config.colorBorder, bd=0,padx=10)
        self.canvasCoffee.pack(side=tk.LEFT, padx=(15, 5),pady=10)
        self.btnShop.pack(side=tk.RIGHT, padx=(15,0), pady=10)

        self.lblDay.pack(side=tk.LEFT,padx = 15,pady= 10)
        self.lblTimer.pack(side=tk.LEFT, expand = True, pady=10)
        self.lblCapital.pack(side=tk.RIGHT, padx = 15, pady = 10 )
        self.drawCoffee(unlocked=False)

    def drawCoffee(self,unlocked, used=False):
        self.canvasCoffee.delete("all")
        if not unlocked:
            self.canvasCoffee.config(bg=config.paper, cursor="arrow")
            return
        self.canvasCoffee.config(bg=config.parchment,cursor="hand2")
        ink = config.mutedSlate if used else config.ink

        if not used:
            self.canvasCoffee.create_arc(10,25,30,35, start=180, extent= 180, fill=ink, outline= ink)
            self.canvasCoffee.create_rectangle(10,15,30, 30, fill=ink, outline=ink)
            self.canvasCoffee.create_arc(10, 10, 30, 20, start=0, extent=360, fill=config.parchment, outline=ink)
            self.canvasCoffee.create_arc(25,15,37,27, start=-90, extent=180, style=tk.ARC,outline= ink, width=2)
            self.canvasCoffee.create_line(15,12, 17 , 4, fill=config.sageGreen, width=2, smooth= True)
            self.canvasCoffee.create_line(22, 10,24,2, fill=config.sageGreen, width=2, smooth =True)
        else:
            self.canvasCoffee.create_polygon(5, 30,25,35,30, 20,10, 15, fill=ink, outline=ink)
            self.canvasCoffee.create_oval(3, 27, 13, 37, fill=config.parchment, outline= ink)
            self.canvasCoffee.create_arc(15, 10, 27,22, start=0, extent=180, style=tk.ARC, outline=ink, width=2)
            self.canvasCoffee.create_oval(25,32, 38, 38, fill=config.terracotta, outline="")


class DossierPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master,bg=config.paper)
        tk.Label(self, text="Client Dossier", font=config.fontHeader, bg=config.paper, fg=config.ink).pack(pady=(10,5))


        self.lblClientname = tk.Label(self, text="Client: Pending...", font=config.fontNarrative, bg=config.paper, fg=config.ink)
        self.lblClientname.pack(anchor="w", padx=10)
        self.lblParams = tk.Label(self, text="Party: 0 | Duration: 0 Days", font=config.fontList, bg=config.paper, fg=config.mutedSlate)
        self.lblParams.pack(anchor="w",padx=10,pady=(0,10))

        self.txtEmail = tk.Text(self, height=8, font=config.fontNarrative, bg=config.parchment, fg=config.ink, wrap=tk.WORD, bd=0,padx=5,pady=5)
        self.txtEmail.pack(fill=tk.X, padx=10, pady=5)
        self.txtEmail.insert(tk.END, "Awaiting client email...")
        self.txtEmail.config(state=tk.DISABLED)

        self.frameBarometer = tk.Frame(self, bg=config.colorBorder,padx=1, pady=1)
        self.frameBarometer.pack(fill=tk.X, padx=10, pady=(10,0))

        innerBaro = tk.Frame(self.frameBarometer, bg=config.parchment)
        innerBaro.pack(fill=tk.BOTH, expand=True)
        self.lblBarometer= tk.Label(innerBaro, text="[ Barometer Slot Locked ]", font=("Georgia", 10,"italic"), bg=config.parchment, fg=config.mutedSlate, height=1)
        self.lblBarometer.pack(pady=4)

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
        self.listFlights.pack(fill=tk.BOTH, expand=True,padx=5, pady= 5)
        self.listLodgings.pack(fill=tk.BOTH,expand = True, padx=5,pady=5)

class ItineraryLedgerPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=config.paper)
        tk.Label(self, text="Itinerary Ledger", font=config.fontHeader, bg=config.paper, fg=config.ink).pack(pady=(10,5))

        self.lblFlightSlot = tk.Label(self, text="Flight: [Empty]", bg=config.paper, font=config.fontList, fg=config.ink)
        self.lblFlightSlot.pack(anchor="w", padx=10, pady=2)
        self.lblLodgingSlot = tk.Label(self, text="Lodging: [Empty]", bg=config.paper, font=config.fontList, fg=config.ink)
        self.lblLodgingSlot.pack(anchor="w", padx=10, pady=2)
        self.lblExcursionSlot = tk.Label(self, text="Excursion: [Empty]", bg=config.paper, font=config.fontList, fg=config.ink)
        self.lblExcursionSlot.pack(anchor="w",padx=10,pady=2)

        budgetFrame = tk.Frame(self, bg=config.parchment, padx=5,pady=5)
        budgetFrame.pack(fill=tk.X, padx=10, pady=20)

        self.lblStarting = tk.Label(budgetFrame, text="Starting Budget: $0", bg=config.parchment, font=config.fontMath, fg=config.ink)
        self.lblCosts = tk.Label(budgetFrame, text="Total Costs: $0", bg=config.parchment, font=config.fontMath, fg=config.terracotta)
        self.lblReserve = tk.Label(budgetFrame, text="Available Funds: $0", bg=config.parchment, font=config.fontMath, fg=config.sageGreen)
        self.lblStarting.pack(anchor="w", pady=2)
        self.lblCosts.pack(anchor="w",pady=2)
        self.lblReserve.pack(anchor="w",pady =2)

        self.btnAdvance = tk.Button(self, text="Advance Day", bg=config.highlight, fg=config.ink, font=config.fontList, relief=tk.FLAT, activebackground=config.colorBorder)
        self.btnAdvance.pack(fill=tk.X, padx=10, pady=5)


        self.btnDispatch = tk.Button(self, text="Dispatch Itinerary", bg=config.ink, fg=config.paper, font=config.fontList, relief = tk.FLAT, activebackground=config.mutedSlate, activeforeground=config.paper)
        self.btnDispatch.pack(fill=tk.X, padx=10, pady=5)
