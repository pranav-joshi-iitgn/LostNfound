const C = document.createElement("canvas")
const c = C.getContext("2d")
C.style.position = 'fixed'
C.style.zIndex = -1
C.style.left = "0"
C.style.top = "0"
var r = 2
var dx = 20
var noiseState = 0
var noise = []
var texture = []
var field = []
var x = 0
var y = 0
var G = 50
var vin = 1000
var foc = 50
function resize(){
    C.width = window.innerWidth
    C.height = window.innerHeight
    if(navigator.userAgent.match(/Android/i)){
        r = 5
        dx = Math.max(C.width,C.height)/20
    }
    texture=[]
    noise=[]
    for(var i=0;i<C.width/dx;i++){
        var L = []
        var N = []
        for(var j=0;j<C.height/dx;j++){
            L.push(Math.random())
            var n = []
            for(var k=0;k<10;k++){
                n.push((dx/20) * Math.random())
            }
            N.push(n)
        }
        texture.push(L)
        noise.push(N)
    }
}
window.onresize = function(){
    resize()
    move()
}
function Dot(x,y,col=0){
    var t = Math.exp(-col/foc)
    var t2 = Math.exp(-col/vin)
    var cos = Math.cos(col/100)
    var sin = Math.sin(col/100)
    //yellow = [255,255,244]
    //random = [100*cos(col),100*sin(col),255]
    c.fillStyle = `rgb(${t2*(255*t+(1-t)*100*(1+cos))},${t2*(255*t+(1-t)*100*(1+sin))},${t2*(255-11*t)})`
    c.beginPath()
    c.arc(x,y,r,0,6.3)
    c.closePath()
    c.fill()
}
function rDots(N=3000){
    c.clearRect(0,0,C.width,C.height)
    for(var i=0;i<N;i++){
        Dot(Math.random()*C.width,Math.random()*C.height)
    }
}
function Disturbance(){
    c.clearRect(0,0,C.width,C.height)
    noiseState = (noiseState+2) % 10
    for(var i = 0;i<noise.length;i+=1){
        for(var j=0;j<noise[0].length;j+=1){
            Dot(field[i][j][1] + noise[i][j][noiseState] + dx*texture[i][j],field[i][j][2] + noise[i][j][noiseState+1] + dx*texture[i][j],field[i][j][0]*(1+4*texture[i][j])/5)
        }
    }
}
function move(){
    field = []
    for(var i = 0;i<noise.length;i+=1){
        L = []
        for(var j=0;j<noise[0].length;j+=1){
            var R = Math.sqrt((x-i*dx)**2 + (y-j*dx)**2)
                L.push([R,i*dx + G*(i*dx-x)/(1+R) ,j*dx+G*(j*dx-y)/(1+R)])
        }
        field.push(L)
    }
}
document.addEventListener("mousemove",function(e){
    x = e.clientX
    y = e.clientY
    move()
})
document.addEventListener("touchmove",function(e){
    x = e.touches[0].clientX
    y = e.touches[0].clientY
    //G = 3*e.touches[0].radiusX
    move()
})
//document.addEventListener("pointerdown",function(){
//    vin = vin/5
//    foc = foc/5
//    var g = setInterval(function(){vin=0.95*vin+50;foc=0.95*foc+2.5;move()},100)
//    setTimeout(function(){clearInterval(g);sig=1000},2000)
//})
resize()
move()
D = setInterval(Disturbance,50)
window.onload = function(e){
    document.body.appendChild(C)
}

