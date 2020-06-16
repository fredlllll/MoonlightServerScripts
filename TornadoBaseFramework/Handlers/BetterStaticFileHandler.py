from tornado.web import StaticFileHandler
import datetime
import mimetypes


class BetterStaticFileHandler(StaticFileHandler):
    """
    better cause it handles cache according to modified time
    added this so browser properly updated out of date files
    """
    last_modified_cache = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_headers(self):
        self.set_header("Accept-Ranges", "bytes")
        self.set_etag_header()

        if self.modified is not None:
            self.set_header("Last-Modified", self.modified)

        content_type = mimetypes.guess_type(self.path)
        if content_type[0] is not None:
            self.set_header("Content-Type", content_type[0])

        cache_time = self.get_cache_time(self.path, self.modified, content_type)

        if cache_time > 0:
            self.set_header("Expires", datetime.datetime.utcnow() + datetime.timedelta(seconds=cache_time))
            self.set_header("Cache-Control", "max-age=" + str(cache_time))
        elif cache_time < 0:  # added this to default behaviour
            self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

        self.set_extra_headers(self.path)

    def _get_set_cached_last_modified(self, path, modified):
        """
        returns the last modified from cache and write the new modified in its place
        :param path: path to file
        :param modified: new modified date
        :return:
        """

        lm = self.last_modified_cache.get(path, 0)
        self.last_modified_cache[path] = modified
        return lm

    def get_cache_time(self, path, modified, mime_type):
        if "v" in self.request.arguments:
            return self.CACHE_MAX_AGE

        cached_modified = self._get_set_cached_last_modified(path, modified)
        if cached_modified != modified:  # invalidate if modified has changed since last time
            return -1

        return 0
