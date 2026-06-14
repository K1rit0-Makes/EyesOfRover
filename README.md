# EyesOfRover 

EyesOfRover is a robotics and AI learning project focused on building the perception and memory systems of an intelligent rover.

Unlike traditional object detection projects that only identify objects in a camera feed, EyesOfRover aims to answer a deeper question:

**How can a robot understand and remember the world around it?**

The project began with real-time object detection using YOLOv8 and gradually evolved into an engineering exploration of memory, reasoning, object identity, and autonomous search.

Current capabilities include:

* Real-time object detection using YOLOv8
* Event-based memory using SQLite
* Object appearance and disappearance tracking
* Confidence-based filtering
* Multi-frame validation to reduce false detections
* Version-controlled engineering development using Git and GitHub

## Engineering Challenges Explored

During development, several real-world robotics problems were discovered and analyzed:

* False positive detections
* Detection flickering
* Memory spam from frame-by-frame storage
* Object persistence after leaving the camera view
* Distinguishing between multiple instances of the same object
* Designing memory systems for autonomous agents

## Long-Term Vision

The ultimate goal is to create a rover capable of:

1. Seeing objects in its environment
2. Remembering what it has seen
3. Understanding object relationships and context
4. Searching for specific objects on command
5. Re-identifying previously observed objects
6. Interacting through natural language
7. Navigating autonomously in the physical world

EyesOfRover is not just a project repository—it is an engineering journal documenting the problems, mistakes, experiments, and solutions encountered while building an intelligent robotic perception system.
