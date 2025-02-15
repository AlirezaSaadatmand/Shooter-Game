package main

import (
	rl "github.com/gen2brain/raylib-go/raylib"
)

const WIDTH = 1200
const HEIGHT = 700

func main() {
	rl.InitWindow(WIDTH, HEIGHT, "Shooter game")

	rl.SetTargetFPS(15)
	defer rl.CloseWindow()

	for !rl.WindowShouldClose() {
		rl.BeginDrawing()

	}
	rl.EndDrawing()
}
