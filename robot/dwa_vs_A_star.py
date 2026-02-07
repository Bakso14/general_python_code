import pygame
import math
import numpy as np
import heapq

# --- Konfigurasi Umum ---
WIDTH, HEIGHT = 1200, 600  # Layar lebih lebar untuk dua tampilan
SCALE = 30 
WHITE, BLACK, RED, BLUE, GREEN, GRAY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (200, 200, 200)

class RobotConfig:
    def __init__(self):
        self.max_speed = 2.5
        self.max_yaw_rate = 120.0 * np.pi / 180.0
        self.dt = 0.1
        self.predict_time = 1.5
        self.robot_radius = 0.5

# --- Algoritma A* (Global Planner) ---
def a_star(start, goal, obs, config):
    def dist(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])
    def is_collision(p):
        for ox, oy in obs:
            if math.hypot(p[0]-ox, p[1]-oy) < config.robot_radius + 0.3: return True
        return False

    start_v = (round(start[0], 1), round(start[1], 1))
    open_set = [(0, start_v)]
    came_from = {}
    g_score = {start_v: 0}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        if dist(current, goal) < 0.8:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(0.5,0),(-0.5,0),(0,0.5),(0,-0.5),(0.5,0.5),(-0.5,-0.5)]:
            neighbor = (round(current[0]+dx, 1), round(current[1]+dy, 1))
            if is_collision(neighbor): continue
            
            tentative_g = g_score[current] + dist(current, neighbor)
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + dist(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))
    return []

# --- Fungsi Pendukung ---
def to_pygame(x, y, offset_x=0): 
    return int(x * SCALE) + offset_x, int(HEIGHT - (y * SCALE))

def motion(state, v, w, dt):
    new_theta = state[2] + w * dt
    new_x = state[0] + v * math.cos(new_theta) * dt
    new_y = state[1] + v * math.sin(new_theta) * dt
    return [new_x, new_y, new_theta]

def calc_control(x, target, obs, config):
    best_u = [0, 0]
    min_cost = float("inf")
    for v in np.arange(0, config.max_speed, 0.3):
        for w in np.arange(-config.max_yaw_rate, config.max_yaw_rate, 0.3):
            predict_state = list(x)
            collision = False
            for _ in range(int(config.predict_time / config.dt)):
                predict_state = motion(predict_state, v, w, config.dt)
                if any(math.hypot(predict_state[0]-ox, predict_state[1]-oy) < config.robot_radius for ox, oy in obs):
                    collision = True; break
            if collision: continue
            
            # Biaya utama adalah jarak ke target (bisa goal akhir atau waypoint A*)
            cost = math.hypot(predict_state[0]-target[0], predict_state[1]-target[1])
            if cost < min_cost:
                min_cost = cost; best_u = [v, w]
    return best_u

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kiri: Pure DWA (Terjebak) | Kanan: A* + DWA (Berhasil)")
    clock = pygame.time.Clock()
    config = RobotConfig()

    # Skenario Trap (Huruf U)
    start_pos = (3.0, 10.0)
    goal_pos = (15.0, 10.0)
    trap_obs = []
    for y in np.arange(7.0, 13.0, 0.5): trap_obs.append([10.0, y]) # Tembok belakang
    for x in np.arange(7.0, 10.0, 0.5): trap_obs.append([x, 13.0]) # Tembok atas
    for x in np.arange(7.0, 10.0, 0.5): trap_obs.append([x, 7.0])  # Tembok bawah

    # State Robot 1 (Pure DWA)
    robot1_state = [start_pos[0], start_pos[1], 0.0]
    
    # State Robot 2 (A* + DWA)
    robot2_state = [start_pos[0], start_pos[1], 0.0]
    global_path = a_star(start_pos, goal_pos, trap_obs, config)
    target_idx = 0

    running = True
    while running:
        screen.fill(GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        # --- UPDATE LOGIC ---
        # 1. Update Robot 1 (Menuju langsung ke Goal)
        u1 = calc_control(robot1_state, goal_pos, trap_obs, config)
        robot1_state = motion(robot1_state, u1[0], u1[1], config.dt)

        # 2. Update Robot 2 (Menuju Waypoint A*)
        if target_idx < len(global_path):
            current_target = global_path[target_idx]
            if math.hypot(robot2_state[0]-current_target[0], robot2_state[1]-current_target[1]) < 0.6:
                target_idx += 1
            u2 = calc_control(robot2_state, current_target, trap_obs, config)
        else:
            u2 = calc_control(robot2_state, goal_pos, trap_obs, config)
        robot2_state = motion(robot2_state, u2[0], u2[1], config.dt)

        # --- RENDER ---
        # Gambar pemisah tengah
        pygame.draw.rect(screen, WHITE, (0, 0, 598, HEIGHT))
        pygame.draw.rect(screen, WHITE, (602, 0, 600, HEIGHT))
        
        for offset in [0, 600]:
            # Gambar Goal & Obstacle di kedua sisi
            pygame.draw.circle(screen, GREEN, to_pygame(goal_pos[0], goal_pos[1], offset), 15)
            for ob in trap_obs:
                pygame.draw.circle(screen, BLACK, to_pygame(ob[0], ob[1], offset), 8)

        # Sisi Kiri: Robot 1
        r1_p = to_pygame(robot1_state[0], robot1_state[1], 0)
        pygame.draw.circle(screen, BLUE, r1_p, int(config.robot_radius * SCALE))
        
        # Sisi Kanan: Robot 2 + Jalur A*
        if len(global_path) > 1:
            points = [to_pygame(p[0], p[1], 600) for p in global_path]
            pygame.draw.lines(screen, GRAY, False, points, 1)
        
        r2_p = to_pygame(robot2_state[0], robot2_state[1], 600)
        pygame.draw.circle(screen, BLUE, r2_p, int(config.robot_radius * SCALE))

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__": main()