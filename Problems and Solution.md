# Problems and Solutions

## Problem #1: Database Spam

### Observation

Every detected object was being saved every frame.

Example:

Bottle
Bottle
Bottle
Bottle
Bottle

### Root Cause

The system stored detections instead of events.

### Solution

Switched to event-based memory.

Stored:

* Bottle appeared
* Bottle disappeared

instead of storing every frame.

### Result

Database size reduced dramatically and memory became meaningful.

---

## Problem #2: False Positive Detections

### Observation

YOLO occasionally detected objects that did not exist.

Examples:

* Bird
* Banana
* Knife

### Root Cause

Single-frame detections were trusted immediately.

### Solution

Introduced confidence threshold planning and multi-frame validation.

### Result

System became more resistant to noisy detections.

---

## Problem #3: Detection Flickering

### Observation

Objects repeatedly appeared and disappeared even when stationary.

### Root Cause

YOLO occasionally missed detections for individual frames.

### Solution

Designed a frame-confirmation system requiring multiple detections before confirming an object's presence.

### Result

Reduced event spam and increased stability.

---

## Problem #4: Object Identity

### Observation

YOLO can identify a bottle but cannot determine which bottle is being observed.

### Example

Blue bottle
Green bottle

Both are classified as:

Bottle

### Current Status

Unsolved.

### Future Direction

Investigate object re-identification and visual fingerprinting.
# Problem #5 - Scene Spam

## Problem

The first version of scene memory stored a new scene whenever the detected object list changed.

Example:

Scene 1:

* Keyboard
* Mouse

Scene 2:

* Keyboard

Scene 3:

* Keyboard
* Mouse

Although the rover never changed location, three separate scenes were created.

## Root Cause

YOLO detections are not perfectly stable.

Sometimes an object is temporarily missed even though it is still present in the scene.

The scene memory system treated these temporary detection losses as completely new environments.

## Observation

A scene is not simply a list of detected objects.

Small detection changes do not necessarily mean the rover has moved.

## Proposed Solution

Introduce scene similarity scoring.

Example:

Scene A:

* Keyboard
* Mouse

Scene B:

* Keyboard

Because most objects overlap, these scenes should be considered the same location.

Future versions should compare scene similarity rather than requiring exact object matches.

## Status

Discovered during Scene Memory Prototype testing.

Solution not yet implemented.
Problem #6

A scene change is not the same thing as an object change.

The room remained the same.

Only the detected objects changed.

Current memory system incorrectly creates new scenes when objects appear or disappear.

Future solution:

Use image similarity before deciding whether a new scene should be created.
---

## Problem #7: Scene Matching Fails When Camera Is Moving

### Observation

The rover sometimes saved new scenes even though it was looking at the same location.

Example:

Scene A:

* Keyboard
* Phone

Scene B:

* Keyboard
* Phone

However, Scene B was captured while the camera was moving, causing motion blur.

The system incorrectly treated the blurred image as a new environment.

### Root Cause

Image similarity comparison assumes both images are reasonably clear.

Motion blur changes pixel information significantly even when the environment remains unchanged.

### Solution

Future rover versions should only capture scene memories when the rover is stationary.

Possible improvements:

* Motion detection
* Blur detection
* Stability checks before saving

### Result

Identified an important limitation of image-based scene recognition.

---

## Problem #8: Object Confidence Thresholds Affect Memory Quality

### Observation

Important objects were visible to a human observer but were not always added to memory.

Example:

Bottle detected at:

0.39 confidence

Current threshold:

0.55 confidence

Result:

Bottle was ignored despite being clearly visible.

### Root Cause

A single confidence threshold is too strict for all object classes.

Small objects, partially occluded objects, and poorly lit objects often receive lower confidence scores.

### Proposed Solution

Use temporal validation instead of relying solely on confidence.

Example:

Accept an object if:

* It appears in most frames over a time window
* Average confidence remains above a minimum threshold

This allows stable low-confidence detections to be remembered.

### Status

Partially solved through multi-frame observation.

Future versions may use confidence averaging and object persistence scoring.

---

## Problem #9: Memory Retrieval Required Hardcoded Logic

### Observation

Early memory retrieval relied on predefined workflows.

Example:

User:

```text
Where is the keyboard?
```

Required a dedicated search pipeline that explicitly extracted the object name and performed a fixed lookup.

The rover could retrieve memory, but it could not reason about user intent.

### Root Cause

Memory retrieval logic was tightly coupled to individual query types.

Each new capability required new hardcoded logic.

Current architecture did not scale well as the number of memory tools increased.

### Solution

Introduce a planner-based architecture.

New workflow:

```text
User Query
↓
Planner
↓
Select Appropriate Tool
↓
Retrieve Memory
↓
Generate Answer
```

The planner interprets the user's request and determines which memory operation should be executed.

### Result

Memory retrieval became modular and extensible.

New capabilities can now be added through tools rather than creating entirely new query pipelines.

### Status

Solved in v0.4.

---

## Problem #10: Rover Had No Conversation Memory

### Observation

The rover could answer questions but could not remember previous interactions.

Example:

User:

```text
Where is the keyboard?
```

Followed by:

```text
How many times was it observed?
```

The rover treated each question as an isolated request.

### Root Cause

No short-term memory existed between interactions.

Previous questions and answers were discarded after response generation.

### Solution

Introduce conversation memory.

Store recent:

* User queries
* Rover responses

Maintain a rolling memory window of recent interactions.

### Result

The rover now possesses short-term conversational memory and can provide context to future reasoning systems.

### Status

Partially solved in v0.4.

Conversation memory exists but is not yet heavily utilized by the planner.

---

## Problem #11: Single Tool Execution Limits Reasoning

### Observation

The rover can access multiple memory tools but can only execute one tool per query.

Example:

User:

```text
What objects do you know and how many times was the keyboard observed?
```

Current behavior:

```text
Select one tool
Return one result
```

Desired behavior:

```text
Select multiple tools
Combine results
Generate unified answer
```

### Root Cause

Current state architecture stores:

```python
action
tool_result
```

which assumes a single action and a single result.

The planner can only route to one operation.

### Proposed Solution

Redesign state architecture.

Current:

```python
action
tool_result
```

Future:

```python
actions
tool_results
```

Planner output:

```json
{
    "actions": [
        {
            "tool": "LIST_ALL_OBJECTS"
        },
        {
            "tool": "COUNT_OBJECT_OCCURRENCES",
            "object_name": "keyboard"
        }
    ]
}
```

Execution engine:

```text
Planner
↓
Execute Tool 1
↓
Execute Tool 2
↓
Aggregate Results
↓
Answer
```

### Expected Benefits

* Multi-tool reasoning
* Better memory utilization
* Richer answers
* More natural conversations
* Foundation for autonomous planning

### Status

Discovered during v0.4 development.

Planned for v0.5.



