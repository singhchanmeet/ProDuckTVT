const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = 3000;

// Middleware to parse JSON data in the request body
app.use(express.json());
app.use(cors());

// Route 1: Handling a POST request with JSON data
app.post('/gendocs/', (req, res) => {
  const { data } = req.body;

  if (data.includes('django')) {
    // Process data related to Django and send a response
    const djangoCode = `
This Django view function, hello_world, responds to HTTP requests by returning an HTTP response containing the message "Hello, World! This is a Django view." It serves as a basic example of a Django view for handling web requests and generating responses.
    `;
    res.send(`Docs for Django:\n\n${djangoCode}`);
  } else if (data.includes('Widget')) {
    // Process data related to Flutter and send a response
    const flutterCode = `
    This Flutter code defines a basic Flutter app with a MyApp widget. When executed, it runs the Flutter app, creating a Material Design-based user interface. The app displays an app bar with the title "Flutter Example" and a centered text widget containing the message "Hello, Flutter!" with a font size of 24. This code serves as a minimal example of a Flutter application's structure and user interface components.
    `;
    res.send(`Docs for Flutter:\n\n${flutterCode}`);
  } else if (data.includes('<iostream>')) {
    // Process data related to C++ and send a response
    const cppCode = `
    
This C++ program is a simple console application that prints the message "Hello, World! This is a C++ program." to the console when executed. It returns a status code of 0 to indicate successful execution to the operating system.
    `;
    res.send(`Docs for C++:\n\n${cppCode}`);
  } else {
    // Handle other cases or invalid data
    res.send(`This code is too complicated for me to right documentation. Sorry But you can refer to other AI tools available online`);
  }
});


// Route 2: Handling a POST request with JSON data
app.post('/improve/', (req, res) => {
  const { data } = req.body;

  if (data.includes('django')) {
    // Process data related to Django and send a response
    const djangoImprovement = `
    When improving Django code, consider optimizing database queries, enhancing view functions, and improving code readability using Django's built-in features and best practices.
    `;
    res.send(`Improvement suggestions for Django:\n\n${djangoImprovement}`);
  } else if (data.includes('Widget')) {
    // Process data related to Flutter and send a response
    const flutterImprovement = `
    When improving Flutter code, focus on optimizing widget layout, managing state efficiently, and adhering to Flutter's UI design guidelines. Utilize state management libraries like Provider or Riverpod for more complex applications.
    `;
    res.send(`Improvement suggestions for Flutter:\n\n${flutterImprovement}`);
  } else if (data.includes('<iostream>')) {
    // Process data related to C++ and send a response
    const cppImprovement = `
    When improving C++ code, consider code refactoring for better maintainability, optimizing algorithms and data structures, and enhancing code organization. Utilize C++ best practices and design patterns.
    `;
    res.send(`Improvement suggestions for C++:\n\n${cppImprovement}`);
  } else {
    // Handle other cases or invalid data
    res.send('Improvement suggestions for this code cannot be provided.');
  }
});


// Route 3: Handling a POST request with JSON data
app.post('/explain/', (req, res) => {
  const { data } = req.body;

  if (data.includes('django')) {
    // Provide an explanation of Django
    const djangoExplanation = `
    Django is a high-level Python web framework known for its simplicity and robustness. It promotes rapid development, follows the Model-View-Controller (MVC) architectural pattern, and provides features like an ORM for database interactions, automatic admin interface generation, and more.
    `;
    res.send(`Explanation for Django:\n\n${djangoExplanation}`);
  } else if (data.includes('Widget')) {
    // Provide an explanation of Flutter Widgets
    const flutterExplanation = `
    In Flutter, Widgets are the fundamental building blocks of the user interface. They describe how the UI should look and behave. Flutter uses a reactive framework, meaning that widgets are rebuilt whenever their state changes, allowing for a declarative UI design.
    `;
    res.send(`Explanation for Flutter Widgets:\n\n${flutterExplanation}`);
  } else if (data.includes('<iostream>')) {
    // Provide an explanation of C++ iostream
    const cppExplanation = `
    In C++, the iostream library provides input and output functionality. It includes classes like 'cin' for input and 'cout' for output. These classes simplify console input and output operations, making C++ programs more interactive.
    `;
    res.send(`Explanation for C++ iostream:\n\n${cppExplanation}`);
  } else {
    // Handle other cases or invalid data
    res.send('Explanation for this topic is not available.');
  }
});


// Route 4: Handling a POST request with JSON data
app.post('/doubts/', (req, res) => {
  const { data } = req.body;
  // Process the JSON data and send a response
  res.send(`You can have a detailed explnation of your Python Code at `);
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
