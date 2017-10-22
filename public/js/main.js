function onSubmit() {
    longVal = longitude.value;
    latVal = latitude.value;
    distanceVal = distance.value;
    queryVal = query.value;
    costVal = cost.value;
    sendPostReq({
        longVal,
        latVal,
        distanceVal,
        queryVal,
        costVal
    });
    //console.log(cityName);
    analytics.innerHTML = '';
    analytics.classList.remove('hidden');
    createGraphs();
}

function sendPostReq(data) {
    console.log(data);
    fetch("/", {method: 'POST', body: JSON.stringify(data), headers: {"content-type": "application/json;charset=UTF-8"}})
        .then((res) => res.json())
        .then(function(json) {
            console.log(json);
        }).catch(function(err) {
            console.log(err);
        });
}

function createGraphs() {
    analytics.textContent = "yay, it worked!"
    console.log(analytics.textContent);
    console.log(longVal + ' ' + latVal + ' ' + distanceVal + ' ' + queryVal + ' ' + costVal);
}
const analytics = document.querySelector('#analytics');
const longitude = document.querySelector('#longitude');
const latitude = document.querySelector('#latitude');
const distance = document.querySelector('#distance');
const query = document.querySelector('#business');
const cost = document.querySelector('#myRange');
const submit = document.querySelector('#submit');
let longVal;
let latVal;
let distanceVal;
let queryVal;
let costVal;
submit.addEventListener('click', onSubmit);