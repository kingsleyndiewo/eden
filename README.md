Eden
=======

Repository for the Eden3D game framework by Funtrench. The library wraps Panda3D
with higher-level world, actor, board-game, UI, XML, and tooling abstractions,
and the repository includes playable examples plus feature demos.

Status
------

- Runtime target: Python 3.10+
- Engine target: Panda3D 1.10.16
- Validation: unit smoke tests plus interactive feature demos

What Is Here
------------

- `eden_lib/Eden`: the reusable framework package
- `eden_games/eden_maze`: 3D maze game built on `Adam`
- `eden_games/eden_ludo`: board game built on `Creation`
- `traffic_sim`: traffic simulator built on `Eve`
- `feature_tests`: interactive demos for framework slices

Core Architecture
-----------------

The framework is layered around a small inheritance tree:

- `Creation`: base Panda3D world bootstrap, MVC path discovery, XML config,
	resources, particles, and physics hooks
- `Genesis`: adds collisions, actor loading, and inventories
- `Adam`: single main actor worlds
- `Eve`: switchable actor worlds with actor picking
- `Board_8x8`: board-game simulator specialization on top of `Creation`

More detail is in `docs/architecture.md`.

Panda3D 1.10.16 Notes
---------------------

The codebase has been updated to remove a few legacy breakpoints that matter on
current Panda3D and Python 3 runtimes:

- `pandac.PandaModules` usage in live game code was replaced with
	`panda3d.core`
- example entry points now call `instance.run()` instead of relying on a bare
	global `run()`
- Python 2 dictionary APIs and print syntax were removed from runtime paths
- core helper defects in actor joint control and sound panning were fixed

Setup
-----

1. Create and activate a Python 3.10+ virtual environment.
2. Install Panda3D 1.10.16.
3. Run commands from the repository root.

Example:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install panda3d==1.10.16
```

Running Examples
----------------

Run from each sample's `scripts` directory or invoke the module path directly.

```bash
cd eden_games/eden_maze/scripts
python3 main.py
```

```bash
cd eden_games/eden_ludo/scripts
python3 main.py
```

```bash
cd traffic_sim/scripts
python3 main.py
```

Development Validation
----------------------

Run the smoke tests:

```bash
python3 -m unittest discover -s tests
```

Compile representative runtime files:

```bash
python3 -m py_compile \
	eden_lib/Eden/Eden3D/Actors/EdenActor.py \
	eden_lib/Eden/Eden3D/Worlds/Creation.py \
	eden_lib/Eden/Eden3D/Simulators/Board/Board_8x8.py \
	eden_games/eden_maze/scripts/EdenMaze.py \
	eden_games/eden_maze/scripts/main.py \
	eden_games/eden_ludo/scripts/main.py \
	traffic_sim/scripts/main.py
```

Interactive demos remain available under `feature_tests/run_all`, but they are
manual and require a graphical environment.
