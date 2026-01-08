const http = require('http');

const PORT = 3001;

http.createServer((req, res) => {
  res.end("Hello from Docker Image\n");
}).listen(PORT, () => {
  console.log(`Server running on ${PORT}`);
});
