#!/usr/bin/env python
# encoding=utf-8

import os
import signal
import time
from tornado.web import StaticFileHandler
from tornado.web import HTTPError


MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 2


class FileFindler(object):
    def get_absolute_path(self, path):
        raise NotImplementedError()

    def validate_absolute_path(self, path):
        """
            take care of the fs side problem
        """
        raise NotImplementedError()


class MultiFileFindler(FileFindler):
    def __init__(self, roots, default_root):
        self.roots = tuple(map(os.path.normpath, roots))
        self.default_root = os.path.normpath(default_root)

    def get_absolute_path(self, path):
        for root in self.roots:
            absolute_path = os.path.abspath(os.path.join(root, path))
            if os.path.exists(absolute_path):
                return absolute_path
        return os.path.abspath(os.path.join(self.default_root, path))

    def validate_absolute_path(self, absolute_path):
        for root in self.roots + (self.default_root,):
            if not (absolute_path + os.path.sep).startswith(root):
                continue
            return
        raise HTTPError(403, "%s is not in root static directory", absolute_path)


class SmartStaticFileHandler(StaticFileHandler):
    file_finder = None

    def initialize(self, path):
        self.root = u'<bad root>'

    @classmethod
    def get_absolute_path(cls, root, path):
        return cls.file_finder.get_absolute_path(path)

    def validate_absolute_path(self, root, absolute_path):
        self.file_finder.validate_absolute_path(absolute_path)

        if not os.path.exists(absolute_path):
            raise HTTPError(404)
        if not os.path.isfile(absolute_path):
            raise HTTPError(403, "%s is not a file", self.path)
        return absolute_path


def install_tornado_shutdown_handler(ioloop, server, logger=None):
    # see https://gist.github.com/mywaiting/4643396 for more detail
    if logger is None:
        import logging
        logger = logging

    def _sig_handler(sig, frame):
        logger.info("Signal %s received. Preparing to stop server.", sig)
        ioloop.add_callback(shutdown)

    def shutdown():
        logger.info("Stopping http server...")
        server.stop()
        logger.info("will shutdown in %s seconds", MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

        def stop_loop():
            now = time.time()
            if now < deadline and (ioloop._callbacks or ioloop._timeouts):
                ioloop.add_timeout(now + 1, stop_loop)
                logger.debug("Waiting for callbacks and timesouts in IOLoop...")
            else:
                ioloop.stop()
                logger.info("Server is shutdown")
        stop_loop()

    signal.signal(signal.SIGTERM, _sig_handler)
    signal.signal(signal.SIGINT, _sig_handler)