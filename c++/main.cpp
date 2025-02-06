#include <iostream>
#include <cmath>
#include <vector>
#include "raylib.h"

const int WIDTH = 1200;
const int HEIGHT = 700;

class Player {
public:
    std::vector<float> pos;
    Color color = WHITE;
    int radius;
    int speed;

    Player(int radius, int speed) {
        pos = { WIDTH / 2.0f, HEIGHT / 2.0f };
        this->radius = radius;
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
            pos[0] += horizontal * diagSpeed;
            pos[1] += vertical * diagSpeed;
        } else {
            pos[0] += horizontal * speed;
            pos[1] += vertical * speed;
        }
    }

    void draw() {
        DrawCircle(pos[0], pos[1], radius, color);
    }
};

float CalculateAngle(Vector2 origin, Vector2 target) {
    return atan2(target.y - origin.y, target.x - origin.x);
}

class Enemy {
public:
    std::vector<float> pos;
    float speed;
    float angle;
    int size;
    Color color;

    Enemy(std::vector<float> playerPos) {
        int side = GetRandomValue(0, 3);
        if (side == 0) { pos = { (float)GetRandomValue(0, WIDTH), -20 }; }
        else if (side == 1) { pos = { (float)GetRandomValue(0, WIDTH), HEIGHT + 20 }; }
        else if (side == 2) { pos = { -20, (float)GetRandomValue(0, HEIGHT) }; }
        else { pos = { WIDTH + 20, (float)GetRandomValue(0, HEIGHT) }; }

        speed = 1.5f;

        color = { 
            (unsigned char)GetRandomValue(0, 255),  
            (unsigned char)GetRandomValue(0, 255),  
            (unsigned char)GetRandomValue(0, 255),  
            255 
        };

        Vector2 enemyPos = { pos[0], pos[1] };
        Vector2 playerVec = { playerPos[0], playerPos[1] };

        angle = CalculateAngle(enemyPos, playerVec);
        size = GetRandomValue(10, 30);
    }

    int Move() {
        Vector2 enemyPos = { pos[0], pos[1] };

        pos[0] += cos(angle) * speed;
        pos[1] += sin(angle) * speed;

        if (pos[0] < -100 || pos[0] > WIDTH + 100 || pos[1] < -100 || pos[1] > HEIGHT + 100){
            return 1;
        } 
        return 0;
    }

    void Draw() {
        DrawCircleV({ pos[0], pos[1] }, size, color);
    }
};

class Projectile {
};

int main() {
    int enemyCount = 50;

    std::vector<Enemy> enemies;
    std::vector<Projectile> projectiles;

    Player player(10, 3);

    InitWindow(WIDTH, HEIGHT, "Projectile Movement Example");
    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        player.move();

        while (enemies.size() < enemyCount){
            enemies.push_back(Enemy(player.pos));
        }

        for (int i = 0 ; i < enemies.size() ; i++) {
            if (enemies[i].Move()){
                enemies.erase(enemies.begin() + i);
            }
        }

        BeginDrawing();

        DrawRectangle(0, 0, WIDTH, HEIGHT, Color{0, 0, 0, 64});

        player.draw();

        for (auto &enemy : enemies) {
            enemy.Draw();
        }

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
