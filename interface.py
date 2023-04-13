from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, last_node):
        
        graph_name = 'trip_graph'

        with self._driver.session() as session:
            # Delete graph if it exists already
            session.run(f"""
                CALL gds.graph.drop('{graph_name}', false)
            """)

            # Create graph
            session.run(f"""
                CALL gds.graph.project(
                    '{graph_name}',
                    'Location',
                    'TRIP'
                );
            """)

            # Run BFS
            result = session.run(f'''
                MATCH (source: Location {{name: {start_node}}}), (target: Location {{name: {last_node}}})
                CALL gds.bfs.stream('{graph_name}', {{
                    sourceNode: source,
                    targetNodes: target }})
                YIELD path
                RETURN path
            ''').data()
        
        return result

    def pagerank(self, max_iterations, weight_property):

        graph_name = 'trip_graph'

        with self._driver.session() as session:
            # Delete graph if it exists already
            session.run(f"""
                CALL gds.graph.drop('{graph_name}', false)
            """)

            # Create graph
            session.run(f"""
                CALL gds.graph.project(
                    '{graph_name}',
                    'Location',
                    'TRIP',
                    {{
                        relationshipProperties: '{weight_property}'
                    }}
                );
            """)

            # Run PageRank
            result = session.run(f'''
                CALL gds.pageRank.stream('{graph_name}', {{
                    maxIterations: {max_iterations},
                    relationshipWeightProperty: '{weight_property}'
                }})
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name as name, score
                ORDER BY score DESC, name ASC
            ''').data()

            max_node = result[0]
            min_node = result[-1]

            return max_node, min_node

