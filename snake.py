#!/usr/bin/env python3
"""
贪吃蛇主程序
"""

import sys
import pygame
from pygame.locals import *

import config
from game import GameState


def draw_grid(surface):
    """绘制网格"""
    for x in range(0, config.SCREEN_WIDTH, config.GRID_SIZE):
        pygame.draw.line(surface, config.GRID_COLOR, (x, 0), (x, config.SCREEN_HEIGHT))
    for y in range(0, config.SCREEN_HEIGHT, config.GID_SIZE):
        pygame.draw.line(surface, config.GRID_COLOR, (0, y), (config.SCREEN_WIDTH, y))


def draw_snake(surface, snake):
    """绘制蛇"""
    # 绘制头部
    head = snake.get_head()
    head_rect = pygame.Rect(
        head.x * config.GRID_SIZE,
        head.y * config.GRID_SIZE,
        config.GRID_SIZE,
        config.GRID_SIZE
    )
    pygame.draw.rect(surface, config.SNAKE_HEAD, head_rect)
    pygame.draw.rect(surface, (255, 255, 255), head_rect, 1)
    
    # 绘制身体
    for i, pos in enumerate(snake.get_body()[1:]):
        body_rect = pygame.Rect(
            pos.x * config.GRID_SIZE,
            pos.y * config.GRID_SIZE,
            config.GRID_SIZE,
            config.GRID_SIZE
        )
        pygame.draw.rect(surface, config.SNAKE_BODY, body_rect)
        pygame.draw.rect(surface, (200, 200, 255), body_rect, 1)


def draw_food(surface, food):
    """绘制食物"""
    pos = food.get_position()
    food_rect = pygame.Rect(
        pos.x * config.GRID_SIZE,
        pos.y * config.GRID_SIZE,
        config.GRID_SIZE,
        config.GRID_SIZE
    )
    pygame.draw.rect(surface, config.FOOD_COLOR, food_rect)
    pygame.draw.rect(surface, (255, 200, 200), food_rect, 1)
    
    # 绘制食物内部的"小点"
    center_x = pos.x * config.GRID_SIZE + config.GRID_SIZE // 2
    center_y = pos.y * config.GRID_SIZE + config.GRID_SIZE // 2
    pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), 3)


def draw_ui(surface, game_state, font):
    """绘制UI（分数、速度、状态）"""
    # 分数
    score_text = font.render(f"分数: {game_state.get_score()}", True, config.TEXT_COLOR)
    surface.blit(score_text, (10, 10))
    
    # 速度
    speed_text = font.render(f"速度: {game_state.get_speed():.1f}", True, config.TEXT_COLOR)
    surface.blit(speed_text, (10, 40))
    
    # 游戏状态
    if game_state.is_game_over():
        game_over_text = font.render("游戏结束! 按 R 重新开始", True, (255, 100, 100))
        text_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        surface.blit(game_over_text, text_rect)
    elif game_state.is_paused():
        pause_text = font.render("游戏暂停 (按 P 继续)", True, (255, 200, 100))
        text_rect = pause_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        surface.blit(pause_text, text_rect)


def handle_input(game_state):
    """处理输入"""
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        
        if event.type == KEYDOWN:
            # 方向控制
            if event.key == K_UP or event.key == K_w:
                game_state.snake.change_direction(0, -1)
            elif event.key == K_DOWN or event.key == K_s:
                game_state.snake.change_direction(0, 1)
            elif event.key == K_LEFT or event.key == K_a:
                game_state.snake.change_direction(-1, 0)
            elif event.key == K_RIGHT or event.key == K_d:
                game_state.snake.change_direction(1, 0)
            
            # 游戏控制
            elif event.key == K_r:
                game_state.reset()
            elif event.key == K_p:
                game_state.toggle_pause()
            elif event.key == K_ESCAPE or event.key == K_q:
                return False
    
    return True


def main():
    """主函数"""
    # 初始化 Pygame
    pygame.init()
    pygame.display.set_caption("贪吃蛇")
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(config.FONT_NAME, config.FONT_SIZE)
    
    # 初始化游戏状态
    game_state = GameState()
    
    # 游戏循环
    running = True
    last_update_time = 0
    
    while running:
        current_time = pygame.time.get_ticks()
        
        # 处理输入
        running = handle_input(game_state)
        
        # 更新游戏状态（根据速度控制更新频率）
        if not game_state.is_paused():
            update_interval = 1000 / game_state.get_speed()
            if current_time - last_update_time >= update_interval:
                game_state.update()
                last_update_time = current_time
        
        # 绘制
        screen.fill(config.BACKGROUND)
        draw_grid(screen)
        draw_snake(screen, game_state.snake)
        draw_food(screen, game_state.food)
        draw_ui(screen, game_state, font)
        
        pygame.display.flip()
        clock.tick(config.FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()