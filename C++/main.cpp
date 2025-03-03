#include <iostream>
#include <cmath>
#include <vector>
#include "raylib.h"

const int WIDTH = 1200;
const int HEIGHT = 700;

class Player {
    public:
        Vector2 pos;
        Color color = WHITE;
        int radius;
        int speed;

        Player(int radius, int speed) {
            pos = { WIDTH / 2.0f, HEIGHT / 2.0f };
            this->radius = radius;
            this->speed = speed;
        }

        void Move() {
            bool up = IsKeyDown(KEY_W);
            bool down = IsKeyDown(KEY_S);
            bool left = IsKeyDown(KEY_A);
            bool right = IsKeyDown(KEY_D);

            int horizontal = (right - left);
            int vertical = (down - up);

            if (horizontal != 0 && vertical != 0) {
                double diagSpeed = speed / std::sqrt(2);
                pos.x += horizontal * diagSpeed;
                pos.y += vertical * diagSpeed;
            } else {
                pos.x += horizontal * speed;
                pos.y += vertical * speed;
            }
        }

        void Draw() {
            DrawCircleV({ pos.x, pos.y }, radius, color);
        }
};

float CalculateAngle(Vector2 origin, Vector2 target) {
    return atan2(target.y - origin.y, target.x - origin.x);
}

class Enemy {
    public:
        Vector2 pos;
        float speed;
        float angle;
        int radius;
        Color color;
        int shirink = 0;

        Enemy(Vector2 playerPos) {
            int side = GetRandomValue(0, 3);
            if (side == 0) { pos = { (float)GetRandomValue(0, WIDTH), -20 }; }
            else if (side == 1) { pos = { (float)GetRandomValue(0, WIDTH), HEIGHT + 20 }; }
            else if (side == 2) { pos = { -20, (float)GetRandomValue(0, HEIGHT) }; }
            else { pos = { WIDTH + 20, (float)GetRandomValue(0, HEIGHT) }; }

            speed = (float)GetRandomValue(50 , 150) / 100.00 + 0.50;

            color = { 
                (unsigned char)GetRandomValue(0, 255),  
                (unsigned char)GetRandomValue(0, 255),  
                (unsigned char)GetRandomValue(0, 255),  
                255 
            };

            angle = CalculateAngle(pos, playerPos);
            radius = GetRandomValue(10, 30);
        }

        int Move() {
            pos.x += cos(angle) * speed;
            pos.y += sin(angle) * speed;

            if (pos.x < -100 || pos.x > WIDTH + 100 || pos.y < -100 || pos.y > HEIGHT + 100){
                return 1;
            } 
            return 0;
        }

        void Shirink() {
            radius--;
        }

        void Draw() {
            DrawCircleV({ pos.x, pos.y }, radius, color);
        }
};

class Projectile {
    public:
        Vector2 pos;
        float speed = 6;
        float angle;
        int radius = 5;
        Color color = WHITE;

        Projectile(Vector2 playerPos , Vector2 mousePos){
            pos = playerPos;
            angle = CalculateAngle(playerPos , mousePos);
        }

        int Move() {
            pos.x += cos(angle) * speed;
            pos.y += sin(angle) * speed;

            if (pos.x < -100 || pos.x > WIDTH + 100 || pos.y < -100 || pos.y > HEIGHT + 100){
                return 1;
            } 
            return 0;
        }

        void Draw() {
            DrawCircleV({ pos.x, pos.y }, radius, color);
        }
};

class Particle {
    public:
        Vector2 pos;
        float speed;
        float angleX;
        float angleY;
        int radius;
        Color color;
        int opacity;

        Particle(Vector2 projectilePos , Color& enemyColor){
            pos = projectilePos;
            color = enemyColor;
            speed = 3;
            radius = (float)GetRandomValue(1 , 300) / 100.0;
            angleX = ((float)GetRandomValue(0 , 100) / 100.0 - 0.5) * ((float)GetRandomValue(0 , 100) / 100.0 * 6);
            angleY = ((float)GetRandomValue(0 , 100) / 100.0 - 0.5) * ((float)GetRandomValue(0 , 100) / 100.0 * 6);
            opacity = GetRandomValue(80 , 200);
        }
        
        int Move(){
            pos.x += angleX * 0.99;
            pos.y += angleY * 0.99;
            opacity--;
            if (opacity <= 0) {
                return 1;
            }
            color.a = opacity;
            return 0;
        }
        void Draw() {
            DrawCircleV({ pos.x, pos.y }, radius, color);
        }
};

int main() {

    std::vector<Enemy> enemies;
    std::vector<Projectile> projectiles;
    std::vector<Particle> particles;

    Player player(10, 3);

    InitWindow(WIDTH, HEIGHT, "Shooter game");
    SetTargetFPS(60);

    int score = 0;
    int gameOver = 0;

    int counter = 0;
    while (!WindowShouldClose() && !gameOver) {
        if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON)) {
            Vector2 mousePos = GetMousePosition();
            projectiles.push_back(Projectile(player.pos, mousePos));
        }


        if (counter % 40 == 0){
            enemies.push_back(Enemy(player.pos));
        }


        BeginDrawing();

        DrawText(TextFormat("Score: %d", score), 20, 20, 20, WHITE);
        DrawRectangle(0, 0, WIDTH, HEIGHT, Color{0, 0, 0, 64});

        player.Move();
        player.Draw();

        for (int i = 0 ; i < particles.size() ; i++){
            if (particles[i].Move()){
                particles.erase(particles.begin() + 1);
                continue;
            }
            particles[i].Draw();
        }

        for (int i = 0 ; i < projectiles.size() ; i++) {
            if (projectiles[i].Move()){
                projectiles.erase(projectiles.begin() + i);
                continue;
            }

            for (int j = 0; j < enemies.size() ; j++) {

                float dx = projectiles[i].pos.x - enemies[j].pos.x;
                float dy = projectiles[i].pos.y - enemies[j].pos.y;
                float distance = sqrt(dx * dx + dy * dy);
                if (distance <= projectiles[i].radius + enemies[j].radius) {

                    score += 100;
                    
                    for (int k = 0 ; k < enemies[j].radius * 2 ; k++){
                        particles.push_back(Particle(projectiles[i].pos , enemies[j].color));
                    }
                    if (enemies[j].radius < 20){
                        enemies.erase(enemies.begin() + j);
                    } else {
                        enemies[j].shirink = counter + enemies[j].radius / 2;
                    }
                    projectiles.erase(projectiles.begin() + i);
                    continue;
                }
            }

            projectiles[i].Draw();
        }

        for (int i = 0 ; i < enemies.size() ; i++) {
            
            float dx = player.pos.x - enemies[i].pos.x;
            float dy = player.pos.y - enemies[i].pos.y;
            float distance = sqrt(dx * dx + dy * dy);
            if (distance <= player.radius + enemies[i].radius) {
                    gameOver = 1;
            }
            if (enemies[i].Move()){
                enemies.erase(enemies.begin() + i);
            }
            if (enemies[i].shirink > counter){
                enemies[i].Shirink();
            }
            enemies[i].Draw();
        }

        EndDrawing();
        counter++;
    }

    CloseWindow();
    return 0;
}
