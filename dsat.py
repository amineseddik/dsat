import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

# Palette de couleurs
color_palette = sns.color_palette("tab20", 20).as_hex()

def dsatur(graph):
    """
    Algorithme DSATUR pour la coloration de graphe.
    """
    colors = {}  # Dictionnaire pour stocker les couleurs attribuées à chaque sommet
    dsat = {}    # DSAT (degré de saturation) pour chaque sommet
    degree = {node: len(neighbors) for node, neighbors in graph.items()}  # Degré de chaque sommet
    uncolored = set(graph.keys())  # Ensemble des sommets non colorés
    
    # Initialiser DSAT pour chaque sommet
    for node in graph:
        dsat[node] = degree[node]
    
    # Colorer le sommet avec le degré maximum
    first_vertex = max(graph.keys(), key=lambda x: degree[x])
    colors[first_vertex] = 1
    uncolored.remove(first_vertex)
    
    # Mettre à jour les valeurs DSAT après avoir colorié le premier sommet
    for neighbor in graph[first_vertex]:
        if neighbor in uncolored:
            dsat[neighbor] = len({colors[n] for n in graph[neighbor] if n in colors})
    
    # Coloration des sommets restants
    while uncolored:
        # Sélectionner le sommet avec le DSAT maximum, puis avec le degré maximum en cas d'égalité
        next_vertex = max(uncolored, key=lambda x: (dsat[x], degree[x]))
        
        # Trouver la plus petite couleur disponible
        used_colors = {colors[neighbor] for neighbor in graph[next_vertex] if neighbor in colors}
        color = 1
        while color in used_colors:
            color += 1
        
        # Attribuer une couleur au sommet
        colors[next_vertex] = color
        uncolored.remove(next_vertex)
        
        # Mettre à jour les valeurs DSAT pour les voisins non colorés
        for neighbor in graph[next_vertex]:
            if neighbor in uncolored:
                colored_neighbors = {colors[n] for n in graph[neighbor] if n in colors}
                if colored_neighbors:
                    dsat[neighbor] = len(colored_neighbors)
                else:
                    dsat[neighbor] = degree[neighbor]
    
    return colors

def visualize_graph(graph, colors):
    """
    Visualiser le graphe avec ses couleurs
    """
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    pos = nx.spring_layout(G, seed=42)
    node_colors = [color_palette[(colors[node]-1) % len(color_palette)] for node in G.nodes()]
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", font_color="black")
    plt.title("Coloration du Graphe (DSATUR)", fontsize=16, fontweight="bold")
    plt.axis('off')
    return plt

def main():
    st.set_page_config(page_title="Coloration de Graphe - DSATUR", page_icon=":art:", layout="wide")
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f5f5dc;
            font-family: "Verdana", sans-serif;
        }
        .main-title {
            text-align: center;
            font-size: 36px;
            color: #1f618d;
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 24px;
            color: #117864;
            margin-top: 20px;
        }
        .color-text {
            font-size: 18px;
            color: #000080; /* Bleu foncé */
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Titre principal
    st.markdown('<div class="main-title">Algorithme DSATUR pour la Coloration de Graphe</div>', unsafe_allow_html=True)
    
    # Saisie du nombre de sommets
    st.markdown('<div class="section-title">1. Configuration de votre graphe</div>', unsafe_allow_html=True)
    num_vertices = st.number_input("Nombre de sommets", min_value=1, max_value=20, value=4, step=1)
    graph = {i+1: [] for i in range(num_vertices)}
    
    # Définir les voisins
    st.markdown('<div class="section-title">2. Définir les voisins de chaque sommet</div>', unsafe_allow_html=True)
    for i in range(num_vertices):
        vertex = i + 1
        neighbors_options = [j+1 for j in range(num_vertices) if j+1 != vertex]
        selected_neighbors = st.multiselect(
            f"Sélectionnez les voisins du sommet {vertex}", 
            neighbors_options, 
            key=f"neighbors_{vertex}"
        )
        graph[vertex] = selected_neighbors
    
    # Exécution et affichage
    st.markdown('<div class="section-title">3. Résultats</div>', unsafe_allow_html=True)
    if st.button("Colorer le Graphe"):
        if any(graph.values()):
            result = dsatur(graph)
            st.subheader("Coloration obtenue :")
            result_text = "".join(
                [f"<p class='color-text'>Sommet {vertex:02d} → Couleur {color}</p>" for vertex, color in sorted(result.items())]
            )
            st.markdown(result_text, unsafe_allow_html=True)
            
            st.subheader("Visualisation du graphe :")
            plt = visualize_graph(graph, result)
            st.pyplot(plt)
            plt.close()
        else:
            st.warning("Veuillez définir les connexions du graphe.")

if __name__ == '__main__':
    main()