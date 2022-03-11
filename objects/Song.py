class Song(object):
    def __init__(self,title, url):
        self.title = title
        self.url = url
        
    def toList(self):
        return [self.title, self.url]

    def getUrl(self):
        return self.url
    
    def getTitle(self):
        return self.title