let currentTest = 'visual-acuity';
let testResults = {
    visualAcuity: [],
    colorVision: [],
    astigmatism: null,
    lensAdjustment: 0
};

const visualAcuityLetters = [
    { size: '72px', letter: 'E' },
    { size: '48px', letter: 'F' },
    { size: '36px', letter: 'P' },
    { size: '24px', letter: 'T' },
    { size: '18px', letter: 'O' }
];

const ishiharaPlates = [
    { id: 1, number: 16, image: 'plate1.jpg' },
    { id: 2, number: 42, image: 'plate2.jpg' },
    { id: 3, number: 6, image: 'plate3.jpg' }
];

let currentLetterIndex = 0;
let currentPlateIndex = 0;

document.addEventListener('DOMContentLoaded', function() {
    startVisualAcuityTest();

    const blurSlider = document.getElementById('blur-slider');
    const plateImage = document.getElementById('plate-image');
    const sliderValue = document.getElementById('slider-value');

    if (blurSlider && plateImage && sliderValue) {
        blurSlider.addEventListener('input', function() {
            const blurValue = blurSlider.value;
            plateImage.style.filter = `blur(${blurValue}px)`;
            sliderValue.textContent = blurValue;
        });

        document.querySelector('.next-button').addEventListener('click', function() {
            const blurValue = blurSlider.value;
            testResults.lensAdjustment = blurValue;
            showResults();
        });
    }
});

function startVisualAcuityTest() {
    const letterDisplay = document.querySelector('.letter-display');
    const currentLetter = visualAcuityLetters[currentLetterIndex];
    letterDisplay.style.fontSize = currentLetter.size;
    letterDisplay.textContent = currentLetter.letter;

    document.querySelector('.next-button').addEventListener('click', handleVisualAcuityAnswer);
}

function handleVisualAcuityAnswer() {
    const input = document.getElementById('letter-input');
    const answer = input.value.toUpperCase();
    const currentLetter = visualAcuityLetters[currentLetterIndex];

    testResults.visualAcuity.push({
        size: currentLetter.size,
        letter: currentLetter.letter,
        answer: answer,
        correct: answer === currentLetter.letter
    });

    currentLetterIndex++;
    input.value = '';

    if (currentLetterIndex < visualAcuityLetters.length) {
        const letterDisplay = document.querySelector('.letter-display');
        const nextLetter = visualAcuityLetters[currentLetterIndex];
        letterDisplay.style.fontSize = nextLetter.size;
        letterDisplay.textContent = nextLetter.letter;
    } else {
        startColorVisionTest();
    }
}

function startColorVisionTest() {
    document.getElementById('visual-acuity-test').style.display = 'none';
    document.getElementById('color-vision-test').style.display = 'block';
    currentTest = 'color-vision';

    const plateImage = document.querySelector('.ishihara-plate');
    plateImage.src = `/static/images/${ishiharaPlates[currentPlateIndex].image}`;

    document.querySelector('#color-vision-test .next-button').addEventListener('click', handleColorVisionAnswer);
}

function handleColorVisionAnswer() {
    const input = document.getElementById('number-input');
    const answer = parseInt(input.value);
    const currentPlate = ishiharaPlates[currentPlateIndex];

    testResults.colorVision.push({
        plateId: currentPlate.id,
        correctNumber: currentPlate.number,
        answer: answer,
        correct: answer === currentPlate.number
    });

    currentPlateIndex++;
    input.value = '';

    if (currentPlateIndex < ishiharaPlates.length) {
        const plateImage = document.querySelector('.ishihara-plate');
        plateImage.src = `/static/images/${ishiharaPlates[currentPlateIndex].image}`;
    } else {
        startAstigmatismTest();
    }
}

