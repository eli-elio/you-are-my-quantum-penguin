# You Are My *Quantum* Penguin

**Game Title:** You Are My *Quantum* Penguin
**Developer:** Eli Zobens

## Game Concept

*You Are My Quantum Penguin* is a single-player 2D puzzle-adventure game in which the player controls a penguin traveling through an Antarctic environment in search of the perfect pebble for their partner.

The game world consists of two connected layers: the ice surface and the water. The penguin can use quantum mechanics to change their state, switch between these layers, enter superposition, and interact with quantum objects. Fish also have quantum states that can change independently during the game.

The player must collect fish, use quantum abilities to overcome obstacles, find the special pebble, and eventually guide the penguin back to their partner.

## Story / Theme

The game takes place in an Antarctic environment of ice, snow and water. The main character is a penguin who wants to find the perfect pebble and bring it back as a gift to their partner.

To find the pebble, the penguin has to explore the surrounding environment. During the journey, they encounter fish, maybe some obstacles, and quantum phenomena that affects the penguin and parts of the game world.

After finding the pebble, the penguin must take their way back to their partner while managing the resources. The game ends when the penguin successfully returns and delivers the pebble.

## Quantum Concepts

The game will use **quantum states, superposition, measurement, and quantum gates**.

The penguin can exist in different quantum states. The state `|0>` represents the penguin being on the ice surface, while `|1>` represents the penguin being underwater. The player will be able to manipulate the penguin's state using quantum gates.

The **X gate** switches the penguin between `|0>` and `|1>`, allowing them to move between the ice and the water.

The **Hadamard (H) gate** can place the penguin into a superposition state (`|+>` or `|->`). In superposition, the penguin is represented in both ice and water at the same time.

The **Z gate** changes the phase of the superposition, switching between `|+>` and `|->`. These two states will allow the penguin to interact with different quantum objects or obstacles in the environment.

**Measurement** collapses a superposition into one of the classical states, `|0>` or `|1>`. Measurement will also be used when interacting with quantum fish.

Fish can have their own quantum states that change independently during the game. A fish in superposition can have two possible locations. When penguin attempts to catch it, the fish is measured and collapses into one of those locations, determining whether the penguin successfully catches it.

## Quantum Game Mechanics

The player must understand and manipulate the penguin's quantum state to explore the environment, collect resources, and reach areas that would otherwise be inaccessible.

The game world has to connected layers: the ice surface (`|0>`) and the water (`|1>`). By applying an X gate, the player can switch the penguin between these states. The two layers contain different paths, obstacles, and objects, so changing the quantum state also changes which parts of environment the player can access.

The H gate allows the penguin to enter superposition. In the `|+>` and `|->` states, the penguin can exist in both layers at the same time and interact with quantum elements. The Z gate switches between `|+>` and `|->`. Some quantum obstacles or paths will react differently to these two states, requiring the player to choose and combine gates to progress.

Measurement collapses the penguin from superposition into either `|0>` or `|1>`. This can change the penguin's position and determine which layer the player continues in.

Quantum mechanics also affect fish. Some fish can exist in a superposition of two possible locations, and their states can change independently without direct player control. When the penguin attempts to catch a fish, a measurement occurs. If the fish collapses into the location of the penguin, it is caught; otherwise, the attempt fails. Caught fish are stored as a limited resource and can be used for the penguin's quantum abilities.

Although measurement introduces probabilistic outcomes, the game is not based only on classical randomness. The player can deliberately manipulate the penguin's quantum state using X, H, and Z gates. The order in which gates are applied changes the state of the penguin and therefore changes the possible actions, paths, and interactions available to the player. The challenge comes from deciding when and how to manipulate or measure quantum states, while the independently changing fish states add an element of uncertainty.

## Gameplay and Rules

The game will be a **single-player 2D puzzle-adventure** played in real time. The player controls one penguin and explores an Antarctic environment consisting of connected ice and water areas.

The main player actions are moving the penguin, interacting with objects, attempting to catch fish, and applying quantum gates to change the penguin's state. The player can use the X gate to switch between the ice and underwater states, the H gate to enter or leave superposition, and the Z gate to change between the `|+>` and `|->` superposition states.

Different quantum states give access to different parts of the environment. Some paths or objects may only be accessible from the ice or water layer, while special quantum obstacles may require the penguin to be in a particular superposition state. The player therefore has to choose when to change states and which gates to apply.

Fish can be encountered while exploring. Some fish have quantum states and can exist in a superposition of two possible locations. Their states may change independently during the game. When the player attempts to catch a fish, it is measured. A successful catch adds the fish to the player's inventory and collected fish can be spent to use certain quantum abilities.

A typical game session begins with the penguin leaving their home to explore the environment. The player moves between ice and water, catches fish, manages the available fish resources, and solves puzzles by manipulating quantum states. The main destination is the location of the special pebble. After finding it, the player must travel back through the environment and return to the starting area while continuing to manage the remaining resources and quantum states.

The game is not turn-based, but some events, such as measurements and changes in the quantum states of fish, can occur during exploration and affect the player's next decision.

## Winning /  Losing /  Game Objectives

The main objective of the game is to explore the Antarctic environment, find the perfect pebble, and bring it back to the penguin's partner.

During the journey, the player must navigate between the ice and underwater layers, collect fish, and solve puzzles by using the penguin's quantum abilities. Finding the pebbles marks the halfway point of the journey, as the player must return to the starting area.

The game does not have a traditional losing condition. The focus is on exploration, puzzle solving, and experimenting with quantum mechanics rather than punishment or survival. If the player makes an unsuccessful measurement or fails to catch a fish, the journey continues and player can try a different approach.

The game is completed when the penguin successfully returns to their partner and gives them the pebble.

## Platform and Development Tools

The game will be developed as a desktop game using **Python** and the **Pygame** library. The main development environment will be **PyCharm**.

**GitHub** will be used for version control, project documentation, and storing the source code throughout development.

The initial target platform is desktop (Linux, Windows, and macOS where the required Python environment is available).

## Originality / Existing Games

The game is not based on or directly inspired by a specific existing game. I chose a penguin as the main character simply because I like penguins and wanted to create a game around a theme that I personally enjoy.

I generally enjoy chill and cozy games that allow the player to explore at their own pace, while still having a small challenge or a clear mission to complete. I also like games that give the player a sense of progress and end with satisfying, positive outcome. These preferences inspired the overall direction of the game: the player has a clear goal, but the journey itself focuses more on exploration, puzzle solving, and experimentation than on winning or losing.

The quantum mechanics were developed around this idea rather than adapted from an existing game. Switching between the ice and underwater states, entering superposition, interacting with state-dependent objects, and measuring quantum fish are intended to provide the puzzle and challenge elements while keeping the overall experience relaxed.

The story of searching for the perfect pebble and eventually returning to the penguin's partner gives the game a simple objective and a positive ending to work toward.
