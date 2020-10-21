from data.models import FinanceData
from typing import List, Iterator
import time, datetime


class IFilter:
    def filter(self, unfiltered_content: List[FinanceData]):
        pass
    def to_object(self):
        """
        to_object() -> serialized: dict
        """
        pass
    
    @classmethod
    def from_object(cls, data_object: dict):
        pass
            
    
class TagFilter(IFilter):
    
    IDENTIFIER = 'TF'
    def __init__(self, tag_name):
        self.tag_name = tag_name
    
    def filter(self, unfiltered_content: List[FinanceData]):
        """
        filter(unfiltered_content: list of FinanceData>) -> filtered_content: list of FinanceData
        """
        output = []
        for piece in unfiltered_content:
            if self.tag_name in piece.tags:
                output.append(piece)
        return output
    
    def to_object(self):
        return {
            'identifier': self.IDENTIFIER,
            'tag-name': self.tag_name
        }
    def __repr__(self):
        return '< filter tag name = "%s" >'%self.tag_name

    @classmethod
    def from_object(cls, data_object: dict):
        return TagFilter(data_object.get('tag-name'))
    

class KeyWordFilter(IFilter):
    
    IDENTIFIER = 'KWF'
    def __init__(self, key_words):
        self.key_words = key_words
        if(len(self.key_words) < 1) # error case; here we bypass this filter to make it more rubust.
            self._bypassed = True
    
    def filter(self, unfiltered_content: List[FinanceData]):
        """
        filter(unfiltered_content: list of FinanceData>) -> filtered_content: list of FinanceData
        """
        if self._bypassed:
            return unfiltered_content
        output = []
        for key_word in self.key_words:
            for piece in unfiltered_content:
                if key_word in piece.description:
                    output.append(piece)
        
        return output
    
    def to_object(self):
        return {
            'identifier': self.IDENTIFIER,
            'key-words': self.key_words
        }

    @classmethod
    def from_object(cls, data_object: dict):
        return KeyWordFilter(data_object.get('key-words'))
    
    def __repr__(self):
        return '< filter keywords in {%s} >'%', '.join(self.key_words)

class DateRangeFilter(IFilter):
    
    IDENTIFIER = 'DRF'
    
    def __init__(self, date_from, date_to):
        
        if date_from is None:
            date_from = 0.0
        if date_to is None:
            date_to = time.time() * 1.28
            
        if type(date_from) == float:
            self.date_from = date_from
        else:
            self.date_from = time.mktime(datetime.datetime.strptime(date_from, "%Y-%m-%d").timetuple())
        
        if type(date_to) == float:
            self.date_to = date_to
        else:
            self.date_to = time.mktime(datetime.datetime.strptime(date_to, "%Y-%m-%d").timetuple())
    
    def filter(self, unfiltered_content: List[FinanceData]):
        """
        filter(unfiltered_content: list of FinanceData>) -> filtered_content: list of FinanceData
        """
        output = []
        for piece in unfiltered_content:
            if self.date_from <= piece.timestamp.timestamp() <= self.date_to:
                output.append(piece)
        return output
    
    def to_object(self):
        return {
            'identifier': self.IDENTIFIER,
            'date-from': self.date_from,
            'date-to': self.date_to
        }

    @classmethod
    def from_object(cls, data_object: dict):
        return DateRangeFilter(data_object.get('date-from'),data_object.get('date-to'),)
    def __repr__(self):
        return '< filter date from "%s" to "%s" >'%(time.strftime("%Y-%m-%d", time.localtime(self.date_from)), time.strftime("%Y-%m-%d", time.localtime(self.date_to)))
class ComposedFilter(IFilter):
    _filter_function_factory = {
        TagFilter.IDENTIFIER: TagFilter.from_object,
        KeyWordFilter.IDENTIFIER: KeyWordFilter.from_object,
        DateRangeFilter.IDENTIFIER: DateRangeFilter.from_object
    }
    
    def __init__(self, filters: List[IFilter] = []):
        self._internal_filters: List[IFilter] = filters
        
    def add_filter(self, new_filer: List[IFilter]):
        self._internal_filters.append(new_filer)
        
    def filter(self, unfiltered_content) -> List[FinanceData]: 
        output = unfiltered_content
        for _filter in self._internal_filters:
            output = _filter.filter(output)
        return output

    def to_object(self):
        return {
            'serialized-filters': [serialized_filter.to_object() for serialized_filter in self._internal_filters]
        }

    @classmethod
    def from_object(cls, data_object: dict):
        deserialized_filters: List[IFilter] = []
        for serialized_filter in data_object.get('serialized-filters'):
            deserialized_filters.append(cls._filter_function_factory.get(serialized_filter.get('identifier'))(serialized_filter))
        return ComposedFilter(deserialized_filters)
    
    def __repr__(self):
        res = "<-- composed filter begin -->"
        for f in self._internal_filters:
            res += '\n' + str(f)
        res += '\n'+'<-- compose filter end   -->'
        return res
        