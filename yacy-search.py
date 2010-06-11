import gtk
import cream
import webkit

import urllib
import thread
import json

YACY_SEARCH_URI = 'http://freeworld.walamt.de:8120/yacysearch.json?query={0}&verify=true'

class YaCySearch(cream.Module):

    def __init__(self):

        cream.Module.__init__(self)

        self.interface = gtk.Builder()
        self.interface.add_from_file('interface/interface.ui')

        self.window = self.interface.get_object('window')
        self.window.set_icon_from_file('interface/YaCyLogo2008.png')
        self.search_entry = self.interface.get_object('search_entry')
        self.search_button = self.interface.get_object('search_button')
        self.content_frame = self.interface.get_object('content_frame')

        self.view = webkit.WebView()
        self.content_frame.add(self.view)

        self.window.connect('destroy', lambda *args: self.quit())

        self.search_entry.connect('activate', self.search_cb)
        self.search_button.connect('clicked', self.search_cb)

        self.window.show_all()


    def search_cb(self, *args):

        query = self.search_entry.get_text()

        thread.start_new_thread(self.search, (query,))


    def search(self, query):

        uri = YACY_SEARCH_URI.format(query)
        result = json.loads(urllib.urlopen(uri).read())

        gtk.gdk.threads_enter()
        print result
        gtk.gdk.threads_leave()


if __name__ == '__main__':
    yacy_search = YaCySearch()
    yacy_search.main()
