function onSubmit() {
    longVal = longitude.value;
    latVal = latitude.value;
    distanceVal = distance.value;
    sendPostReq({
        longVal,
        latVal,
        distanceVal
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
    console.log(longVal + ' ' + latVal + ' ' + distanceVal);
}
const analytics = document.querySelector('#analytics');
const longitude = document.querySelector('#longitude');
const latitude = document.querySelector('#latitude');
//const city = document.querySelector('#city');
//const state = document.querySelector('#state');
const distance = document.querySelector('#distance');
const submit = document.querySelector('#submit');
let longVal;
let latVal;
let distanceVal;
submit.addEventListener('click', onSubmit);