// main.js
import Messaging from './messaging.js';
import UI from './ui.js';

$(function () {
    UI.stopButton.on('click', () => {
        UI.setIterationsValue(0);
    });

    UI.startButton.on('click', () => {
        const objective = UI.getObjectiveInputValue();
        const feedback = UI.getFeedbackInputValue();
        let iterations = UI.getIterationsValue();
        if (iterations == 0) {
            iterations = 1;
            UI.setIterationsValue(iterations)
        }
        Messaging.socket.emit('new_settings', { objective: objective, user_input: feedback, num_iterations: parseInt(iterations) });
    });

    UI.submitEmbedding.on('click', () => {
        const embedding = UI.getEmbeddingInputValue();
        if (!embedding) return;
        Messaging.socket.emit('new_embedding', { embedding: embedding });
        UI.clearEmbeddingInput();
    });
});
