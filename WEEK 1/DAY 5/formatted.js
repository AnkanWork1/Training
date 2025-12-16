function greetUser(name) {
  if (!name) {
    console.log("No name provided.");
    return;
  }

  console.log(`Hello, ${name}! Welcome to Day 5 tasks.`);
}

greetUser("Ankan");
