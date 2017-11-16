# Lob Coding Challenge

1.  Before running the command line program, set up your virtual environment:

    ```
    virtualenv env
    ```

2.  Source into your virtual environment:

    ```
    source env/bin/activate
    ```

3.  Set up the required libraries and dependencies from the requirements text file:

    ```
    pip install -r requirements.txt
    ```

4.  Then set your Google API and Lob (Test) API keys as an environment variable locally:

    ```
    export GOOGLE_CIVIC_KEY='your_Google_API_key'
    export LOB_TEST_API_KEY='your_Lob_API_key'
    ```

5.  Run the following code in Terminal/your command line interface (replacing 'input_file.txt' with the name of your input file):

    ```
    python send_to_legislator.py input_file.txt
    ```

6.  Preview the letter in the Lob Dashboard > Letters API section.