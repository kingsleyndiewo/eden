Eden Architecture
=================

Overview
--------

Eden is a Panda3D-based framework that exposes ready-made classes for building
games and simulations. It combines engine bootstrap, config parsing, scene
assembly, UI helpers, simulation helpers, and sample projects in a single repo.

Package Layout
--------------

- `eden_lib/Eden/Eden2D`: menus, HUDs, text, and basic visual helpers
- `eden_lib/Eden/Eden3D`: worlds, actors, terrain, and board simulators
- `eden_lib/Eden/EdenTools`: XML parsers/generators, pickers, particles,
  session tooling, and MVC helpers

World Hierarchy
---------------

`Creation`

- Bootstraps Panda3D via `ShowBase`
- Validates the expected MVC-style project layout
- Parses `config.xml`
- Creates scene graph roots for geometry, actors, statics, and physics nodes
- Provides helpers for geometry, sounds, particles, screen capture, and physics

`Genesis`

- Extends `Creation`
- Adds collision handlers and a global collision traverser
- Adds actor loading and inventory loading
- Maintains actor and toolbox stores

`Adam`

- Extends `Genesis`
- Loads a single configured main actor
- Sets up actor collision and main camera offset

`Eve`

- Extends `Genesis`
- Loads multiple selectable actors
- Switches the active avatar and updates camera tracking
- Integrates actor picking

`Board_8x8`

- Extends `Creation`
- Implements board texture, tile, move logging, replay, and AI scaffolding
- Provides the base for checkers/chess-style simulators

Data Flow
---------

The dominant control flow is config-driven.

1. A sample or game-specific subclass instantiates a world class.
2. `Creation` discovers the MVC directory structure relative to the current
   script layout.
3. `config.xml` and related XML files provide world details, actor data,
   resources, HUD definitions, and simulator settings.
4. Game subclasses bind input, tasks, collision responses, HUD updates, and
   gameplay rules.

Strengths
---------

- Fast path from framework class to working sample
- Large amount of behavior exposed through XML configuration
- Reusable building blocks for several styles of Panda3D application

Current Constraints
-------------------

- World startup depends on current working directory conventions
- Core stores use loosely structured dictionaries and positional lists
- Engine globals such as `base`, `render`, and `taskMgr` are used directly
- Public behavior is defined more by inheritance and side effects than by a
  narrow explicit API
- Validation is still light compared with the size of the surface area

Suggested Development Style
---------------------------

- Treat `Creation` and `Genesis` as the stable integration seams
- Keep sample-specific logic in subclasses, not in the framework core
- Prefer adding coverage around utility methods before refactoring them
- Move path resolution and config handling toward explicit objects over time