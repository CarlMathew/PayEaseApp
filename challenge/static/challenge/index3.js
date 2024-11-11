const serverName = "http://192.168.1.11:5000/payEase"

const cashless = document.querySelector('#cashless')
const cash = document.querySelector("#cash")
const indexHTML = "#index"
const pickUp = "#pickupLocation"
const dropOff = "#dropOffLocation"
const scanningModal = '#modalRFID'
const successfulModal = '#modalPayment'
const lowBalModal = '#low_balance'
const notRegistered = '#no_rfid'
const checkBal = '#checkBal'
const cashPayment = "#modalcashPayment"
let cardPayment = ""


let pickuplocation = ''
let dropofflocation = ''
let intervalID;

function getCSRFToken() {
    return document
      .querySelector('meta[name="csrf-token"]')
      .getAttribute("content");
}


const closeAllModal = document.querySelectorAll(".closeModal")

closeAllModal.forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelector(scanningModal).close()
        document.querySelector(successfulModal).close()
        document.querySelector(lowBalModal).close()
        document.querySelector(notRegistered).close()
    })
})

function scanRFID(location1, location2){ 
    console.log("api running")
    $.ajax({
        url:`http://127.0.0.1:8000/payEase/scan`,
        method: "POST",
        contentType: 'application/json',
        data: JSON.stringify({
            "loc1": location1,
            "loc2": location2
        }),
        headers: {
            "X-CSRFToken": getCSRFToken(), // Include the CSRF token
        },
        success: (response) => {
            var status = response['data']
            console.log(response)
            // const audio1 = new Audio('/static/challenge/rfid_scanner_sounds.wav');
            
            // audio1.play()

            if (status == 0){
                var total = response['total_payment']
                var new_bal = response['new_bal']
                console.log(response)
                console.log(total)
                console.log(new_bal)
    
                document.querySelector("#paid").innerText = total
                document.querySelector("#balance").innerText = new_bal
                document.querySelector(scanningModal).close()
                document.querySelector(successfulModal).showModal()
            }
            else if (status == 1){
                document.querySelector(scanningModal).close()
                document.querySelector(lowBalModal).showModal()
            }
            else if (status == 2){
                document.querySelector(scanningModal).close()
                document.querySelector(notRegistered).showModal()
            }
        },
        error: (xhr, status, error) => {
            console.log(error)
        }
    })
}


function checkBalance(){
    console.log('reading')
    $.ajax({
        url: `http://127.0.0.1:8000/payEase/check`,
        method: 'POST',
        contentType: 'application/json',
        headers: {
            "X-CSRFToken": getCSRFToken(), // Include the CSRF token
        },
        success: (response) => {
            let status = response['data']
            if (status == 0){
                document.querySelector("#balRFID").close()
                document.querySelector(notRegistered).showModal() 
            }
            else if (status == 1){
                current_balance_check = response['current_bal']
                document.querySelector('#curr_balance').innerText = current_balance_check
                document.querySelector("#balRFID").close()
                document.querySelector("#modalChecking").showModal()
            }
        },
        error: (xhr, status, error) => {
            console.log(error)
        }
    })
}

function coinInsert(location1, location2){
    $.ajax({
        url: `http://127.0.0.1:8000/payEase/coins`,
        method: "POST",
        contentType: 'application/json',
        headers: {
            "X-CSRFToken": getCSRFToken(), // Include the CSRF token
        },
        data: JSON.stringify({
            "loc1": location1,
            "loc2": location2,
            "coin": document.querySelector("#coin_balance").innerText
        }),
        success: (response) => {
            console.log(response);
        },
        error: (xhr, status, error) => {
            console.log(error)
        }

    })
}


function printing(){
    $.ajax({
        url: `http://127.0.0.1:8000/payEase/receipt`,
        method: "POST",
        contentType: 'application/json',
        headers: {
            "X-CSRFToken": getCSRFToken(), // Include the CSRF token
        },
        data: JSON.stringify({
            "payment": document.querySelector("#coin_balance").innerHTML
        }),
        success: (response) => {
            window.location.reload();
        },
        error: (xhr, status, error) => {
            console.log(error)
        }

    })
}

function total_coin(){

    intervalID = setInterval(() => {
        $.ajax({
            url: `http://127.0.0.1:8000/payEase/totalCoin`,
            method: "GET",
            contentType: 'application/json',
            headers: {
                "X-CSRFToken": getCSRFToken(), // Include the CSRF token
            },
            success: (response) =>{
                if (response.data !== ''){
                    document.querySelector("#coin_balance").innerHTML = response.data
                }
            },
            error: (xhr, status, error) => {
                console.log(error)
            }
        })
    }, 2000)
}


$("#return1").on("click", function(){
    $(indexHTML).show()
    $(pickUp).hide()
})


$("#return2").on("click", function(){
    $(pickUp).show()
    $(dropOff).hide()
    $(indexHTML).hide()
})



$(pickUp).hide()
$(dropOff).hide()
cashless.addEventListener('click', function(){
    cardPayment = "cashless"
    $(indexHTML).hide()
    $(pickUp).show()
})
cash.addEventListener("click", function(){
    cardPayment = "cash"
    $(indexHTML).hide()
    $(pickUp).show()
})


document.querySelector("#pickup_south").addEventListener('click', function(){ 
    pickuplocation = 'South Station'
    $(pickUp).hide()
    $(dropOff).show()
})

document.querySelector("#pickup_festi").addEventListener('click', function(){
    pickuplocation = 'Festival'
    $(pickUp).hide()
    $(dropOff).show()
})

document.querySelector('#pickup_feu').addEventListener('click', function(){
    pickuplocation = 'FEU Alabang'
    $(pickUp).hide()
    $(dropOff).show()
})

document.querySelector("#dropoff_south").addEventListener("click", () => {
    dropofflocation = 'South Station'
    if (cardPayment == "cashless"){
   
        document.querySelector(scanningModal).showModal()
        scanRFID(pickuplocation, dropofflocation)
        console.log("rnning")
    }
    else if(cardPayment == "cash"){
        total_coin()
        document.querySelector(cashPayment).showModal()
        coinInsert(pickuplocation, dropofflocation)
    }
})

document.querySelector("#dropoff_festi").addEventListener("click", () => {
    dropofflocation = "Festival"
    if (cardPayment == "cashless"){
        
        scanRFID(pickuplocation, dropofflocation)
        document.querySelector(scanningModal).showModal()
    }  else if(cardPayment == "cash") {
        total_coin()
        document.querySelector(cashPayment).showModal()
        coinInsert(pickuplocation, dropofflocation)
    }

})

document.querySelector("#dropoff_feu").addEventListener("click", () => {
    dropofflocation = "FEU Alabang"
    if (cardPayment == "cashless"){
 
        scanRFID(pickuplocation, dropofflocation)
        document.querySelector(scanningModal).showModal()
    } else if(cardPayment == "cash") {
        total_coin()
        document.querySelector(cashPayment).showModal()
        coinInsert(pickuplocation, dropofflocation)
    }

})

document.querySelector(checkBal).addEventListener('click', () => {
    document.querySelector('#balRFID').show()
    checkBalance()
})



document.querySelector(".paying").addEventListener("click", () => {
    clearInterval(intervalID)
   
    const fare = 25;
    const payment = document.querySelector("#coin_balance").innerHTML;
    console.log(payment)
    printing();

})
