import tkinter as tk
import random, config

class GameController:
    def __init__(self, app, data):
        self.app = app
        self.data = data
        self.timeLeft = 120
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday","Sunday"]
        self.currentDayIdx = 0

        self.activeClient = random.choice(self.data.clients) if self.data.clients else None
        self.itinerary = {"flight":None, "lodging":None, "excursion":None}

        self.app.ledgerPanel.btnAdvance.config(command=self.advanceDay)
        self.app.matrixPanel.listFlights.bind("<<ListboxSelect>>", lambda e: self.onSelect('flight'))
        self.app.matrixPanel.listLodgings.bind("<<ListboxSelect>>", lambda e: self.onSelect('lodging'))
        self.app.matrixPanel.listExcursions.bind("<<ListboxSelect>>", lambda e: self.onSelect('excursion'))

        self.loadClient()
        self.refreshMarketUI()
        self.tick()

    def loadClient(self):
        if not self.activeClient: return
        dp=self.app.dossierPanel
        dp.lblClientName.config(text=f"Client:{self.activeClient.clientName}")
        dp.lblParams.config(text=f"Party: {self.activeClient.partySize} | Duration: {self.activeClient.durationDays} Days")
        dp.txtEmail.config(state=tk.NORMAL)
        dp.txtEmail.delete(1.0, tk.END)
        dp.txtEmail.insert(tk.END, self.activeClient.narrativeEmail)
        dp.txtEmail.config(state=tk.DISABLED)
        self.updateLedger()

    def onSelect(self, category):
        panels = {
            'flight': (self.app.matrixPanel.listFLights, self.data.flights, self.app.ledgerPanel.lblFlightSlot),
            'lodging': (self.app.matrixPanel.listLodgings, self.data.lodgings, self.app.ledgerPanel.lblLodgingSlot),
            'excursion':(self.app.matrixPanel.listExcursions, self.data.excursions, self.app.ledgerPanel.lblExcursionSlot)
        }
        listbox, dataList, label =panels[category]
        selection = listbox.curselection()
        if selection:
            item = dataList[selection[0]]
            self.itinerary[category] = item
            label.config(text=f"{category.capitalize()}: {item.name}")
            self.updateLedger()

    def updateLedger(self):
        if not self.activeClient: return
        c = self.activeClient
        costs=0
        f, l, e = self.itinerary['flight'], self.itinerary['lodging'], self.itinerary['excursion']
        if f: costs += f.currentPrice*c.partySize
        if l: costs+= l.currentPrice*c.durationDays
        if e: costs+=e.currentPrice*c.partySize

        reserve = c.budget-costs
        lp= self.app.ledgerPanel

        lp.lblStarting.config(text=f"Starting Budget: ${c.budget}")
        lp.lblCosts.config(text=f"Total Costs: ${costs}")
        lp.lblReserve.config(text=f"Available Funds: ${reserve}")
        lp.lblReserve.config(fg=config.terracotta if reserve<0 else config.sageGreen)
    def tick(self):
        if self.timeLeft>0:
            self.timeLeft-= 1
            self.app.headerPanel.lblTimer.config(text=f"Timer: {self.timeLeft}")
            self.app.root.after(1000, self.tick)
        else:
            self.app.headerPanel.lblTimer.config(text="TIME EXPIRED")

    def advanceDay(self):
        if self.currentDayIdx<len(self.days)-1:
            self.currentDayIdx+=1
            self.timeLeft=120
            self.app.headerPanel.lblDay.config(text=f"Day: {self.days[self.currentDayIdx]}")
            self.data.mutatePrices()
            self.refreshMarketUI()
        else: self.app.headerPanel.lblDay.config(text="Day: Sunday (LAST DAY)")


    def refreshMarketUI(self):
        panels=[
            (self.app.matrixPanel.listFlights, self.data.flights),
            (self.app.matrixPanel.listLodgings, self.data.lodgings),
            (self.app.matrixPanel.listExcursions, self.data.excursions)
        ]
        for listbox, items in panels:
            listbox.delete(0, tk.END)
            for item in items:
                trend = "▲" if item.currentPrice>item.prevPrice else "▼" if item.currentPrice<item.prevPrice else "-"
                listbox.insert(tk.END, f"{trend} ${item.currentPrice}|{item.name}")