function startAstigmatismTest() {
    document.getElementById('color-vision-test').style.display = 'none';
    document.getElementById('astigmatism-test').style.display = 'block';
    currentTest = 'astigmatism';

    const optionButtons = document.querySelectorAll('.option-button');
    optionButtons.forEach(button => {
        button.addEventListener('click', handleAstigmatismAnswer);
    });

    // Set the astigmatism image
    const astigmatismPlate = document.querySelector('.astigmatism-plate');
    astigmatismPlate.src = '../static/images/astigmatism.jpg';

}

function handleAstigmatismAnswer(event) {
    const selectedOption = event.target.dataset.option;
    console.log('Astigmatism answer selected:', selectedOption);
    
    testResults.astigmatism = event.target.dataset.value;
    window.location.href = '/lens-adjustment';
}

function startLensAdjustmentTest() {
    const lensAdjustmentTest = document.getElementById('lens-adjustment-test');
    if (lensAdjustmentTest) {
        lensAdjustmentTest.style.display = 'block';
        currentTest = 'lens-adjustment';

        const blurSlider = document.getElementById('blur-slider');
        const plateImage = document.getElementById('plate-image');
        const sliderValue = document.getElementById('slider-value');

        if (blurSlider && plateImage && sliderValue) {
            blurSlider.addEventListener('input', function() {
                const blurValue = blurSlider.value;
                plateImage.style.filter = `blur(${blurValue}px)`;
                sliderValue.textContent = blurValue;
            });

            document.querySelector('.next-button').addEventListener('click', function() {
                const blurValue = blurSlider.value;
                testResults.lensAdjustment = blurValue;
                showResults();
            });
        }
    }
}

// function handleLensAdjustment(event) {
//     const adjustment = parseInt(event.target.dataset.adjustment);
//     const lensPowerElement = document.querySelector('.lens-power');
//     let currentPower = parseInt(lensPowerElement.textContent);
//     currentPower += adjustment;
//     lensPowerElement.textContent = currentPower;
//     testResults.lensAdjustment = currentPower;
// }

function showResults() {

    const resultsPageUrl = '/results.html';
    const queryParams = new URLSearchParams(testResults).toString();
    window.location.href = `${resultsPageUrl}?${queryParams}`;
}

    //const visualAcuityScore = testResults.visualAcuity.filter(result => result.correct).length;
    //const colorVisionScore = testResults.colorVision.filter(result => result.correct).length;

    // alert(`
    // Test Results:
    // Visual Acuity Score: ${visualAcuityScore}/${visualAcuityLetters.length}
    // Color Vision Score: ${colorVisionScore}/${ishiharaPlates.length}
    // Astigmatism: ${testResults.astigmatism}
    // Lens Adjustment Power: ${testResults.lensAdjustment}
    // Recommendations: ${generateRecommendations(visualAcuityScore, colorVisionScore, testResults.astigmatism)}
    // `);

    // saveResults();


function generateRecommendations(visualScore, colorScore, astigmatism) {
    let recommendations = '<h3>Recommendations</h3>';
    
    if (visualScore < visualAcuityLetters.length * 0.8) {
        recommendations += '<p>Consider getting your vision checked by an optometrist.</p>';
    }
    
    if (colorScore < ishiharaPlates.length * 0.8) {
        recommendations += '<p>You may have some color vision deficiency. Professional evaluation is recommended.</p>';
    }
    
    if (astigmatism === 'blur') {
        recommendations += '<p>You may have astigmatism. Schedule an appointment with an eye care professional.</p>';
    }
    
    if (visualScore === visualAcuityLetters.length && 
        colorScore === ishiharaPlates.length && 
        astigmatism === 'clear') {
        recommendations += '<p>Your vision appears to be normal. Continue with regular eye check-ups.</p>';
    }
    
    return recommendations;
}

function saveResults() {
    const results = {
        visualAcuity: testResults.visualAcuity,
        colorVision: testResults.colorVision,
        astigmatism: testResults.astigmatism,
        lensAdjustment: testResults.lensAdjustment
    };
    
    fetch('/api/save-results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(testResults)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Results saved:', data);
    })
    .catch(error => {
        console.error('Error saving results:', error);
    });
}
