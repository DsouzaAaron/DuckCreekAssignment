# News Article Entity Extraction

My solutions to the News Article Entity Extraction assignment. There are three parts, each in its own folder with a README covering the approach, assumptions and output.

| Part | Folder | What it does |
|---|---|---|
| A | [part_A](part_A/) | Cleans a small list of news articles and counts articles per topic per calendar week |
| B1 | [part_b1](part_b1/) | Scores an LLM's extraction of people, organizations and locations against a reference |
| B2 | [part_b2](part_b2/) | Models articles, people, organizations and locations as a graph, and queries it |

## Setup

You need Python 3 and two libraries:

```bash
pip install pandas networkx
```

Part A uses pandas and Part B2 uses networkx. Part B1 only needs the standard library.

## Running

Run every script from the repository root:

```bash
python part_A/main.py
python part_b1/run_eval.py
python part_b2/graph.py
```

## Layout

```
part_A/
  input.json     the raw articles from the assignment
  parse.py       cleaning and weekly counts
  main.py        loads the input and prints the counts
part_b1/
  eval.py        precision, recall and F1 by entity type
  run_eval.py    scores the example from the assignment
part_b2/
  graph.py       the graph, the query and sample data
```
