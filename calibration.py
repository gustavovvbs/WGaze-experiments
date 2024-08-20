import tobii_research as tr 

ets = tr.find_all_eyetrackers()
print(ets[0].model)
