const questions = [
  {
    text: "Do you experience frequent headaches while reading or working on a computer?",
    weight: 2
  },
  {
    text: "Do you have difficulty reading text from a distance (like road signs or presentations)?",
    weight: 3
  },
  {
    text: "Do you experience eye strain or fatigue after looking at screens for extended periods?",
    weight: 2
  },
  {
    text: "Do you often need to squint to see things clearly?",
    weight: 3
  },
  {
    text: "Do you experience blurred vision when looking at objects up close?",
    weight: 2
  }
];

let currentQuestion = 0;
let score = 0;

window.startTest = function() {
  document.getElementById('welcome-screen').style.display = 'none';
  document.getElementById('question-screen').style.display = 'block';
  showQuestion();
};

window.restartTest = function() {
  currentQuestion = 0;
  score = 0;
  document.getElementById('result-screen').style.display = 'none';
  document.getElementById('question-screen').style.display = 'block';
  showQuestion();
};

window.answer = function(response) {
  if (response === 'yes') {
    score += questions[currentQuestion].weight;
  }
  
  currentQuestion++;
  
  if (currentQuestion < questions.length) {
    showQuestion();
  } else {
    showResult();
  }
};

function showQuestion() {
  document.getElementById('question').textContent = questions[currentQuestion].text;
}

function showResult() {
  document.getElementById('question-screen').style.display = 'none';
  document.getElementById('result-screen').style.display = 'block';
  
  let resultText = '';
  const maxScore = questions.reduce((sum, q) => sum + q.weight, 0);
  const percentage = (score / maxScore) * 100;
  
  if (percentage < 30) {
    resultText = "Your eyes appear to be functioning well. However, it's still recommended to have regular eye check-ups.";
  } else if (percentage < 60) {
    resultText = "You may have mild vision issues. It's recommended to schedule an eye examination with an optometrist.";
  } else {
    resultText = "You show several signs of vision problems. Please schedule an appointment with an eye care professional as soon as possible.";
  }
  
  document.getElementById('result-text').textContent = resultText;
}