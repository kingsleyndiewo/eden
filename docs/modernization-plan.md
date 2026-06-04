Eden Modernization Plan
=======================

Goals
-----

- Keep existing samples runnable on Panda3D 1.10.16
- Reduce hidden runtime assumptions
- Make core APIs safer to change
- Add enough automated validation to support incremental refactors

Phase 1: Stabilize Runtime
--------------------------

- Keep removing Python-2-era syntax and APIs from runtime code
- Fix helper defects in small reusable methods before changing architecture
- Add smoke tests for world helpers, XML parsers, and simulator utilities
- Ensure examples use explicit `instance.run()` entry points

Phase 2: Make Project Discovery Explicit
----------------------------------------

- Replace cwd-dependent MVC discovery with explicit project-root resolution
- Allow world classes to accept a project root or config path directly
- Stop relying on relative `../` chains for resources and config

Phase 3: Introduce Typed Data Structures
----------------------------------------

- Replace positional list storage in `objectStore` and similar containers with
  `dataclass` records or small classes
- Add type hints for public framework methods and config-derived structures
- Separate config parsing from scene-object mutation where practical

Phase 4: Narrow Integration Boundaries
--------------------------------------

- Replace raw picker dependency bundles with focused interfaces
- Isolate Panda3D globals behind world methods where feasible
- Separate board-game rules from rendering and input plumbing

Phase 5: Improve Packaging and Tooling
--------------------------------------

- Add a `pyproject.toml` with optional development dependencies
- Standardize test entry points and lint/type-check commands
- Add CI for smoke tests and compile checks
- Consider packaging `eden_lib/Eden` as an installable distribution

High-Value Early Refactors
--------------------------

- `Creation.checkMVC` and config loading path assumptions
- `Creation.loadGeometry` storage shape and side effects
- `Genesis.loadActor` config-to-actor transformation
- picker initialization in `Eve` and `Board_8x8`

Definition of Done for Modernization
------------------------------------

- Samples still launch under Panda3D 1.10.16
- Core helper methods have automated coverage
- Runtime no longer depends on Python-2 idioms
- Project startup can be driven from explicit paths
- Documentation explains both current architecture and migration direction