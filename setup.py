#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import glob, os, re, setuptools, sys
from os.path import join, isfile

# List all data files
def data():
    files = []
    for root, dirnames, filenames in os.walk('openerp'):
        for filename in filenames:
            if not re.match(r'.*(\.pyc|\.pyo|\~)$',filename):
                files.append(os.path.join(root, filename))
    d = {}
    for v in files:
        k=os.path.dirname(v)
        if k in d:
            d[k].append(v)
        else:
            d[k]=[v]
    r = d.items()
    if os.name == 'nt':
        r.append(("Microsoft.VC90.CRT", glob.glob('C:\Microsoft.VC90.CRT\*.*')))

    import babel
    r.append(("localedata",
              glob.glob(os.path.join(os.path.dirname(babel.__file__), "localedata" , '*'))))

    return r

def gen_manifest():
    file_list="\n".join(data())
    open('MANIFEST','w').write(file_list)

if os.name == 'nt':
    sys.path.append("C:\Microsoft.VC90.CRT")

def py2exe_options():
    if os.name == 'nt':
        import py2exe
        return {
            "console" : [ { "script": "openerp-server", "icon_resources": [(1, join("install","openerp-icon.ico"))], }],
            'options' : {
                "py2exe": {
                    "skip_archive": 1,
                    "optimize": 2,
                    "dist_dir": 'dist',
                    "packages": [ "DAV", "HTMLParser", "PIL", "asynchat", "asyncore", "commands", "dateutil", "decimal", "email", "encodings", "imaplib", "lxml", "lxml._elementpath", "lxml.builder", "lxml.etree", "lxml.objectify", "mako", "openerp", "poplib", "pychart", "pydot", "pyparsing", "reportlab", "select", "simplejson", "smtplib", "uuid", "vatnumber", "vobject", "xml", "xml.dom", "yaml", ],
                    "excludes" : ["Tkconstants","Tkinter","tcl"],
                }
            }
        }
    else:
        return {}

execfile(join(os.path.dirname(__file__), 'openerp', 'release.py'))

setuptools.setup(
      name             = 'openerp',
      version          = version,
      description      = description,
      long_description = long_desc,
      url              = url,
      author           = author,
      author_email     = author_email,
      classifiers      = filter(None, classifiers.split("\n")),
      license          = license,
      scripts          = ['openerp-server'],
      data_files       = data(),
      packages         = setuptools.find_packages(),
      dependency_links = ['http://download.gna.org/pychart/'],
      #include_package_data = True,
      install_requires = [
          'pychart',
          'babel',
          'docutils',
          'feedparser',
          'gdata',
          'lxml < 3',
          'mako',
          'psutil',
          'psycopg2',
          'pydot',
          'python-dateutil < 2',
          'python-ldap',
          'python-openid',
          'pytz',
          'pywebdav',
          'pyyaml',
          'reportlab',
          'simplejson',
          'vatnumber',
          'vobject',
          'werkzeug',
          'xlwt',
          'zsi',
      ],
      extras_require = {
          'SSL' : ['pyopenssl'],
      },
      tests_require = ['unittest2'],
      **py2exe_options()
)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
