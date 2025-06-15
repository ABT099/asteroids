from src.game.constants import MARGIN, SCREEN_WIDTH


class Game:
    def __init__(self, screen, font):
        self.screen = screen
        self.current_score = 0
        self.previous_score = 0
        self.highest_score = 0
        self.font = font

    def render_scores(self):
        current_text = self.font.render(f"Score: {self.current_score}", True, (255, 255, 255))
        previous_text = self.font.render(f"Previous: {self.previous_score}", True, (255, 255, 255))
        highest_text = self.font.render(f"Highest: {self.highest_score}", True, (255, 255, 255))

        current_rect = current_text.get_rect(topright=(SCREEN_WIDTH - MARGIN, MARGIN))
        previous_rect = previous_text.get_rect(topright=(SCREEN_WIDTH - MARGIN, MARGIN + 40))
        highest_rect = highest_text.get_rect(topright=(SCREEN_WIDTH - MARGIN, MARGIN + 80))

        self.screen.blit(current_text, current_rect)
        self.screen.blit(previous_text, previous_rect)
        self.screen.blit(highest_text, highest_rect)

    def render_game_over(self):
        game_over_text = self.font.render("Game Over! Press R to restart", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_WIDTH / 2))
        self.screen.blit(game_over_text, game_over_rect)
    
    def die(self, player):
        self.previous_score = self.current_score
        self.current_score = 0
        player.kill()
        if not player.could_respawn():
            # Only update highest score when player is completely dead
            self.highest_score = max(self.highest_score, self.previous_score)

    def reset_game(self, player):
        player.respawn()
        player.lives = 3
        self.current_score = 0
        self.previous_score = 0
        self.highest_score = max(self.highest_score, self.previous_score)

    def update_score(self, points):
        self.current_score += points
        largest = max(self.current_score, self.previous_score)
        if largest > self.highest_score:
            self.highest_score = largest
