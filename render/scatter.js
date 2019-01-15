function make_editable(d, field) {

    console.log(d);
    // console.log("make_editable", arguments);


    this.on("mouseover", function () {
        d3.select(this).style("fill", "red");
    })
        .on("mouseout", function () {
            d3.select(this).style("fill", null);
        })
        .on("click", function (d) {
            let p = this.parentNode;
            console.log(this, arguments);

            // inject a HTML form to edit the content here...

            // bug in the getBBox logic here, but don't know what I've done wrong here;
            // anyhow, the coordinates are completely off & wrong. :-((
            let xy = this.getBBox();
            let p_xy = p.getBBox();

            xy.x -= p_xy.x;
            xy.y -= p_xy.y;

            let el = d3.select(this);
            let p_el = d3.select(p);

            let frm = p_el.append("foreignObject");

            let inp = frm
                .attr("x", xy.x)
                .attr("y", xy.y)
                .attr("width", 300)
                .attr("height", 25)
                .append("xhtml:form")
                .append("input")
                .attr("value", function () {
                    // nasty spot to place this call, but here we are sure that the <input> tag is available
                    // and is handily pointed at by 'this':
                    this.focus();

                    return d[field];
                })
                .attr("style", "width: 294px;")
                // make the form go away when you jump out (form looses focus) or hit ENTER:
                .on("blur", function () {
                    console.log("blur", this, arguments);

                    let txt = inp.node().value;

                    d[field] = txt;
                    el
                        .text(function (d) {
                            return d[field];
                        });

                    // Note to self: frm.remove() will remove the entire <g> group! Remember the D3 selection logic!
                    p_el.select("foreignObject").remove();
                })
                .on("keypress", function () {
                    console.log("keypress", this, arguments);

                    // IE fix
                    if (!d3.event)
                        d3.event = window.event;

                    let e = d3.event;
                    if (e.keyCode == 13) {
                        if (typeof(e.cancelBubble) !== 'undefined') // IE
                            e.cancelBubble = true;
                        if (e.stopPropagation)
                            e.stopPropagation();
                        e.preventDefault();

                        let txt = inp.node().value;

                        d[field] = txt;
                        el
                            .text(function (d) {
                                return d[field];
                            });

                        // odd. Should work in Safari, but the debugger crashes on this instead.
                        // Anyway, it SHOULD be here and it doesn't hurt otherwise.
                        p_el.select("foreignObject").remove();
                    }
                });
        });
}

function plot_scatter(data, target, total_duration) {

    let w = total_duration / 10;
    let h = 300;

//Create SVG element
    let svg = d3.select(target)
        .append("svg")
        .attr("width", w)
        .attr("height", h)
        .style("background-color", "#444444");

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
            fill: '#00aa88',
            stroke: 'white',
            'stroke-width': 1,
            opacity: 1
        });


    svg.selectAll("text")
        .data(data)
        .enter()
        .append("text")
        .text(function (d) {
            return d[2];
        })
        .attr("x", function (d) {
            return d[0] / 10 + 3;
        })
        .attr("y", function (d) {
            return 50;
        })
        .attr("font-size", "15px")
        .attr("fill", "white")

        .append("circle")
        .attr("r", 10)
        .attr("fill", "black")
        .on("mouseover", function () {
            d3.select(this).style("fill", "red");
        });

    // svg.selectAll("text")
    //
    //     .call(make_editable, 2);

}

