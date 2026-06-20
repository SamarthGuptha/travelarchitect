import json, os, random

class Client:
    def __init__(self, data):
        self.clientId =data.get("clientId")
        self.clientName=data.get("clientName")
        self.budget = data.get("budget",0)
        self.partySize = data.get("partySize", 1)
        self.durationDays = data.get("durationDays", 1)
        self.narrativeEmail = data.get("narrativeEmail","")
        self.hiddenMustHaves = data.get("hiddenMustHaves", [])
        self.hiddenDealBreakers=data.get("hiddenDealBreakers", [])
        self.reviews = data.get("reviews",{})

class CatalogItem:
    def __init__(self, data, item_type):
        self.id = data.get("id")
        self.name=data.get("name")
        self.country = data.get("country")
        self.basePrice = data.get("basePrice",0)
        self.item_type=item_type

        self.tags=data.get("tags", [])
        self.volatility = data.get("volatility", "low")
        self.currentPrice = self.basePrice
        self.prevPrice = self.basePrice

class ChaosEvent:
    def __init__(self,data):
        self.event_id = data.get("eventId")
        self.message = data.get("message")
        self.choices = data.get("choices",[])
class DataManager:
    def __init__(self):
        self.clients = []
        self.flights = []
        self.lodgings=[]
        self.excursions=[]
        self.events = []

    def load_databases(self):
        baseDir = "jsondata"
        clientsPath = os.path.join(baseDir, "clients_database.json")
        if os.path.exists(clientsPath):
            with open(clientsPath, 'r',encoding='utf-8') as f:
                self.clients = [Client(c) for c in json.load(f)]
        else: print(f"missing {clientsPath}")
        if os.path.exists(os.path.join(baseDir,"catalog_database.json")):
            with open(os.path.join(baseDir,"catalog_database.json"),'r',encoding='utf-8') as f:
                data=json.load(f)
                self.flights=[CatalogItem(item,"flight") for item in data.get("flights",[])]
                self.lodgings = [CatalogItem(item,"lodging") for item in data.get("lodgings", [])]
                self.excursions = [CatalogItem(item,"excursion") for item in data.get("excursions", [])]
        else: print(f"missing file")

        if os.path.exists(os.path.join(baseDir, "chaos_events_database.json")):
            with open(os.path.join(baseDir, "chaos_events_database.json"), 'r', encoding='utf-8') as f:
                self.events = [ChaosEvent(e) for e in json.load(f)]
        else: print(f"Missing chaos events file")

    def mutatePrices(self):
        volMap = {'low':(0.02, 0.05), 'medium': (0.05, 0.15), 'high': (0.10, 0.30)}
        for category in (self.flights, self.lodgings, self.excursions):
            for item in category:
                item.prevPrice = item.currentPrice
                minV, maxV = volMap.get(item.volatility, (0.02, 0.05))
                change = random.uniform(minV, maxV)*random.choice([1, -1])
                item.currentPrice = max(1, int(item.currentPrice*(1+change)))

