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
                     'rates': (4, 5),
                     'accumulated': 10,
                     'birthoffset': 10,
                     'birthmin': 15,
                 },
                 'N':
                 {
                     'consume': {'NFood': 1},
                     'produce': {'Shit': 1},
                     'rates': (5, 6),
                     'accumulated': 10,
                     'birthoffset': 10,
                     'birthmin': 15,
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
                     'rates': (1, 2),
                     'accumulated': 5,
                     'birthoffset': 10,
                     'birthmin': 20,
                 },
                 'N':
                 {
                     'consume': {'NH3': 1},
                     'produce': {'NFood': 1},
                     'rates': (3, 4),
                     'accumulated': 5,
                     'birthoffset': 10,
                     'birthmin': 20,
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
                     'rates': (5, 6),
                     'accumulated': 10,
                     'birthoffset': 20,
                     'birthmin': 40,
                 },
             }
        },
    }
}
