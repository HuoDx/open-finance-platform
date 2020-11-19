function getVisible(originalString) {
    return originalString.replace(/[\s]+/g, "")
}

function getExceptional(messageString, keys) {
    var exceptional = messageString;
    for (let key of keys) {
        let re = new RegExp(`${key}: ([^;]*); `)
        exceptional = exceptional.replace(re, '')
    }
    return exceptional
}

function filter(messageString, key) {
    let re = new RegExp(`${key}: ([^;]*);`)
    let result = messageString.match(re)
    return result === null ? null : result[1]
}

function replaceValue(messageString, newValue, key) {
    let re = new RegExp(`${key}: ([^;]*);`)
    let result = messageString.replace(re, `${key}: ${newValue};`)
    return result
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

var examineBuilder = function(numberOfDigits = 5) {
    var examiner = function(value) {
        for (let ch of value.substring(0, numberOfDigits)) {
            if (ch != '0') return false
        }
        return true
    }
    return examiner
}

var mine = function(examiner, hasher, message, sp) {
    let nonce = Math.random().toString(16).replace('.', '').substring(0, 10)
    let steps = 0
    while (!examiner(hasher(message + nonce))) {
        nonce = Math.random().toString(16).replace('.', '').substring(0, 10)
        steps++
    }
    console.log(`${steps} guesses to mine.`)
    return nonce;
}

var jsonFetch = async function(url) {
    let response = await fetch(url)
    let jsonResponse = await response.json()
    return jsonResponse
}

async function postData(url, form) {
    console.log(form)
    let result = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
                // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(form)
    })
}