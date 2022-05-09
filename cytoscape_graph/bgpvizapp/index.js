const express = require("express");
const path = require("path");
var cytoscape = require("cytoscape");

const app = express();
const port = 3000;

app.use("/css", express.static(path.join(__dirname, "css")));
app.use("/js", express.static(path.join(__dirname, "js")));

console.log(path.join(__dirname, "css"));

app.get("/popper.js", function (req, res) {
  res.sendFile(
    __dirname + "/node_modules/cytoscape-popper/cytoscape-popper.js"
  );
});

// app.get("/cise.js", function (res, req) {
//   res.sendFile(__dirname + "/node_modules/cytoscape-cise/cytoscape-cise.js");
// });

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "/index.html"));
});

app.listen(port, () => {
  console.log(`Example app listening on port http://127.0.0.1:${port}`);
});

//Every once in a while, this express server will fetch data from the API
//This api data will be pass into the index.html..
