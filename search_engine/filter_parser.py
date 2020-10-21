from search_engine.filters import ComposedFilter, KeyWordFilter, TagFilter, DateRangeFilter

import re

# Legacy version.
# keywords_parser = 'Keywords:'
# tag_parser = 'Tag:'
# date_from_parser = 'From:'
# date_to_parser = 'To:'

# def get_result_from_parser(value, parser, stop = ';'):
#     buff = []
#     ans = ""
#     value = value.replace(' ', '')
#     dump_mode = False
#     for c in value:
        
#         if c == stop:
#             if dump_mode == True:
#                 # print('dump', ans)
#                 return ans
#             else:
#                 # print('buffer content: ', ''.join(buff))
#                 buff = []
#         else:
                
#             if dump_mode == True:
#                 ans += c
#             else:
#                 buff.append(c)
            
#         if ''.join(buff) == parser:
#             # print('trigger dump', buff)
#             dump_mode = True
#             buff = []
#     return None
import re
keywords_parser = re.compile('Keywords: ([^;]*);')
tag_parser = re.compile('Tag: ([^;]*);')
date_from_parser = re.compile('From: ([^;]*);')
date_to_parser = re.compile('To: ([^;]*);')

def get_result_from_parser(value, parser):
    result = parser.findall(value)
    if len(result) > 0:
        # return the last match to make it more logically rubust
        return result[-1]
    else:
        return None
    


def parse(filter_string: str):
    global keywords_parser, tag_parser, date_from_parser, date_to_parser
    result_filter = ComposedFilter()
    
    keywords_result:str = get_result_from_parser(filter_string, keywords_parser)
    # print('DEBUG', keywords_result)
    if keywords_result is not None:
        # start parsing keywords to construct the filter
        keywords = keywords_result.split()
        keyword_filter = KeyWordFilter(key_words=keywords)
        result_filter.add_filter(keyword_filter)
    
    tag_result:str = get_result_from_parser(filter_string, tag_parser)
    # print('DEBUG', tag_result)
    if tag_result is not None:
        tag_filter = TagFilter(tag_result)
        result_filter.add_filter(tag_filter)
    
    date_from_result = get_result_from_parser(filter_string, date_from_parser)
    date_to_result = get_result_from_parser(filter_string, date_to_parser)
    print('DEBUG', date_from_result, date_to_result)
    if date_from_parser is not None or date_to_parser is not None:
        date_filter = DateRangeFilter(date_from_result, date_to_result)
        result_filter.add_filter(date_filter)
        
    return result_filter
