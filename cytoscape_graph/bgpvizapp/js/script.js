function choose(choices) {
    var index = Math.floor(Math.random() * choices.length);
    return choices[index];
}
var cy = cytoscape({
    container: document.getElementById("cy"),
    elements: [{ data: { id: "a", color: "#87BBEC" } }],
    style: [
        {
        selector: "node",
        style: {
            // shape: "circle",
            "background-color": "data(color)",
            label: "data(id)",
        },
        },
    ],
});

for (var i = 0; i < 10; i++) {
    cy.add({
        data: {
        id: "node" + i,
        color: choose(["#808080", "#FF0000", "#008000", "#FF69B4"]),
        },
    });
    var source = "node" + i;
    cy.add({
        data: {
        id: "edge" + i,
        source: source,
        target: "a",
        },
    });
    }
    cy.nodes().forEach((a) => {
    let data = "AS " + a._private.data.color.substring(1);
    console.log(data);
    let popper = a.popper({
        content: () => {
        let div = document.createElement('div');
        div.innerHTML = data;
        document.body.appendChild(div);
        return div;
        }
    });
    let update = () => {
        popper.update();
    }
    a.on('position', update);
    cy.on('pan zoom resize', update);
});
    
var layout = cy.elements().layout({ name: "cose", animate: true });
layout.run();