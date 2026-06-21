import tkinter as tk
from ui_components import MetaHeaderPanel, DossierPanel, LogisticsMatrixPanel, ItineraryLedgerPanel
from data_manager import DataManager
from game_controller import GameController
import config

class TravelArchitectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Travel Architect")
        self.root.geometry("1050x650")
        self.root.resizable(False, False)
        self.root.configure(bg=config.parchment)
        self.setup_grid()
        self.mountPanels()

    def setup_grid(self):
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1, uniform="cols")
        self.root.grid_columnconfigure(1, weight=2, uniform="cols")
        self.root.grid_columnconfigure(2, weight=1, uniform="cols")
    def mountPanels(self):
        self.headerBorder=config.applyFlatBorder(self.root)
        self.headerBorder.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=(10,5))
        self.headerPanel =MetaHeaderPanel(self.headerBorder)
        self.headerPanel.pack(fill=tk.BOTH, expand=True)

        self.leftBorder =config.applyFlatBorder(self.root)
        self.leftBorder.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(5,10))
        self.dossierPanel = DossierPanel(self.leftBorder)
        self.dossierPanel.pack(fill=tk.BOTH, expand=True)

        self.centerBorder = config.applyFlatBorder(self.root)
        self.centerBorder.grid(row=1, column=1, sticky="nsew", padx=5, pady=(5, 10))
        self.matrixPanel =LogisticsMatrixPanel(self.centerBorder)
        self.matrixPanel.pack(fill=tk.BOTH, expand=True)
        self.rightBorder = config.applyFlatBorder(self.root)

        self.rightBorder.grid(row=1, column=2, sticky="nsew", padx=(5, 10), pady=(5, 10))
        self.ledgerPanel = ItineraryLedgerPanel(self.rightBorder)
        self.ledgerPanel.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app= TravelArchitectApp(root)
    data= DataManager()
    gc = GameController(app, data)
    root.mainloop()
