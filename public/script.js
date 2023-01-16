 let h2 = document.querySelector('h2')

  const geoSuccess = (position) => {
    h2.textContent = `Latitude: ${position.coords.latitude}\nLongitude: ${position.coords.longitude}`
    }
  const geoErr = (err) => {
    console.log(`Something went wrong: ${err}`)
}  

  navigator.geolocation.getCurrentPosition(geoSuccess, geoErr)