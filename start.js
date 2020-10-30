const fs = require('fs');
var JSONStream = require( "JSONStream" );
let rawdata = fs.readFileSync("test.json");
let data2 = JSON.parse(rawdata);

var list = {};
for (let i = 0; i < data2.length; i++){
    list[(i+1).toString()] = data2[i];
}

function getSentence(value, key) {
    if (value > 87) {
        return {wasFound: false, value: null};
    } else if (value < 87) {
        let options = {};
        for (const property2 in list[value + 1]) {
            let result = getSentence(list[value+1][property2], property2);
            if(result.wasFound) {
                options[property2] = result.value;
            }
        }
        return {wasFound: true, value: options};
    } else {
        return {wasFound: true, value: {  key: key }};
    }
}

function getCompleteSentence(data) {
    let tmpList = [];
    for (const property in data){
        if (property != "key"){
            let results = getCompleteSentence(data[property], tmpList);
            for (const item in results){
                tmpList.push(property + " " + results[item]);
            }
        } else {
            return [data["key"]]
        }
    }
    return tmpList;
}

var stream;
stream = fs.createWriteStream(__dirname + "/data4.txt"); 


for (const property in list["27"]) {
    let value = list["27"][property];
    let data = {};
    data[property] = getSentence(value).value;
    
    let sentences = [];
    let reformedData = getCompleteSentence(data[property]);
    for (const item in reformedData) {
        stream.write(property + " " + reformedData[item] + '\n');
    }
}

