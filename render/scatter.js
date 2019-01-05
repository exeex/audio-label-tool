function plot_scatter(data, target) {

    let w = 2000;
    let h = 300;

//Create SVG element
    let svg = d3.select(target)
        .append("svg")
        .attr("width", w)
        .attr("height", h);

    svg.selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", function (d) {
            return d[0] / 10;
        })
        .attr("y", function (d) {
            return 30;
        })
        .attr("width", function (d) {
            return d[1] / 10;
        })
        .attr("height", function (d) {
            return 30;
        })
        .styles({
		fill: 'steelblue',
		stroke: 'green',
		'stroke-width': 10,
		opacity: .5
	});


    svg.selectAll("text")
        .data(data)
        .enter()
        .append("text")
        .text(function (d) {
            return d[2];
        })
        .attr("x", function (d) {
            return d[0] / 10;
        })
        .attr("y", function (d) {
            return 60;
        })
        .attr("font-size", "15px")
        .attr("fill", "black");

}
