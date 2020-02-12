let width,
    height,
    svg,
    simulation,
    color,
    zoomHandler,
    graphGlobal,
    link,
    node,
    g,
    nodeContainer;


let t = d3.transition()
    .duration(1500)
    .ease(d3.easeSin);

function drawGraph(graph) {

    // if no width, initialize
    if (width === undefined) {
        initializeGraph();
    }
    // if graph different from global, update
    if (graphGlobal === undefined) {
        graphGlobal = graph;
        updateGraph();
    }
    else if ((Object.keys(graph.links).length !== Object.keys(graphGlobal.links).length) || (Object.keys(graph.nodes).length !== Object.keys(graphGlobal.nodes).length)) {
        graphGlobal = graph;
        updateGraph();
    }

}

function initializeGraph() {

    // get the height and width of the window
    width = window.innerWidth;
    height = window.innerHeight;

    svg = d3.select("#author-rank").append("svg")
        .attr("id", "author-rank-svg")
        .attr("width", width)
        .attr("height", height)
        .style("display", "block")
        .style("margin", "auto");

    g = svg.append("g")
        .attr("class", "everything");

    simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-600))
        .force("x", d3.forceX().x(width / 2))
        .force("y", d3.forceY().y(height / 2))
        .alphaDecay(0.05);

    zoomHandler = d3.zoom()
        .scaleExtent([.1, 4])
        .on("zoom", zoom_actions);

    zoomHandler(svg);

    link = g.append("g")
        .attr("class", "links")
        .selectAll("line");

    node = g.append("g")
        .attr("class", "nodes")
        .selectAll("circle");
}

function updateGraph() {

    g.selectAll('.links').remove();
    g.selectAll('.nodes').remove();
    g.select('#annotation-parent').remove(); // remove previous annotations

    link = g.selectAll('.links').data(graphGlobal.links);
    link.exit().transition(t).style("opacity", 0).remove();
    link = link.enter().append("line")
        .attr('class', 'links')
        .attr('stroke-width', function(d) {
            return Math.max(Math.sqrt(d.weight) - 2., 0.5);
        })
        .attr('stroke', "lightgray")
        .style("opacity", 0.2)
        .merge(link);
    link.transition(t);

    node = g.selectAll('.nodes').data(graphGlobal.nodes);
    node.exit().transition(t).attr("r", 1e-6).remove();
    nodeContainer = node.enter().append("g");

    node = nodeContainer.append("circle")
        .attr('class', 'nodes')
        .attr("r", function (d) {

            // the maximum score is a 1
            let maxArea = 15 + (100 * d.score); // which is equal to pi * r^2
            let r2 = maxArea / Math.PI;
            let r = Math.sqrt(r2);

            return r
        })
        .attr("fill", "gray")
        .on("mouseover", function (d) {

            // on hover highlight node
            node.attr("fill", function (o) {
                if (d.id === o.id) {
                    return "#D5FF00"
                } else {
                    return "gray"
                }
            });

            // raise the circle to the top so the annotation isn't displayed over it
            d3.select(this.parentElement).raise();

            // display this information in the info box
            d3.select("#score")
                .text(function() {
                    return "AuthorRank score: " + d.score.toFixed(2)
                });

            // *********************************
            // HIGHLIGHT CONNECTED LINKS (thanks Chris Laporte)

            let nodesObj = {};
            nodesObj[d.id] = true;
            // iterate through links and get connected nodes
            let connectedNodes = graphGlobal.links.reduce((acc, cur) => {
                if( cur.source.id === d.id ) {
                    acc[cur.target.id] = true; // our node is source, add the target
                } else if( cur.target.id === d.id ) {
                    acc[cur.source.id] = true; // our node is target, add the source
                }
                return acc;
            }, nodesObj);

            // unhighlight non-connected nodes
            g.selectAll('.links').filter((d2) => {
                // return true if a link exists between d and d2
                return !connectedNodes[d2.source.id];
            }).style('opacity', 0.2);

            g.selectAll('.links').filter((d2) => {
                // return true if a link exists between d and d2
                return connectedNodes[d2.source.id];
            }).style('opacity', 0.5);

            // END OF HIGHLIGHT CONNECTED LINKS
            // *********************************

        })
        .on("mouseout", function () {
            node.attr('opacity', 1);
            node.attr('fill', "gray");
            link.style("opacity", 0.2);
            d3.select("#score").text("")
        })
        .merge(node);

    nodeContainer.filter((d) => { return d.rank <= 3} ).append("text")
        .attr("font-size", function(d) {
            return String(0.25 + d.score) + "rem"
        })
        .attr("text-anchor", "end")
        .attr("fill",  "#2E8FFF")
        .attr("font-weight",  "bold")
        .text(function(d) {
            return d.rank;
        });

    nodeContainer.call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

    node.transition(t);

    simulation
        .nodes(graphGlobal.nodes)
        .on("tick", function() {
            link
                .attr("x1", function (d) {
                    return d.source.x;
                })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });

            nodeContainer
                .style("transform", function(d) {
                    return "translate(" + String(d.x) + "px, " + String(d.y) + "px)"
                });

            // draw the annotations
            makeAnnotations.annotations().forEach((d, i) => {
                d.position = graphGlobal.nodes[i]
            });

        });

    simulation.force("link")
        .links(graphGlobal.links);

    simulation.alpha(1.).restart();

    // annotation generator
    let makeAnnotations = d3.annotation()
        .type(d3.annotationCalloutElbow)
        .annotations(graphGlobal.nodes.map((d) => {
            return {
            data: {x: d.x, y: d.y},
            note: { label: d.id,
              align: "top",
              orientation: "fixed" },
            connector: { type: "elbow" },
            dy: -10,
            dx: 10
          }
        }))
        .accessors({ x: d => d.x , y: d => d.y});

    // append the annotations
    g.append("g")
        .attr("id", "annotation-parent")
        .call(makeAnnotations);

}


//Zoom functions
function zoom_actions() {
    g.attr("transform", d3.event.transform)
}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(.05).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    // we do not reset the position as we wish for the user to
    // be able to pull apart individual nodes in the network
    // d.fx = null;
    // d.fy = null;
}


// initialize
function addScoresToGraph(graph, scores) {
    let nodes = graph.nodes;
    nodes.forEach(function(d, i) {
        d.score = scores[d.id];
    });

    // sort nodes by score
    nodes.sort(function(a, b) {
        return b.score - a.score;
    });

    // add rank as an annotation
    nodes.forEach(function(d, i) {
       d.rank = i + 1;
    });

    return graph
}

Promise.all([
    d3.json("data/author_graph.json"),
    d3.json("data/author_scores.json"),
]).then(function (files) {

    // load the top authors
    let graph = files[0];
    let scores = files[1];

    // reduce each UID list to a concatenated string in both nodes and links
    graph.nodes.forEach(function(d) {
        d.id = d.id.join(" ");
    });
    graph.links.forEach(function(d) {
        d.source = d.source.join(" ");
        d.target = d.target.join(" ");
    });

    // add scores to the graph
    graph = addScoresToGraph(graph, scores);

    // initialize
    initializeGraph(graph);

    // draw
    drawGraph(graph);

});
