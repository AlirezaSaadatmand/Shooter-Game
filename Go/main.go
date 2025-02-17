package main

import (
	"fmt"
	"image/color"
	"math"

	rl "github.com/gen2brain/raylib-go/raylib"
)

const WIDTH = 1200
const HEIGHT = 700

var projectiles []Projectile
var enemies []Enemy

var gameOver bool = false

type Player struct {
	x      float32
	y      float32
	radius int
	color  color.RGBA
	speed  float32

	goingUp    bool
	goingDown  bool
	goingRight bool
	goingLeft  bool
}

func playerMove(player *Player) {
	up := rl.IsKeyDown(rl.KeyW)
	down := rl.IsKeyDown(rl.KeyS)
	left := rl.IsKeyDown(rl.KeyA)
	right := rl.IsKeyDown(rl.KeyD)

	horizontal := 0
	vertical := 0

	if right {
		horizontal = 1
	} else if left {
		horizontal = -1
	}

	if down {
		vertical = 1
	} else if up {
		vertical = -1
	}

	if horizontal != 0 && vertical != 0 {
		diagSpeed := player.speed / float32(math.Sqrt2)
		player.x += float32(horizontal) * diagSpeed
		player.y += float32(vertical) * diagSpeed
	} else {
		player.x += float32(horizontal) * player.speed
		player.y += float32(vertical) * player.speed
	}

}

type Projectile struct {
	x      float32
	y      float32
	radius float32
	speed  float32
	angle  float32
}

func projectileMove(projectile *Projectile) bool {
	projectile.x += float32(math.Cos(float64(projectile.angle)) * float64(projectile.speed))
	projectile.y += float32(math.Sin(float64(projectile.angle)) * float64(projectile.speed))

	if projectile.x > WIDTH+projectile.radius || projectile.x < 0-projectile.radius ||
		projectile.y > HEIGHT+projectile.radius || projectile.y < 0-projectile.radius {
		return true
	}
	return false
}

type Enemy struct {
	x      float32
	y      float32
	speed  float32
	color  rl.Color
	angle  float32
	radius int32
}

func enemyMove(enemy *Enemy) bool {
	enemy.x += float32(math.Cos(float64(enemy.angle)) * float64(enemy.speed))
	enemy.y += float32(math.Sin(float64(enemy.angle)) * float64(enemy.speed))

	if enemy.x < -100 || enemy.x > WIDTH+100 || enemy.y < -100 || enemy.y > HEIGHT+100 {
		return true
	}
	return false
}

func createEnemy(player Player) {
	randomValue := rl.GetRandomValue(int32(0), int32(3))

	var x float32
	var y float32

	if randomValue == 0 {
		x = float32(rl.GetRandomValue(int32(0), int32(WIDTH)))
		y = float32(-30)
	} else if randomValue == 1 {
		x = float32(rl.GetRandomValue(int32(0), int32(WIDTH)))
		y = float32(HEIGHT + 30)
	} else if randomValue == 2 {
		x = float32(-30)
		y = float32(rl.GetRandomValue(int32(0), int32(HEIGHT)))
	} else {
		x = float32(WIDTH + 30)
		y = float32(rl.GetRandomValue(int32(0), int32(HEIGHT)))
	}

	speed := float32(rl.GetRandomValue(50, 150))/100.00 + 0.50
	radius := float32(rl.GetRandomValue(10, 40))

	color := color.RGBA{R: uint8(rl.GetRandomValue(0, 255)), G: uint8(rl.GetRandomValue(0, 255)), B: uint8(rl.GetRandomValue(0, 255)), A: 255}

	angle := float32(math.Atan2(float64(player.y-y), float64(player.x-x)))

	enemies = append(enemies, Enemy{x: x, y: y, speed: speed, radius: int32(radius), color: color, angle: angle})
}

type Particle struct {
}

func collision(enemy Enemy, projectile Projectile) bool {
	dx := float64(enemy.x - projectile.x)
	dy := float64(enemy.y - projectile.y)
	distance := math.Sqrt(dx*dx + dy*dy)

	return distance < float64(enemy.radius+int32(projectile.radius))
}

func reset(player *Player) {
	player.goingUp = false
	player.goingDown = false
	player.goingRight = false
	player.goingLeft = false
}

func restart(player *Player) {
	player.x = WIDTH / 2
	player.y = HEIGHT / 2
	player.color = rl.White
	player.radius = 10
	player.speed = 3

	reset(player)
}

func main() {

	player := Player{}

	restart(&player)

	rl.InitWindow(WIDTH, HEIGHT, "Shooter game")
	rl.SetTargetFPS(60)

	defer rl.CloseWindow()
	counter := 0
	for !rl.WindowShouldClose() && !gameOver {
		counter++
		if counter%40 == 0 {
			fmt.Println(len(projectiles))
			createEnemy(player)
		}
		if rl.IsMouseButtonPressed(rl.MouseLeftButton) {
			mousePos := rl.GetMousePosition()
			angle := math.Atan2(float64(mousePos.Y)-float64(player.y), float64(mousePos.X)-float64(player.x))
			projectiles = append(projectiles, Projectile{x: player.x, y: player.y, speed: 6, radius: 5, angle: float32(angle)})
		}

		rl.BeginDrawing()
		rl.DrawRectangle(int32(0), int32(0), int32(WIDTH), int32(HEIGHT), color.RGBA{34, 40, 49, 150})

		for i := 0; i < len(projectiles); i++ {
			if projectileMove(&projectiles[i]) {
				projectiles = append(projectiles[:i], projectiles[i+1:]...)
				i--
				continue
			}

			for j := 0; j < len(enemies); j++ {
				if collision(enemies[j], projectiles[i]) {
					projectiles = append(projectiles[:i], projectiles[i+1:]...)
					enemies = append(enemies[:j], enemies[j+1:]...)
					i--
					break
				}
			}

			if i >= 0 && i < len(projectiles) {
				rl.DrawCircle(int32(projectiles[i].x), int32(projectiles[i].y), float32(projectiles[i].radius), color.RGBA{255, 255, 255, 255})
			}
		}

		for i := 0; i < len(enemies); i++ {
			if enemyMove(&enemies[i]) {
				enemies = append(enemies[:i], enemies[i+1:]...)
				i--
				continue
			}
			rl.DrawCircle(int32(enemies[i].x), int32(enemies[i].y), float32(enemies[i].radius), enemies[i].color)
		}

		playerMove(&player)
		rl.DrawCircle(int32(player.x), int32(player.y), float32(player.radius), player.color)
		rl.EndDrawing()
	}
}
