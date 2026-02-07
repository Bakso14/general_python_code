import pygame
import math
import numpy as np
import heapq

# --- Konfigurasi ---
WIDTH, HEIGHT = 800, 600
SCALE = 40 
WHITE, BLACK, RED, BLUE, GREEN, GRAY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (200, 200, 200)

class RobotConfig:
    def __init__(self):
        self.max_speed = 2.0
        self.max_yaw_rate = 100.0 * np.pi / 180.0
        self.dt = 0.1
        self.predict_time = 1.0
        self.robot_radius = 0.5

# --- Algoritma A* (Global Planner) ---
def a_star(start, goal, obs, config):
    def dist(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])
    def is_collision(p):
        for ox, oy in obs:
            if math.hypot(p[0]-ox, p[1]-oy) < config.robot_radius + 0.2: return True
        return False

    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: dist(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]
        if dist(current, goal) < 0.5:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        # Cek 8 arah tetangga
        for dx, dy in [(0.5,0),(-0.5,0),(0,0.5),(0,-0.5),(0.5,0.5),(-0.5,-0.5),(0.5,-0.5),(-0.5,0.5)]:
            neighbor = (round(current[0]+dx, 2), round(current[1]+dy, 2))
            if is_collision(neighbor): continue
            
            tentative_g = g_score[current] + dist(current, neighbor)
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + dist(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

# --- Fungsi Pendukung ---
def to_pygame(x, y): return int(x * SCALE), int(HEIGHT - (y * SCALE))

def motion(state, v, w, dt):
    new_theta = state[2] + w * dt
    new_x = state[0] + v * math.cos(new_theta) * dt
    new_y = state[1] + v * math.sin(new_theta) * dt
    return [new_x, new_y, new_theta]

def calc_control(x, current_target, obs, config):
    best_u = [0, 0]
    min_cost = float("inf")
    for v in np.arange(0, config.max_speed, 0.2):
        for w in np.arange(-config.max_yaw_rate, config.max_yaw_rate, 0.2):
            predict_state = list(x)
            collision = False
            for _ in range(int(config.predict_time / config.dt)):
                predict_state = motion(predict_state, v, w, config.dt)
                if any(math.hypot(predict_state[0]-ox, predict_state[1]-oy) < config.robot_radius for ox, oy in obs):
                    collision = True; break
            if collision: continue
            
            # Biaya berdasarkan jarak ke waypoint A* saat ini
            cost = math.hypot(predict_state[0]-current_target[0], predict_state[1]-current_target[1])
            if cost < min_cost:
                min_cost = cost; best_u = [v, w]
    return best_u

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    config = RobotConfig()
    
    start_node = (1.0, 1.0)
    goal_node = (18.0, 13.0)
    obstacles = [[4,3],[3,4],[6,3],[7,6],[8,7],[8.5,6.5],[9,6],[9.5,5.5],[10,5],[1,4],[4,1],[3.5,3.5],[12,10],[14,12]]
    
    # HITUNG JALUR GLOBAL SEKALI DI AWAL
    print("Menghitung Jalur A*...")
    global_path = a_star(start_node, goal_node, obstacles, config)
    
    robot_state = [start_node[0], start_node[1], 0.0]
    target_idx = 0

    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        if target_idx < len(global_path):
            current_waypoint = global_path[target_idx]
            # Jika sudah dekat waypoint saat ini, pindah ke waypoint berikutnya
            if math.hypot(robot_state[0]-current_waypoint[0], robot_state[1]-current_waypoint[1]) < 0.5:
                target_idx += 1
            
            u = calc_control(robot_state, current_waypoint, obstacles, config)
            robot_state = motion(robot_state, u[0], u[1], config.dt)

        # Draw Global Path (A*)
        if len(global_path) > 1:
            points = [to_pygame(p[0], p[1]) for p in global_path]
            pygame.draw.lines(screen, GRAY, False, points, 2)

        # Draw Goal, Obstacles, & Robot
        pygame.draw.circle(screen, GREEN, to_pygame(goal_node[0], goal_node[1]), 10)
        for ob in obstacles:
            pygame.draw.circle(screen, BLACK, to_pygame(ob[0], ob[1]), int(config.robot_radius * SCALE))
        
        r_pos = to_pygame(robot_state[0], robot_state[1])
        pygame.draw.circle(screen, BLUE, r_pos, int(config.robot_radius * SCALE))
        pygame.draw.line(screen, RED, r_pos, to_pygame(robot_state[0]+0.5*math.cos(robot_state[2]), robot_state[1]+0.5*math.sin(robot_state[2])), 3)

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__": main()