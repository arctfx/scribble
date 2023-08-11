const panel = document.getElementById("canvas-panel")
const canvas = document.getElementById("canvas")
//panel.height = 0.75 * window.innerHeight
//panel.width = 1.5 * panel.height
// Fit canvas to the canvas container
canvas.style.width ='100%'
canvas.style.height='100%'
canvas.width  = canvas.offsetWidth
canvas.height = canvas.offsetHeight

const ctx = canvas.getContext("2d")
ctx.fillStyle = "black"
ctx.strokeStyle = "black"

let prevX = null
let prevY = null
let chosen_color = "black"

ctx.lineWidth = 5

let isDrawing = false
//let can_draw = false


function changeColor(newColor) {
    ctx.fillStyle = newColor
    ctx.strokeStyle = newColor
}

function draw(current_x, current_y, prev_x, prev_y, color) {
    changeColor(color)

    ctx.beginPath()
    ctx.moveTo(prev_x, prev_y)
    ctx.lineTo(current_x, current_y)
    ctx.stroke()
    ctx.arc(current_x, current_y, 2, 0, 2 * Math.PI)
    ctx.fill()

    changeColor(chosen_color)
}

//WebSocket
const drawingBoardSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/drawing-board/'
    + roomName
    + '/'
)

drawingBoardSocket.onmessage = function(e) {
    console.log("Message received!")
    const data = JSON.parse(e.data)
    draw(data.current_x, data.current_y, data.prev_x, data.prev_y, data.color)
}


let clrs = document.querySelectorAll(".clr")
clrs = Array.from(clrs)
clrs.forEach(clr => {
    clr.addEventListener("click", () => {
        chosen_color = clr.dataset.clr
    })
})

let clearBtn = document.querySelector(".clear")
clearBtn.addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
})

// Saving drawing as image
let saveBtn = document.querySelector(".save")
saveBtn.addEventListener("click", () => {
    let data = canvas.toDataURL("imag/png")
    let a = document.createElement("a")
    a.href = data
    a.download = "sketch.png"
    a.click()
})

window.addEventListener("mousedown", (e) => isDrawing = true)
window.addEventListener("mouseup", (e) => isDrawing = false)

window.addEventListener("mousemove", (e) => {
    let offsetX = panel.getBoundingClientRect().left
    let offsetY = panel.getBoundingClientRect().top

    if(prevX == null || prevY == null || !isDrawing){
        prevX = e.clientX - offsetX
        prevY = e.clientY - offsetY
        //console.log("PanelX: "+ x)
        //console.log("PanelY: "+ y)
        return
    }

    if(isDrawing) {
    let currentX = e.clientX - offsetX
    let currentY = e.clientY - offsetY

    var msg = {
                "current_x": currentX,
                "current_y": currentY,
                "prev_x": prevX,
                "prev_y": prevY,
                "color": chosen_color
			  }
    drawingBoardSocket.send(JSON.stringify(msg))

    prevX = currentX
    prevY = currentY
    }
})