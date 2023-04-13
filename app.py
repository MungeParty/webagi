from os import getenv
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from ai.agency import Agency
from time import time
from datetime import datetime

load_dotenv()

PINECONE_TABLE_NAME = getenv("PINECONE_TABLE_NAME", "test-table")
OBJECTIVE = getenv("OBJECTIVE", "Come up with a cool objective")

agency = Agency("agent_configurations.json", OBJECTIVE, PINECONE_TABLE_NAME)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*", logger=True, engineio_logger=True)

num_iterations = -1
objective = OBJECTIVE
user_feedback = ""

iteration_in_progress = False

@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('new_settings')
def handle_new_settings(data):
	global objective, num_iterations, user_feedback
	num_iterations = data.get("num_iterations", -1)
	objective = data.get("objective", OBJECTIVE)
	user_feedback = data.get("user_input", "")
	execute_agency_iteration()

@socketio.on('stop')
def handle_stop():
	global num_iterations
	num_iterations = 0

@socketio.on('get_current_state')
def handle_get_current_state():
	send_event(f'Connected to server, returning current state.', True)

def execute_agency_iteration():
	global objective, num_iterations, user_feedback, iteration_in_progress
	if iteration_in_progress:
		return

	iteration_in_progress = True
	start_time = time()
	send_event(f'Iteration started: {start_time}')
	iteration_result = agency.run({
		'objective': objective,
		'user_feedback': user_feedback})

	end_time = time()
	time_taken = end_time - start_time
	if num_iterations > -1:
		num_iterations -= 1

	response = {
		'objective': objective,
		'task_list': [{"id": t["task_id"], "name": t["task_name"]} for t in agency.task_list],
		'new_tasks': iteration_result["new_tasks"],
		'last_task_result': iteration_result["result"],
		'iterations_left': num_iterations,
		'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		'time_taken': time_taken
	}

	emit('response', response, broadcast=True)
	iteration_in_progress = False

def get_state():
	return {
		'objective': objective,
		'iterations_left': num_iterations,
		'task_list': [{"id": t["task_id"], "name": t["task_name"]} for t in agency.task_list],
	}

def send_event(summary: str, overwrite: bool = False):
	emit('event_summary', {
		'summary': summary,
		'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		'state': get_state(),
		'overwrite': overwrite
	})

if __name__ == '__main__':
	socketio.run(app, debug=True)
