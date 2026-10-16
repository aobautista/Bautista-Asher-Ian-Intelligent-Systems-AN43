import random
import agentpy as ap
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class RandomWalker(ap.Agent):
    def step(self):
        x, y = self.position
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Make rightward movement more likely when selected.
        if self.model.p.movement_rule == "preferred":
            moves += [(1, 0), (1, 0)]

        # Avoid cells occupied by other agents when possible.
        if self.model.p.movement_rule == "avoid":
            occupied = {
                other.position
                for other in self.model.agents
                if other is not self
            }
            safe_moves = [
                move for move in moves
                if self.model.bounded_position(
                    x + move[0], y + move[1]
                ) not in occupied
            ]
            if safe_moves:
                moves = safe_moves

        dx, dy = random.choice(moves)
        self.position = self.model.bounded_position(x + dx, y + dy)
        self.path.append(self.position)


class RandomWalkModel(ap.Model):
    def bounded_position(self, x, y):
        """Keep coordinates inside the grid."""
        maximum = self.p.grid_size - 1
        return (
            max(0, min(maximum, x)),
            max(0, min(maximum, y)),
        )

    def setup(self):
        self.agents = ap.AgentList(self, self.p.agents, RandomWalker)

        for agent in self.agents:
            agent.position = (
                random.randint(0, self.p.grid_size - 1),
                random.randint(0, self.p.grid_size - 1),
            )
            agent.path = [agent.position]

    def step(self):
        for agent in self.agents:
            agent.step()


def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Please enter a whole number greater than zero.")


def main():
    print("\n--- Random Walk Simulation ---")
    num_agents = get_positive_int("Enter number of agents: ")
    grid_size = get_positive_int("Enter grid size: ")
    num_steps = get_positive_int("Enter number of steps: ")

    rule = input(
        "Movement rule (random / avoid / preferred) "
        "[default: random]: "
    ).strip().lower()

    if rule not in {"random", "avoid", "preferred"}:
        rule = "random"

    parameters = {
        "agents": num_agents,
        "grid_size": grid_size,
        "steps": num_steps,
        "movement_rule": rule,
    }

    model = RandomWalkModel(parameters)
    model.setup()

    print("\nInitial positions:")
    for number, agent in enumerate(model.agents, start=1):
        print(f"Agent {number}: {agent.position}")

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_title(f"Random Walk — {rule} movement")
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(-0.5, grid_size - 0.5)
    ax.set_xticks(range(grid_size))
    ax.set_yticks(range(grid_size))
    ax.grid(True, alpha=0.4)

    positions = [agent.position for agent in model.agents]
    dots = ax.scatter(
        [position[0] for position in positions],
        [position[1] for position in positions],
        s=120,
        color="crimson",
        zorder=3,
    )

    colors = plt.colormaps["tab20"].resampled(num_agents)
    path_lines = [
        ax.plot([], [], color=colors(i), linewidth=1.5, alpha=0.7)[0]
        for i in range(num_agents)
    ]

    last_frame = -1

    def update(frame):
        nonlocal last_frame

        # Matplotlib may request the first frame more than once.
        if frame > last_frame:
            model.step()
            last_frame = frame

        positions = [agent.position for agent in model.agents]
        dots.set_offsets(positions)

        for agent, line in zip(model.agents, path_lines):
            x_values, y_values = zip(*agent.path)
            line.set_data(x_values, y_values)

        ax.set_xlabel(f"Step {last_frame + 1} of {num_steps}")
        return [dots, *path_lines]

    # Keep this variable alive while the window is open.
    animation = FuncAnimation(
        fig,
        update,
        frames=num_steps,
        interval=300,
        repeat=False,
        blit=False,
    )

    plt.show()

    print("\nFinal positions and recorded paths:")
    for number, agent in enumerate(model.agents, start=1):
        print(f"Agent {number}:")
        print(f"  Final position: {agent.position}")
        print(f"  Path: {agent.path}")


if __name__ == "__main__":
    main()