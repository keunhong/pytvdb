import urllib
import urllib2
import xml.etree.ElementTree as ETree

class TheTVDB:
    """Implementation of the TheTVDB API in Python"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_mirror_url = "http://www.thetvdb.com"
        self.api_base_url = "%s/api" % self.api_mirror_url
        self.api_key_url = "%s/%s" % (self.api_base_url, self.api_key)
        
    class Series:
        def __init__(self, tree, is_search=False):
            if tree is None: return
            
            st = tree.find("Series")
            if st is None: 
                st = tree
            
            # Available in search mode
            self.id = st.findtext("id")
            self.name = st.findtext("SeriesName")
            self.language = st.findtext("Language")
            self.overview = st.findtext("Overview")
            self.first_aired = st.findtext("FirstAired")
            
            self.imdb_id = st.findtext("IMDB_ID")
            self.zap2it_id = st.findtext("zap2it_id")
            
            self.banner_img = st.findtext("banner")
            #
            
            if is_search: return
            
            self.air_day = st.findtext("Airs_DayOfWeek")
            self.air_time = st.findtext("Airs_Time")
            self.content_rating = st.findtext("ContentRating")
            
            try:
                self.actors = [x for x in st.findtext("Actors").split("|") if x]
            except AttributeError:
                pass
                
            try:
                self.genre = [x for x in st.findtext("Genre").split("|") if x]
            except AttributeError:
                pass
                
            self.network = st.findtext("Network")
            #self.network_id = st.findtext("NetworkID")
            self.rating = st.findtext("Rating")
            self.runtime = st.findtext("Runtime")
            self.status = st.findtext("Status")
            self.fanart_img = st.findtext("fanart")
            self.last_updated = st.findtext("lastupdated")

            
            et = tree.findall("Episode")
            if et is None: return
            
            self.episodes = [TheTVDB.Episode(x) for x in et]
        
    class Episode:
        def __init__(self, tree):
            if tree is None: return
            
            et = tree.find("Episode")
            if et is None:
                et = tree
            
            self.id = et.findtext("id")
            
            self.series_id = et.findtext("series_id")
            
            # dvd info
            self.dvd_chapter = et.findtext("DVD_chapter")
            self.dvd_discid = et.findtext("DVD_discid")
            self.dvd_episodenumber =et.findtext("DVD_episodenumber")
            self.dvd_season = et.findtext("DVD_season")
            
            # info
            self.name = et.findtext("EpisodeName")
            self.number = et.findtext("EpisodeNumber")
            self.director = et.findtext("Director")
            self.first_aired = et.findtext("FirstAired")
            try:
                self.guest_stars = [x for x in et.findtext("GuestStars").split("|") if x]
            except AttributeError:
                pass
            self.imdb_id = et.findtext("IMDB_ID")
            self.language = et.findtext("language")
            self.overview =et.findtext("overview")
            self.production_code = et.findtext("ProductionCode")
            self.rating = et.findtext("Rating")
            self.season_number = et.findtext("SeasonNumber")
            self.writer = et.findtext("Writer")
            
            self.airsafter_season = et.findtext("airsafter_season")
            self.airsbefore_episode = et.findtext("airsbefore_episode")
            self.airsbefore_season = et.findtext("airsbefore_season")
            
            self.lastupdated = et.findtext("lastupdated")
            
            # Artwork
            self.artwork_img = et.findtext("filename")
            
            # ??
            self.ep_img_flag = et.findtext("EpImgFlag")
            self.combined_episode_number = et.findtext("Combined_episodenumber")
            self.combined_season = et.findtext("Combined_season")
            self.absolute_number = et.findtext("absolute_number")
            self.season_id = et.findtext("season_id")


    # XML related functions
    def get_xml_raw(self, url):
        try:
            data = urllib2.urlopen(url)
        except URLError as e:
            print e
        return data
        
    def get_xml_tree(self, url):
        data = self.get_xml_raw(url)
        if(data):
            try:
                tree = ETree.parse(data)
            except SyntaxError:
                print "Syntax Error"
            else:
                return tree

    
    def get_series_by_search(self, series_name):
        params = urllib.urlencode({"seriesname" : series_name})
        query_url = "%s/GetSeries.php?%s" % (self.api_base_url, params)
        tree = self.get_xml_tree(query_url)
        series = tree.findall("Series")
        return [self.Series(x, True) for x in series if x]
        
    def get_series_by_id(self, id):
        query_url = "%s/series/%s" % (self.api_key_url, id)
        tree = self.get_xml_tree(query_url)
        return self.Series(tree)
        
    def get_series_all_by_id(self, id):
        query_url = "%s/series/%s/all" % (self.api_key_url, id)
        tree = self.get_xml_tree(query_url)
        return self.Series(tree)
        
    def get_episode_by_number(self, series_id, season_number, episode_number):
        query_url = "%s/series/%s/default/%s/%s" % (self.api_key_url, series_id, season_number, episode_number)
        tree = self.get_xml_tree(query_url)
        return self.Episode(tree)
        
    def get_episode_by_id(self, id):
        query_url = "%s/episode/%s/" % (self.api_key_url, id)
        tree = self.get_xml_tree(query_url)
        return self.Episode(tree)
        