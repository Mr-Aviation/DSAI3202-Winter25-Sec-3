
# Maze Explorer - Question 1 Answer

## Question 1: How does the automated maze explorer work?

This answer explains how the maze explorer works step by step. We will look at the algorithm it uses, how it avoids going in circles, how it goes back when stuck, and what kind of stats it gives when it finishes solving the maze.

---

## What algorithm does the explorer use?

The maze explorer uses something called the **right-hand rule**. It’s a simple idea: just imagine you're walking through a maze with your right hand always touching the wall. As long as you keep your right hand on the wall, you’ll eventually find the way out—at least in most mazes.

Here's what the explorer does:

1. **Try turning right** and see if it can go that way.
2. If that doesn’t work, it **tries going straight**.
3. If that also doesn’t work, it **turns left**.
4. If all directions are blocked, it **turns around** and moves back.

This step-by-step check helps it to keep following walls and exploring all paths in an organized way.

---

## How does it avoid getting stuck in a loop?

Sometimes in a maze, you might go in circles without realizing it. The explorer is smart enough to notice when it’s going in a loop. 

Here’s how it works:

- It keeps track of the last **three positions** it moved to.
- If all three of those positions are the **same**, it means it’s stuck.
- When it notices that, it decides to **stop exploring that direction** and starts backtracking (which we explain next).

This is a simple but clever way to break out of loops without needing a map of the whole maze.

---

## What backtracking strategy does it use?

When the explorer realizes it's stuck or can't find a new way forward, it starts to **backtrack**. That means it goes back to a place it visited earlier where there were other possible paths it didn’t try.

Here’s how it backtracks:

1. It looks at all the moves it has made so far.
2. It finds a place where it had **more than one direction** to go.
3. Then it builds a path **back to that place** and starts moving there step by step.
4. Once it reaches that point, it starts exploring again from there.

This helps the explorer to find a way out even if the current path is a dead end.

The explorer also counts how many times it had to backtrack and keeps track of that.

---

## What statistics does it show after solving the maze?

After it finishes exploring and reaches the goal, it gives some stats to show how it did. These help us understand how hard the maze was and how well the explorer performed.

Here’s what it shows:

- **Time taken** to solve the maze.
- **Total number of moves** it made (how many steps).
- **Number of backtracks** (how many times it had to go backward).
- **Average moves per second**, which tells how fast it was moving.

These stats appear clearly in the console so you can compare runs with and without visualization or between different mazes.

---

## Summary

To wrap it all up:

- The maze explorer uses a simple method called the **right-hand rule** to find its way.
- It avoids getting stuck by checking if it’s visiting the same spot over and over.
- When stuck, it **backtracks** to a spot with other options.
- In the end, it gives you useful stats to see how it did.

This smart little program can solve many types of mazes, even if they are tricky. It’s designed in a way that beginners can understand but still solves the maze effectively.



