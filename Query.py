import re

import util.data_storage as ds
import util.ret as ret
import util.log as log

from obj.Series import Series
from obj.Character import Character

class Query:

    def __init__(self, x_axis: str, y_axis: str, filters: list):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.filters = filters
        self.field = []
        self.query_results = {}
        self.query_log = "New Query Created with these parameters:\n" \
            + "X-Axis: " + str(x_axis) + "\n" \
            + "Y-Axis: " + str(y_axis) + "\n"
        for f in filters:
            self.query_log += "Filter: " + str(f) + "\n"

    def make_query_list(self):
        series = data_storage.load_pickle(data_storage.ACTIVE_FILE)
        query_list = []
        filter_list = []
        if self.x_axis == 'x_characters':
            source = series.characters
        #TODO: add new x_axis parameters here
        for b in series.books:
            for c in b.chapters:
                for v in c.viewpoints:
                    self.field.append(v)
        #TODO: add more field options here
        for s in source:
            query_list.append(s)
        for f in self.filters:
            filter_re = re.match("^([a-zA-Z]+)([!<>=]=)([\S ]+)", f, re.RegexFlag.IGNORECASE)
            if not filter_re:
                self.query_log += "Unable to match filter: " + str(f) + "\n"
                continue
            subject = str.lower(filter_re.group(1))
            comparator = filter_re.group(2)
            object = str.rstrip(str.lower(filter_re.group(3)))
            for q in query_list:
                filter_result = q.apply_filter(subject, comparator, object)
                if filter_result == ret.ERROR:
                    self.query_log += "Error in filter syntax: " + str(f) + "\n"
                    break
                elif not filter_result:
                    if not q in filter_list:
                        filter_list.append(q)
        #remove items from dict based on filter_list
        for f in filter_list:
            query_list.remove(f)
        for q in query_list:
            self.query_results[q.name] = 0 #note this requires all sources to have a name
        #add field values to query_values
        for f in self.field:
            for q in query_list:
                if f.is_featured(q.name):
                    self.query_results[q.name] += int(f.wordcount)
        self.query_log += "\n"
        for q in self.query_results:
            self.query_log += q + ": " + str(self.query_results[q]) + "\n"