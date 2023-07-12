from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_name = models.CharField(max_length=255)
    games_played = models.PositiveIntegerField(default=0)
    highscore = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.avatar_name:
            self.avatar_name = self.user.username
        super().save(*args, **kwargs)

    def increment_games_played(self):
        self.games_played += 1

    def update_highscore(self, score):
        if score > self.highscore:
            self.highscore = score


class Game(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    board_width = models.PositiveIntegerField()
    board_height = models.PositiveIntegerField()
    snake_body = models.TextField(default='')
    food_position_row = models.PositiveIntegerField()
    food_position_col = models.PositiveIntegerField()

    def initialize_snake(self, initial_length):
        initial_row = self.board_height // 2
        initial_col = self.board_width // 2
        snake_body = [
            (initial_row, initial_col - i) for i in range(initial_length)
            ]
        self.snake_body = self._serialize_body(snake_body)

    """Retrieves the snake's body as a list of tuples representing
       each segment's position."""
    def get_snake_body(self):
        return self._deserialize_body(self.snake_body)

    """Updates the snake's body position with a new body provided
       as a list of tuples."""
    def update_snake_position(self, new_body):
        self.snake_body = self._serialize_body(new_body)

    """Serializes the snake's body from a list of tuples into a
       string representation."""
    def _serialize_body(self, body):
        return ','.join(f'{row},{col}' for row, col in body)

    """Deserializes the snake's body from a string representation
       into a list of tuples."""
    def _deserialize_body(self, body_str):
        return [tuple(map(int, segment.split(','))
                      ) for segment in body_str.split(',')]

    """Check for snake hitting walls"""
    def check_collision(self, next_row, next_col):
        if next_row < 0 or next_row >= self.board_height or \
           next_col < 0 or next_col >= self.board_width:
            return True

        snake_body = self.get_snake_body()
        if (next_row, next_col) in snake_body[1:]:
            return True

        return False

        """Set control meanings for snake direction input"""
    def move_snake(self):
        snake_head = self.get_snake_head()
        snake_body = self.get_snake_body()

        if not snake_head:
            return

        next_row, next_col = snake_head
        if self.direction == 'up':
            next_row -= 1
        elif self.direction == 'down':
            next_row += 1
        elif self.direction == 'left':
            next_col -= 1
        elif self.direction == 'right':
            next_col += 1
        
        new_body = [snake_head] + snake_body[:-1]
        self.update_snake_position(new_body)


class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.player.avatar_name}: {self.score}'
