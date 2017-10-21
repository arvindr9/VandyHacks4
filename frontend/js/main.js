function onSubmit() {
    cityName = city.value;
    stateName = state.value;
    distanceValue = distance.value;
    console.log(cityName);
    analytics.innerHTML = '';
    analytics.classList.remove('hidden');
    createGraphs();
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