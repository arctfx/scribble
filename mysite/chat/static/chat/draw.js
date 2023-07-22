const panel = document.getElementById("canvas-panel")
const canvas = document.getElementById("canvas")
panel.height = 0.75 * window.innerHeight
panel.width = 1.5 * panel.height
//canvas.height = panel.height
//canvas.width = panel.width
canvas.height = 300
canvas.width = 500

const ctx = canvas.getContext("2d")
ctx.fillStyle = "black"
ctx.strokeStyle = "black"

let prevX = null
let prevY = null

ctx.lineWidth = 5

let isDrawing = false
//let can_draw = false

function draw(current_x, current_y, prev_x, prev_y) {
    console.log("draw")
    ctx.beginPath()
    ctx.moveTo(prev_x, prev_y)
    ctx.lineTo(current_x, current_y)
    ctx.stroke()
    //ctx.arc(current_x, current_y, 4, 0, 2 * Math.PI)
    ctx.arc(current_x, current_y, 2, 0, 2 * Math.PI);
    ctx.fill()
    //ctx.fillStyle("red")
    //ctx.fill()

}

//WebSocket
const drawingBoardSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/drawing-board/'
    + roomName
    + '/'
);

drawingBoardSocket.onmessage = function(e) {
    console.log("Message received!")
    const data = JSON.parse(e.data);
    draw(data.current_x, data.current_y, data.prev_x, data.prev_y)
};


let clrs = document.querySelectorAll(".clr")
clrs = Array.from(clrs)
clrs.forEach(clr => {
    clr.addEventListener("click", () => {
        ctx.strokeStyle = clr.dataset.clr
        ctx.fillStyle = clr.dataset.clr
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
    // what ever name you specify here
    // the image will be saved as that name
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
                "prev_y": prevY
			  };
    drawingBoardSocket.send(JSON.stringify(msg))

    prevX = currentX
    prevY = currentY
    }
})