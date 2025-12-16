const http = require("http");

let counter = 0; // In-memory counter

const server = http.createServer((req, res) => {
  res.setHeader("Content-Type", "application/json");

  // GET /ping
  if (req.url === "/ping" && req.method === "GET") {
    res.writeHead(200);
    res.end(JSON.stringify({ timestamp: Date.now() }));
  }

  // GET /count
  else if (req.url === "/count" && req.method === "GET") {
    counter++;
    res.writeHead(200);
    res.end(JSON.stringify({ count: counter }));
  }

  // POST /counter  → create/reset counter
  else if (req.url === "/counter" && req.method === "POST") {
    counter = 0;
    res.writeHead(201); // Created
    res.end(JSON.stringify({ message: "Counter created/reset", count: counter }));
  }

  // PUT /counter → set counter to a specific value
  else if (req.url === "/counter" && req.method === "PUT") {
    let body = "";

    req.on("data", chunk => {
      body += chunk.toString();
    });

    req.on("end", () => {
      const data = JSON.parse(body);
      counter = data.value ?? counter;

      res.writeHead(200);
      res.end(JSON.stringify({ message: "Counter updated", count: counter }));
    });
  }

  // DELETE /counter → delete/reset counter
  else if (req.url === "/counter" && req.method === "DELETE") {
    counter = 0;
    res.writeHead(200);
    res.end(JSON.stringify({ message: "Counter deleted", count: counter }));
  }

  // Default 404
  else {
    res.writeHead(404);
    res.end(JSON.stringify({ message: "Not Found" }));
  }
});

// Start server
server.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
