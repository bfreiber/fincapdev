function showPool(tgt, data) {

console.log("Starting d3 stuff...");


var diameter = 500;
var NODE_RAD = 30;
var PIC_SIZE = NODE_RAD * Math.sqrt(2); // half of the diagonal = radius of circle

var tree = d3.layout.tree()
    .size([360, diameter / 2 - 120])
    .separation(function(a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });

var diagonal = d3.svg.diagonal.radial()
    .projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });

var svg = d3.select(tgt).append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
  .append("g")
    .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

d3.json(data, function(error, root) {
  var nodes = tree.nodes(root),
      links = tree.links(nodes);

  var link = svg.selectAll(".link")
      .data(links)
    .enter().append("path")
      .attr("class", "link")
      .attr("d", diagonal);

  var node = svg.selectAll(".node")
      .data(nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

  var node_circle = node.append("g")
  
  node_circle.append("circle")
      .attr("r", NODE_RAD); // set node radius here
  node_circle.append("image")
          .attr("xlink:href", function(d) { return d.pic; }) // get pic attribute from json
          .attr('width', PIC_SIZE)
          .attr('height', PIC_SIZE)
          .attr('x', -PIC_SIZE / 2)
          .attr('y', -PIC_SIZE / 2)
          .attr("transform", function(d) {
             return "rotate(" + (-d.x + 90) + ")";});

  node.append("text")
      .attr("dy", ".31em")
      .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
      .attr("transform", function(d) { return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)"; })
      .text(function(d) { return d.name; });
});

d3.select(self.frameElement).style("height", diameter + "px");
}
