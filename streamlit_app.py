#!/usr/bin/env python3
"""
Elephant Memory Cloud - Streamlit Dashboard
Real-time memory monitoring with minimal code.
"""

import streamlit as st
import gc
from datetime import datetime
from models import Elephant, Herd, Event, WaterSource
from models.event import EventType
from memory import MemoryMonitor, GarbageCollectionAnalyzer

# Page config
st.set_page_config(
    page_title="🐘 Elephant Memory Cloud",
    page_icon="🐘",
    layout="wide"
)

# Initialize session state
if 'monitor' not in st.session_state:
    st.session_state.monitor = MemoryMonitor()
    st.session_state.analyzer = GarbageCollectionAnalyzer()
    st.session_state.herd = None
    st.session_state.family_created = False

# Header
st.title("🐘 Elephant Memory Cloud")
st.markdown("**Real-time Memory Management & Circular Reference Demonstration**")
st.divider()

# Main dashboard
col1, col2, col3 = st.columns(3)

# Get current stats
gc.collect()
gc_count = gc.get_count()
memory_mb = st.session_state.monitor.get_process_memory_mb()
elephant_count = Elephant.get_instance_count()
herd_size = len(st.session_state.herd.members) if st.session_state.herd else 0

with col1:
    st.metric("Process Memory", f"{memory_mb:.2f} MB")
    st.metric("Elephant Count", elephant_count)

with col2:
    st.metric("Object Count", f"{len(gc.get_objects()):,}")
    st.metric("Herd Size", herd_size)

with col3:
    st.metric("GC Gen 0", gc_count[0])
    st.metric("GC Gen 1", gc_count[1])

st.divider()

# Controls
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("🐘 Create Ella's Family", use_container_width=True):
        # Start tracking
        if not st.session_state.monitor.tracking_enabled:
            st.session_state.monitor.start_tracking()
        
        snapshot_before = st.session_state.monitor.take_snapshot("Before creation")
        
        # Create herd and family
        st.session_state.herd = Herd("Savanna Wanderers", "Central Savanna")
        
        ella = Elephant("Ella", 1990, "F", use_weak_refs=False)
        emma = Elephant("Emma", 2005, "F", use_weak_refs=False)
        eric = Elephant("Eric", 2008, "M", use_weak_refs=False)
        elsa = Elephant("Elsa", 2012, "F", use_weak_refs=False)
        emily = Elephant("Emily", 2020, "F", use_weak_refs=False)
        
        # Create circular references
        ella.add_child(emma)
        ella.add_child(eric)
        ella.add_child(elsa)
        emma.add_child(emily)
        
        # Add to herd
        for elephant in [ella, emma, eric, elsa, emily]:
            st.session_state.herd.add_member(elephant)
        
        st.session_state.family_created = True
        st.session_state.ella = ella
        
        snapshot_after = st.session_state.monitor.take_snapshot("After creation")
        
        # Analyze
        has_cycles = st.session_state.analyzer.detect_cycles(ella)
        ref_analysis = st.session_state.analyzer.analyze_referrers(ella)
        
        st.success(f"✅ Created {Elephant.get_instance_count()} elephants!")
        st.info(f"⚠️ Circular references: {'Yes' if has_cycles else 'No'}")
        st.info(f"📌 Memory delta: +{snapshot_after['process_memory_mb'] - snapshot_before['process_memory_mb']:.2f} MB")
        st.rerun()

with col_btn2:
    cleanup_disabled = not st.session_state.family_created
    if st.button("🧹 Cleanup & GC", disabled=cleanup_disabled, use_container_width=True):
        snapshot_before = st.session_state.monitor.take_snapshot("Before cleanup")
        count_before = Elephant.get_instance_count()
        
        # Delete references
        st.session_state.herd = None
        st.session_state.ella = None
        st.session_state.family_created = False
        
        # Force GC
        collected = gc.collect()
        
        snapshot_after = st.session_state.monitor.take_snapshot("After cleanup")
        count_after = Elephant.get_instance_count()
        
        st.success("🧹 Cleanup complete!")
        st.info(f"Elephants: {count_before} → {count_after}")
        st.info(f"Objects collected: {collected}")
        st.info(f"Memory freed: {snapshot_before['process_memory_mb'] - snapshot_after['process_memory_mb']:.2f} MB")
        st.rerun()

with col_btn3:
    if st.button("🔄 Refresh Stats", use_container_width=True):
        st.rerun()

st.divider()

# Family Tree
st.subheader("👨‍👩‍👧‍👦 Family Tree")

if st.session_state.family_created and st.session_state.herd:
    # Check for circular references
    has_cycles = st.session_state.analyzer.detect_cycles(st.session_state.ella)
    
    if has_cycles:
        st.warning("⚠️ Circular References Detected")
    else:
        st.success("✅ No Cycles")
    
    # Display family tree
    st.markdown("### Matriarch: Ella 🐘")
    
    ella = st.session_state.ella
    
    # Show Ella's info
    col_a, col_b, col_c = st.columns([1, 2, 2])
    with col_a:
        st.markdown(f"**♀️ Ella**")
    with col_b:
        st.text(f"Born: {ella.birth_year}")
    with col_c:
        st.text(f"Children: {len(ella.children)}")
    
    # Show children
    for child in ella.children:
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;└─ **{'♂️' if child.gender == 'M' else '♀️'} {child.name}** (Born: {child.birth_year})")
        
        # Show grandchildren
        if child.children:
            for grandchild in child.children:
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ **{'♂️' if grandchild.gender == 'M' else '♀️'} {grandchild.name}** (Born: {grandchild.birth_year})")
    
    # Memory analysis
    with st.expander("📊 Detailed Memory Analysis"):
        ref_analysis = st.session_state.analyzer.analyze_referrers(ella)
        st.json({
            "Referrer Count": ref_analysis['referrer_count'],
            "Object Size (bytes)": ref_analysis['size_bytes'],
            "Total Elephants": Elephant.get_instance_count(),
            "Herd Members": len(st.session_state.herd.members)
        })

else:
    st.info("👆 Click 'Create Ella's Family' to visualize the elephant family tree with circular references")

# Footer
st.divider()
st.caption("🐘 Elephant Memory Cloud - Demonstrating Python's Cyclic Garbage Collection")
