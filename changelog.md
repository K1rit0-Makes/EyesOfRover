Changelog

v0.1 - Initial EyesOfRover Setup

Added

* YOLOv8 object detection
* SQLite memory database
* Event-based tracking
* GitHub integration

 Discovered Issues

* False positives
* Detection flickering
* Duplicate event storage

 Notes

This version focuses on proving the vision and memory pipeline.

## v0.2 - Scene Memory and Visual Memory System

### Added

* Scene-based memory architecture
* JSON scene storage (`scene_memory.json`)
* Scene change detection system
* Visual scene memory using saved camera images
* Automatic scene image linking inside memory records
* Scene timestamps for temporal tracking
* Runtime memory separation using `.gitignore`
* GitHub project documentation updates

### Improved

* Memory system evolved from event-only storage to scene-level storage
* Added support for storing object context instead of only appearance/disappearance events
* Scene records now store both detected objects and corresponding visual snapshots
* Repository structure cleaned and organized for future development

### Problems Identified

#### Problem #4 - Object Flickering Creates False Scene Changes

YOLO occasionally detects objects inconsistently between frames, causing the memory system to think a scene has changed when the environment has not.

**Example:**

Scene A:

* keyboard
* mouse

Next memory snapshot:

* keyboard

The mouse was not removed from the real world; YOLO simply failed to detect it.

---

#### Problem #5 - Visual Context Was Missing

The memory system stored only object names.

**Example:**

```json
{
    "objects": [
        "keyboard",
        "mouse"
    ]
}
```

This provided no visual evidence of what the rover actually saw.

**Solution:**

Store an image alongside each saved scene.

---

#### Problem #6 - Object Change Is Not Scene Change

The rover currently assumes that changes in detected objects automatically mean a new scene.

**Example:**

Scene 1:

* person
* bottle

Scene 2:

* person

Current system:

```text
New Scene
```

Actual reality:

```text
Same Scene
Bottle Removed
```

Future solution:

* Image similarity comparison
* Scene matching
* Change tracking within existing scenes

### Engineering Lessons Learned

* Runtime-generated data should never be committed to GitHub.
* Visual memory is required before scene comparison can exist.
* Scene understanding requires more than object detection.
* A robot must remember environments, not just labels.
* Proper Git workflows (commit, rebase, push) are essential for project maintenance.

### Notes

This version marks the transition from simple object detection to the first stage of environmental memory. EyesOfRover can now remember both what it detected and what it visually observed, laying the foundation for future scene recognition, place recognition, and SLAM-inspired navigation systems.

## v0.3 - Scene Recognition and Known Scene Matching

### Added

* Scene comparison engine (`scene_compare.py`)
* Image similarity-based scene matching
* Known scene recognition system
* Automatic duplicate scene prevention
* Scene ID tracking and retrieval
* YOLOv8m integration for improved detection accuracy
* Improved Git repository structure and asset management

### Improved

* Reduced duplicate scene saves caused by minor object fluctuations
* Scene recognition now considers visual similarity instead of only detected objects
* Added support for recognizing previously observed environments
* Improved detection reliability for small and partially occluded objects
* Runtime-generated files are now excluded from Git tracking

### Problems Identified

#### Problem #7 - Object Detection Alone Cannot Represent a Scene

The system initially attempted to identify scenes solely using detected object lists.

Example:

Scene A:

* keyboard
* mouse
* phone

Scene B:

* keyboard
* mouse
* phone

Although the object lists are identical, the actual environments may be completely different.

Result:

```text
False Scene Match
```

Lesson:

A scene must be compared visually, not only semantically.

---

#### Problem #8 - Camera Motion Creates False Scenes

When the webcam moves rapidly, captured frames become blurred.

Example:

* Same desk
* Same objects
* Motion blur introduced

Current system:

```text
New Scene Detected
```

Actual reality:

```text
Same Scene
Poor Frame Quality
```

Future solution:

* Rover captures scenes only when stationary
* Blur detection before saving
* Quality scoring for scene images

---

#### Problem #9 - Object Confidence Thresholds Affect Memory Quality

