const http = require("http");

let counter = 0; // In-memory counter

const server = http.createServer((req, res) => {
  res.setHeader("Content-Type", "application/json");

  if (req.url === "/ping") {
    res.writeHead(200);
    res.end(JSON.stringify({ timestamp: Date.now() }));
  }

  else if (req.url === "/headers") {
    res.writeHead(200);
    res.end(JSON.stringify({ headers: req.headers }, null, 2));
  }

  else if (req.url === "/count") {
    counter++;
    res.writeHead(200);
    res.end(JSON.stringify({ count: counter }));
  }

  else if (req.url === "/laugh") {
    res.writeHead(200); // FIXED
    res.end(JSON.stringify({ text: "hahahaahhahahahaaha" }));
  }

  else {
    res.writeHead(404);
    res.end(JSON.stringify({ message: "Not Found" }));
  }
});

server.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
