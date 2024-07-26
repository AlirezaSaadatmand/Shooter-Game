const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");
const span = document.querySelector("#span");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let x = canvas.width / 2;
let y = canvas.height / 2;

let score = 0;

let projectile_lst = [];
let enemy_lst = [];
let particle_lst = [];

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
                i++;
            }
        });

        if (i == 1) {
            let speed = (this.speed ** 2 * 2) ** 0.5;
            if (this.goingup) { this.y -= speed };
            if (this.goingdown) { this.y += speed };
            if (this.goingright) { this.x += speed };
            if (this.goingleft) { this.x -= speed };

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
        this.angle = angle;
        this.speed = 6;
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

class Particle {
    constructor(x, y, radius, color, anglex, angley, alpha) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
        this.anglex = anglex;
        this.angley = angley;
        this.alpha = alpha;
    }
    update() {
        this.x += this.anglex * 0.99;
        this.y += this.angley * 0.99;
        this.alpha -= 0.01;
    }
    draw() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.restore();
    }
}

const player = new Player(x, y, 15, "white");

// player movement

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
    let angle = Math.atan2(event.clientY - player.y, event.clientX - player.x);
    projectile_lst.push(new Projectile(player.x, player.y, 5, "white", angle));
});

let animationId;

function createEnemy() {
    setInterval(() => {
        if (Math.floor(Math.random() * 10) + 1  in [1 , 2]){
            var radius = Math.random() * 300;
        }else{
            var radius = Math.random() * (30 - 4) + 4;
        }

        let x;
        let y;

        if (Math.random() < 0.5) {
            x = Math.random() < 0.5 ? 0 - radius : canvas.width + radius;
            y = Math.random() * canvas.height;
        } else {
            x = Math.random() * canvas.width;
            y = Math.random() < 0.5 ? 0 - radius : canvas.height + radius;
        }

        const color = `hsl(${Math.random() * 360}, 50%, 50%)`;

        const angle = Math.atan2(player.y - y, player.x - x);
        const speed = Math.random() + 0.5;

        enemy_lst.push(new Enemy(x, y, radius, color, angle, speed));
    }, 800);
}
createEnemy();

function animate() {
    animationId = requestAnimationFrame(animate);
    ctx.fillStyle = 'rgba(0 , 0 , 0 , 0.2)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // player draw
    player.move();
    player.draw();

    // particle draw
    particle_lst.forEach((particle) => {
        if (particle.alpha < 0.01) {
            particle_lst.splice(particle_lst.indexOf(particle), 1);
        } else {
            particle.update();
            particle.draw();
        }
    });

    // projectile draw and hitting enemies
    projectile_lst.forEach((pro) => {
        if (pro.x < -pro.radius || pro.x > canvas.width + pro.radius || pro.y < -pro.radius || pro.y > canvas.height + pro.radius) {
            projectile_lst.splice(projectile_lst.indexOf(pro), 1);
        }

        enemy_lst.forEach((enemy) => {
            let dist = Math.hypot(pro.x - enemy.x, pro.y - enemy.y);
            if (dist - pro.radius - enemy.radius < 0) {
                if (enemy.radius < 50){
                    var s = 2;
                }else{
                    var s = 0.5;
                }
                for (let i = 0; i < enemy.radius * s; i++) {
                    particle_lst.push(new Particle(pro.x, pro.y, Math.random() * 2, enemy.color, (Math.random() - 0.5) * (Math.random() * 6), (Math.random() - 0.5) * (Math.random() * 6), 1));
                }
                if (enemy.radius > 20) {
                    let last = enemy.radius;
                    let interval = setInterval(() => {
                        enemy.radius -= 1
                        if (last - 10 == enemy.radius || enemy.radius < 10) {
                            clearInterval(interval)
                        }
                    }, 20);
                } else {
                    enemy_lst.splice(enemy_lst.indexOf(enemy), 1);
                }
                score += 100;
                span.innerHTML = `Score : ${score}`;
                projectile_lst.splice(projectile_lst.indexOf(pro), 1);
            }
        })
        pro.update();
        pro.draw();
    });

    // enemy draw and end game
    enemy_lst.forEach((enemy) => {
        if (enemy.x < -enemy.radius || enemy.x > canvas.width + enemy.radius || enemy.y < -enemy.radius || enemy.y > canvas.height + enemy.radius) {
            enemy_lst.splice(enemy_lst.indexOf(enemy), 1);
        }
        let dist = Math.hypot(player.x - enemy.x, player.y - enemy.y);
        if (dist - player.radius - enemy.radius <= 0) {
            cancelAnimationFrame(animationId);
        }
        enemy.update();
        enemy.draw();
    });
}

animate();