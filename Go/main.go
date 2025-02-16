package main

import (
	"image/color"

	rl "github.com/gen2brain/raylib-go/raylib"
)

const WIDTH = 1200
const HEIGHT = 700

type Player struct {
	x      int
	y      int
	radius int
	color  color.RGBA
}

type Enemy struct {
	// x int
	// y int
}

type Particle struct {
}

func main() {

	player := Player{}
	player.x = WIDTH / 2
	player.y = HEIGHT / 2
	player.color = rl.White
	player.radius = 5

	rl.InitWindow(WIDTH, HEIGHT, "Shooter game")
	rl.SetTargetFPS(15)

	defer rl.CloseWindow()

	for !rl.WindowShouldClose() {
		rl.BeginDrawing()
		rl.DrawCircle(int32(player.x), int32(player.y), float32(player.radius), player.color)
	}
	rl.EndDrawing()
}
