import functools
import requests
import matplotlib.pyplot as plt
import numpy as np

list = ['alabama', 'alaska', 'arizona', 'arkansas', 'california',
        'colorado','connecticut', 'delaware', 'florida', 'georgia', 'hawaii',
        'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky',
        'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan',
        'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska',
        'nevada', 'new-hampshire', 'new-jersey', 'new-mexico', 'new-york',
        'north-carolina', 'north-dakota', 'ohio', 'oklahoma', 'oregon',
        'pennsylvania', 'rhode-island', 'south-carolina', 'south-dakota',
        'tenneessee', 'texas', 'utah', 'vermont', 'virginia','washington',
        'west-virginia', 'wisconsin', 'wyoming']

for state in list:
    arrayAll = []
    arrayi = []
    arrayB = []
    arrayT = []
    array3 = []

    x = requests.get(f'https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/{state}/president.json').json()['data']['races'][0]['timeseries']

    for i, item in enumerate(x[1:],1):
        total= item['votes']
        time = item['timestamp']
        added = item['votes']-x[i-1]['votes']
        perB = item['vote_shares']['bidenj']
        perT = item['vote_shares']['trumpd']
        per3 = 1 - perB - perT
        totalB = perB*total
        totalT = perT*total
        total3 = per3*total
        addedB = totalB-x[i-1]['vote_shares']['bidenj']*x[i-1]['votes']
        addedT = totalT-x[i-1]['vote_shares']['trumpd']*x[i-1]['votes']
        added3 = added-addedB-addedT
        if added != 0:
            perAddB = addedB/added
            perAddT = addedT/added
            perAdd3 = added3/added

            arrayi.append(i)
            arrayAll.append(total)
            arrayB.append(perAddB*100)
            arrayT.append(perAddT*100)
            array3.append(perAdd3*100)

    plt.plot(arrayi, arrayB, 'b.', arrayi, arrayT, 'r.',
             arrayi, array3, 'g.')
    plt.grid(True)
    plt.legend(('biden', 'trump', '3rd party'))
    plt.title(state)
    plt.xlabel('drop number')
    plt.ylabel('percentage of votes/drop')
    plt.hlines(y = 100, xmin = -20, xmax = arrayi[-1]+20)
    plt.hlines(y = 0, xmin = -20, xmax = arrayi[-1]+20)
    plt.text(100, 0, '100%', ha='left', va='center')
    plt.text(-10,100,'100%')
    plt.yscale('log')
    filename = 'plots/president_by_drops_percentage/' + state + '.png'
    figure = plt.gcf()
    figure.set_size_inches(24,16)
    plt.savefig(filename, dpi=400)
    plt.clf()

