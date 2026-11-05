import networkx as nx

SSCHEMA={
    "worksAt": ({"Person"},{"Organization"}),
    "locatedIn": ({"Organization"},{"Location"}),
    "mentions": ({"Article"},{"Person","Organization"})
}

class NewGraph:
    def __init__(self):
        self.g = nx.MultiDiGraph()

    def add_entity(self, kind, name, **attrs):
        node_id = f"{kind}:{name}"
        self.g.add_node(node_id, kind=kind, name=name, **attrs)
        return node_id
        ...

    def add_relation(self, src, rel, dst):
        #check if rel is allowed in Schema
        if rel not in SSCHEMA:
            raise ValueError(f"Unknown Relation: {rel}")
        src_kinds, dest_kinds = SSCHEMA[rel]
        if self.g.nodes[src]["kind"] not in src_kinds or self.g.nodes[dst]["kind"] not in dest_kinds:
            raise ValueError(f"Invalid Edge {src} -{rel}-> {dst}")
        self.g.add_edge(src, dst, rel=rel)
        ...

    def sources(self, node, rel):
        result = set()
        for from_node, to_node, edge_rel in self.g.in_edges(node, data="rel"):
            if edge_rel == rel:
                result.add(from_node)
        return result
        ...

    def targets(self, node, rel):
        result = set()
        for from_node, to_node, edge_rel in self.g.out_edges(node, data="rel"):
            if edge_rel == rel:
                result.add(to_node)
        return result

    def orgs_mentioned_with(self, person_name):
        person = f"Person:{person_name}"
        if person not in self.g:
            return set()
        articles = self.sources(person,rel="mentions")
        orgs = set()
        for article in articles:
            for node in self.targets(article, rel="mentions"):
                if self.g.nodes[node]['kind'] == "Organization":
                    orgs.add(self.g.nodes[node]['name'])
        return orgs


def build_graph():
    ng = NewGraph()
    maria = ng.add_entity("Person","Maria Gomez")
    john = ng.add_entity("Person","John Lee")

    northwind = ng.add_entity("Organization", "Northwind Logistics")
    acme = ng.add_entity("Organization", "Acme")
    contoso = ng.add_entity("Organization", "Contoso")

    denver = ng.add_entity("Location", "Denver")
    seattle = ng.add_entity("Location", "Seattle")

    a1 = ng.add_entity("Article", "A1", title="Maria Gomez, CEO of Northwind Logistics, announces Denver partnership")
    a2 = ng.add_entity("Article", "A2", title="Maria Gomez signs Northwind deal with Acme Freight")
    a3 = ng.add_entity("Article", "A3", title="Contoso names John Lee as CFO")

    ng.add_relation(maria, "worksAt", northwind)
    ng.add_relation(john, "worksAt", contoso)
    ng.add_relation(northwind, "locatedIn", denver)
    ng.add_relation(contoso, "locatedIn", seattle)

    ng.add_relation(a1, "mentions", maria)
    ng.add_relation(a1, "mentions", northwind)
    ng.add_relation(a2, "mentions", maria)
    ng.add_relation(a2, "mentions", northwind)
    ng.add_relation(a2, "mentions", acme)
    ng.add_relation(a3, "mentions", john)
    ng.add_relation(a3, "mentions", contoso)

    return ng

def main():
    ng = build_graph()
    print(f"Graph: {ng.g.number_of_nodes()} nodes, {ng.g.number_of_edges()} edges\n")
    for person in ["Maria Gomez", "John Lee", "Unknown Person"]:
        orgs = ng.orgs_mentioned_with(person)
        if orgs:
             print(f"{person}: {sorted(orgs)}")
        else:
            print(f"{person}: no organizations found")

if __name__=="__main__":
    main()