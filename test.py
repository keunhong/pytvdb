from thetvdb import *

API_KEY = ''

api = TheTVDB(API_KEY)
series = api.get_series_all_by_id(79335)
for i in series.episodes:
    print "%s %s %s" % (i.season_number, i.number, i.name)

found = api.get_series_by_search("Lost");
for i in found:
    print "%s %s" % (i.name, i.id)

episode = api.get_episode_by_number(79335, 1, 1);
print episode.name
