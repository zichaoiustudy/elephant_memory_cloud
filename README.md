# Elephant Memory Cloud 🐘

A **Streamlit-based** memory management visualization system demonstrating Python's garbage collection with circular references.

## Features

- **Real-time Memory Monitoring**: Live dashboard showing memory usage, object counts, and GC statistics
- **Interactive Family Tree**: Visual representation of elephant relationships with circular references
- **Garbage Collection Demo**: See Python's cyclic GC in action as it cleans up circular references
- **Minimal Code**: Built with Streamlit for simplicity and elegance

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run the Dashboard

```bash
streamlit run streamlit_app.py
```

The dashboard will automatically open in your browser at **http://localhost:8501**

## How It Works

This project demonstrates **circular references** in Python:
- Ella Elephant has children (Emma, Eric, Elsa)
- Each child has a reference back to their parent
- Emma has a child (Emily) who references back to Emma
- These circular references would cause memory leaks in languages without garbage collection

Python's **cyclic garbage collector** successfully identifies and cleans up these circular references when objects are no longer reachable.

## Streamlit Dashboard Features

### Real-time Metrics
- **Memory Statistics**: Process memory, elephant count, object count in live cards
- **GC Counters**: Monitor garbage collection generations (0, 1, 2)
- **Auto-refresh**: Click refresh or interact with buttons to update

### Interactive Controls
- **Create Ella's Family**: Generate family with circular references
- **Cleanup & GC**: Delete references and run garbage collection
- **Refresh Stats**: Update all metrics

### Family Tree Visualization
- Text-based hierarchy showing parent-child relationships
- Gender indicators (♂️/♀️)
- Circular reference detection badges
- Expandable detailed memory analysis

## Project Structure

```
elephant_memory_cloud/
├── streamlit_app.py    # Streamlit dashboard
├── models/             # Core data models
│   ├── elephant.py     # Elephant with circular refs
│   ├── herd.py         # Herd management
│   ├── event.py        # Historical events
│   └── water_source.py # Water source tracking
└── memory/             # Memory monitoring utilities
    ├── monitor.py      # MemoryMonitor class
    └── gc_analyzer.py  # gc_analyzer class
```

## Scientific Focus

This project explores:
- **Reference Counting** vs **Cyclic Garbage Collection**
- **Memory Leaks** in circular object relationships
- **Weak References** as alternative solutions
- **Performance Monitoring** of complex object graphs

