import pygame
import math
import numpy as np
import random

# --- Konfigurasi ---
WIDTH, HEIGHT = 800, 600
SCALE = 40 
WHITE, BLACK, RED, BLUE, GREEN, GRAY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (200, 200, 200)

class RobotConfig:
    def __init__(self):
        self.max_speed = 1.0       # Dipercepat sedikit agar lebih responsif
        self.max_yaw_rate = 120.0 * np.pi / 180.0
        self.dt = 0.1
        self.predict_time = 1.5    # Robot melihat 1.5 detik ke depan
        self.robot_radius = 0.5

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Kecepatan acak antara -0.1 sampai 0.1 unit per frame
        self.vx = random.uniform(-0.1, 0.1)
        self.vy = random.uniform(-0.1, 0.1)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        # Memantul jika menabrak batas (skala dunia)
        if self.x <= 0 or self.x >= WIDTH/SCALE: self.vx *= -1
        if self.y <= 0 or self.y >= HEIGHT/SCALE: self.vy *= -1

# --- Fungsi Pendukung ---
def to_pygame(x, y): return int(x * SCALE), int(HEIGHT - (y * SCALE))

def motion(state, v, w, dt):
    new_theta = state[2] + w * dt
    new_x = state[0] + v * math.cos(new_theta) * dt
    new_y = state[1] + v * math.sin(new_theta) * dt
    return [new_x, new_y, new_theta]

def calc_control(x, goal, obs_list, config):
    best_u = [0, 0]
    min_cost = float("inf")
    
    # Iterasi kecepatan linear dan angular (Dynamic Window)
    for v in np.arange(0, config.max_speed, 0.3):
        for w in np.arange(-config.max_yaw_rate, config.max_yaw_rate, 0.3):
            predict_state = list(x)
            collision = False
            
            # Simulasi trajektori ke depan
            for _ in range(int(config.predict_time / config.dt)):
                predict_state = motion(predict_state, v, w, config.dt)
                
                # Cek tabrakan dengan setiap rintangan
                for ob in obs_list:
                    if math.hypot(predict_state[0]-ob.x, predict_state[1]-ob.y) < config.robot_radius + 0.2:
                        collision = True
                        break
                if collision: break
            
            if collision: continue
            
            # Biaya = Jarak ke Goal + (Opsional: Kecepatan tinggi lebih disukai)
            dist_to_goal = math.hypot(predict_state[0]-goal[0], predict_state[1]-goal[1])
            speed_cost = config.max_speed - v 
            cost = dist_to_goal + speed_cost
            
            if cost < min_cost:
                min_cost = cost
                best_u = [v, w]
    return best_u

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pure DWA with Moving Obstacles")
    clock = pygame.time.Clock()
    config = RobotConfig()
    
    start_node = [1.0, 1.0, 0.0]
    goal_node = [18.0, 13.0]
    
    # Inisialisasi Rintangan Bergerak
    obstacles = [
        Obstacle(4,3), Obstacle(3,4), Obstacle(6,3), Obstacle(7,6), 
        Obstacle(8,7), Obstacle(12,10), Obstacle(14,12), Obstacle(10,5)
    ]
    
    robot_state = list(start_node)

    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        # 1. Update Posisi Rintangan
        for ob in obstacles:
            ob.update()

        # 2. Update Kontrol Robot (DWA)
        dist_to_goal = math.hypot(robot_state[0]-goal_node[0], robot_state[1]-goal_node[1])
        if dist_to_goal > 0.3:
            u = calc_control(robot_state, goal_node, obstacles, config)
            robot_state = motion(robot_state, u[0], u[1], config.dt)

        # --- DRAWING ---
        # Draw Goal
        pygame.draw.circle(screen, GREEN, to_pygame(goal_node[0], goal_node[1]), 15)
        
        # Draw Moving Obstacles
        for ob in obstacles:
            pygame.draw.circle(screen, BLACK, to_pygame(ob.x, ob.y), int(config.robot_radius * SCALE))
        
        # Draw Robot
        r_pos = to_pygame(robot_state[0], robot_state[1])
        pygame.draw.circle(screen, BLUE, r_pos, int(config.robot_radius * SCALE))
        # Garis arah robot
        end_x = robot_state[0] + 0.6 * math.cos(robot_state[2])
        end_y = robot_state[1] + 0.6 * math.sin(robot_state[2])
        pygame.draw.line(screen, RED, r_pos, to_pygame(end_x, end_y), 3)

        pygame.display.flip()
        clock.tick(30)
        
    pygame.quit()

if __name__ == "__main__":
    main()