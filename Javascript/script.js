const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let x = canvas.width / 2;
let y = canvas.height / 2;

let projectile_lst = [];
let enemy_lst = [];

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

        this.speed = 2.5
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
        this.speed = -8
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

class Enemy {
    constructor(x, y, radius, color, angle, speed) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.angle = angle;
        this.color = color;
        this.speed = speed;
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

// addEventListener("keydown", (event) => {
//     if ((event.key == "w" || event.key == "W") && ~player.goingdown) {
//         player.goingup = true;
//     } else if ((event.key == "a" || event.key == "A") && ~player.goingright) {
//         player.goingleft = true;
//     } else if ((event.key == "d" || event.key == "D") && ~player.goingleft) {
//         player.goingright = true;
//     } else if ((event.key == "s" || event.key == "S") && ~player.goingup) {
//         player.goingdown = true;
//     }
// });

// addEventListener("keyup", (event) => {
//     if (event.key == "w" || event.key == "W") {
//         player.goingup = false;
//     } else if (event.key == "s" || event.key == "S") {
//         player.goingdown = false;
//     } else if (event.key == "d" || event.key == "D") {
//         player.goingright = false;
//     } else if (event.key == "a" || event.key == "A") {
//         player.goingleft = false;
//     }
// });

addEventListener("click", (event) => {
    let angle = Math.atan2(player.y - event.clientY, player.x - event.clientX)
    projectile_lst.push(new Projectile(player.x, player.y, 5, "white", angle))
});

let animationId;

function createEnemy() {
    setInterval(() => {
        const radius = Math.random() * (30 - 4) + 4

        let x
        let y

        if (Math.random() < 0.5) {
            x = Math.random() < 0.5 ? 0 - radius : canvas.width + radius
            y = Math.random() * canvas.height
        } else {
            x = Math.random() * canvas.width
            y = Math.random() < 0.5 ? 0 - radius : canvas.height + radius
        }

        const color = `hsl(${Math.random() * 360}, 50%, 50%)`

        const angle = Math.atan2(player.y - y, player.x - x)
        const speed = Math.random() * 2 + 1

        enemy_lst.push(new Enemy(x, y, radius, color, angle, speed))
    }, 1000);
}
createEnemy()

function animate() {
    animationId = requestAnimationFrame(animate);
    ctx.fillStyle = 'rgba(0 , 0 , 0 , 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    player.move()
    player.draw()

    projectile_lst.forEach((pro) => {
        if (pro.x < -pro.radius || pro.x > canvas.width + pro.radius || pro.y < -pro.radius || pro.y > canvas.height + pro.radius) {
            projectile_lst.splice(projectile_lst.indexOf(pro), 1)
        }
        pro.update()
        pro.draw()
    });

    enemy_lst.forEach((enemy) => {
        if (enemy.x < -enemy.radius || enemy.x > canvas.width + enemy.radius || enemy.y < -enemy.radius || enemy.y > canvas.height + enemy.radius) {
            enemy_lst.splice(enemy_lst.indexOf(enemy), 1)
        }
        enemy.update()
        enemy.draw()
    });
}

animate()