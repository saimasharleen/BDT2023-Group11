let svg = d3.select("svg");
var container = svg.append("g"),
    width = +svg.attr("width"),
    height = +svg.attr("height");
svg.call(
    d3.zoom()
        .scaleExtent([.1, 4])
        .on("zoom", function() { container.attr("transform", d3.event.transform); })
);

let file_name = "email-Eu-core.json";
let strength = -500;
let distance = 500;
let link_str = 0.005;
if (low) {
  file_name = "email-Eu-core-low.json";
  strength = -20;
  distance = 100;
  link_str = 2;
}
if (high) {
  file_name = "email-Eu-core-high.json";
  strength = -25;
  distance = 150;
  link_str = 2;
}
if (node_card) {
  if (low) {
    file_name = "email-Eu-core-low-node.json";
    strength = -25;
    distance = 100;
    link_str = 2;
  }
  if (high) {
    file_name = "email-Eu-core-high-node.json";
    strength = -1000;
    distance = 150;
    link_str = 0.01;
  }
}

let simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id((d, i) => d.id))
    .force("charge", d3.forceManyBody().strength(strength))
    .force("center", d3.forceCenter(width / 2, height / 2));

let aray = Array(42).fill(0)
let label_index = 0
aray.map(function(x) {
  return toString(label_index++);
});

var color = d3.scaleSequential(d3.interpolateSinebow).domain([0, 42]);

d3.json(file_name).then(function(graph) {
  var node = container.append("g")
                .attr("class", "nodes")
                .selectAll("g")
                .data(graph.nodes)
                .enter().append("g")

  var circles = node.append("circle")
                    .attr("r", 10)
                    .attr("fill", function(d) { return color(parseInt(d.label)); })
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended));

  var link = container.append("g")
                .attr("class", "links")
                .selectAll("line")
                .data(graph.links)
                .enter().append("line")
                .attr("stroke-width", 2);


  simulation.nodes(graph.nodes)
            .on("tick", ticked);

  simulation.force("link")
            .links(graph.links)
            .distance(distance).strength(link_str);

  function ticked() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
        });
  }
});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
