Project Structure

- SpamDetector
    - detector
        - test (Contains all the testing files)
        - train (Contains all the training files)
        - model_training.py (File for generating model for all the training files)
        - model_testing.py (File for evaluating model file on all the testing files and store the result in result file)
        - model.txt (Model file)
        - result.txt (Final result file)
    - readme.txt

Running the code (Requirement python 3+)

    - Training the model
        - run "model_training.py"
        - model.txt will be generated in the same folder

    - Testing the model
        - run "model_testing.py"
        - result.txt will be generated in the same folder