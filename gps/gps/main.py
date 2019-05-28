"""
 Created by hanruida on 2019-03-22
"""

import sys
import os
from scrapy.cmdline import execute

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

execute(['scrapy', 'crawl', 'gpsspg'])