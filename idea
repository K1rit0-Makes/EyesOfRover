# Future Idea: Scene-Based Navigation (Inspired by SLAM Concepts)

## Origin

While developing EyesOfRover, a problem was discovered:

The rover could detect and remember objects, but it had no understanding of where it was.

This led to a new question:

> The real problem is not "Where is the bottle?"
>
> The real problem is "Where am I?"

## Proposed Approach

Instead of relying on GPS, coordinates, or expensive sensors, the rover can build a memory of scenes.

Example:

Scene A:

* Desk
* Chair
* Monitor

Scene B:

* Desk
* Chair
* Bed

Scene C:

* Bed
* Window
* Bottle

The rover stores these observations and links them together as it moves.

## Navigation Concept

1. Observe surroundings.
2. Save a scene snapshot.
3. Move.
4. Observe again.
5. Compare with previously seen scenes.
6. Build a mental map of connected locations.

When searching for an object, the rover can attempt to return to the last scene in which the object was observed.

## Inspiration

After discussing the concept, it was discovered that this idea shares similarities with SLAM (Simultaneous Localization and Mapping), particularly scene-based and topological mapping approaches.

This idea was independently reached during development of EyesOfRover while attempting to solve the object search problem.

## Current Status

Concept only.

Future research topics:

* Scene similarity scoring
* Place recognition
* Topological maps
* Visual localization
* SLAM
* Object search and retrieval
