def get_room_state(room_name):
    """Ask the user whether a room starts dirty or clean."""
    while True:
        state = input(
            f"Enter the initial state of Room {room_name} (Dirty/Clean): "
        ).strip().lower()

        if state in ("dirty", "clean"):
            return state.title()

        print("Invalid input. Please enter Dirty or Clean.")


def is_dirty(environment, room):
    """Check whether a room is dirty."""
    return environment[room] == "Dirty"


def clean_room(environment, room):
    """Clean a room."""
    environment[room] = "Clean"


class RuleBasedAgent:
    """An agent that cleans a dirty room or moves from a clean room."""

    def __init__(self, starting_room="A"):
        self.location = starting_room

    def move(self):
        """Switch between Rooms A and B."""
        self.location = "B" if self.location == "A" else "A"

    def perceive_and_act(self, environment):
        """Check the current room and apply one rule."""
        if is_dirty(environment, self.location):
            clean_room(environment, self.location)
            return f"Cleaned Room {self.location}"

        previous_room = self.location
        self.move()
        return f"Moved from Room {previous_room} to Room {self.location}"


def get_steps():
    """Ask for a positive number of simulation steps."""
    while True:
        try:
            steps = int(input("How many simulation steps should the agent run? "))
            if steps > 0:
                return steps
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def main():
    # Set up the two-room environment.
    environment = {
        "A": get_room_state("A"),
        "B": get_room_state("B"),
    }

    agent = RuleBasedAgent()
    steps = get_steps()

    print("\n--- Rule-Based Agent Simulation ---")
    print(
        f"Initial environment: Room A = {environment['A']}, "
        f"Room B = {environment['B']}"
    )

    # Run one perceive-and-act cycle per step.
    for step in range(1, steps + 1):
        action = agent.perceive_and_act(environment)

        print(f"\nStep {step}")
        print(f"Agent location: Room {agent.location}")
        print(f"Action taken: {action}")
        print(
            f"Environment: Room A = {environment['A']}, "
            f"Room B = {environment['B']}"
        )


if __name__ == "__main__":
    main()