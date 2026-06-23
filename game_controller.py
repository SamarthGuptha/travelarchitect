import tkinter as tk
import random, config

class GameController:
    def __init__(self, app, data):
        self.app = app
        self.data = data
        self.timeLeft = 120
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday","Sunday"]
        self.currentDayIdx = 0
        self.timerId = None
        self.capital = 10000
        self.rating =3.0
        self.reviewsCount=1

        self.activeClient = random.choice(self.data.clients) if self.data.clients else None
        self.itinerary = {"flight":None, "lodging":None, "excursion":None}

        self.app.ledgerPanel.btnAdvance.config(command=self.advanceDay)
        self.app.ledgerPanel.btnDispatch.config(command=self.dispatchItinerary)
        self.app.matrixPanel.listFlights.bind("<<ListboxSelect>>", lambda e: self.onSelect('flight'))
        self.app.matrixPanel.listLodgings.bind("<<ListboxSelect>>", lambda e: self.onSelect('lodging'))
        self.app.matrixPanel.listExcursions.bind("<<ListboxSelect>>", lambda e: self.onSelect('excursion'))

        self.loadClient()
        self.refreshMarketUI()
        self.tick()

    def loadClient(self):
        if not self.activeClient: return
        dp=self.app.dossierPanel
        dp.lblClientname.config(text=f"Client:{self.activeClient.clientName}")
        dp.lblParams.config(text=f"Party: {self.activeClient.partySize} | Duration: {self.activeClient.durationDays} Days")
        dp.txtEmail.config(state=tk.NORMAL)
        dp.txtEmail.delete(1.0, tk.END)
        dp.txtEmail.insert(tk.END, self.activeClient.narrativeEmail)
        dp.txtEmail.config(state=tk.DISABLED)
        self.updateLedger()

    def onSelect(self, category):
        panels = {
            'flight': (self.app.matrixPanel.listFlights, self.data.flights, self.app.ledgerPanel.lblFlightSlot),
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

    def dispatchItinerary(self):
        if self.timerId:
            self.app.root.after_cancel(self.timerId)
            self.timerId= None

        self.baseScore = self.data.evaluate_itinerary(self.activeClient, self.itinerary)
        self.triggerChaos()

    def triggerChaos(self):
        if not self.data.events:
            self.resolveDispatch(0)
            return

        event = random.choice(self.data.events)
        modal = tk.Toplevel(self.app.root)
        modal.title("Chaos Intercept!")
        modal.geometry("550x350")
        modal.configure(bg=config.parchment)
        modal.transient(self.app.root)
        modal.grab_set()
        tk.Label(modal, text=event.message, font=config.fontNarrative, bg=config.parchment, fg= config.terracotta, wraplength=500).pack(pady=20)

        for choice in event.choices:
            btn= tk.Button(modal, text=choice["text"], font=config.fontList, bg=config.paper, fg= config.ink, wraplength=450, command= lambda c=choice, m=modal:self.applyChaosChoice(c, m))
            btn.pack(fill=tk.X, padx=20, pady=10)

    def applyChaosChoice(self, choice, modal):
        modal.destroy()
        self.capital += choice.get("budgetImpact", 0)
        self.resolveDispatch(choice.get("scorePenalty", 0))

    def resolveDispatch(self, scoreMod):
        finalScore= self.baseScore+scoreMod
        c =self.activeClient
        if finalScore>= 80:
            stars, reward, text = 5, 2000, c.reviews.get("perfect", "Perfect!")
        elif finalScore>=40:
            stars, reward,text=3, 500, c.reviews.get("pass", "Okay.")
        else:
            stars,reward,text=1, -1000, c.reviews.get("fail","Terrible.")

        self.rating = ((self.rating*self.reviewsCount)+stars)/(self.reviewsCount+1)
        self.reviewsCount+=1
        self.capital+=reward

        self.app.headerPanel.lblCapital.config(text=f"Capital: ${self.capital:,} | Rating: {self.rating:.1f} ★")
        self.showReviewModal(text,stars,reward)

    def showReviewModal(self, text, stars, reward):
        modal =tk.Toplevel(self.app.root)
        modal.title("Final Review")
        modal.geometry("450x250")
        modal.configure(bg=config.paper)
        modal.transient(self.app.root)
        modal.grab_set()

        tk.Label(modal, text=f"{stars} Star Review", font=config.fontHeader, bg=config.paper,fg=config.ink).pack(pady=10)
        tk.Label(modal, text=f'"{stars}"', font=config.fontNarrative, bg=config.paper,fg= config.mutedSlate, wraplength=400).pack(pady=10)
        rewardColor = config.sageGreen if reward >=0 else config.terracotta
        tk.Label(modal, text=f"Agency Payout: ${reward:,}", font=config.fontMath, bg=config.paper, fg=rewardColor).pack(pady=10)
        tk.Button(modal, text="Next Client", bg=config.ink, fg=config.paper,command=lambda: [modal.destroy(), self.resetGameCycle()]).pack(pady=15)


    def resetGameCycle(self):
        self.activeClient = random.choice(self.data.clients)
        self.itinerary = {"flights": None, "lodging": None, "excursion": None}
        self.timeLeft= 120
        self.app.headerPanel.lblDay.config(text=f"Day: {self.days[self.currentDayIdx]}")
        self.app.ledgerPanel.lblFlightSlot.config(text="Flight: [Empty]")
        self.app.ledgerPanel.lblLodgingSlot.config(text="Lodging: [Empty]")
        self.app.ledgerPanel.lblExcursionSlot.config(text="Excursion: [Empty]")
        self.loadClient()
        self.tick()