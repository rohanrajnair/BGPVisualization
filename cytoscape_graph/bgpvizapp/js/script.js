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

function addNode(cy, node_data) {
    const peer_asn = node_data.peer_asn;
    const path = node_data.path; //path of ASNs
    const main_node_obj = { id: peer_asn, color: "#90EE90" };
    if (cy.getElementById(peer_asn).length === 0) {
      cy.add({
        data: main_node_obj,
      });
    } else {
      if (node_data.withdrawals) {
        cy.getElementById(peer_asn).data("color", "#FF0000");
      } else {
        cy.getElementById(peer_asn).data("color", "#ADD8E6");
      }
    }
    for (let i = 1; i < path.length; i++) {
      const target_id = path[i];
      if (
        cy.getElementById(target_id).length > 0 &&
        cy.getElementById(`${peer_asn}_to_${target_id}`).length === 0
      ) {
        cy.add({
          data: {
            id: `${peer_asn}_to_${target_id}`,
            source: peer_asn,
            target: target_id,
          },
        });
      }
    }
    // var layout = cy.elements().layout({ name: "circle", animate: true });
    // layout.run();
  }

function choose(choices) {
    var index = Math.floor(Math.random() * choices.length);
    return choices[index];
}
var cy = cytoscape({
    container: document.getElementById("cy"),
    elements: [],
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