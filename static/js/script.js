



    const allCountries = document.querySelectorAll("[data-country]")
    console.log(allCountries)
    gsap.fromTo(
        allCountries,
        {
            opacity:0, 
            x:-20
        },
        {
            opacity:1,
            x:0,
            stagger:0.2,
            ease:"linear",
            duration:0.5
        }
    )













// const logoElement = document.getElementById("logo")

// console.log(logoElement)

// // logoElement.style.color = "red"
// // logoElement.style.fontWeight = "bold"


// // def nazwa():
// function nazwa() {
//     logoElement.textContent = "Państwa"
// }

// function randomTitle() {
//     logoElement.textContent = Math.random()*100
// }

// // setTimeout( nazwa, 4000 )

// // setInterval(randomTitle, 4000)




// const searchInput = document.getElementById("searchField")

// function changeBackground () {
//     searchInput.style.backgroundColor = "coral"
// }

// searchInput.addEventListener("click", changeBackground)



// const ball = document.createElement("div")
// ball.style.width = "50px"
// ball.style.height = "50px"
// ball.style.backgroundColor = "red"
// ball.style.borderRadius = "50%"
// ball.style.position = "absolute"

// document.body.append(ball)


// document.body.addEventListener("mousemove", function (e) {
//     console.log("x: " + e.screenX , "y: " + e.screenY)
    
//     ball.style.left = e.screenX + "px"
//     ball.style.top = (e.screenY - 100) + "px"

// })















