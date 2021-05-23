def getHTML(dataJson, edgeMaxColor, vertexMaxColor, force, pageSize = 8000, showName = True):
	file = f'''
<!DOCTYPE html>
<meta charset="utf-8">
<style>

.links line {{
  stroke-opacity: 0.6;
}}

.nodes circle {{
  stroke: #fff;
  stroke-width: 1.5px;
}}

text {{
  font-family: sans-serif;
  font-size: 12px;
}}

</style>
<svg width="{pageSize}" height="{pageSize}"></svg>
<script src="https://d3js.org/d3.v4.min.js"></script>
<script>

// data
var graphJson = `{dataJson}`

// drawing board
var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

// color map from gray to red
var color = function(idx, size) {{return `hsl(${{270 - idx * 270 / size}}, ${{idx * 100 / size}}%, 50%`}};

// force layout setting
var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) {{ return d.id; }}))
    .force("charge", d3.forceManyBody().strength({force}))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(function(d) {{ return 5 + Math.sqrt(d.peel);}}));


// read data
var graph = JSON.parse(graphJson)

// draw edges
var link = svg.append("g")
    .attr("class", "links")
  .selectAll("line")
  .data(graph.links)
  .enter().append("line")
    .attr("stroke-width", function(d) {{ return Math.sqrt(d.size); }})
    .attr("stroke", function(d) {{return color(d.colorGroup, {edgeMaxColor})}});

// draw vertices
var node = svg.append("g")
    .attr("class", "nodes")
  .selectAll("g")
  .data(graph.nodes)
  .enter().append("g")

var circles = node.append("circle")
    .attr("r", function(d) {{ return 5 + Math.sqrt(d.size); }})
    .attr("fill", function(d) {{ return color(d.colorGroup, {vertexMaxColor}) }})
    .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

// draw labels
var lables = node.append("text")
    .text(function(d) {{
      return `${{d.name}}`;
    }})
    .attr('x', 6)
    .attr('y', 3);

// vertex hovering tooltip
node.append("title")
    .text(function(d) {{ return `${{d.name}} @${{d.id}}\npeel value: ${{d.peel}}`; }});

// force layout
simulation
    .nodes(graph.nodes)
    .on("tick", ticked);

simulation.force("link")
    .links(graph.links);

function ticked() {{
  link
      .attr("x1", function(d) {{ return d.source.x; }})
      .attr("y1", function(d) {{ return d.source.y; }})
      .attr("x2", function(d) {{ return d.target.x; }})
      .attr("y2", function(d) {{ return d.target.y; }});

  node
      .attr("transform", function(d) {{
        return "translate(" + d.x + "," + d.y + ")";
      }})
}};


// on draging vertices
function dragstarted(d) {{
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}}

function dragged(d) {{
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}}

function dragended(d) {{
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}}

</script>
'''
	return file