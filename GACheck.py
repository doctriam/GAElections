import functools
import requests

state = 'georgia'

x = requests.get(f'https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/{state}/president.json').json()['data']['races'][0]['timeseries']

subTotal = 0
subB = 0
subT = 0
sub3 = 0
badB = 0
badT = 0
bad3 = 0

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
    addedB = totalB - x[i-1]['vote_shares']['bidenj']*x[i-1]['votes']
    addedT = totalT - x[i-1]['vote_shares']['trumpd']*x[i-1]['votes']
    added3 = added - addedB - addedT

    if added < (addedB or addedT or added3) or (added or addedB or addedT or added3) < 0:
        print("Dump %d: %s" % (i, time))
        print("Total Count = %.2f, Added this dump = %.2f" % (total, added))
        print("Biden Total = %.2f, Biden Added = %.2f" % (totalB, addedB))
        print("Trump Total = %.2f, Trump Added = %.2f" % (totalT, addedT))
        print("3rd Party Total = %.2f, 3rd Added = %.2f" % (total3, added3))
        print("----------------------------")
        badB = badB + addedB
        badT = badT + addedT
        bad3 = bad3 + added3

    if (added < 0):
        subTotal = subTotal + added
    if (addedB < 0):
        subB = subB + addedB
    if (addedT < 0):
        subT = subT + addedT
    if (added3 < 0):
        sub3 = sub3 + added3

bad = badB + badT + bad3
print("Total subtracted = ", subTotal)
print("Total subtracted from Biden = ", subB)
print("Total subtracted from Trump = ", subT)
print("Total subtracted from 3rd party = ", sub3)
print("Clearly false dumps:")
print("    Total = ", bad)
print("    Biden Bad Totals = ", badB)
print("    Trump Bad Totals = ", badT)
print("    3rd Bad Totals = ", bad3)
