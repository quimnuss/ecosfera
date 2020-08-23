# -*- coding: utf-8 -*-


class ConsumerProducer:
    
    def __init__(self, entity, id, consume, produce, rates, accumulated=3):
        self.entity = entity
        self.id = id
        self.reason = None
        self.accumulated = accumulated
        self.consumeRecipe = consume
        self.produceRecipe = produce
        self.rates = rates
        self.consumeTimer = 0
        self.produceTimer = 0
    
    def displayName(self):
        return self.id
    
    def consume(self, pool):
        recipePoolResult = {k: (pool[k] - v) for k,v in self.consumeRecipe.items()}
        if any(v < 0 for v in recipePoolResult.values()):
            self.reason = {k:v for k, v in recipePoolResult.items() if v < 0}
            return False
        self.accumulated = self.accumulated+1
        pool.update(recipePoolResult)
        return True

    
    def produce(self, pool):
        if self.accumulated > 0:
            self.accumulated = self.accumulated-1
            newpool = pool
            newpool.update({k: pool[k] + v for k,v in self.produceRecipe.items()})
            return True
        else:
            return False

    def breakout(self, pool):
        pool.update({k: pool[k] + v*self.accumulated for k,v in self.produceRecipe.items()})
        self.accumulated = 0

    def snapshot(self):
        return f"{self.id}: {self.accumulated}"

    def tick(self, pool):
        consumed = None
        if self.consumeTimer <= 0:
            consumed = self.consume(pool)
            self.consumeTimer = self.rates[0]
        else:
            self.consumeTimer = self.consumeTimer-1
            
        produced = None
        if self.consumeTimer <= 0:
            produced = self.produce(pool)
            self.produceTimer = self.rates[1]
        else:
            self.produceTimer = self.produceTimer-1
            
        return consumed, produced


class Game:
    def __init__(self):
        self.tickCount = 0
        self.entities = []
        self.pool = {
            'O2': 5, 
            'CO2': 5,
        }
        self.poolhistory = []
        self.poolhistory.append(self.pool)
        self.log = []
    
    def loadWorld(self, yaml):
        shrimp1_C = ConsumerProducer(entity="Shrimp1", id="Shrimp1_C", consume={'O2': 1}, produce={'CO2': 1}, rates=(4,6), accumulated=10)
        self.entities.append(shrimp1_C)
        algae1_C = ConsumerProducer(entity="Algae1", id="Algae1_C", consume={'CO2': 1}, produce={'O2': 1}, rates=(2,3), accumulated=10)
        self.entities.append(algae1_C)
        
        self.entities.sort(key=lambda e: e.id)
        print(" ".join(f"{e.id}" for e in self.entities))
    
    def tick(self):
        dead = []

        for e in self.entities:
            didConsume, didProduce = e.tick(self.pool)
            if didConsume == False:
                self.log.append(f"{self.tickCount} {e.displayName()} failed consumption - {e.reason}")
            if didProduce == False:
                dead.append(e)
                self.log.append(f"{e.id} died because {e.reason}")
                print(f"{e.id} died because {e.reason}")

        survivors = []
        for e in self.entities:
            if any(e.entity == d.entity for d in dead):
                e.breakout(self.pool)
            else:
                survivors.append(e)
        
        survivors.sort(key=lambda e: e.id)
        self.entities = survivors
        self.poolhistory.append(self.pool)
        self.tickCount = self.tickCount+1
        
    def snapshot(self):
        self.entities.sort(key=lambda e: e.id)
        entitiesSnapshot = (" ".join(f"{e.id}: {e.accumulated}\t" for e in self.entities))
        return str(self.pool) + ' -- ' + entitiesSnapshot




if __name__ == "__main__":
    g = Game()
    g.loadWorld("world1.yaml")
    for i in range(300):
        g.tick()
        print(f"{g.tickCount}: {g.snapshot()}")

