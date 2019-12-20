from tabulate import tabulate


def round_floats(results):
    for result in results:
        for k, v in result.items():
            try:
                result[k] = int(v)
            except ValueError:
                pass

def merge_values(results):
    for i in range(0, len(results)):
        try:
            results[i]['trueskill'] = str(results[i]['mu']) + " +/- " + str(results[i]['sigma'])
            results[i]['kd'] = str(results[i]['kills']) + " / " + str(results[i]['deaths'])
            results[i]['win/loss'] = str(results[i]['wins']) + " / " + str(results[i]['losses'])
            del results[i]['mu']
            del results[i]['sigma']
            del results[i]['wins']
            del results[i]['losses']
            del results[i]['kills']
            del results[i]['deaths']
        except:
            print( results[i])

def ctf_rankings(db):
    pipeline = [
        {
            '$lookup': {
                'from': 'players', 
                'localField': 'player', 
                'foreignField': '_id', 
                'as': 'newplayer'
            }
        }, {
            '$project': {
                'player.platform': 1, 
                'mu': 1, 
                'sigma': 1, 
                'first': {
                    '$arrayElemAt': [
                        '$newplayer', 0
                    ]
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'mu': 1, 
                'sigma': 1, 
                'result': {
                    '$subtract': [
                        '$mu', {
                            '$multiply': [
                                3, '$sigma'
                            ]
                        }
                    ]
                }, 
                'name': {
                    '$arrayElemAt': [
                        '$first.name', 0
                    ]
                }
            }
        }, {
            '$sort': {
                'result': -1
            }
        }
    ]
    result = list(db.ctf_profiles.aggregate(pipeline))[:20]
    for i in range(0, len(result)):
        result[i]['rank'] = i+1
    round_floats(result)
    rankings = tabulate(result, headers="keys")
    return "```{}```".format(rankings)


def dm_rankings(db):
    pipeline = [
        {
            '$lookup': {
                'from': 'players', 
                'localField': 'player', 
                'foreignField': '_id', 
                'as': 'newplayer'
            }
        }, {
            '$project': {
                'player.platform': 1, 
                'mu': 1, 
                'sigma': 1, 
                'first': {
                    '$arrayElemAt': [
                        '$newplayer', 0
                    ]
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'mu': 1, 
                'sigma': 1, 
                'result': {
                    '$subtract': [
                        '$mu', {
                            '$multiply': [
                                3, '$sigma'
                            ]
                        }
                    ]
                }, 
                'name': {
                    '$arrayElemAt': [
                        '$first.name', 0
                    ]
                }
            }
        }, {
            '$sort': {
                'result': -1
            }
        }
    ]
    result = list(db.dm_profiles.aggregate(pipeline))[:20]
    for i in range(0, len(result)):
        result[i]['rank'] = i+1
    round_floats(result)
    rankings = tabulate(result, headers="keys")
    return "```{}```".format(rankings)

def tdm_rankings(db):
    pipeline = [
        {
            '$lookup': {
                'from': 'players', 
                'localField': 'player', 
                'foreignField': '_id', 
                'as': 'newplayer'
            }
        }, {
            '$project': {
                'player.platform': 1, 
                'mu': 1, 
                'sigma': 1, 
                'elo': 1, 
                'kills': 1, 
                'deaths': 1, 
                'wins': 1, 
                'losses': 1, 
                'first': {
                    '$arrayElemAt': [
                        '$newplayer', 0
                    ]
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'mu': 1, 
                'sigma': 1, 
                'elo': 1, 
                'kills': 1, 
                'deaths': 1, 
                'wins': 1, 
                'losses': 1, 
                'result': {
                    '$subtract': [
                        '$mu', {
                            '$multiply': [
                                3, '$sigma'
                            ]
                        }
                    ]
                }, 
                'name': {
                    '$arrayElemAt': [
                        '$first.name', 0
                    ]
                }
            }
        }, {
            '$sort': {
                'result': -1
            }
        }
    ]

    full_result = list(db.tdm_profiles.aggregate(pipeline))
    result = full_result[:15]

    for i in range(0, len(result)):
        result[i]['rank'] = i+1
    round_floats(result)
    
    merge_values(result)
    rankings = tabulate(result , headers="keys")
    return "```{}```".format(rankings)


