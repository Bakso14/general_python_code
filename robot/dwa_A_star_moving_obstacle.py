import pygame
import math
import numpy as np
import heapq
import random

# --- Konfigurasi ---
WIDTH, HEIGHT = 1200, 600
SCALE = 30 
WHITE, BLACK, RED, BLUE, GREEN, GRAY, YELLOW = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (200, 200, 200), (255, 215, 0)

class RobotConfig:
    def __init__(self):
        self.max_speed = 3.0
        self.max_yaw_rate = 150.0 * np.pi / 180.0
        self.dt = 0.1
        self.predict_time = 1.0  # Waktu prediksi sedikit dikurangi agar lebih gesit
        self.robot_radius = 0.5

class DynamicObstacle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        # Variasi kecepatan agar lebih dinamis
        self.vx = random.uniform(-0.2, 0.2)
        self.vy = random.uniform(-0.2, 0.2)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        # Memantul di batas dunia (skala 20 unit)
        if self.x < 1 or self.x > 19: self.vx *= -1
        if self.y < 1 or self.y > 19: self.vy *= -1

# --- A* Global Planner ---
def a_star(start, goal, obs, config):
    def dist(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])
    def is_collision(p):
        for ox, oy in obs:
            if math.hypot(p[0]-ox, p[1]-oy) < config.robot_radius + 0.4: return True
        return False

    start_v = (round(start[0], 1), round(start[1], 1))
    open_set = [(0, start_v)]
    came_from, g_score = {}, {start_v: 0}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        if dist(current, goal) < 0.8:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        # Cek tetangga lebih rapat agar jalur lebih halus
        for dx, dy in [(0.5,0),(-0.5,0),(0,0.5),(0,-0.5),(0.5,0.5),(-0.5,-0.5)]:
            neighbor = (round(current[0]+dx, 1), round(current[1]+dy, 1))
            if is_collision(neighbor): continue
            t_g = g_score[current] + dist(current, neighbor)
            if t_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor], g_score[neighbor] = current, t_g
                heapq.heappush(open_set, (t_g + dist(neighbor, goal), neighbor))
    return []

def to_pygame(x, y, offset_x=0): 
    return int(x * SCALE) + offset_x, int(HEIGHT - (y * SCALE))

def calc_control(x, target, static_obs, dynamic_obs, config):
    best_u = [0, 0]
    min_cost = float("inf")
    # Gabungkan semua rintangan untuk pengecekan tabrakan instan
    all_obs = static_obs + [[d.x, d.y] for d in dynamic_obs]
    
    # Simulasi jendela kecepatan (DWA)
    for v in np.arange(0, config.max_speed, 0.4):
        for w in np.arange(-config.max_yaw_rate, config.max_yaw_rate, 0.4):
            predict_state = list(x)
            collision = False
            for _ in range(int(config.predict_time / config.dt)):
                predict_state = [
                    predict_state[0] + v * math.cos(predict_state[2] + w * config.dt) * config.dt,
                    predict_state[1] + v * math.sin(predict_state[2] + w * config.dt) * config.dt,
                    predict_state[2] + w * config.dt
                ]
                if any(math.hypot(predict_state[0]-o[0], predict_state[1]-o[1]) < config.robot_radius + 0.1 for o in all_obs):
                    collision = True; break
            
            if not collision:
                # Cost function: jarak ke waypoint target
                cost = math.hypot(predict_state[0]-target[0], predict_state[1]-target[1])
                if cost < min_cost:
                    min_cost = cost; best_u = [v, w]
    return best_u

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crowded Environment: Pure DWA vs A*+DWA")
    clock = pygame.time.Clock()
    config = RobotConfig()

    start_p, goal_p = (2.0, 10.0), (18.0, 10.0)
    
    # 1. Rintangan Statis (Tembok U + Random)
    static_obs = []
    # Tembok jebakan di tengah
    for y in np.arange(7.0, 13.5, 0.5): static_obs.append([10.0, y])
    for x in np.arange(8.0, 10.5, 0.5): static_obs.append([x, 13.0]); static_obs.append([x, 7.0])
    # Tambahan rintangan statis acak
    for _ in range(15):
        rx, ry = random.uniform(3, 17), random.uniform(2, 18)
        if math.hypot(rx-start_p[0], ry-start_p[1]) > 2 and math.hypot(rx-goal_p[0], ry-goal_p[1]) > 2:
            static_obs.append([rx, ry])

    # 2. Rintangan Dinamis (Banyak)
    dyn_obs = [DynamicObstacle(random.uniform(2,18), random.uniform(2,18)) for _ in range(10)]

    # Init Robots
    r1_state = [start_p[0], start_p[1], 0.0] # Pure DWA
    r2_state = [start_p[0], start_p[1], 0.0] # A* + DWA
    
    print("Menghitung jalur A*...")
    global_path = a_star(start_p, goal_p, static_obs, config)
    t_idx = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
        
        screen.fill(WHITE)
        for d in dyn_obs: d.update()

        # Update Robot 1 (Direct to Goal)
        u1 = calc_control(r1_state, goal_p, static_obs, dyn_obs, config)
        r1_state = [r1_state[0]+u1[0]*math.cos(r1_state[2]+u1[1]*0.1)*0.1, r1_state[1]+u1[0]*math.sin(r1_state[2]+u1[1]*0.1)*0.1, r1_state[2]+u1[1]*0.1]

        # Update Robot 2 (A* Path Following)
        curr_t = global_path[t_idx] if t_idx < len(global_path) else goal_p
        if math.hypot(r2_state[0]-curr_t[0], r2_state[1]-curr_t[1]) < 0.8 and t_idx < len(global_path)-1: t_idx += 1
        u2 = calc_control(r2_state, curr_t, static_obs, dyn_obs, config)
        r2_state = [r2_state[0]+u2[0]*math.cos(r2_state[2]+u2[1]*0.1)*0.1, r2_state[1]+u2[0]*math.sin(r2_state[2]+u2[1]*0.1)*0.1, r2_state[2]+u2[1]*0.1]

        # --- Visualisasi ---
        pygame.draw.line(screen, GRAY, (600, 0), (600, HEIGHT), 5) # Pemisah
        
        for off in [0, 600]:
            # Goal & Obstacles
            pygame.draw.circle(screen, GREEN, to_pygame(goal_p[0], goal_p[1], off), 15)
            for s in static_obs: pygame.draw.circle(screen, BLACK, to_pygame(s[0], s[1], off), 6)
            for d in dyn_obs: pygame.draw.circle(screen, RED, to_pygame(d.x, d.y, off), 10)

        # Sisi Kanan: Jalur A*
        points = [to_pygame(p[0], p[1], 600) for p in global_path]
        if len(points) > 1: pygame.draw.lines(screen, YELLOW, False, points, 2)

        # Robot Biru
        pygame.draw.circle(screen, BLUE, to_pygame(r1_state[0], r1_state[1], 0), 12)
        pygame.draw.circle(screen, BLUE, to_pygame(r2_state[0], r2_state[1], 600), 12)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__": main()