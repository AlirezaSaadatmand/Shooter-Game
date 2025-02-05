#include <iostream>
#include <cmath>
#include "raylib.h"

class Projectile {
public:
    int x;
    int y;
    Color color;
    int radius;
    int speed;

    Projectile(int x, int y, int radius, Color color, int speed) {
        this->x = x;
        this->y = y;
        this->radius = radius;
        this->color = color;
        this->speed = speed;
    }

    void move() {
        bool up = IsKeyDown(KEY_W);
        bool down = IsKeyDown(KEY_S);
        bool left = IsKeyDown(KEY_A);
        bool right = IsKeyDown(KEY_D);

        int horizontal = (right - left);
        int vertical = (down - up);

        if (horizontal != 0 && vertical != 0) {

            double diagSpeed = speed / std::sqrt(2);
            x += horizontal * diagSpeed;
            y += vertical * diagSpeed;
        } else {

            x += horizontal * speed;
            y += vertical * speed;
        }
    }

    void draw() {
        DrawCircle(x, y, radius, color);
    }
};

int main(void) {
    const int WIDTH = 1200;
    const int HEIGHT = 700;

    InitWindow(WIDTH, HEIGHT, "Projectile Movement Example");
    SetTargetFPS(60);

    Projectile player(WIDTH / 2, HEIGHT / 2, 10, BLUE, 3);

    while (!WindowShouldClose()) {
        player.move();

        BeginDrawing();
        ClearBackground(RAYWHITE);

        player.draw();

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
