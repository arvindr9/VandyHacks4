function onSubmit() {
    cityName = city.value;
    stateName = state.value;
    distanceValue = distance.value;
    sendPostReq({
        cityName,
        stateName,
        distanceValue
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
    console.log(cityName + ' ' + stateName + ' ' + distanceValue);
}
const analytics = document.querySelector('#analytics');
const city = document.querySelector('#city');
const state = document.querySelector('#state');
const distance = document.querySelector('#distance');
const submit = document.querySelector('#submit');
let cityName;
let stateName;
let distanceValue;
submit.addEventListener('click', onSubmit);