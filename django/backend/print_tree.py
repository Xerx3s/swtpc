# plot tree
from numpy import loadtxt
from xgboost import to_graphviz
from floc_analyzer.scripts.modules.mlalgorithms import load_pipeline

# load pipe
pipe = load_pipeline("./floc_analyzer/data/pipelines/pipe_tur.dump")
tree = to_graphviz(pipe[3])

tree.render("tree.png", "png")