class GameLogic:
    def __init__(self):
        self.level = 1
        self.tasks_completed = 0
        self.current_task = None

    def process_input(self, user_input):
        user_input = user_input.lower().strip()

        if user_input == "next level":
            return self.next_level()
        elif user_input == "next task":
            return self.next_task()
        elif self.current_task:
            return self.handle_task_answer(user_input)
        else:
            return "Unknown command. Try 'Next Task' or 'Next Level'."

    def next_level(self):
        if self.tasks_completed >= self.level * 2:
            self.level += 1
            return f"Congrats! You've advanced to Level {self.level}."
        else:
            return f"You need more tasks completed to level up. Current: {self.tasks_completed}, Required: {self.level * 2}"

    def next_task(self):
        self.current_task = self.task_is_sky_blue
        return "Task: Is the sky blue? (yes/no)"

    def handle_task_answer(self, answer):
        result = self.current_task(answer)
        self.current_task = None
        return result

    def task_is_sky_blue(self, answer):
        if answer in ["yes", "y"]:
            self.tasks_completed += 1
            return "Correct! Task completed."
        else:
            return "Incorrect. Try again later."
