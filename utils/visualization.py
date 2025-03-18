"""
Visualization utilities for generating charts, graphs and mind maps.
"""

import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
import numpy as np
from PIL import Image
import base64
import io
from datetime import datetime

def create_mind_map(mind_map_data):
    """Create a text-based mind map representation instead of visual blocks."""
    try:
        # Parse the mind map data
        data = json.loads(mind_map_data)
        center = data["center"]
        main_branches = data["main_branches"]
        
        # Create a text-based representation
        mind_map_text = f"# {center}\n\n"
        
        # Process main branches
        for i, branch in enumerate(main_branches):
            branch_name = branch["name"]
            sub_branches = branch["sub_branches"]
            
            # Add main branch
            mind_map_text += f"## {branch_name}\n"
            
            # Add sub-branches
            for sub_branch in sub_branches:
                mind_map_text += f"* {sub_branch}\n"
            
            mind_map_text += "\n"
        
        return mind_map_text
    except Exception as e:
        import traceback
        error_msg = f"Error creating mind map: {e}\n{traceback.format_exc()}"
        return f"```\n{error_msg}\n```"

def display_mind_map(mind_map_data):
    """Utility function to display a text-based mind map in Streamlit."""
    mind_map_text = create_mind_map(mind_map_data)
    if mind_map_text:
        st.markdown(mind_map_text)
        return True
    return None

def create_skills_graph(skills_data):
    """Create a force-directed graph for skills visualization."""
    try:
        # Parse the skills data
        data = json.loads(skills_data)
        
        # Create a graph object
        G = nx.Graph()
        
        # Add nodes
        for node in data.get("nodes", []):
            # Make sure node has an id
            if "id" not in node:
                continue
                
            # Add node with default group=1 if not specified
            G.add_node(node["id"], group=node.get("group", 1))
        
        # Add edges
        for link in data.get("links", []):
            # Skip if source or target is missing
            if ("source" not in link) or ("target" not in link) or (link["source"] not in G.nodes) or (link["target"] not in G.nodes):
                continue
                
            G.add_edge(link["source"], link["target"], weight=link.get("value", 1))
        
        # Skip visualization if the graph is empty
        if len(G.nodes) == 0:
            raise ValueError("No valid nodes found in the skills data")
            
        # Create a figure
        plt.figure(figsize=(10, 8), facecolor='#f5f5f5')
        
        # Define node colors based on group
        node_colors = []
        for node in G.nodes:
            # Ensure the group attribute exists with default value 1
            if "group" not in G.nodes[node]:
                G.nodes[node]["group"] = 1
            node_colors.append(plt.cm.Set3(G.nodes[node]["group"] % 10 / 10))
        
        # Define layout
        pos = nx.spring_layout(G, k=0.3, iterations=50, seed=42)
        
        # Draw the network
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, alpha=0.8)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
        
        # Draw edges with varying width based on weight
        for (u, v, d) in G.edges(data=True):
            width = d.get('weight', 1) * 1.5
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=width, alpha=0.6)
        
        plt.axis('off')
        plt.tight_layout()
        
        return plt
    except Exception as e:
        print(f"Error creating skills graph: {e}")
        
        # Create a simple error visualization
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, f"Error creating skills graph:\n{e}", ha='center', va='center',
                 fontsize=12, color='red')
        plt.axis('off')
        return plt

def create_interactive_skills_graph(skills_data):
    """Create an interactive skills graph using Plotly."""
    try:
        # Parse the skills data
        data = json.loads(skills_data)
        
        # Extract nodes and links
        nodes = data.get("nodes", [])
        links = data.get("links", [])
        
        # Create node and link data for Plotly
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        
        # Create a temporary networkx graph for layout calculation
        G = nx.Graph()
        
        # Add nodes and edges to the graph
        for node in nodes:
            G.add_node(node["id"], group=node.get("group", 1))
        
        for link in links:
            G.add_edge(link["source"], link["target"], weight=link.get("value", 1))
        
        # Get node positions using a force-directed layout
        pos = nx.spring_layout(G, seed=42)
        
        # Extract positions for Plotly
        for node in nodes:
            node_id = node["id"]
            node_x.append(pos[node_id][0])
            node_y.append(pos[node_id][1])
            node_text.append(node_id)
            node_color.append(node.get("group", 1))
        
        # Create edges for Plotly
        edge_x = []
        edge_y = []
        edge_width = []
        
        for link in links:
            source = link["source"]
            target = link["target"]
            x0, y0 = pos[source]
            x1, y1 = pos[target]
            
            # Add each edge as a line
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_width.append(link.get("value", 1) * 2)
        
        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')
        
        # Create node trace
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                color=node_color,
                size=15,
                line=dict(width=2, color='#FFFFFF')
            )
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title='Skills Network Graph',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        plot_bgcolor='#f8f9fa',
                        paper_bgcolor='#f8f9fa',
                        annotations=[
                            dict(
                                text="Skills required for this project",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002
                            )
                        ]
                    )
                )
        
        return fig
    except Exception as e:
        print(f"Error creating interactive skills graph: {e}")
        
        # Create error figure
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error creating interactive skills graph: {e}",
            showarrow=False,
            font=dict(color="red", size=14)
        )
        fig.update_layout(height=500)
        return fig

def create_project_timeline(timeline_data):
    """Create a Gantt chart for the project timeline."""
    try:
        # Parse timeline data
        data = json.loads(timeline_data)
        
        # Extract the data
        phases = data.get("phases", [])
        start_dates = data.get("start_dates", [])
        end_dates = data.get("end_dates", [])
        descriptions = data.get("descriptions", [""] * len(phases))
        
        # Create DataFrame for Gantt chart
        df = []
        for i in range(len(phases)):
            if i < len(start_dates) and i < len(end_dates):
                df.append(dict(
                    Task=phases[i],
                    Start=start_dates[i],
                    Finish=end_dates[i],
                    Description=descriptions[i] if i < len(descriptions) else ""
                ))
        
        # Colors for phases
        colors = {
            phase: f'rgb({50+i*40}, {100+i*20}, {200-i*20})' 
            for i, phase in enumerate(phases)
        }
        
        # Create Gantt chart
        fig = ff.create_gantt(
            df, 
            colors=colors, 
            index_col='Task', 
            show_colorbar=True,
            group_tasks=True,
            showgrid_x=True,
            showgrid_y=True,
            title='Project Timeline'
        )
        
        # Update layout
        fig.update_layout(
            autosize=True,
            height=400,
            margin=dict(l=50, r=50, b=100, t=50, pad=4)
        )
        
        return fig
    except Exception as e:
        print(f"Error creating timeline: {e}")
        import plotly.graph_objects as go
        
        # Create error figure
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error creating timeline: {e}",
            showarrow=False,
            font=dict(color="red", size=14)
        )
        fig.update_layout(height=300)
        return fig
