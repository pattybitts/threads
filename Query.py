import data_storage, re, ret, log
from Series import Series

class Query:

    def __init__(self, x_axis: str, y_axis: str, filters: list):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.filters = filters
        self.series = data_storage.load_pickle(data_storage.ACTIVE_FILE)
        self.field = []
        self.query_list = []
        self.query_values = {}
        self.query_log = "New Query Created with these parameters:\n" \
            + "X-Axis: " + str(x_axis) + "\n" \
            + "Y-Axis: " + str(y_axis) + "\n"
        for f in filters:
            self.query_log += "Filter: " + str(f) + "\n"
    
    def make_query_list(self):
        if self.x_axis == 'x_characters':
            source = self.series.characters
        #TODO: add new x_axis parameters here
        for b in self.series.books:
            for c in b.chapters:
                for v in c.viewpoints:
                    self.field.append(v)
        #TODO: add more field options here
        #make initial query list
        for s in source:
            self.query_list.append(s)
        #remove items from query list based on filters
        for f in self.filters:
            filter_re = re.match("^([a-zA-Z]+)([!<>=]=)([\S ]+)", f, re.RegexFlag.IGNORECASE)
            if not filter_re:
                self.query_log += "Unable to match filter: " + str(f)
                continue
            subject = str.lower(filter_re.group(1))
            comparator = filter_re.group(2)
            object = str.rstrip(str.lower(filter_re.group(3)))
            for q in self.query_list:
                filter_result = q.apply_filter(subject, comparator, object)
                if filter_result == ret.ERROR:
                    self.query_log += "Error in filter syntax: " + str(f)
                elif not filter_result:
                    self.query_list.remove(q)
        #create dictionary with remaining items
        for q in self.query_list:
            self.query_values[q.name] = 0
        #add field values to query_values
        for f in self.field:
            for q in self.query_list:
                if f.is_featured(q.name):
                    self.query_values[q.name] += int(f.wordcount)
        for q in self.query_values:
            self.query_log += q + ": " + str(self.query_values[q]) + "\n"

    def output_query_results(self):
        return self.query_log
        
            






    