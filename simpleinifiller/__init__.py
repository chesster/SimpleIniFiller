#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
import ConfigParser
import logging

logger = logging.getLogger('SimpleIniFiller')

def debug(string):
    logger.debug(string)

class SimpleIniFiller(object):

    def __init__(self, config_filename, config_parameters = {}):
        super(SimpleIniFiller, self).__init__()
        self.config = self.config_parameters = {}
        self.config_filename = expanduser('~/%s' % config_filename)
        self.config_parser = ConfigParser.ConfigParser()
        self._map()
        self._map_config_parameters(config_parameters)
        self._find_missing()

    def _map(self):
        self.config_parser.read(self.config_filename)
        for section in self.config_parser.sections():
            self.config[section] = self._section_map(section)

    def _map_config_parameters(self, config_parameters):
        for k in config_parameters.keys():
            for parameter in config_parameters[k]:
                config_parameters[k][config_parameters[k].index(parameter)] = parameter.lower()
        self.config_parameters = config_parameters

    def _section_map(self, section):
        dict1 = {}
        options = self.config_parser.options(section)
        for option in options:
            try:
                dict1[option] = self.config_parser.get(section, option)
                if dict1[option] == -1:
                    debug("skip: %s" % option)
            except:
                debug("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def _find_missing(self):
        for k in self.config_parameters.keys():
            for parameter in self.config_parameters[k]:
                current_param = {
                    'section': k,
                    'parameter': parameter,
                }
                parram = None
                if self.config.get(k):
                    parram = self.config[k].get(parameter, None)
                if parram:
                    debug("Found: %(section)s: %(parameter)s" % current_param)
                else:
                    debug("NOT Found: %(section)s: %(parameter)s" % current_param)
                    self._fill_missing(**current_param)
        self._map()

    def _fill_missing(self, section, parameter, parameter_default_value = ''):
        cfgfile = open(self.config_filename ,'w')
        try:
            self.config_parser.add_section(section)
        except ConfigParser.DuplicateSectionError, e:
            debug("Section %s is present" % section)

        self.config_parser.set(section, parameter, raw_input('Enter %s: '% (parameter,))  or parameter_default_value)
        self.config_parser.write(cfgfile)
        cfgfile.close()
