package main

import (
	"image/color"
	"math"

	rl "github.com/gen2brain/raylib-go/raylib"
)

const WIDTH = 1200
const HEIGHT = 700

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

type Enemy struct {
	// x int
	// y int
}

type Particle struct {
}

func reset(player *Player) {
	player.goingUp = false
	player.goingDown = false
	player.goingRight = false
	player.goingLeft = false
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

func restart(player *Player) {
	player.x = WIDTH / 2
	player.y = HEIGHT / 2
	player.color = rl.White
	player.radius = 10
	player.speed = 5

	reset(player)
}

func main() {

	player := Player{}

	restart(&player)

	rl.InitWindow(WIDTH, HEIGHT, "Shooter game")
	rl.SetTargetFPS(60)

	defer rl.CloseWindow()

	for !rl.WindowShouldClose() {
		rl.BeginDrawing()
		rl.ClearBackground(color.RGBA{34, 40, 49, 50})
		playerMove(&player)
		rl.DrawCircle(int32(player.x), int32(player.y), float32(player.radius), player.color)
		rl.EndDrawing()
	}
}
