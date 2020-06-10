from pymongo import collection
def get_standings(db : collection.Collection, page : int):
    '''
        Gets the current standings of the ladder tournament
        @param collection: the database collection
        @param page: the page of the ladder, there are ten entries per page
    '''
    if 10 * (page - 1) > db.ladder_player.count_documents({}) or page < 1:
        return []

    players = list(db.ladder_player.aggregate([
        {
            '$project': {
                '_id': -1, 
                'name': 1,  
                'elo': 1,
                'clan_tag' : 1
            }
        }, {
            '$sort': {
                'elo': -1
            }
        }, {
            '$skip': (page - 1) * 10
        }, {
            '$limit': 10
        }
    ]))
    for p in players:
        del p['_id']
        if p['clan_tag'] == "unknown":
            p['clan_tag'] = "No clan"
    return players