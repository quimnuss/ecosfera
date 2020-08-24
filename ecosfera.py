# -*- coding: utf-8 -*-
# libraries
from bokeh.io import output_notebook, show
output_notebook()
from bokeh.plotting import figure, output_file, show

from worldExamples import world1

class EcosferaException(Exception):
    """Base class for other exceptions"""
    pass

class WorldFactory:

    def __init__(self):
        self.entityTypes = ['Shrimp', 'Algae', 'Bacteria']
        self.lasteid = {k:0 for k in self.entityTypes}
        self.entitiesBase = []

    def printWorld(self, entities, pool):
        entitiesStr = " ".join(e.eid for e in entities)
        print(entitiesStr)
        print(pool)

    def createWorld(self, serializedWorld):
        entities = []
        pool = serializedWorld['pool']
        self.entitiesBase = serializedWorld['entitiesBase']

        entities = [cp for entityDict in serializedWorld['entities'] for cp in self.createEntity(entityDict)]

        return entities, pool

    def createEntity(self, serializedEntity):

        cps = []
        # create base instance
        entityType = serializedEntity['entityType']
        entityName = self.nextName(entityType)

        for c in self.entitiesBase[entityType]['cycles'].keys():
            cp = self.createConsumerProducer(entityName, serializedEntity['entityType'], c)

            # TODO update dictionary of serializedEntity instead of updated the accumulated value
            # update if it's there
            cp.accumulated = serializedEntity.get('cycles', {}).get(c,{}).get('accumulated', cp.accumulated)
            cps.append(cp)

        return cps

    def nextName(self, entityType):
        entityName = entityType+str(self.lasteid[entityType])
        self.lasteid[entityType] += 1
        return entityName

    def unpackCPValues(self, entityType, cycleName):

        consumeDict = self.entitiesBase[entityType]['cycles'][cycleName]['consume'] # 'consume': [('CO2', 1, 2)],
        produceDict = self.entitiesBase[entityType]['cycles'][cycleName]['produce']

        arates      = self.entitiesBase[entityType]['cycles'][cycleName]['rates']
        startAccumulated = self.entitiesBase[entityType]['cycles'][cycleName]['accumulated']

        return consumeDict, produceDict, arates, startAccumulated

    def createConsumerProducer(self, entityName, entityType, cycleName):
        if entityType in self.entityTypes:
            neweid = entityName+'_'+cycleName

            consumeDict, produceDict, arates, startAccumulated = self.unpackCPValues(entityType, cycleName)

            newCP = ConsumerProducer(
                entityType=entityType,
                entityName=entityName,
                eid=neweid,
                consume=consumeDict,
                produce=produceDict,
                rates=arates,
                accumulated=startAccumulated
            )
            return newCP

        raise EcosferaException(f"Unknown ConsumerProducer Type '{entityType}'")


class ConsumerProducer:

    def __init__(self, entityName, entityType, eid, consume, produce, rates, accumulated=3):
        self.entityName = entityName
        self.entityType = entityType
        self.eid = eid
        self.reason = None
        self.accumulated = accumulated
        self.consumeRecipe = consume # {'O2': 1, 'CFood': 1}
        self.produceRecipe = produce # {'CO2': 1}
        self.rates = rates
        self.consumeTimer = 0
        self.produceTimer = 0

    def displayName(self):
        return self.eid

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
        return f"{self.eid}: {self.accumulated}"

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
        self.plotdata = {'time' : [],}

    def loadWorld(self, yaml):
        shrimp1_C = ConsumerProducer(entityName="Shrimp1", eid="Shrimp1_C", consume={'O2': 1}, produce={'CO2': 1}, rates=(4,6), accumulated=10)
        self.entities.append(shrimp1_C)
        algae1_C = ConsumerProducer(entityName="Algae1", eid="Algae1_C", consume={'CO2': 1}, produce={'O2': 1}, rates=(2,3), accumulated=10)
        self.entities.append(algae1_C)

        self.entities.sort(key=lambda e: e.eid)
        print(" ".join(f"{e.eid}" for e in self.entities))

    def setState(self, entities, pool):
        self.entities = entities
        self.entities.sort(key=lambda e: e.eid)
        self.pool = pool

    def tick(self):
        dead = []

        for e in self.entities:
            didConsume, didProduce = e.tick(self.pool)
            if didConsume == False:
                self.log.append(f"{self.tickCount} {e.displayName()} failed consumption - {e.reason}")
            if didProduce == False:
                dead.append(e)
                self.log.append(f"{e.eid} died because {e.reason}")
                print(f"{e.eid} died because {e.reason}")

        survivors = []
        for e in self.entities:
            if any(e.entityName == d.entityName for d in dead):
                e.breakout(self.pool)
            else:
                survivors.append(e)

        survivors.sort(key=lambda e: e.eid)
        self.entities = survivors
        self.poolhistory.append(self.pool)
        self.tickCount = self.tickCount+1

    def snapshot(self):
        if not self.entities:
            return str(self.pool) + ' -- ' + "Dead Ecosystem"
        self.entities.sort(key=lambda e: e.eid)
        entitiesSnapshot = (" ".join(f"{e.eid}: {e.accumulated}\t" for e in self.entities))
        return str(self.pool) + ' -- ' + entitiesSnapshot


class PlotManager:

    def __init__(self):
        self.df = None

    def initialize(self, ):
        # Data
        pass

    def plot(self):
        # multiple line plot
        plt.plot( 'x', 'y1', data=self.df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
        plt.plot( 'x', 'y2', data=self.df, marker='', color='olive', linewidth=2)
        plt.plot( 'x', 'y3', data=self.df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
        plt.legend()
        plt.show()


if __name__ == "__main__":

    factory = WorldFactory()

    entities, pool = factory.createWorld(world1)
    factory.printWorld(entities, pool)

    g = Game()
    g.setState(entities, pool)
    print("Start simulation")
    for i in range(300):
        g.tick()
        print(f"{g.tickCount}: {g.snapshot()}")

    # p = PlotManager()
    # p.initialize()
    # p.plot()

    # #on spyder, to show plots, run %matplotlib auto

    # # prepare some data
    # x = [1, 2, 3, 4, 5]
    # y = [6, 7, 2, 4, 5]

    # # output to static HTML file
    # output_file("lines.html")

    # # create a new plot with a title and axis labels
    # p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # # add a line renderer with legend and line thickness
    # p.line(x, y, legend_label="Temp.", line_width=2)

    # # show the results
    # show(p)
