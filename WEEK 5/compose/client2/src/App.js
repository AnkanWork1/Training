export default function App() {
  fetch("http://server:3000/api/message")
    .then(res => res.json())
    .then(data => {
      document.getElementById("root").innerHTML =
        `<h1>${data.message}</h1>`;
    });

  return null;
}