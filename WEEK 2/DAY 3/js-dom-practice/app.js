const faqItems = document.querySelectorAll(".faq-item");
var c=10;
faqItems.forEach(item => {
  const question = item.querySelector(".faq-question");
  const answer = item.querySelector(".faq-answer");
  const toggle = item.querySelector(".faq-toggle");

  toggle.addEventListener("click", () => {
    logError();
    answer.classList.toggle("show");
    c+=1;
    if (toggle.textContent === "+") {
      toggle.textContent = "–";
    } else {
      toggle.textContent = "+";
    }
  });
});

function logError(error) {
    let logs = JSON.parse(localStorage.getItem("errors")) || [];

    logs.push({
        message: error,
        time: new Date().toISOString()
    });

    localStorage.setItem("errors", JSON.stringify(logs));
}

