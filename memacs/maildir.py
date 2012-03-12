#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-011 14:11:25 daniel>

import sys
import os
import logging
from lib.memacs import Memacs
from lib.reader import CommonReader
from lib.mailparser import MailParser



class MaildirMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
           "-fp", "--folder_path",
           dest="folder_path",
           help="path to the Maildir folder"
                "path/to/Maildirfolder")


    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

        if not self._args.folder_path:
            self._parser.error("please specify the path to Maildir folder")
            

    def __read_mails_and_write(self, data):
        """
        Read all files, let Mailparser parse each mail,
        write to outputfile

        @param data: string contains a maildir email
        """
        timestamp, output, note, properties = \
            MailParser.parse_message(data)
        self._writer.write_org_subitem(timestamp,
                                           output,
                                           note,
                                           properties)
                         
    def __get_files(self, cur_path):     
                       
            listing = os.listdir(cur_path)
            for maildir_file in listing:
                path = cur_path + '/' + maildir_file
                data = CommonReader.get_data_from_file(path)
                self.__read_mails_and_write(data)
                
    def _main(self):
        """
        get's automatically called from Memacs class
        """
        if self._args.folder_path:
            cur_path = (self._args.folder_path + "/cur")
            self.__get_files(cur_path)

            
            

        