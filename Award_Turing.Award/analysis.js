let raw = require('./turing_award.json')

let countOfYear = {}
let data = []
for (let name in raw) {
    let p = raw[name]
    if (countOfYear[p.year] == null) {
        countOfYear[p.year] = 1
    } else {
        countOfYear[p.year] += 1
    }
    if (p.BIRTH == null) {
        console.log(`${p.year}年得主${name}没有出生数据`)
    } else {
        p.name = name
        p.birth = parseInt(p.BIRTH[0].match('[0-9]{4}')[0])
        if (p.DEATH) {
            p.death = parseInt(p.DEATH[0].match('[0-9]{4}')[0])
        }
        if (p.death) {
            p.age = p.death - p.birth
        } else {
            p.age = 2020 - p.birth
        }

        p.award_age = p.year - p.birth

        data.push(p)
    }
}

console.log(countOfYear)

data.sort(function (a, b) {
    //return a.award_age - b.award_age
    //return a.age - b.age
    return a.year - b.year
})

console.log(data.map(e => [e.name, parseInt(e.year), e.birth, e.death, e.age, e.award_age]))

console.log(">>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<")
data.sort(function (a, b) {
    //return a.award_age - b.award_age
    return a.age - b.age
})
console.log(
    data
    //.filter(e => e.death == null)
    .map(e => [e.name, parseInt(e.year), e.birth, e.death, e.age, e.award_age])
)
