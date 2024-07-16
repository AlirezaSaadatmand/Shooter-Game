const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let x = canvas.width / 2;
let y = canvas.height / 2;

let projectile_lst = [];

ctx.fillStyle = "black"
ctx.fillRect(0, 0, canvas.width, canvas.height)

class Player {
    constructor(x, y, radius, color) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;

        this.goingup = false;
        this.goingright = false;
        this.goingleft = false;
        this.goingdown = false;

        this.speed = 3
    }

    move() {
        let lst = [this.goingup, this.goingright, this.goingleft, this.goingdown];
        let i = 0;
        lst.forEach((t) => {
            if (t == true) {
                i++
            }
        });

        if (i == 1) {
            let speed = (this.speed ** 2 * 2) ** 0.5
            if (this.goingup) { this.y -= speed }
            if (this.goingdown) { this.y += speed }
            if (this.goingright) { this.x += speed }
            if (this.goingleft) { this.x -= speed }

        } else if (i == 2) {
            if (this.goingup && this.goingright) {
                this.x += this.speed;
                this.y -= this.speed;
            } else if (this.goingup && this.goingleft) {
                this.x -= this.speed;
                this.y -= this.speed;
            } else if (this.goingdown && this.goingright) {
                this.x += this.speed;
                this.y += this.speed;
            } else if (this.goingdown && this.goingleft) {
                this.x -= this.speed;
                this.y += this.speed;
            }

        }
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

class Projectile {
    constructor(x, y, radius, color, angle) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
        this.angle = angle
        this.speed = -10
    }
    update() {
        this.x += Math.cos(this.angle) * this.speed;
        this.y += Math.sin(this.angle) * this.speed;
    }
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

const player = new Player(x, y, 15, "white");

addEventListener("keydown", (event) => {
    if ((event.key == "w" || event.key == "W") && ~player.goingdown) {
        player.goingup = true;
    } else if ((event.key == "a" || event.key == "A") && ~player.goingright) {
        player.goingleft = true;
    } else if ((event.key == "d" || event.key == "D") && ~player.goingleft) {
        player.goingright = true;
    } else if ((event.key == "s" || event.key == "S") && ~player.goingup) {
        player.goingdown = true;
    }
});

addEventListener("keyup", (event) => {
    if (event.key == "w" || event.key == "W") {
        player.goingup = false;
    } else if (event.key == "s" || event.key == "S") {
        player.goingdown = false;
    } else if (event.key == "d" || event.key == "D") {
        player.goingright = false;
    } else if (event.key == "a" || event.key == "A") {
        player.goingleft = false;
    }
});

addEventListener("click", (event) => {
    let angle = Math.atan2(player.y - event.clientY, player.x - event.clientX)
    projectile_lst.push(new Projectile(player.x, player.y, 5, "white", angle))
});

let animationId;

function animate() {
    animationId = requestAnimationFrame(animate);
    ctx.fillStyle = 'rgba(0 , 0 , 0 , 0.2)';
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    player.move()
    player.draw()

    projectile_lst.forEach((i) => {
        i.update()
        i.draw()
    })

}

animate()