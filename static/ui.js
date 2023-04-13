// ui.js
function formatTimeDiff(timestamp) {
  const now = Date.now();
  const diff = now - timestamp;
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  if (days > 0) {
    return `${days} day${days > 1 ? 's' : ''} ago`;
  }
  if (hours > 0) {
    return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  }
  if (minutes > 0) {
    return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  }
  if (seconds > 10) {
    return `${seconds} second${seconds !== 1 ? 's' : ''} ago`;
  }
  return 'Just now';
}

const UI = (() => {
  const $taskList = $('#task-list');
  const $history = $('#history');
  const $statusText = $('#status-text');
  const $progressBarContainer = $('#progress-bar-container');
  const $progressBar = $('#progress-bar');
  const $objectiveInput = $('#objective-input');
  const $feedbackInput = $('#feedback-input');
  const $iterationsValue = $('#iterations-value');
  const $iterationsSlider = $('#iterations-slider');
  const $unlimitedCheckbox = $('#unlimited-checkbox');
  const $openEmbedForm = $('#open-embed-form');
  const $embedFormContainer = $('#embed-form-container');
  const $startButton = $('#start-button');
  const $stopButton = $('#stop-button');
  const $embeddingInput = $('#embedding-input');
  const $submitEmbedding = $('#submit-embedding');

  function updateTaskList(tasks) {
    const tasksHtml = tasks.map(t => `<li>${t.id}: ${t.name}</li>`).join('');
    $taskList.html(tasksHtml);
  }

  function appendToHistory(data) {
    console.log(data)
    const timestamp = new Date(data.timestamp);
    console.log(timestamp)
    const timeAgo = formatTimeDiff(timestamp);
    console.log(`new item: ${timestamp} vs ${timeAgo}`)
    const $updateItem = $('<div>').addClass('mb-3');
    const $timestamp = $('<p>').text(timestamp).hide().attr('name', 'timestamp');
    const $timeText = $('<p>').text(timeAgo).attr('name', 'timeText');
    const $objective = $('<p>').text(`${data.summary}`);
    $updateItem.append($timestamp, $timeText, $objective);
    const $historyItems = $history.find('div');
    $historyItems.each(function () {
      const $timestamp = $(this).find('[name="timestamp"]');
      const $timeText = $(this).find('[name="timeText"]');
      const timestamp = new Date($timestamp.text());
      const timeAgo = formatTimeDiff(timestamp);
      console.log(`history item: ${timestamp} vs ${timeAgo}`)
      $timeText.text(timeAgo);
    });
    $history.prepend($updateItem);
  }

  function updateStatusText(iterationsLeft) {
    $statusText.text(iterationsLeft == 0 ? 'Stopped' : 'Running');
  }

  function updateProgressBar(numIterations, iterationsLeft) {
    if (numIterations == -1) {
      $progressBarContainer.hide();
    } else {
      const progress = (numIterations - iterationsLeft) / numIterations * 100;
      $progressBar.css('width', progress + '%').attr('aria-valuenow', progress);
      $progressBarContainer.show();
    }
  }

  function overwriteSettings(state) {
    $objectiveInput.val(state.objective || "{{OBJECTIVE}}");
    $iterationsValue.text(state.iterations_left == -1 ? 'unlimited' : state.iterations_left);
    $iterationsSlider.val(state.iterations_left == -1 ? 50 : state.iterations_left);
    $iterationsSlider.prop('disabled', state.iterations_left == -1);
    $unlimitedCheckbox.prop('checked', state.iterations_left == -1);
  }

  // Getter functions for messaging.js
  function getObjectiveInputValue() {
    return $objectiveInput.val();
  }

  function getFeedbackInputValue() {
    return $feedbackInput.val();
  }

  function getEmbeddingInputValue() {
    return $embeddingInput.val();
  }

  function clearEmbeddingInput() {
    $embeddingInput.val('');
  }

  function getFeedbackInputValue() {
    return $feedbackInput.val();
  }

  function getIterationsValue() {
    const unlimited = $unlimitedCheckbox.prop('checked');
    return unlimited ? -1 : parseInt($iterationsSlider.val());
  }

  function setIterationsValue(iterations) {
    const unlimited = $unlimitedCheckbox.prop('checked');
    if (iterations == 0) {
      $iterationsSlider.val(0);
      $iterationsValue.text(0);
      $unlimitedCheckbox.prop('checked', false);
      $iterationsSlider.prop('disabled', false);
    } else if (!unlimited) {
      $iterationsSlider.val(iterations);
      $iterationsValue.text(iterations);
    }
  }

  function handleIterationComplete() {
    const unlimited = $unlimitedCheckbox.prop('checked');
    const iterationsLeft = getIterationsValue();
    if (!unlimited && iterationsLeft > 0) {
      $iterationsValue.text(iterationsLeft - 1);
    }
  }

  $openEmbedForm.on('click', (e) => {
    e.preventDefault();
    $embedFormContainer.toggleClass("hidden");
  });

  $iterationsSlider.on('input', () => {
    const iterations = $iterationsSlider.val();
    $iterationsValue.text(iterations);
  });

  $unlimitedCheckbox.on('change', () => {
    const unlimited = $unlimitedCheckbox.prop('checked');
    $iterationsSlider.prop('disabled', unlimited);
    if (unlimited) {
      $iterationsSlider.val(50);
      $iterationsValue.text('unlimited');
    } else {
      $iterationsSlider.val(0);
      $iterationsValue.text('1');
    }
  });

  $openEmbedForm.on('click', (e) => {
    e.preventDefault();
    if ($embedFormContainer.css('display') === 'none') {
      $embedFormContainer.show();
    } else {
      $embedFormContainer.hide();
    }
  });

  $iterationsSlider.on('input', () => {
    const iterations = $iterationsSlider.val();
    $iterationsValue.text(iterations);
  });

  $unlimitedCheckbox.on('change', () => {
    const unlimited = $unlimitedCheckbox.prop('checked');
    $iterationsSlider.prop('disabled', unlimited);
    if (unlimited) {
      $iterationsSlider.val(50);
      $iterationsValue.text('unlimited');
    } else {
      $iterationsSlider.val(0);
      $iterationsValue.text('1');
    }
  });

  return {
    stopButton: $stopButton,
    startButton: $startButton,
    submitEmbedding: $submitEmbedding,
    updateTaskList,
    appendToHistory,
    updateStatusText,
    updateProgressBar,
    overwriteSettings,
    getObjectiveInputValue,
    getFeedbackInputValue,
    getIterationsValue,
    setIterationsValue,
    getEmbeddingInputValue,
    clearEmbeddingInput,
    handleIterationComplete
  };
})();

export default UI;
