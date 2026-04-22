"""
贪吃蛇游戏逻辑
"""

import random
from dataclasses import dataclass
from typing import List, Tuple, Optional
import config


@dataclass
class Position:
    """网格位置"""
    x: int
    y: int
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))


class Snake:
    """蛇类"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置蛇的状态"""
        # 初始位置在屏幕中央
        center_x = config.GRID_WIDTH // 2
        center_y = config.GRID_HEIGHT // 2
        self.body = [
            Position(center_x, center_y),
            Position(center_x - 1, center_y),
            Position(center_x - 2, center_y)
        ]
        self.direction = (1, 0)  # 初始向右
        self.next_direction = self.direction
        self.grow = False
    
    def change_direction(self, dx: int, dy: int):
        """改变方向（防止直接反向）"""
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.next_direction = (dx, dy)
    
    def move(self):
        """移动一步"""
        self.direction = self.next_direction
        head = self.body[0]
        new_head = Position(
            head.x + self.direction[0],
            head.y + self.direction[1]
        )
        
        # 检查是否撞墙
        if not (0 <= new_head.x < config.GRID_WIDTH and 0 <= new_head.y < config.GRID_HEIGHT):
            return False
        
        # 检查是否撞到自己
        if new_head in self.body:
            return False
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        return True
    
    def eat(self):
        """标记需要增长"""
        self.grow = True
    
    def get_head(self) -> Position:
        """获取头部位置"""
        return self.body[0]
    
    def get_body(self) -> List[Position]:
        """获取身体位置列表"""
        return self.body


class Food:
    """食物类"""
    
    def __init__(self, snake: Snake):
        self.position = self.generate_position(snake)
    
    def generate_position(self, snake: Snake) -> Position:
        """生成不在蛇身上的随机位置"""
        while True:
            pos = Position(
                random.randint(0, config.GRID_WIDTH - 1),
                random.randint(0, config.GRID_HEIGHT - 1)
            )
            if pos not in snake.get_body():
                return pos
    
    def respawn(self, snake: Snake):
        """重新生成食物"""
        self.position = self.generate_position(snake)
    
    def get_position(self) -> Position:
        """获取食物位置"""
        return self.position


class GameState:
    """游戏状态"""
    
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = 0
        self.speed = config.INITIAL_SPEED
        self.game_over = False
        self.paused = False
    
    def reset(self):
        """重置游戏"""
        self.snake.reset()
        self.food = Food(self.snake)
        self.score = 0
        self.speed = config.INITIAL_SPEED
        self.game_over = False
        self.paused = False
    
    def update(self):
        """更新游戏状态"""
        if self.game_over or self.paused:
            return
        
        # 移动蛇
        if not self.snake.move():
            self.game_over = True
            return
        
        # 检查是否吃到食物
        if self.snake.get_head() == self.food.get_position():
            self.snake.eat()
            self.score += 1
            self.speed += config.SPEED_INCREMENT
            self.food.respawn(self.snake)
    
    def get_score(self) -> int:
        """获取当前分数"""
        return self.score
    
    def get_speed(self) -> float:
        """获取当前速度"""
        return self.speed
    
    def is_game_over(self) -> bool:
        """游戏是否结束"""
        return self.game_over
    
    def is_paused(self) -> bool:
        """游戏是否暂停"""
        return self.paused
    
    def toggle_pause(self):
        """切换暂停状态"""
        self.paused = not self.paused