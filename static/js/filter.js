// parse
function _purifyContent(rawContent) {
    let splitted = rawContent.replaceAll(/[\s]/g, '').split(',')
    return splitted;
}

function extractFromKey(inputString, key) {
    let regExp = new RegExp(`${key}:([^;]*);`)
    let tagMatchResult = inputString.match(regExp)
    if (tagMatchResult !== null) return _purifyContent(tagMatchResult[1])
    return null
}

function basicValueValid(value) {
    return (value != null && value.length > 0);
}

function buildParser(inputString) {
    // obtain the values in the given input string
    tagValue = extractFromKey(inputString, 'Tag')
    keywords = extractFromKey(inputString, 'Keywords')
    dateFrom = extractFromKey(inputString, 'From')
    dateTo = extractFromKey(inputString, 'To')
    console.info(tagValue, keywords, dateFrom, dateTo)
        //starting to build the parser
    let composedFilter = new Array()
        // push tag filter
        // notice that it must be provided witha a valid financial record object
    if (basicValueValid(tagValue)) {
        tagValue = tagValue[0]
        composedFilter.push((unfiltered) => {
            let filtered = Array()
            for (var element of unfiltered) {
                if (element.tags.includes(tagValue))
                    filtered.push(element)
            }
            return filtered;
        })
    }
    // push keywords filter
    if (basicValueValid(keywords)) {
        composedFilter.push((unfiltered) => {
            let filtered = Array()
            for (var element of unfiltered) {
                for (var keyword of keywords) {
                    if (element.description.includes(keyword)) {
                        filtered.push(element)
                        break; // one keyword match is enough for a word to be displayed.
                    }
                }
            }
            return filtered;
        })
    }
    // push date(from) filter
    if (basicValueValid(dateFrom) && !isNaN(Date.parse(dateFrom[0]))) {
        dateFrom = Date.parse(dateFrom[0])
        composedFilter.push((unfiltered) => {
            let filtered = Array()
            for (var element of unfiltered) {
                if (Date.parse(element.timestamp) >= dateFrom) {
                    filtered.push(element)
                }
            }
            return filtered;
        })
    }
    // push date(to) filter
    if (basicValueValid(dateTo) && !isNaN(Date.parse(dateTo[0]))) {
        dateTo = Date.parse(dateTo[0])
        composedFilter.push((unfiltered) => {
            let filtered = Array()
            for (var element of unfiltered) {
                if (Date.parse(element.timestamp) <= dateTo) {
                    filtered.push(element)
                }
            }
            return filtered;
        })
    }

    return function(value) {
        let result = value;
        if (!basicValueValid(composedFilter)) {
            console.warn("Invalid composed filter; cannot prepare.")
            console.warn(composedFilter)
            return result;
        }
        for (var filter of composedFilter)
            result = filter(result)
        return result
    }
}