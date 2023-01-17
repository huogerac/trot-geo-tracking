 let lat = document.getElementById('get-lat')
 let lon = document.getElementById('get-lon')
 let time = document.getElementById('get-time')

  let geoSuccess = (position) => {
    lat.textContent = `Latitude: ${position.coords.latitude}`
    lon.textContent = `Longitude: ${position.coords.longitude}`
    time.textContent = `Tempo: ${new Date().getTime()}`
    }
  let geoErr = (err) => {
    console.log(`Something went wrong: ${err}`)
}  
let evento = () => {
  navigator.geolocation.getCurrentPosition(geoSuccess, geoErr)
}