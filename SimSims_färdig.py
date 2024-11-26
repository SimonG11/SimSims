from random import randint


class Product:
    """
    Ett produkt objekt som används som förbrukningsvara.
    """

    def __init__(self):
        self._product = "Järn"


class Food:
    """
    Ett matobjekt med ett slupmässigt värde kopplat till den.
    """

    def __init__(self):
        self._min = -20
        self._max = 30
        self._quality = (randint(self._min,self._max)) # Sätter ett slumpmässigt värde på matbjektet mellan min och maxvärdet.

    def get_value(self):
        return self._quality


class Barn:
    """
    Barn är ett kö objekt (FIF0 - Först In, Först Ut) där matprodukter lagras.
    Klassen kan retunera sig själv i string representation, sin längd även hämta och lämna produkter på rätt plats.
    """

    def __init__(self) -> None:
        self._stored_food = []    

    def __str__(self): #Gör att vi kan få en strängrepresentation av kön.
        return str(self._stored_food)

    def __len__(self): # Gör att vi kan använda len-funktionen på kö-objektet
        return len(self._stored_food)

    def get(self):
        return self._stored_food.pop(0) # Hämtar en produkt på första platsen

    def put(self):
        self._stored_food.insert(0, Food()) # Sätter in en produkt på första platsen


class Storges:
    """
    Storages är ett kö objekt (LIFO - Sist In, Först Ut) där prodktobjekt lagras och fördelas.
    Klassen kan retunera sig själv i string representation, sin längd även hämta och lämna produkter på rätt plats.
    """

    def __init__(self):
        self._stored_products = []

    def __str__(self): #Gör att vi kan få en strängrepresentation av kön.
        return str(self._stored_products)

    def __len__(self): # Gör att vi kan använda len-funktionen på kö-objektet
        return len(self._stored_products)

    def get(self):
        return self._stored_products.pop() # Hämtar en produkt på sista platsen

    def put(self):
        self._stored_products.insert(0, Product()) # Sätter in en produkt på första platsen


class Factories:
    """
    Factgories är object som tar in arbetarobjekt och retunerar arbetsobjekt (om objektet överlevt) och ett produktobjekt.
    """
    def __init__(self, Road_in, Road_out, Storage):
        self._danger_risk_min = -20
        self._danger_risk_max = -100
        self._storage = Storage
        self._road_in = Road_in
        self._road_out = Road_out

    def update_storage(self):
        self._storage.put() # Lägger till en produkt i storages

    def update_lifeforce(self):
        worker = self._road_in.dequeue() #hämtar första objektet från vägen
        worker.update_lifeforce(randint(self._danger_risk_max,self._danger_risk_min)) # uppdaterar arbetarens hp
        self._road_out.enqueue(worker) # Lägger tillbaka arbetaren på vägen

    def round(self):
        if len(self._road_in) == 0: #säkerställer att prgramet inte krachar om vägen är tom.
            return None
        self.update_lifeforce()
        self.update_storage()


class Fields:
    """
    Fields är object som tar in arbetarobjekt och retunerar arbetsobjekt (om objektet överlevt) och ett matobjekt.
    """

    def __init__(self, road_in, road_out, barn):
        self._danger_risk_min = -20
        self._danger_risk_max = -100
        self._barn = barn
        self._road_in = road_in
        self._road_out = road_out

    def update_barn(self):
        self._barn.put() # Lägger till ett matobjekt i barn

    def update_lifeforce(self):
        worker = self._road_in.dequeue()
        worker.update_lifeforce(randint(self._danger_risk_max,self._danger_risk_min))
        self._road_out.enqueue(worker)

    def round(self):
        if len(self._road_in) == 0: #säkerställer att prgramet inte krachar om vägen är tom.
            return None
        self.update_lifeforce()
        self.update_barn()


class Road:
    """
    Road är ett kö objekt (FIF0 - Först In, Först Ut) där workers lagras.
    Klassen kan retunera sig själv i string representation, sin längd även hämta och lämna produkter på rätt plats.
    Klassen har även en funkton som kollart om kön är tom eller inte
    """

    def __init__(self):
        self._road = []
        self._health_reduction = -5
    
    def __str__(self): #Gör att vi kan få en strängrepresentation av kön.
        return str(self._road)

    def __len__(self): # Gör att vi kan använda len-funktionen på kö-objektet
        return len(self._road)

    def is_empty(self):
        return len(self._road) == 0
        
    def enqueue(self, worker):
        if worker.get_lifeforce() > 0:
            self._road.append(worker) # Lägger till ett värde till höger (sist) i listan

    def dequeue(self):
        assert(len(self._road) > 0)
        return self._road.pop(0) # Tar bort och returnerar värdet till vänster (först) i listan.

    def front(self):
        assert(len(self._road) > 0)
        return self._road[0] # Returnerar första värdet i listan

    def round(self):
        for worker in self._road:
            worker.update_lifeforce(self._health_reduction)
            if worker.get_lifeforce() <= 0:
                self._road.remove(worker)
            

