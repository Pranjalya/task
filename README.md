# Instructions

Do not spend more than 1-2 hours on any task.

## Task 1

- Fork this repo  
- Read the instructions in `task.py`
- Modify the `detect_coughs` function

## Task 2

- Build a simple cloud function to deploy `detect_coughs` (what you built in task 1). Use the Google Cloud platform.  
- Write a basic script in python or bash for sending the files in `sounds` to your endpoint and receiving the outputs
- Add this script to your forked repo.

When finished, email the URL of your forked repo to joe@hyfe.ai.

## Results

- `app` contains Flask server deployed at https://cough-detector.herokuapp.com/ 
- It can be accessed through CLI too by hitting on https://cough-detector.herokuapp.com/detect_coughs/ 

Example : 
```
curl -X POST -F file=@$file https://cough-detector.herokuapp.com/detect_coughs
```

- Example scripts have been provided in [Python format](https://github.com/Pranjalya/task/blob/main/test.py) and in [Shell script](https://github.com/Pranjalya/task/blob/main/test.sh)
