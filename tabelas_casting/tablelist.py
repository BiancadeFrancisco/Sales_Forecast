
import json
import pathlib
lojas = {'lojas': ['DB063',
                   'DB069', 
                   'DB088',
                   'DB092',
                   'DB101',
                   'DB102',
                   'DB108',
                   'DB109',
                   'DB113']}
with open(f'.\\lojas.json','w') as fi:
    json.dump(lojas,fi)