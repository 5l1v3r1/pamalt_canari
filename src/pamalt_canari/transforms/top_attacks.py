#!/usr/bin/env python

import xml.etree.ElementTree as ET

from canari.framework import configure
from common.entities import topAttacks, paThreat
from common import pamod

__author__ = 'bostonlink'
__copyright__ = 'Copyright 2012, Pamalt_canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'bostonlink'
__email__ = 'bostonlink@pentest-labs.org'
__status__ = 'Development'

__all__ = [
    'dotransform',
    'onterminate'
]

@configure(
    label='To Top Attacks [PaloAlto]',
    description='Returns PaloAlto top attack alerts within the last 24 hours',
    uuids=[ 'pamalt_canari.v2.paMaltTopAttacksToThreat' ],
    inputs=[ ( 'PaloAlto', topAttacks ) ],
    debug=False
)

def dotransform(request, response):

    # Check PAN Authentication AND KEY
    key = pamod.get_login()
    # Get report XML response and parse XML
    root = ET.fromstring(pamod.pa_pred_report('top-attacks', key))
    entry_list = []

    for result in root:
        for entry in result:
            entry_dic = {}
            for data in entry:
                entry_dic[data.tag] = data.text

            entry_list.append(entry_dic)

    for d in entry_list:
        response += paThreat(
            d['threatid'],
            tid=d['tid'],
            subtype=d['subtype'],
            count=d['count']
            )

    return response