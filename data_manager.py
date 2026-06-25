import json, os, random, sys

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

        self.coffeeUnlocked= False
        self.barometerUnlocked= False
        self.coffeeUsedThisWeek = False
        self.tomorrowForecast =None
        self.load_databases()

    def resourcePath(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def load_databases(self):
        baseDir = self.resourcePath("jsondata")
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

    def generateForecast(self):
        categories = [("flights",self.flights), ("lodgings",self.lodgings), ("excursions", self.excursions)]
        catName, catList= random.choice(categories)
        direction = random.choice([1, -1])
        amount=random.uniform(0.10, 0.25)
        trendWord= "rising ▲" if direction> 0 else "dropping ▼"
        text = f"Barometer: Tomorrow's {catName}{trendWord} ~{int(amount*100)}%"
        self.tomorrowForecast = {
            "category":catName,
            "change":direction*amount,
            "text": text
        }

    def mutatePrices(self):
        volMap = {'low':(0.02, 0.05), 'medium': (0.05, 0.15), 'high': (0.10, 0.30)}

        forecastCat = self.tomorrowForecast['category'] if self.tomorrowForecast else None
        forecastChange = self.tomorrowForecast['change'] if self.tomorrowForecast else 0
        for catName, category in [("flights", self.flights), ("lodgings", self.lodgings), ("excursions", self.excursions)]:
            for item in category:
                item.prevPrice = item.currentPrice
                if catName==forecastCat:
                    change=forecastChange+random.uniform(-0.02,0.02)
                else:
                    minV, maxV= volMap.get(item.volatility, (0.02, 0.05))
                    change= random.uniform(minV, maxV)*random.choice([1, -1])
                item.currentPrice = max(1, int(item.currentPrice*(1+change)))

        self.generateForecast()

    def evaluate_itinerary(self, client, itinerary):
        tags= set()
        for item in itinerary.values():
            if item: tags.update(item.tags)

        score=70
        for req in client.hiddenMustHaves:
            if req in tags: score +=15
            else: score -= 15

        for db in client.hiddenDealBreakers:
            if db in tags: score -= 30

        return score

