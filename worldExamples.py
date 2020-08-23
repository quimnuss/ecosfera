# -*- coding: utf-8 -*-

world1 = {
    'pool': 
    {
        'O2': 3, 
        'CO2': 3,
        'CFood': 0,
        'NFood': 0,
        'Shit': 0,
        'NH3': 3,
    },
    'entities': 
    [
        {
         'entityType': 'Shrimp',
        },
        {
         'entityType': 'Shrimp',
         'cycles':
         {
             'C':
             {
                 'accumulated': 4,
             }
         }
        },
        {
         'entityType': 'Shrimp',
        },
        {
         'entityType': 'Algae',
        },
        {
         'entityType': 'Bacteria',
        },
        {
         'entityType': 'Bacteria',
        },
        {
         'entityType': 'Bacteria',
        }
    ],
    'entitiesBase': 
    {
        'Shrimp': 
        {
             'cycles': 
             {
                 'C': 
                 {
                     'consume': {'O2': 1, 'CFood': 1},
                     'produce': {'CO2': 1},
                     'rates': (2, 3),
                     'accumulated': 10,
                 },
                 'N':
                 {
                     'consume': {'NFood': 1},
                     'produce': {'Shit': 1},
                     'rates': (2, 3),
                     'accumulated': 10,
                 },
             }
        },
        'Algae':
        {
             'cycles': 
             {
                 'C':
                 {
                     'consume': {'CO2': 1},
                     'produce': {'O2': 1, 'CFood': 1},
                     'rates': (3, 4),
                     'accumulated': 10,
                 },
                 'N':
                 {
                     'consume': {'NH3': 1},
                     'produce': {'NFood': 1},
                     'rates': (4, 5),
                     'accumulated': 10,
                 },
             }
        },
        'Bacteria': 
        {
             'cycles': 
             {
                 'N':
                 {
                     'consume': {'Shit': 1},
                     'produce': {'NH3': 1},
                     'rates': (6, 8),
                     'accumulated': 10,
                 },
             }
        },
    }
}