class Worker:
    """
    Worker ett objekt som har ett livskraftatribut som klassen själv kan reglera. 
    Klassen ser även till att arbetaren inte får mer livskraft än 100.
    """

    def __init__(self):
        self._lifeforce = 100

    def get_lifeforce(self):
        return self._lifeforce

    def update_lifeforce(self, amount):
        self._lifeforce = self._lifeforce + amount
        if self._lifeforce > 100:
            self._lifeforce = 100


class Cafeteria:
    """
    Cafeteria är ett klass objekt som tar in ett arbetarobjekt samt ett matobjekt
    Cafetrian uppdaterar arbetarens livskraft med värdet från matobjektet.
    Sedan retunerar cafeterien arbetern med uppdaterad livskraft.
    """

    def __init__(self,road_in, road_out, barn):
        self._barn = barn
        self._road_in = road_in
        self._road_out = road_out      

    def get_food(self):
        return self._barn.get()

    def update_lifeforce(self):
        worker = self._road_in.dequeue()
        worker.update_lifeforce(self.get_food().get_value())
        self._road_out.enqueue(worker)

    def round(self):
        if len(self._road_in) != 0 and len(self._barn) != 0:
            self.update_lifeforce()


class Home:
    """
    Home är ett klass objekt som kan göra två olika saker. 
    1. Ta in ett arbetarobjekt samt ett produkt-objekt, retunera arbetare med ökad livskraft
    2. Ta in två arbetar objekt samt ett produkt objekt, retunera 3 arbetare, 2 arbetare med samma livskraft som från början och 1 ny.
    """

    def __init__(self,road_in, road_out, storage):
        self._storages = storage
        self._road_in = road_in
        self._road_out = road_out      

    def get_product(self):
        return self._storages.get()

    def update_lifeforce(self):
        worker = self._road_in.dequeue()
        worker.update_lifeforce(randint(20,40))
        self._road_out.enqueue(worker)

    def round(self):
        _house_choice = randint(20,100)
        if _house_choice > 50:
            if len(self._road_in) >= 1 and len(self._storages) >= 1:
                self.update_lifeforce()
                self.get_product()

        if _house_choice <=50:
            if len(self._road_in) >= 2 and len(self._storages) >= 1:
                self.get_product()
                worker1 = self._road_in.dequeue()
                worker2 = self._road_in.dequeue()
                self._road_out.enqueue(worker1)
                self._road_out.enqueue(worker2)
                self._road_out.enqueue(Worker()) # Skapar en tredje arbetare

            
class Universe:
    """
    Universum objektet konstuerar sambanden mellan olika objekt, sätter in startvärden samt simulerar sambanden och värdena.
    """

    def __init__(self):
        self._r1 = Road() 
        self._r2 = Road()
        self._s1 = Storges()
        self._b1 = Barn()
        self._b2 = Barn()
        self._fi1 = Fields(self._r1, self._r1, self._b1)
        self._fi2 = Fields(self._r2, self._r2, self._b2)
        self._c1 = Cafeteria(self._r1, self._r1, self._b1)
        self._c2 = Cafeteria(self._r1, self._r2, self._b2)
        self._c3 = Cafeteria(self._r2, self._r1, self._b2)
        self._fa1 = Factories(self._r1, self._r1, self._s1)
        self._fa2 = Factories(self._r2, self._r2, self._s1)
        self._h1 = Home(self._r1, self._r1, self._s1)
        self._h2 = Home(self._r1, self._r2, self._s1)
        self._h3 = Home(self._r2, self._r1, self._s1)
        self._h4 = Home(self._r2, self._r2, self._s1)
        self._transitions = [self._fi1, self._fi2, self._c1, self._c2, self._c3, self._fa1, self._fa2, self._h1, self._h2, self._h3, self._h4, self._r1, self._r2]
        self._roads = [self._r1, self._r2]

    def starting_values(self):
        starting_num_products = 1000
        starting_num_food = 1000
        starting_num_workers = 10000
        for x in range(starting_num_products):
            self._s1.put()
        for x in range(starting_num_food):
            self._b1.put()
        for x in range(starting_num_workers):
            self._r1.enqueue(Worker())
            self._r2.enqueue(Worker())



    def roads(self): 
        Road_number = 0
        tot_workers = 0
        road_empty = False
        for road in self._roads:
            Road_number += 1
            tot_workers += len(road)
            if not road.is_empty():
                print(f"Väg {Road_number} innehåller {len(road)} arbetare")
                road_empty = True
            if road.is_empty():
                print(f"Väg {Road_number} är tom")
        print(f"Totalt antal arbetare kvar: {tot_workers}")
        return road_empty

    def simulate(self): 
        simulate = True
        Round = 0
        while simulate:
            Round +=1
            print(f"------------------ Runda {Round} ----------------")
            for x in self._transitions:
                x.round()
            simulate = self.roads()


if __name__ == "__main__":
    u1 = Universe()
    u1.starting_values()
    u1.simulate()
