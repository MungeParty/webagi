// messaging.js
import UI from './ui.js';

const socket = io();

socket.on('connect', () => {
  console.log('Connected to server');
  socket.emit('get_current_state');
});

socket.on('response', (data) => {
  UI.updateTaskList(data.task_list);
  UI.appendToHistory(data);
  UI.updateStatusText(data.iterations_left);
  UI.handleIterationComplete();
  // UI.updateProgressBar(data.num_iterations, data.iterations_left);
  iterationComplete();
});

socket.on('event_summary', (data) => {
  const state = data.state;
  if (data.overwrite === true) {
    UI.overwriteSettings(state);
    UI.updateTaskList(state.task_list);
  }
  UI.appendToHistory(data);
  // UI.updateProgressBar(state.num_iterations, state.iterations_left);
});

function iterationComplete() {
  const iterationsLeft = UI.getIterationsValue();
  if (iterationsLeft > 0 || iterationsLeft == -1) {
    socket.emit('new_settings', {
      objective: UI.getObjectiveInputValue() || "{{OBJECTIVE}}",
      user_input: UI.getFeedbackInputValue() || "",
      num_iterations: iterationsLeft
    });
  }
}

const Messaging = {
  socket
};

export default Messaging;