Objects such as bottles, cups, and small desk items often appear with lower confidence scores.

Example:

```text
Bottle: 0.39 confidence
```

Current challenge:

Strict confidence thresholds prevent useful objects from entering memory.

Future solution:

* Temporal confidence averaging
* Multi-frame voting
* Object persistence tracking

### Engineering Lessons Learned

* Object detection and scene recognition are separate problems.
* Visual memory must exist before intelligent search can exist.
* Scene similarity is more reliable than object lists alone.
* Runtime data should remain local and not be committed to Git.
* Model weights should never be stored inside the repository.
* AI search requires structured memory before reasoning can occur.

### Notes

This version marks the transition from scene storage to scene recognition.

EyesOfRover can now compare newly observed environments against previously stored visual memories and determine whether the rover has encountered a scene before.

This milestone establishes the foundation for the next phase:

* LangChain integration
* Tool-calling AI agents
* Natural language scene search
* Visual memory retrieval
* Context-aware rover reasoning
  -----------------------------
  ## v0.4 - Planner-Based Memory Agent and Natural Language Reasoning

### Added

* LangGraph-based agent architecture
* Planner node for natural language query interpretation
* Local LLM integration (`llm.py`)
* Conversation memory system (`conversation_memory.py`)
* Natural language memory querying
* Tool-driven memory retrieval pipeline
* Object occurrence counting tool
* Nearby object analysis tool
* Latest scene retrieval tool
* First observation retrieval tool
* Last observation retrieval tool
* Object timeline retrieval tool
* Scene comparison tool
* Expanded memory search capabilities
* Git version tagging (`v0.4`)

### Improved

* Transitioned from hardcoded object extraction to planner-driven reasoning
* Separated reasoning, memory retrieval, and response generation into independent modules
* Expanded memory capabilities beyond simple scene lookup
* Improved project structure and maintainability
* Added support for conversational interactions with rover memory
* Introduced short-term conversation memory for contextual responses

### Problems Identified

#### Problem #10 - Memory Retrieval Was Not Intelligent

Previous versions relied on predefined logic to retrieve information.

Example:

```text
Where is keyboard?
```

Required a dedicated search pipeline.

The rover could not reason about the user's intent before selecting a memory operation.

Current solution:

* Planner node
* Tool routing architecture
* LLM-driven query interpretation

---

#### Problem #11 - No Conversational Memory

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

The rover lacked conversation awareness.

Current solution:

* Short-term conversation memory
* Automatic storage of recent questions and answers
* Context injection during answer generation

---

#### Problem #12 - Memory Tools Were Isolated

Memory operations existed independently but were not exposed through a unified reasoning layer.

Example:

```text
Scene Search
Object Count
Nearby Object Analysis
```

All existed separately.

The rover lacked a centralized decision-making system capable of selecting the correct operation.

Current solution:

* Planner architecture
* Unified tool interface
* Agent-driven memory retrieval

---

#### Problem #13 - Single Tool Execution Limits Reasoning

Current planner architecture selects only one tool per query.

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
Aggregate results
Generate combined answer
```

Future solution:

* Multi-tool execution engine
* Action list architecture
* Tool result aggregation
* Multi-step reasoning chains

### Engineering Lessons Learned

* Memory retrieval and reasoning are separate system components.
* Tools provide capabilities; agents decide when to use them.
* Storing memory is easier than reasoning over memory.
* Planner-based architectures scale better than hardcoded pipelines.
* Conversation memory significantly improves user interaction quality.
* Agent systems should be designed around extensibility rather than fixed workflows.
* Single-tool agents eventually become a bottleneck for complex reasoning tasks.

### Notes

This version marks the transition from memory retrieval to agent-based reasoning.

EyesOfRover can now interpret natural language questions, determine the appropriate memory operation, retrieve information from memory systems, and generate contextual responses using a local language model.

The rover has evolved from a visual memory system into an interactive memory agent.

This milestone establishes the foundation for the next phase:

* Multi-tool execution
* Tool aggregation pipelines
* Context-aware planning
* Memory-aware reasoning
* Navigation memory
* Position tracking
* Rover autonomy


