import ast
import re

def list_parser(res):
    assert res.count("[") == res.count("]") == 1, res

    res = res[res.find("["): res.find("]") + 1]

    return ast.literal_eval(res)

def subreddit_parser(res):
    assert res.count("r/") > 0
    
    pattern = r'r\/[a-zA-Z0-9_]+'

    matches = re.findall(pattern, res)

    return matches[0]


    