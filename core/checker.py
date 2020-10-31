import re
import copy
from fuzzywuzzy import fuzz
from core.config import xsschecker
from urllib.parse import quote_plus
from core.requester import requester
from core.utils import replacer, fillHoles

def checker(url, params, headers, GET, delay, payload, positions, timeout):
    checkString = 'st4r7s' + payload + '3nd'
    paramsCopy = copy.deepcopy(params)
    response = requester(url, replacer(paramsCopy, xsschecker, checkString), headers, GET, delay, timeout).text.lower()
    reflectedPositions = []
    for match in re.finditer('st4r7s', response):
        reflectedPositions.append(match.start())
    filledPositions = fillHoles(positions, reflectedPositions)
    # Itretating over the reflections
    num = 0
    efficiencies = []
    for position in filledPositions:
        allEfficiencies = []
        try:
            reflected = response[reflectedPositions[num]:reflectedPositions[num]+len(checkString)]
            efficiency = fuzz.partial_ratio(reflected, checkString.lower())
            allEfficiencies.append(efficiency)
        except IndexError:
            pass
        if position:
            reflected = response[position:position+len(checkString)]
            efficiency = fuzz.partial_ratio(reflected, checkString.lower())
            if reflected[:-2] == ('\\%s' % checkString.replace('st4r7s', '').replace('3nd', '')):
                efficiency = 90
            allEfficiencies.append(efficiency)
            efficiencies.append(max(allEfficiencies))
        else:
            efficiencies.append(0)
        num += 1
    return list(filter(None, efficiencies))